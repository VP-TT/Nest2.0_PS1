import json, os, datetime

STATE_PATH = "state/history.json"
LATEST_PATH = "state/latest_snapshot.json"

def _load(path):
    if not os.path.exists(path):
        return None
    try:
        text = open(path).read().strip()
        if not text:
            return None
        return json.loads(text)
    except:
        return None

def _save(path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

def load_memory():
    hist = _load(STATE_PATH)
    return hist if isinstance(hist, list) else []

def save_snapshot(snapshot):
    snapshot["timestamp"] = datetime.datetime.utcnow().isoformat()
    history = load_memory()
    history.append(snapshot)
    _save(STATE_PATH, history)
    _save(LATEST_PATH, snapshot)

def load_latest_snapshot():
    return _load(LATEST_PATH)

def load_last_n(n=5):
    hist = load_memory()
    return hist[-n:]
