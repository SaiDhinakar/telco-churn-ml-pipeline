import yaml
import threading

_config = None
_lock = threading.Lock()
CONFIG_PATH = "configs/prod.yml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def get_config():
    global _config
    if _config is None:
        _config = load_config()
    return _config

def reload_config():
    global _config
    with _lock:
        _config = load_config()
    return _config
