import json
import os

SENT_LOG_FILE = "sent_problems.json"

def load_sent():
    if os.path.isfile(SENT_LOG_FILE):
        with open(SENT_LOG_FILE, "r") as f:
            try:
                return set(json.load(f))
            except Exception:
                return set()
    return set()

def save_sent(sent_set):
    with open(SENT_LOG_FILE, "w") as f:
        json.dump(list(sent_set), f)
