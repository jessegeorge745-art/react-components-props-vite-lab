# lib/user.py
# Defines the Person base class and User subclass (inheritance).

from lib.project import Project


class Person:
    """Base class representing any person in the system."""

    _id_counter = 0  # class attribute: auto-incrementing ID

    def __init__(self, name: str, email: str):
        Person._id_counter += 1
        self._id = Person._id_counter
        self._name = name
        self._email = email

    # ── properties (encapsulation) ────────────────────────────
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if "@" not in value or "." not in value:
            raise ValueError(f"Invalid email address: '{value}'")
        self._email = value.strip().lower()

    def __repr__(self):
        return f"Person(id={self._id}, name={self._name!r})"


class User(Person):
    """A system user who can own multiple projects (one-to-many)."""

    def __init__(self, name: str, email: str, role: str = "developer"):
        super().__init__(name, email)
        self._role = role
        self.projects: list[Project] = []

    # ── role property ─────────────────────────────────────────
    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, value: str):
        allowed = {"developer", "manager", "admin", "designer", "tester"}
        if value.lower() not in allowed:
            raise ValueError(f"Role must be one of: {', '.join(sorted(allowed))}")
        self._role = value.lower()

    # ── project helpers ───────────────────────────────────────
    def add_project(self, project: Project) -> None:
        """Attach a project to this user."""
        self.projects.append(project)

    def find_project(self, title: str):
        """Case-insensitive project lookup. Returns Project or None."""
        for p in self.projects:
            if p.title.lower() == title.lower():
                return p
        return None

    def remove_project(self, title: str) -> bool:
        """Remove a project by title. Returns True on success."""
        project = self.find_project(title)
        if project:
            self.projects.remove(project)
            return True
        return False

    # ── serialisation ─────────────────────────────────────────
    def to_dict(self) -> dict:
        """Serialise User → dict for JSON storage."""
        return {
            "name": self._name,
            "email": self._email,
            "role": self._role,
            "projects": [p.to_dict() for p in self.projects],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Rebuild a User (and nested projects/tasks) from a JSON dict."""
        user = cls(data["name"], data["email"], data.get("role", "developer"))
        for p in data.get("projects", []):
            user.add_project(Project.from_dict(p))
        return user

    def __str__(self):
        return (
            f"{self._name} <{self._email}> "
            f"[{self._role}] — {len(self.projects)} project(s)"
        )

    def __repr__(self):
        return f"User(name={self._name!r}, email={self._email!r}, role={self._role!r})"