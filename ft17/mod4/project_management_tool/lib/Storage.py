# utils/storage.py
# Handles all JSON file I/O — saving and loading the full object graph.

import json
import os

from models.user import User

# Paths relative to this file so the tool works from any working directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "data.json")


def _ensure_data_dir():
    """Create the data/ directory if it does not already exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def save_users(users: list[User]) -> None:
    """
    Persist all users (and their nested projects/tasks) to JSON.

    Args:
        users: List of User objects to serialise.
    """
    _ensure_data_dir()
    payload = {"users": [u.to_dict() for u in users]}
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(payload, f, indent=2)
    except OSError as e:
        print(f"[ERROR] Could not write to {DATA_FILE}: {e}")


def load_users() -> list[User]:
    """
    Load all users from the JSON data file.

    Returns:
        List of User objects, or an empty list if the file is
        missing, empty, or malformed.
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
        if not content:
            return []

        payload = json.loads(content)
        users = [User.from_dict(u) for u in payload.get("users", [])]

        # Re-sync class-level ID counters so new objects never clash with
        # IDs that were assigned in a previous session.
        from models.user import User as U
        from models.project import Project as P
        from models.task import Task as T

        all_user_ids    = [u.id for u in users]
        all_project_ids = [p.id for u in users for p in u.projects]
        all_task_ids    = [t.id for u in users for p in u.projects for t in p.tasks]

        if all_user_ids:
            U._id_counter = max(all_user_ids) + 1
        if all_project_ids:
            P._id_counter = max(all_project_ids) + 1
        if all_task_ids:
            T._id_counter = max(all_task_ids) + 1

        return users

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"[WARNING] Data file is malformed and will be ignored: {e}")
        return []