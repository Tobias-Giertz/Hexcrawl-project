import json
from pathlib import Path

_settings_cache = None

def load_settings():
    global _settings_cache
    if _settings_cache is None:
        root = Path(__file__).resolve().parents[1]
        with open(root / "settings.json", "r") as f:
            _settings_cache = json.load(f)
    return _settings_cache

def get_section(section_name):
    settings = load_settings()
    return settings.get(section_name, {})