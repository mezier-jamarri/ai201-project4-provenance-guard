import json
import os
from datetime import datetime, timezone

LOG_FILE = "audit_log.json"

def init_log():
    """Creates the log file with an empty list if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

def write_log(entry: dict):
    """Appends a new structured entry to the JSON log file."""
    init_log()
    with open(LOG_FILE, "r+") as f:
        logs = json.load(f)
        
        # Auto-inject a UTC timestamp if not provided
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now(timezone.utc).isoformat()
            
        logs.append(entry)
        
        # Reset file pointer and overwrite with updated list
        f.seek(0)
        json.dump(logs, f, indent=4)
        f.truncate()

def get_logs() -> list:
    """Retrieves all entries from the log file."""
    init_log()
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def update_log_for_appeal(content_id: str, reasoning: str):
    """Finds a log entry by content_id and updates its status and reasoning."""
    init_log()
    with open(LOG_FILE, "r+") as f:
        logs = json.load(f)
        for entry in logs:
            if entry.get("content_id") == content_id:
                entry["status"] = "under_review"
                entry["appeal_reasoning"] = reasoning
                break
        
        f.seek(0)
        json.dump(logs, f, indent=4)
        f.truncate()