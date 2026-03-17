from riotwatcher import LolWatcher, RiotWatcher, ApiError
from config import api_key

lol_watcher = LolWatcher(api_key)
riot_watcher = RiotWatcher(api_key)

def fetch_puuid(player_name, player_tag):
    region = "americas"

    account = riot_watcher.account.by_riot_id(region, player_name, player_tag)

    return account["puuid"]

my_puuid = fetch_puuid("schumaZ", "fox")
print(f"My puuid is: {my_puuid}")