# utils/storage.py
# Handles saving and loading all data to/from data/data.json.

import json
import os
import logging
from lib.user import User

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "data.json")


def load_data() -> list[User]:
    """
    Load all users (with nested projects and tasks) from JSON.
    Returns an empty list if the file does not exist or is malformed.
    """
    if not os.path.exists(DATA_FILE):
        logger.info("No data file found — starting fresh.")
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        users = [User.from_dict(u) for u in raw]
        logger.info("Loaded %d user(s) from %s", len(users), DATA_FILE)
        return users
    except json.JSONDecodeError as e:
        logger.error("Malformed JSON in data file: %s", e)
        return []
    except (KeyError, TypeError) as e:
        logger.error("Data schema error while loading: %s", e)
        return []


def save_data(users: list[User]) -> None:
    """
    Persist all users to JSON, creating the data/ directory if needed.
    """
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in users], f, indent=2)
        logger.info("Saved %d user(s) to %s", len(users), DATA_FILE)
    except OSError as e:
        logger.error("Failed to save data: %s", e)
        raise