import json


def safe_json_loads(text, fallback=None):
    try:
        return json.loads(text)
    except Exception:
        return fallback