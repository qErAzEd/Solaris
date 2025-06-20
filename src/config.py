import json
import os

def load_config(config_file):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    if not os.path.exists(config_path):
        return 15, 20, "f6"
    with open(config_path, "r") as f:
        data = json.load(f)
    return data.get("min_cps", 15), data.get("max_cps", 20), data.get("bound_key", "f6")

def save_config(config_file, min_cps, max_cps, bound_key):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    data = {
        "min_cps": min_cps,
        "max_cps": max_cps,
        "bound_key": bound_key
    }
    with open(config_path, "w") as f:
        json.dump(data, f)
