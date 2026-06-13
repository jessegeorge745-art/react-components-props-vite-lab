# lib/task.py
# Defines the Task class.

from __future__ import annotations

VALID_STATUSES = {"pending", "in-progress", "complete"}


class Task:
    """A single unit of work inside a Project."""

    _id_counter = 0  # class attribute

    def __init__(self, title: str, assigned_to: str = "Unassigned", status: str = "pending"):
        Task._id_counter += 1
        self._id = Task._id_counter
        self._title = title
        self._assigned_to = assigned_to
        self._status = status

    # ── properties ────────────────────────────────────────────
    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value.strip()

    @property
    def assigned_to(self) -> str:
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value: str):
        self._assigned_to = value.strip() if value else "Unassigned"

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value.lower() not in VALID_STATUSES:
            raise ValueError(
                f"Status must be one of: {', '.join(sorted(VALID_STATUSES))}"
            )
        self._status = value.lower()

    # ── serialisation ─────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "title": self._title,
            "assigned_to": self._assigned_to,
            "status": self._status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            data["title"],
            data.get("assigned_to", "Unassigned"),
            data.get("status", "pending"),
        )

    def __str__(self):
        return f"[{self._status.upper()}] {self._title} → {self._assigned_to}"

    def __repr__(self):
        return f"Task(title={self._title!r}, status={self._status!r})"