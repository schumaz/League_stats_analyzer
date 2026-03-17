import json
import os

main_data_file = "match_history.json"

def is_match_saved(match_id):
    if not os.path.exists(main_data_file):
        return False
    
    with open(main_data_file, 'r', encoding='utf-8') as file:
        history = json.load(file)

    for match in history:
        if match["match_id"] == match_id:
            return True
    
    return False

def save_match_data(match_data):
    history = []

    if os.path.exists(main_data_file):
        with open(main_data_file, 'r', encoding='utf-8') as file:
            history = json.load(file)

    history.append(match_data)

    with open(main_data_file, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=4)

    print("Match saved on the local database!")