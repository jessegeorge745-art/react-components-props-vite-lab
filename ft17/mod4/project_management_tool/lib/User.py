# lib/user.py
# Defines the User class.


class User:
    """Represents a system user who owns projects."""

    def __init__(self, name, email, role="developer"):
        self.name = name
        self.email = email
        self.role = role
        self.projects = []  # one user has many projects

    def add_project(self, project):
        """Add a project to this user."""
        self.projects.append(project)

    def find_project(self, title):
        """Find a project by title (case-insensitive). Returns None if not found."""
        for project in self.projects:
            if project.title.lower() == title.lower():
                return project
        return None

    def to_dict(self):
        """Convert User to a dictionary for JSON storage."""
        return {
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "projects": [p.to_dict() for p in self.projects],
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild a User from a dictionary loaded from JSON."""
        from lib.project import Project
        user = cls(data["name"], data["email"], data.get("role", "developer"))
        for p in data.get("projects", []):
            user.add_project(Project.from_dict(p))
        return user

    def __str__(self):
        return f"{self.name} <{self.email}> [{self.role}] — {len(self.projects)} project(s)"