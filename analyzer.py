import json
from collections import Counter

database = "match_history.json"

def analyze_performance(target_role=None):
    """
    Reads match history and calculates average performance stats, 
    optionally filtered by a specific role.
    """
    with open(database, 'r', encoding='utf-8') as file:
        history = json.load(file)

    total_matches = 0
    
    # Accumulators for basic stats
    total_kills, total_deaths, total_assists = 0, 0, 0
    total_farm_per_min = 0

    # Accumulators for advanced metrics
    total_dmg_per_min = 0
    total_gold_per_min = 0
    total_vision_score = 0
    total_pinks = 0
    total_obj_dmg = 0
    total_towers = 0
    total_wards = 0

    champions_played = Counter()

    for match in history:
        # Process match only if it matches the target role (or if no role is targeted)
        if target_role is None or match["role"] == target_role:
            total_matches += 1
            
            # KDA and Farm
            total_kills += match.get("kills", 0)
            total_deaths += match.get("deaths", 0)
            total_assists += match.get("assists", 0)
            total_wards += match.get("wards_placed", 0)
            total_farm_per_min += match.get("farm_per_min", 0)

            # Per min metrics
            total_dmg_per_min += match.get("dmg_per_min", 0)
            total_gold_per_min += match.get("gold_per_min", 0)
            total_vision_score += match.get("vision_score", 0)
            total_pinks += match.get("bought_pinks", 0)
            total_obj_dmg += match.get("dmg_to_objectives", 0)
            total_towers += match.get("tower_destroyed", 0)

            champions_played[match.get("champ")] += 1

    # Exit early if no matches are found
    if total_matches == 0:
        print(f"No matches found for role: {target_role}")
        return None
    
    # Prevent division by zero for perfect KDA
    if total_deaths == 0:
        kda_ratio = float('inf')
    else:
        kda_ratio = (total_kills + total_assists) / total_deaths

    # Compile the final averaged statistics
    stats = {
        "Total Matches": total_matches,
        "Most Played Champs": dict(champions_played.most_common(3)),
        
        # Performance
        "Avg Kills": round(total_kills / total_matches, 1),
        "Avg Deaths": round(total_deaths / total_matches, 1),
        "Avg Assists": round(total_assists / total_matches, 1),
        "KDA Ratio": round(kda_ratio, 2),
        
        # Economy and Damage
        "Avg Farm/Min": round(total_farm_per_min / total_matches, 1),
        "Avg Gold/Min": round(total_gold_per_min / total_matches, 1),
        "Avg Damage/Min (DPM)": round(total_dmg_per_min / total_matches, 1),
        
        # Objectives
        "Avg DMG to objectives": round(total_obj_dmg / total_matches, 0),
        "Avg Towers destroyed": round(total_towers / total_matches, 1),
        
        # Vision
        "Total Wards Placed": total_wards,
        "Avg Vision Score": round(total_vision_score / total_matches, 1),
        "Avg Pinks Bought": round(total_pinks / total_matches, 1)
    }

    title = target_role if target_role is not None else "GLOBAL"
    print(f"\n=== PERFORMANCE OVERVIEW: {title} ===")

    for key, value in stats.items():
        print(f"{key}: {value}")
        
    print("=======================================\n")
    return stats