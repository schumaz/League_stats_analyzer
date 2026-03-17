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

def fetch_match_details(match_id):
    match_data = lol_watcher.match.by_id(region, match_id)

    return match_data

my_puuid = fetch_puuid("schumaZ", "fox")
my_matches = fecth_match_history(my_puuid)

recent_match_id = my_matches[0]

details = fetch_match_details(recent_match_id)

print("This is the data of my most recent match:")
print(details.keys())