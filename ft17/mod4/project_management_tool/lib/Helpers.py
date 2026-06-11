# utils/helpers.py
# Shared lookup utilities used across CLI command handlers.

from models.user import User
from models.project import Project


def find_user(users: list[User], name: str) -> User | None:
    """
    Return the first User whose name matches (case-insensitive).

    Args:
        users: The full in-memory list of users.
        name:  The name to search for.

    Returns:
        The matching User, or None if not found.
    """
    for user in users:
        if user.name.lower() == name.lower():
            return user
    return None


def find_project(user: User, title: str) -> Project | None:
    """
    Return the first Project in a user's list that matches the title
    (case-insensitive).

    Args:
        user:  The User to search within.
        title: The project title to match.

    Returns:
        The matching Project, or None if not found.
    """
    return user.get_project_by_title(title)