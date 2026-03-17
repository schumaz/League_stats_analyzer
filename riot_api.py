from riotwatcher import LolWatcher, RiotWatcher, ApiError
from database import save_match_data

def fetch_puuid(api_key, player_name, player_tag, region):
    riot_watcher = RiotWatcher(api_key)
    account = riot_watcher.account.by_riot_id(region, player_name, player_tag)

    return account["puuid"]

def fetch_match_history(api_key, puuid, region):
    lol_watcher = LolWatcher(api_key)
    match_ids = lol_watcher.match.matchlist_by_puuid(region, puuid)

    return match_ids

def fetch_match_details(api_key, match_id, region):
    lol_watcher = LolWatcher(api_key)
    match_data = lol_watcher.match.by_id(region, match_id)

    return match_data

def extract_player_stats(match_data, puuid):
    participants = match_data["info"]["participants"]

    for player in participants:
        if player["puuid"] == puuid:
            return player
        
    return None

def clean_player_stats(player_stats, game_duration_seconds):
    # Total game minutes calculation
    minutes = game_duration_seconds / 60

    # Total farm calculation
    total_farm = player_stats['totalMinionsKilled'] + player_stats["neutralMinionsKilled"]

    # Per minute calculations
    farm_per_min = total_farm / minutes
    gold_per_min = player_stats["goldEarned"] / minutes
    wards_per_min = player_stats["wardsPlaced"] / minutes
    dmg_per_min = player_stats["totalDamageDealtToChampions"] / minutes

    return {
        # --- PLAYER ---
        "assists": player_stats["assists"],
        "champ": player_stats["championName"],
        "deaths": player_stats["deaths"],
        "dmg_per_min": round(dmg_per_min, 1),
        "kills": player_stats["kills"],
        "role": player_stats["teamPosition"],
        "total_dmg": player_stats["totalDamageDealtToChampions"],

        # --- ECONOMY ---
        "farm_per_min": round(farm_per_min, 1),
        "gold_per_min": round(gold_per_min, 1),
        "total_farm": total_farm,
        "total_gold": player_stats["goldEarned"],

        # --- VISION ---
        "bought_pinks": player_stats["visionWardsBoughtInGame"],
        "vision_score": player_stats["visionScore"],
        "wards_per_min": round(wards_per_min, 1),
        "wards_placed": player_stats["wardsPlaced"],

        # --- OBJECTIVES ---
        "dmg_to_objectives": player_stats['damageDealtToObjectives'],
        "tower_destroyed": player_stats['turretTakedowns'],

        # --- TIME ---
        "match_duration": round(minutes, 2),
    }