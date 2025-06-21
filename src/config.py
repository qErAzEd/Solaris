import json
import os

def load_config(config_file):
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), config_file))
    try:
        with open(config_path, "r") as f:
            data = json.load(f)
        min_cps = data.get("min_cps", 15)
        max_cps = data.get("max_cps", 20)
        bound_key = data.get("bound_key", "f6") or "f6"
        return min_cps if isinstance(min_cps, int) else 15, max_cps if isinstance(max_cps, int) else 20, bound_key if isinstance(bound_key, str) else "f6"
    except:
        save_config(config_file, 15, 20, "f6")
        return 15, 20, "f6"

def save_config(config_file, min_cps, max_cps, bound_key):
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), config_file))
    data = {
        "min_cps": min_cps,
        "max_cps": max_cps,
        "bound_key": bound_key
    }
    try:
        with open(config_path, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass
