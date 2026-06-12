# utils/storage.py
# Handles saving and loading all data to/from a JSON file.

import json
import os

from lib.user import User

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")


def save_users(users):
    """Save all users to the JSON data file."""
    # Make sure the data/ folder exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, "w") as f:
        json.dump({"users": [u.to_dict() for u in users]}, f, indent=2)


def load_users():
    """Load all users from the JSON data file. Returns an empty list if missing."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
        if not content:
            return []
        data = json.loads(content)
        return [User.from_dict(u) for u in data.get("users", [])]
    except (json.JSONDecodeError, KeyError):
        print("Warning: data file is corrupted. Starting fresh.")
        return []