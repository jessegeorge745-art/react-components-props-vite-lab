# lib/task.py
# Defines the Task class.


class Task:
    """Represents a single task inside a project."""

    def __init__(self, title, assigned_to="Unassigned", status="pending"):
        self.title = title
        self.assigned_to = assigned_to
        self.status = status

    def to_dict(self):
        """Convert Task to a dictionary for JSON storage."""
        return {
            "title": self.title,
            "assigned_to": self.assigned_to,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Task from a dictionary loaded from JSON."""
        return cls(
            data["title"],
            data.get("assigned_to", "Unassigned"),
            data.get("status", "pending"),
        )

    def __str__(self):
        return f"[{self.status.upper()}] {self.title} (assigned to: {self.assigned_to})"