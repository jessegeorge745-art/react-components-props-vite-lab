# testing/test_project_management.py
# Unit tests for User, Project, Task, and storage.

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.user import User
from lib.project import Project
from lib.task import Task


# ── Task tests ────────────────────────────────────────────────────────────────

class TestTask:

    def test_task_created_with_defaults(self):
        task = Task("Write tests")
        assert task.title == "Write tests"
        assert task.status == "pending"
        assert task.assigned_to == "Unassigned"

    def test_task_created_with_values(self):
        task = Task("Deploy app", assigned_to="Alex", status="complete")
        assert task.assigned_to == "Alex"
        assert task.status == "complete"

    def test_task_serialisation_roundtrip(self):
        task = Task("Fix bug", assigned_to="Sam", status="pending")
        restored = Task.from_dict(task.to_dict())
        assert restored.title == task.title
        assert restored.assigned_to == task.assigned_to
        assert restored.status == task.status


# ── Project tests ─────────────────────────────────────────────────────────────

class TestProject:

    def test_project_created(self):
        project = Project("CLI Tool", description="Build it", due_date="2025-12-31")
        assert project.title == "CLI Tool"
        assert project.description == "Build it"
        assert project.due_date == "2025-12-31"

    def test_add_task(self):
        project = Project("My Project")
        project.add_task(Task("First task"))
        assert len(project.tasks) == 1

    def test_find_task(self):
        project = Project("My Project")
        task = Task("Fix bug")
        project.add_task(task)
        assert project.find_task("fix bug") is task

    def test_find_task_not_found(self):
        project = Project("My Project")
        assert project.find_task("Ghost") is None

    def test_complete_task(self):
        project = Project("My Project")
        project.add_task(Task("Fix bug"))
        result = project.complete_task("Fix bug")
        assert result is True
        assert project.tasks[0].status == "complete"

    def test_complete_task_not_found(self):
        project = Project("My Project")
        assert project.complete_task("Ghost task") is False

    def test_project_serialisation_roundtrip(self):
        project = Project("My Project", description="desc", due_date="2025-01-01")
        project.add_task(Task("Task one", assigned_to="Bob"))
        restored = Project.from_dict(project.to_dict())
        assert restored.title == project.title
        assert len(restored.tasks) == 1
        assert restored.tasks[0].title == "Task one"


# ── User tests ────────────────────────────────────────────────────────────────

class TestUser:

    def test_user_created(self):
        user = User("Alice", "alice@example.com", role="admin")
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.role == "admin"

    def test_user_default_role(self):
        user = User("Bob", "bob@example.com")
        assert user.role == "developer"

    def test_add_project(self):
        user = User("Carol", "carol@example.com")
        user.add_project(Project("New Project"))
        assert len(user.projects) == 1

    def test_find_project(self):
        user = User("Dave", "dave@example.com")
        project = Project("Find Me")
        user.add_project(project)
        assert user.find_project("find me") is project

    def test_find_project_not_found(self):
        user = User("Eve", "eve@example.com")
        assert user.find_project("Ghost") is None

    def test_user_serialisation_roundtrip(self):
        user = User("Frank", "frank@example.com", role="developer")
        project = Project("Frank's Project")
        project.add_task(Task("Write docs"))
        user.add_project(project)
        restored = User.from_dict(user.to_dict())
        assert restored.name == "Frank"
        assert len(restored.projects) == 1
        assert len(restored.projects[0].tasks) == 1


# ── Storage tests ─────────────────────────────────────────────────────────────

class TestStorage:

    def test_save_and_load(self, tmp_path, monkeypatch):
        import utils.storage as storage
        monkeypatch.setattr(storage, "DATA_FILE", str(tmp_path / "data.json"))

        user = User("Judy", "judy@example.com")
        project = Project("Test Project")
        project.add_task(Task("Persist me"))
        user.add_project(project)

        storage.save_users([user])
        loaded = storage.load_users()

        assert len(loaded) == 1
        assert loaded[0].name == "Judy"
        assert len(loaded[0].projects) == 1
        assert len(loaded[0].projects[0].tasks) == 1

    def test_load_missing_file(self, tmp_path, monkeypatch):
        import utils.storage as storage
        monkeypatch.setattr(storage, "DATA_FILE", str(tmp_path / "missing.json"))
        assert storage.load_users() == []

    def test_load_empty_file(self, tmp_path, monkeypatch):
        import utils.storage as storage
        empty = tmp_path / "empty.json"
        empty.write_text("")
        monkeypatch.setattr(storage, "DATA_FILE", str(empty))
        assert storage.load_users() == []

    def test_load_corrupted_file(self, tmp_path, monkeypatch):
        import utils.storage as storage
        bad = tmp_path / "bad.json"
        bad.write_text("{ not valid json }")
        monkeypatch.setattr(storage, "DATA_FILE", str(bad))
        assert storage.load_users() == []