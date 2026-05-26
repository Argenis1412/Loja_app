import os
from pathlib import Path

_ENV_LOADED = False

def bootstrap_environment():
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    _ENV_LOADED = True
