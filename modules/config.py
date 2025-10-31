import json
from pathlib import Path

_settings_cache = None

def _settings_path():
    root_dir = Path(__file__).resolve().parents[1]
    return root_dir / "settings.json"  

def load_settings():
    """
    Läser och cachar settings.json. Ger lättbegripliga felmeddelanden
    med rad och kolumn om JSON inte är giltig.
    """
    global _settings_cache
    if _settings_cache is not None:
        return _settings_cache

    path = _settings_path()  # Path-objekt till settings.json
    if not path.exists():
        raise FileNotFoundError(
            f"Hittar inte {path}. Förväntar mig settings.json i projektroten."
        )

    try:
        # explicit encoding minskar problem med BOM
        with path.open("r", encoding="utf-8") as f:  # filhandtag med UTF-8
            _settings_cache = json.load(f)           # parse till Python-dict
            return _settings_cache
    except json.JSONDecodeError as e:
        # e.lineno / e.colno pekar exakt på felet
        # Vi läser om filen som text för att kunna visa problemraden.
        raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
        bad_line = raw[e.lineno - 1] if 0 < e.lineno <= len(raw) else ""
        pointer = " " * (e.colno - 1) + "^"
        msg = (
            f"Ogiltig JSON i {path}\n"
            f"Rad {e.lineno}, kolumn {e.colno}: {e.msg}\n"
            f"{bad_line}\n{pointer}\n\n"
            "Vanliga orsaker: sista-komma, kommentarer, enkla citationstecken, "
            "NaN/Infinity, oescapade backslashar."
        )
        raise ValueError(msg) from e

def get_section(section_name):

    settings = load_settings()
    return settings.get(section_name, {})