# models/project.py
# Project belongs to a User (one-to-many) and owns many Tasks (one-to-many).

from models.task import Task


class Project:
    """
    Represents a project owned by a user.

    Attributes:
        title       (str) : Project name.
        description (str) : Brief summary.
        due_date    (str) : Target date (YYYY-MM-DD).
        tasks       (list): Collection of Task objects.
    """

    _id_counter: int = 1

    def __init__(self, title: str, description: str = "", due_date: str = ""):
        self.id: int = Project._id_counter
        Project._id_counter += 1

        self._title = ""
        self._description = description.strip()
        self._due_date = due_date.strip()
        self._tasks: list[Task] = []

        self.title = title  # validated through setter

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Project title must be a non-empty string.")
        self._title = value.strip()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value.strip()

    @property
    def due_date(self) -> str:
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        self._due_date = value.strip()

    @property
    def tasks(self) -> list[Task]:
        """Return a copy of the task list to protect internal state."""
        return list(self._tasks)

    # ------------------------------------------------------------------ #
    # Task management methods
    # ------------------------------------------------------------------ #

    def add_task(self, task: Task):
        """
        Append a Task to this project.

        Raises:
            TypeError: If the argument is not a Task instance.
        """
        if not isinstance(task, Task):
            raise TypeError("Only Task instances can be added to a project.")
        self._tasks.append(task)

    def get_task_by_title(self, title: str) -> Task | None:
        """Find a task by title (case-insensitive). Returns None if not found."""
        for task in self._tasks:
            if task.title.lower() == title.lower():
                return task
        return None

    def complete_task(self, title: str) -> bool:
        """
        Mark a task complete by title.

        Returns:
            True on success, False if no matching task exists.
        """
        task = self.get_task_by_title(title)
        if task:
            task.complete()
            return True
        return False

    @property
    def completion_summary(self) -> str:
        """Return a human-readable progress string, e.g. '2/5 tasks complete'."""
        total = len(self._tasks)
        done = sum(1 for t in self._tasks if t.status == "complete")
        return f"{done}/{total} tasks complete"

    # ------------------------------------------------------------------ #
    # Serialisation
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "tasks": [t.to_dict() for t in self._tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        project = cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
        )
        project.id = data.get("id", project.id)
        for task_data in data.get("tasks", []):
            project.add_task(Task.from_dict(task_data))
        return project

    def __str__(self) -> str:
        return (
            f"Project #{self.id}: {self._title} | "
            f"Due: {self._due_date or 'N/A'} | {self.completion_summary}"
        )

    def __repr__(self) -> str:
        return f"Project(id={self.id}, title={self._title!r})"