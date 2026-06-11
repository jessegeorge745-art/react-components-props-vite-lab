# testing/test_models.py
# Full unit test suite — covers Task, Project, User, helpers, and storage.

import os
import sys
import pytest

# Ensure project root is importable regardless of where pytest runs from
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.task import Task
from models.project import Project
from models.user import User
from utils.helpers import find_user, find_project


# ══════════════════════════════════════════════════════════════════════════════
# Task
# ══════════════════════════════════════════════════════════════════════════════

class TestTask:

    def test_task_created_with_defaults(self):
        t = Task(title="Write tests")
        assert t.title == "Write tests"
        assert t.status == "pending"
        assert t.assigned_to == "Unassigned"

    def test_task_complete(self):
        t = Task(title="Deploy app")
        t.complete()
        assert t.status == "complete"

    def test_task_invalid_status_raises(self):
        with pytest.raises(ValueError):
            Task(title="Bad task", status="in-progress")

    def test_task_empty_title_raises(self):
        with pytest.raises(ValueError):
            Task(title="")

    def test_task_serialisation_roundtrip(self):
        t = Task(title="API integration", assigned_to="Alex", status="pending")
        restored = Task.from_dict(t.to_dict())
        assert restored.title == t.title
        assert restored.status == t.status
        assert restored.assigned_to == t.assigned_to


# ══════════════════════════════════════════════════════════════════════════════
# Project
# ══════════════════════════════════════════════════════════════════════════════

class TestProject:

    def test_project_created(self):
        p = Project(title="CLI Tool", description="A test project", due_date="2025-12-31")
        assert p.title == "CLI Tool"
        assert p.description == "A test project"
        assert p.due_date == "2025-12-31"

    def test_project_empty_title_raises(self):
        with pytest.raises(ValueError):
            Project(title="")

    def test_add_task_to_project(self):
        p = Project(title="My Project")
        p.add_task(Task(title="First task"))
        assert len(p.tasks) == 1

    def test_add_non_task_raises(self):
        p = Project(title="My Project")
        with pytest.raises(TypeError):
            p.add_task("not a task")

    def test_complete_task_by_title(self):
        p = Project(title="My Project")
        p.add_task(Task(title="Fix bug"))
        assert p.complete_task("Fix bug") is True
        assert p.tasks[0].status == "complete"

    def test_complete_nonexistent_task_returns_false(self):
        p = Project(title="My Project")
        assert p.complete_task("Ghost task") is False

    def test_completion_summary(self):
        p = Project(title="My Project")
        p.add_task(Task(title="Task A"))
        p.add_task(Task(title="Task B"))
        p.complete_task("Task A")
        assert p.completion_summary == "1/2 tasks complete"

    def test_project_serialisation_roundtrip(self):
        p = Project(title="Roundtrip", description="desc", due_date="2025-01-01")
        p.add_task(Task(title="task one", assigned_to="Bob"))
        restored = Project.from_dict(p.to_dict())
        assert restored.title == p.title
        assert len(restored.tasks) == 1
        assert restored.tasks[0].title == "task one"


# ══════════════════════════════════════════════════════════════════════════════
# User
# ══════════════════════════════════════════════════════════════════════════════

class TestUser:

    def test_user_created(self):
        u = User(name="Alice", email="alice@example.com", role="admin")
        assert u.name == "Alice"
        assert u.email == "alice@example.com"
        assert u.role == "admin"

    def test_user_invalid_email_raises(self):
        with pytest.raises(ValueError):
            User(name="Bob", email="not-an-email")

    def test_user_empty_name_raises(self):
        with pytest.raises(ValueError):
            User(name="", email="bob@example.com")

    def test_add_project_to_user(self):
        u = User(name="Carol", email="carol@example.com")
        u.add_project(Project(title="New Project"))
        assert len(u.projects) == 1

    def test_duplicate_project_title_raises(self):
        u = User(name="Dave", email="dave@example.com")
        u.add_project(Project(title="Duplicate"))
        with pytest.raises(ValueError):
            u.add_project(Project(title="Duplicate"))

    def test_add_non_project_raises(self):
        u = User(name="Eve", email="eve@example.com")
        with pytest.raises(TypeError):
            u.add_project("not a project")

    def test_get_project_by_title_case_insensitive(self):
        u = User(name="Frank", email="frank@example.com")
        p = Project(title="Find Me")
        u.add_project(p)
        assert u.get_project_by_title("find me") is p

    def test_user_serialisation_roundtrip(self):
        u = User(name="Grace", email="grace@example.com", role="developer")
        p = Project(title="Grace's Project")
        p.add_task(Task(title="Write docs"))
        u.add_project(p)
        restored = User.from_dict(u.to_dict())
        assert restored.name == "Grace"
        assert len(restored.projects) == 1
        assert len(restored.projects[0].tasks) == 1


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

class TestHelpers:

    def setup_method(self):
        self.users = [
            User(name="Heidi", email="heidi@example.com"),
            User(name="Ivan",  email="ivan@example.com"),
        ]
        self.users[0].add_project(Project(title="Alpha"))

    def test_find_user_found(self):
        assert find_user(self.users, "Heidi") is self.users[0]

    def test_find_user_case_insensitive(self):
        assert find_user(self.users, "heidi") is self.users[0]

    def test_find_user_not_found(self):
        assert find_user(self.users, "Nobody") is None

    def test_find_project_found(self):
        project = find_project(self.users[0], "Alpha")
        assert project is not None
        assert project.title == "Alpha"

    def test_find_project_not_found(self):
        assert find_project(self.users[0], "Beta") is None


# ══════════════════════════════════════════════════════════════════════════════
# Storage
# ══════════════════════════════════════════════════════════════════════════════

class TestStorage:

    def test_save_and_load_roundtrip(self, tmp_path, monkeypatch):
        """Full save → load cycle using a temporary directory."""
        import utils.storage as storage_module
        monkeypatch.setattr(storage_module, "DATA_DIR",  str(tmp_path))
        monkeypatch.setattr(storage_module, "DATA_FILE", str(tmp_path / "data.json"))

        u = User(name="Judy", email="judy@example.com")
        p = Project(title="Storage Project")
        p.add_task(Task(title="Persist me"))
        u.add_project(p)

        storage_module.save_users([u])
        loaded = storage_module.load_users()

        assert len(loaded) == 1
        assert loaded[0].name == "Judy"
        assert len(loaded[0].projects) == 1
        assert len(loaded[0].projects[0].tasks) == 1

    def test_load_returns_empty_list_when_no_file(self, tmp_path, monkeypatch):
        import utils.storage as storage_module
        monkeypatch.setattr(storage_module, "DATA_FILE", str(tmp_path / "missing.json"))
        assert storage_module.load_users() == []

    def test_load_handles_malformed_json(self, tmp_path, monkeypatch):
        import utils.storage as storage_module
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{ not valid json }")
        monkeypatch.setattr(storage_module, "DATA_FILE", str(bad_file))
        assert storage_module.load_users() == []

    def test_load_handles_empty_file(self, tmp_path, monkeypatch):
        import utils.storage as storage_module
        empty_file = tmp_path / "empty.json"
        empty_file.write_text("")
        monkeypatch.setattr(storage_module, "DATA_FILE", str(empty_file))
        assert storage_module.load_users() == []