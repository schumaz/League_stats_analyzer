from riotwatcher import LolWatcher, RiotWatcher, ApiError
from database import save_match_data

def fetch_puuid(api_key, player_name, player_tag, region):
    """Fetches the player's unique PUUID from the Riot API."""
    riot_watcher = RiotWatcher(api_key)
    account = riot_watcher.account.by_riot_id(region, player_name, player_tag)
    return account["puuid"]

def fetch_match_history(api_key, puuid, region):
    """Retrieves a list of recent match IDs for the given player."""
    lol_watcher = LolWatcher(api_key)
    return lol_watcher.match.matchlist_by_puuid(region, puuid)

def fetch_match_details(api_key, match_id, region):
    """Fetches detailed data for a specific match."""
    lol_watcher = LolWatcher(api_key)
    return lol_watcher.match.by_id(region, match_id)

def extract_player_stats(match_data, puuid):
    """Finds and extracts the specific player's stats from the match data."""
    participants = match_data["info"]["participants"]
    for player in participants:
        if player["puuid"] == puuid:
            return player
    return None

def clean_player_stats(player_stats, game_duration_seconds):
    """Calculates and formats key player metrics (like per-minute stats)."""
    minutes = game_duration_seconds / 60
    total_farm = player_stats['totalMinionsKilled'] + player_stats["neutralMinionsKilled"]

    return {
        # Basic Stats
        "assists": player_stats["assists"],
        "champ": player_stats["championName"],
        "deaths": player_stats["deaths"],
        "kills": player_stats["kills"],
        "role": player_stats["teamPosition"],
        "match_duration": round(minutes, 2),

        # Performance & Economy
        "total_dmg": player_stats["totalDamageDealtToChampions"],
        "dmg_per_min": round(player_stats["totalDamageDealtToChampions"] / minutes, 1),
        "total_farm": total_farm,
        "farm_per_min": round(total_farm / minutes, 1),
        "total_gold": player_stats["goldEarned"],
        "gold_per_min": round(player_stats["goldEarned"] / minutes, 1),

        # Vision & Objectives
        "bought_pinks": player_stats["visionWardsBoughtInGame"],
        "vision_score": player_stats["visionScore"],
        "wards_placed": player_stats["wardsPlaced"],
        "wards_per_min": round(player_stats["wardsPlaced"] / minutes, 1),
        "dmg_to_objectives": player_stats['damageDealtToObjectives'],
        "tower_destroyed": player_stats['turretTakedowns'],
    }