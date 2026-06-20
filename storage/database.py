import json
import os
from datetime import datetime

HISTORY_FILE = "storage/history.json"

def init_db():
    os.makedirs("storage", exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

def load_history():
    init_db()
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_match(level_name, algo_name, total_steps, execution_time, status):
    history = load_history()
    match_data = {
        "id": len(history) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": level_name,
        "algo": algo_name,
        "steps": total_steps,
        "time": f"{execution_time:.2f}s",
        "status": status
    }
    history.append(match_data)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def delete_history_item(match_id):
    history = load_history()
    history = [m for m in history if m["id"] != match_id]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def clear_all_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)