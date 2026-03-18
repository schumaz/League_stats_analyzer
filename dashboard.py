import streamlit as st
import pandas as pd
import json
import subprocess
import altair as alt
import os 
import sys

from riot_api import fetch_puuid

SETTINGS_FILE = "user_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

st.set_page_config(page_title="LoL Stats Analyzer", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    div[data-baseweb="select"] > div, label, .stCheckbox {
        cursor: pointer !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("League of Legends - Analytical Dashboard")

ROLE_DICTIONARY = {
    "TOP": "TOP",
    "JUNGLE": "JUNGLE",
    "MIDDLE": "MID",
    "BOTTOM": "ADC",
    "UTILITY": "SUPPORT"
}

METRIC_DICTIONARY = {
    "champ": "Champion",
    "kills": "Kills",
    "deaths": "Deaths",
    "assists": "Assists",
    "total_dmg": "Total Damage",
    "dmg_per_min": "Damage per Minute (DPM)",
    "farm_per_min": "Farm per Minute",
    "gold_per_min": "Gold per Minute",
    "total_farm": "Total Farm",
    "total_gold": "Total Gold",
    "vision_score": "Vision Score",
    "bought_pinks": "Control Wards Bought",
    "wards_per_min": "Wards per Minute",
    "wards_placed": "Wards Placed",
    "dmg_to_objectives": "Damage to Objectives",
    "tower_destroyed": "Towers Destroyed",
    "match_duration": "Match Duration (Min)" 
}

@st.cache_data
def load_data():
    try:
        with open("match_history.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
            df = pd.DataFrame(data)
            df = df.rename(columns=METRIC_DICTIONARY)
            df["Match"] = range(len(df), 0, -1)
            return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

st.sidebar.header("Filters")

official_roles = ["ALL", "TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]
formatted_roles = [ROLE_DICTIONARY.get(r, r) if r != "ALL" else "ALL" for r in official_roles]

chosen_role = st.sidebar.selectbox("Filter by Position:", formatted_roles)

st.sidebar.markdown("---")
st.sidebar.header("🔑 Authentication")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.settings = load_settings()
    
    if st.session_state.settings.get("api_key"):
        try:
            fetch_puuid(
                st.session_state.settings["api_key"], 
                st.session_state.settings["player_name"], 
                st.session_state.settings["player_tag"], 
                st.session_state.settings["region"]
            )
            st.session_state.authenticated = True
        except Exception:
            st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.sidebar.warning("API Key is missing or expired.")
    with st.sidebar.form("auth_form"):
        current_settings = st.session_state.settings
        new_api_key = st.text_input("Riot API Key:", type="password", value=current_settings.get("api_key", ""))
        new_name = st.text_input("Player Name (e.g. Player):", value=current_settings.get("player_name", ""))
        new_tag = st.text_input("Player Tag (e.g. BR1):", value=current_settings.get("player_tag", ""))
        
        regions = ["americas", "europe", "asia"]
        default_region = current_settings.get("region", "americas")
        new_region = st.selectbox("Region:", regions, index=regions.index(default_region) if default_region in regions else 0)
        
        if st.form_submit_button("Save & Authenticate"):
            try:
                fetch_puuid(new_api_key, new_name, new_tag, new_region)
                new_settings = {
                    "api_key": new_api_key,
                    "player_name": new_name,
                    "player_tag": new_tag,
                    "region": new_region
                }
                save_settings(new_settings)
                st.session_state.settings = new_settings
                st.session_state.authenticated = True
                st.rerun()
            except Exception:
                st.error("Invalid API Key or Player not found. Try again.")
    st.stop()
else:
    s = st.session_state.settings
    st.sidebar.success(f"Logged in: **{s['player_name']}#{s['player_tag']}**")
    if st.sidebar.button("⚙️ Change Account / API Key"):
        st.session_state.authenticated = False
        st.rerun()

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Sync Recent Matches", use_container_width=True):
    with st.spinner("Downloading from Riot Games..."):
        s = st.session_state.settings
        
        current_folder = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(current_folder, "main.py")
        subprocess.run([sys.executable, main_path, s["api_key"], s["player_name"], s["player_tag"], s["region"]])
        st.cache_data.clear()
        st.success("Sync Complete!")
        st.rerun()

if st.sidebar.button("🗑️ Clear Database", use_container_width=True):
    st.session_state.confirm_delete = True

if st.session_state.get("confirm_delete", False):
    st.sidebar.error("⚠️ Are you sure? This deletes ALL matches.")
    
    col_yes, col_no = st.sidebar.columns(2)
    with col_yes:
        if st.button("✔️ Yes", use_container_width=True):
            if os.path.exists("match_history.json"):
                os.remove("match_history.json")
            st.session_state.confirm_delete = False
            st.cache_data.clear()
            st.rerun()
            
    with col_no:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.confirm_delete = False
            st.rerun()
            
st.sidebar.markdown("---")

if df.empty:
    st.warning("No data found. Click the Sync button on the sidebar to download your matches!")
    st.stop()

if chosen_role != "ALL":
    original_role = [k for k, v in ROLE_DICTIONARY.items() if v == chosen_role][0]
    df_filtered = df[df["role"] == original_role].copy()
else:
    df_filtered = df.copy()

if df_filtered.empty:
    st.warning(f"You don't have any saved matches playing as **{chosen_role}** yet. Go play some to see the charts!")
    st.stop() 

tab_overview, tab_custom, tab_champs = st.tabs(["📊 Global Overview", "🛠️ Custom Chart Builder", "🦸 Champion Stats"])

with tab_overview:
    st.subheader(f"Overview: {chosen_role}")
    
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.write("⚔️ **Damage per Minute (DPM) over matches**")
        chart_dpm = alt.Chart(df_filtered).mark_line(point=True).encode(
            x="Match",
            y=METRIC_DICTIONARY["dmg_per_min"],
            tooltip=["Match", "Champion", METRIC_DICTIONARY["dmg_per_min"]]
        ).interactive()
        st.altair_chart(chart_dpm, use_container_width=True)

    with row1_col2:
        st.write("💰 **Gold per Minute over matches**")
        chart_gold = alt.Chart(df_filtered).mark_bar().encode(
            x="Match:O",
            y=METRIC_DICTIONARY["gold_per_min"],
            tooltip=["Match", "Champion", METRIC_DICTIONARY["gold_per_min"]],
            color=alt.value("#F5D04C")
        ).interactive()
        st.altair_chart(chart_gold, use_container_width=True)
        
    st.markdown("---")
    
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.write("🌾 **Farm per Minute over matches**")
        chart_farm = alt.Chart(df_filtered).mark_line(point=True).encode(
            x="Match",
            y=METRIC_DICTIONARY["farm_per_min"],
            tooltip=["Match", "Champion", METRIC_DICTIONARY["farm_per_min"]]
        ).interactive()
        st.altair_chart(chart_farm, use_container_width=True)

    with row2_col2:
        st.write("👁️ **Vision Score over matches**")
        chart_vision = alt.Chart(df_filtered).mark_bar().encode(
            x="Match:O",
            y=METRIC_DICTIONARY["vision_score"],
            tooltip=["Match", "Champion", METRIC_DICTIONARY["vision_score"]],
            color=alt.value("#636EFA")
        ).interactive()
        st.altair_chart(chart_vision, use_container_width=True)

    st.markdown("---")
    row3_col1, row3_col2 = st.columns(2)
    
    with row3_col1:
        st.write("🍕 **Champion Play Rate**")
        champ_counts = df_filtered[METRIC_DICTIONARY["champ"]].value_counts().reset_index()
        champ_counts.columns = [METRIC_DICTIONARY["champ"], "Count"]
        
        chart_pie_champ = alt.Chart(champ_counts).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field=METRIC_DICTIONARY["champ"], type="nominal"),
            tooltip=[METRIC_DICTIONARY["champ"], "Count"]
        ).interactive()
        st.altair_chart(chart_pie_champ, use_container_width=True)

    with row3_col2:
        st.write("🍕 **Kills / Deaths / Assists Distribution**")
        k_sum = df_filtered[METRIC_DICTIONARY["kills"]].sum()
        d_sum = df_filtered[METRIC_DICTIONARY["deaths"]].sum()
        a_sum = df_filtered[METRIC_DICTIONARY["assists"]].sum()
        
        kda_data = pd.DataFrame({
            "Category": ["Kills", "Deaths", "Assists"],
            "Total": [k_sum, d_sum, a_sum]
        })
        
        kda_colors = alt.Scale(domain=["Kills", "Deaths", "Assists"], range=["#00C853", "#D50000", "#2962FF"])
        
        chart_pie_kda = alt.Chart(kda_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Total", type="quantitative"),
            color=alt.Color(field="Category", type="nominal", scale=kda_colors),
            tooltip=["Category", "Total"]
        ).interactive()
        st.altair_chart(chart_pie_kda, use_container_width=True)


with tab_custom:
    st.subheader("🛠️ Create your own Chart (X / Y)")
    
    champ_list_for_custom = ["All"] + sorted(df_filtered[METRIC_DICTIONARY["champ"]].unique().tolist())
    custom_champ_filter = st.selectbox("Focus on a specific Champion:", champ_list_for_custom)
    
    if custom_champ_filter != "All":
        df_custom = df_filtered[df_filtered[METRIC_DICTIONARY["champ"]] == custom_champ_filter]
    else:
        df_custom = df_filtered
    
    st.write("Select which statistics you want to compare:")

    numeric_columns = df_custom.select_dtypes(include=['float64', 'int64']).columns.tolist()

    sel_x, sel_y, sel_color = st.columns(3)

    with sel_x:
        axis_x = st.selectbox("X-Axis (Horizontal):", numeric_columns, index=numeric_columns.index(METRIC_DICTIONARY["match_duration"]))
    with sel_y:
        axis_y = st.selectbox("Y-Axis (Vertical):", numeric_columns, index=numeric_columns.index(METRIC_DICTIONARY["dmg_per_min"]))
    with sel_color:
        st.write(" ")
        st.write(" ")
        use_color = st.checkbox("Color by Champion?", value=True)

    st.write(f"Comparing **{axis_x}** vs **{axis_y}**")

    if use_color:
        st.scatter_chart(df_custom, x=axis_x, y=axis_y, color=METRIC_DICTIONARY["champ"], height=600)
    else:
        st.scatter_chart(df_custom, x=axis_x, y=axis_y, height=600)

with tab_champs:
    st.subheader("🦸 Champion Stats")
    
    played_champions = sorted(df_filtered[METRIC_DICTIONARY["champ"]].unique().tolist())
    
    if not played_champions:
        st.warning("No champions found with the current filters.")
    else:
        selected_champ = st.selectbox("Select a Champion:", played_champions)
        
        df_champ = df_filtered[df_filtered[METRIC_DICTIONARY["champ"]] == selected_champ]
        matches_played = len(df_champ)
        
        col_img, col_stats1, col_stats2 = st.columns([1, 2, 2])
        
        with col_img:
            champ_formatado = selected_champ.replace(" ", "").replace("'", "")
            st.image(f"https://ddragon.leagueoflegends.com/cdn/14.4.1/img/champion/{champ_formatado}.png", width=120)
        
        with col_stats1:
            st.metric("Matches Played", matches_played)
            
            avg_kills = round(df_champ[METRIC_DICTIONARY['kills']].mean(), 1)
            avg_deaths = round(df_champ[METRIC_DICTIONARY['deaths']].mean(), 1)
            avg_assists = round(df_champ[METRIC_DICTIONARY['assists']].mean(), 1)
            st.metric("Avg KDA", f"{avg_kills} / {avg_deaths} / {avg_assists}")
            
        with col_stats2:
            avg_dpm = round(df_champ[METRIC_DICTIONARY['dmg_per_min']].mean(), 1)
            st.metric("Avg DPM", avg_dpm)
            
            avg_farm = round(df_champ[METRIC_DICTIONARY['farm_per_min']].mean(), 1)
            st.metric("Avg Farm/Min", avg_farm)

        st.markdown("### 🔍 In-Depth Averages")
        col_det1, col_det2, col_det3, col_det4 = st.columns(4)

        with col_det1:
            st.metric("Vision Score", round(df_champ[METRIC_DICTIONARY['vision_score']].mean(), 1))
            st.metric("Wards Placed", round(df_champ[METRIC_DICTIONARY['wards_placed']].mean(), 1))

        with col_det2:
            st.metric("Control Wards (Pinks)", round(df_champ[METRIC_DICTIONARY['bought_pinks']].mean(), 1))
            st.metric("Wards/Min", round(df_champ[METRIC_DICTIONARY['wards_per_min']].mean(), 2))

        with col_det3:
            st.metric("Total Gold", f"{df_champ[METRIC_DICTIONARY['total_gold']].mean():.0f}")
            st.metric("Gold/Min", round(df_champ[METRIC_DICTIONARY['gold_per_min']].mean(), 1))

        with col_det4:
            st.metric("Obj. Damage", f"{df_champ[METRIC_DICTIONARY['dmg_to_objectives']].mean():.0f}")
            st.metric("Towers Destroyed", round(df_champ[METRIC_DICTIONARY['tower_destroyed']].mean(), 1))