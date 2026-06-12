# utils/storage.py
# Handles saving and loading all data to/from data/data.json.

import json
import os
from lib.user import User

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "data.json")


def load_data() -> list[User]:
    """Load users (with nested projects and tasks) from JSON. Returns an empty list if no file exists."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError:
            return []
    return [User.from_dict(u) for u in raw]


def save_data(users: list[User]) -> None:
    """Persist all users to JSON, creating the data/ directory if needed."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in users], f, indent=2)