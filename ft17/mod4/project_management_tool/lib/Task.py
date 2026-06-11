# models/task.py
# Task belongs to a Project (one-to-many).


class Task:
    """
    Represents a single unit of work inside a project.

    Attributes:
        title       (str): Short description of the work.
        status      (str): 'pending' or 'complete'.
        assigned_to (str): Team member responsible.
    """

    VALID_STATUSES = ("pending", "complete")

    # Class-level counter — every Task gets a unique auto-incremented ID
    _id_counter: int = 1

    def __init__(self, title: str, assigned_to: str = "Unassigned", status: str = "pending"):
        self.id: int = Task._id_counter
        Task._id_counter += 1

        # Initialise backing fields before setters run
        self._title = ""
        self._status = ""
        self._assigned_to = ""

        self.title = title
        self.status = status
        self.assigned_to = assigned_to

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Task title must be a non-empty string.")
        self._title = value.strip()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in self.VALID_STATUSES:
            raise ValueError(
                f"Status must be one of {self.VALID_STATUSES}, got {value!r}."
            )
        self._status = value

    @property
    def assigned_to(self) -> str:
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value: str):
        self._assigned_to = value.strip() if value else "Unassigned"

    # ------------------------------------------------------------------ #
    # Instance methods
    # ------------------------------------------------------------------ #

    def complete(self):
        """Mark this task as complete."""
        self._status = "complete"

    # ------------------------------------------------------------------ #
    # Serialisation helpers
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Convert Task to a JSON-serialisable dictionary."""
        return {
            "id": self.id,
            "title": self._title,
            "status": self._status,
            "assigned_to": self._assigned_to,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Reconstruct a Task from a dictionary loaded from JSON."""
        task = cls(
            title=data["title"],
            assigned_to=data.get("assigned_to", "Unassigned"),
            status=data.get("status", "pending"),
        )
        task.id = data.get("id", task.id)
        return task

    def __str__(self) -> str:
        return (
            f"[{self._status.upper()}] Task #{self.id}: "
            f"{self._title} (assigned to: {self._assigned_to})"
        )

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self._title!r}, status={self._status!r})"