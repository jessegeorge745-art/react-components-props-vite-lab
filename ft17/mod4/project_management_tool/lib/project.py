# lib/project.py
# Defines the Project class.


class Project:
    """Represents a project that belongs to a user and contains tasks."""

    def __init__(self, title, description="", due_date=""):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []  # one project has many tasks

    def add_task(self, task):
        """Add a task to this project."""
        self.tasks.append(task)

    def find_task(self, title):
        """Find a task by title (case-insensitive). Returns None if not found."""
        for task in self.tasks:
            if task.title.lower() == title.lower():
                return task
        return None

    def complete_task(self, title):
        """Mark a task as complete. Returns True on success, False if not found."""
        task = self.find_task(title)
        if task:
            task.status = "complete"
            return True
        return False

    def to_dict(self):
        """Convert Project to a dictionary for JSON storage."""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Project from a dictionary loaded from JSON."""
        from lib.task import Task
        project = cls(data["title"], data.get("description", ""), data.get("due_date", ""))
        for t in data.get("tasks", []):
            project.add_task(Task.from_dict(t))
        return project

    def __str__(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.status == "complete")
        return f"{self.title} | Due: {self.due_date or 'N/A'} | {done}/{total} tasks complete"