# lib/project.py
# Defines the Project class with one-to-many relationship to Task.

from __future__ import annotations


class Project:
    """A project owned by a User, containing multiple Tasks."""

    _id_counter = 0  # class attribute

    def __init__(self, title: str, description: str = "", due_date: str = ""):
        Project._id_counter += 1
        self._id = Project._id_counter
        self._title = title
        self.description = description
        self.due_date = due_date
        self.tasks: list = []  # one-to-many: Project → Tasks

    # ── title property ────────────────────────────────────────
    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    # ── task helpers ──────────────────────────────────────────
    def add_task(self, task) -> None:
        """Add a Task to this project."""
        self.tasks.append(task)

    def find_task(self, title: str):
        """Case-insensitive task lookup. Returns Task or None."""
        for t in self.tasks:
            if t.title.lower() == title.lower():
                return t
        return None

    def complete_task(self, title: str) -> bool:
        """Mark a task complete. Returns True on success, False if not found."""
        task = self.find_task(title)
        if task:
            task.status = "complete"
            return True
        return False

    def remove_task(self, title: str) -> bool:
        """Delete a task by title. Returns True on success."""
        task = self.find_task(title)
        if task:
            self.tasks.remove(task)
            return True
        return False

    @property
    def progress(self) -> str:
        """Return 'done/total' progress string."""
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.status == "complete")
        return f"{done}/{total}"

    # ── serialisation ─────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "title": self._title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        from lib.task import Task
        project = cls(data["title"], data.get("description", ""), data.get("due_date", ""))
        for t in data.get("tasks", []):
            project.add_task(Task.from_dict(t))
        return project

    def __str__(self):
        return (
            f"{self._title} | Due: {self.due_date or 'N/A'} "
            f"| Progress: {self.progress}"
        )

    def __repr__(self):
        return f"Project(title={self._title!r}, tasks={len(self.tasks)})"