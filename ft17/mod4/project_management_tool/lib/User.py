# models/user.py
# User extends Person — demonstrates inheritance.
# One User owns many Projects (one-to-many relationship).

from models.person import Person
from models.project import Project


class User(Person):
    """
    Represents a registered system user who owns projects.

    Inherits:
        name, email — from Person (with validated setters).

    Additional attributes:
        role     (str) : The user's role, e.g. 'developer', 'admin'.
        projects (list): Projects owned by this user.
    """

    _id_counter: int = 1

    def __init__(self, name: str, email: str, role: str = "developer"):
        super().__init__(name, email)          # Person.__init__ with validation
        self.id: int = User._id_counter
        User._id_counter += 1
        self._role = role.strip()
        self._projects: list[Project] = []

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, value: str):
        self._role = value.strip()

    @property
    def projects(self) -> list[Project]:
        """Return a copy of the project list to protect internal state."""
        return list(self._projects)

    # ------------------------------------------------------------------ #
    # Project management methods
    # ------------------------------------------------------------------ #

    def add_project(self, project: Project):
        """
        Associate a Project with this user.

        Raises:
            TypeError : If argument is not a Project instance.
            ValueError: If a project with the same title already exists.
        """
        if not isinstance(project, Project):
            raise TypeError("Only Project instances can be added to a user.")
        if any(p.title.lower() == project.title.lower() for p in self._projects):
            raise ValueError(
                f"User '{self._name}' already has a project titled '{project.title}'."
            )
        self._projects.append(project)

    def get_project_by_title(self, title: str) -> Project | None:
        """Find a project by title (case-insensitive). Returns None if not found."""
        for project in self._projects:
            if project.title.lower() == title.lower():
                return project
        return None

    # ------------------------------------------------------------------ #
    # Serialisation
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self._name,
            "email": self._email,
            "role": self._role,
            "projects": [p.to_dict() for p in self._projects],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(
            name=data["name"],
            email=data["email"],
            role=data.get("role", "developer"),
        )
        user.id = data.get("id", user.id)
        for project_data in data.get("projects", []):
            user.add_project(Project.from_dict(project_data))
        return user

    def __str__(self) -> str:
        return (
            f"User #{self.id}: {self._name} <{self._email}> "
            f"[{self._role}] — {len(self._projects)} project(s)"
        )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self._name!r}, email={self._email!r})"