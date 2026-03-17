import streamlit as st
from analyzer import analyze_performance

st.set_page_config(page_title="League Stats Analyzer", page_icon="🎮", layout="wide")

st.title("League of Legends - Personal Dashboard")
st.markdown("---")

st.header("Global account data")
global_stats = analyze_performance()

if global_stats:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Matches analyzed", global_stats["Total Matches"])
    with col2:
        st.metric("AVG KDA", global_stats["KDA Ratio"])
    with col3:
        st.metric("AVG DMG per min (DPM)", global_stats["Avg Damage/Min (DPM)"])
    with col4:
        st.metric("AVG Farm per min", global_stats["Avg Farm/Min"])

    st.markdown("---")
else:
    st.warning("No data found in the database. Please execute main.py first.")