import sys
from riot_api import fetch_puuid, fetch_match_history, fetch_match_details, extract_player_stats, clean_player_stats
from database import save_match_data, is_match_saved

if len(sys.argv) < 5:
    print("Error: Missing arguments to run main.py")
    sys.exit(1)

user_api_key = sys.argv[1]
player_name = sys.argv[2]
player_tag = sys.argv[3]
region = sys.argv[4]

user_puuid = fetch_puuid(user_api_key, player_name, player_tag, region)
match_history_ids = fetch_match_history(user_api_key, user_puuid, region)

print("Starting match sync... Please wait.")

for current_match_id in match_history_ids:
    if is_match_saved(current_match_id):
        print(f"The match id: {current_match_id} is already on the local database, we're skipping it.")
        continue

    print(f"Downloading new match: {current_match_id}")

    match_raw_details = fetch_match_details(user_api_key, current_match_id, region)
    player_raw_stats = extract_player_stats(match_raw_details, user_puuid)
    total_game_duration = match_raw_details["info"]["gameDuration"]

    processed_player_stats = clean_player_stats(player_raw_stats, total_game_duration)
    processed_player_stats["match_id"] = current_match_id

    save_match_data(processed_player_stats)

print("Sync is complete!")