from riot_api import fetch_puuid, fetch_match_history, fetch_match_details, extract_player_stats, clean_player_stats
from database import save_match_data, is_match_saved

user_puuid = fetch_puuid("schumaZ", "fox")
match_history_ids = fetch_match_history(user_puuid)

print("Starting match sync... Please wait.\n")

for current_match_id in match_history_ids:
    if is_match_saved(current_match_id):
        print(f"The match id: {current_match_id} is already on the local databse, we're skipping it.")
        continue

    print(f"Downloaing new match: {current_match_id}")

    match_raw_details = fetch_match_details(current_match_id)
    player_raw_stats = extract_player_stats(match_raw_details, user_puuid)
    total_game_duration = match_raw_details["info"]["gameDuration"]

    processed_player_stats = clean_player_stats(player_raw_stats, total_game_duration)

    processed_player_stats["match_id"] = current_match_id

    save_match_data(processed_player_stats)

print("Sync is complete!")