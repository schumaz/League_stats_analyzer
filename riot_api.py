from riotwatcher import LolWatcher, RiotWatcher, ApiError
from config import api_key

lol_watcher = LolWatcher(api_key)
riot_watcher = RiotWatcher(api_key)
region = "americas"

def fetch_puuid(player_name, player_tag):
    account = riot_watcher.account.by_riot_id(region, player_name, player_tag)

    return account["puuid"]

def fecth_match_history(puuid):
    match_ids = lol_watcher.match.matchlist_by_puuid(region, puuid)

    return match_ids

my_puuid = fetch_puuid("schumaZ", "fox")
print(f"1. My puuid is: {my_puuid}")

my_matches = fecth_match_history(my_puuid)
print(f"2. My last matches is: {my_matches}")