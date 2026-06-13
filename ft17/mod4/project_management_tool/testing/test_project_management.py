# testing/test_project_management.py
# Unit tests for User, Project, Task classes and storage utilities.

import json
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lib.task import Task
from lib.project import Project
from lib.user import User


# ═══════════════════════════════════════════════════════════════
# Task tests
# ═══════════════════════════════════════════════════════════════

class TestTask:
    def test_default_status_is_pending(self):
        t = Task("Write tests")
        assert t.status == "pending"

    def test_default_assigned_to(self):
        t = Task("Write tests")
        assert t.assigned_to == "Unassigned"

    def test_custom_assigned_to(self):
        t = Task("Fix bug", assigned_to="Alex")
        assert t.assigned_to == "Alex"

    def test_set_valid_status(self):
        t = Task("Deploy")
        t.status = "in-progress"
        assert t.status == "in-progress"
        t.status = "complete"
        assert t.status == "complete"

    def test_invalid_status_raises(self):
        t = Task("Deploy")
        with pytest.raises(ValueError):
            t.status = "done"

    def test_empty_title_raises(self):
        with pytest.raises(ValueError):
            t = Task("")
            t.title = ""

    def test_to_dict(self):
        t = Task("Fix bug", "Alex", "pending")
        d = t.to_dict()
        assert d == {"title": "Fix bug", "assigned_to": "Alex", "status": "pending"}

    def test_from_dict(self):
        data = {"title": "Fix bug", "assigned_to": "Alex", "status": "complete"}
        t = Task.from_dict(data)
        assert t.title == "Fix bug"
        assert t.assigned_to == "Alex"
        assert t.status == "complete"

    def test_from_dict_defaults(self):
        t = Task.from_dict({"title": "Minimal"})
        assert t.assigned_to == "Unassigned"
        assert t.status == "pending"

    def test_str(self):
        t = Task("Fix bug", "Alex", "complete")
        assert "COMPLETE" in str(t)
        assert "Fix bug" in str(t)


# ═══════════════════════════════════════════════════════════════
# Project tests
# ═══════════════════════════════════════════════════════════════

class TestProject:
    def test_create_project(self):
        p = Project("My App", "Cool app", "2025-12-31")
        assert p.title == "My App"
        assert p.description == "Cool app"
        assert p.due_date == "2025-12-31"
        assert p.tasks == []

    def test_add_task(self):
        p = Project("My App")
        t = Task("Fix bug")
        p.add_task(t)
        assert len(p.tasks) == 1

    def test_find_task_case_insensitive(self):
        p = Project("My App")
        p.add_task(Task("Fix Bug"))
        assert p.find_task("fix bug") is not None
        assert p.find_task("FIX BUG") is not None

    def test_find_task_missing(self):
        p = Project("My App")
        assert p.find_task("nonexistent") is None

    def test_complete_task(self):
        p = Project("My App")
        p.add_task(Task("Fix bug"))
        result = p.complete_task("Fix bug")
        assert result is True
        assert p.find_task("Fix bug").status == "complete"

    def test_complete_task_not_found(self):
        p = Project("My App")
        assert p.complete_task("Ghost task") is False

    def test_remove_task(self):
        p = Project("My App")
        p.add_task(Task("Fix bug"))
        assert p.remove_task("Fix bug") is True
        assert len(p.tasks) == 0

    def test_remove_task_not_found(self):
        p = Project("My App")
        assert p.remove_task("Ghost") is False

    def test_progress_empty(self):
        p = Project("My App")
        assert p.progress == "0/0"

    def test_progress_partial(self):
        p = Project("My App")
        p.add_task(Task("Task 1"))
        t2 = Task("Task 2")
        t2.status = "complete"
        p.add_task(t2)
        assert p.progress == "1/2"

    def test_to_dict(self):
        p = Project("My App", "desc", "2025-01-01")
        p.add_task(Task("Fix bug", "Alex"))
        d = p.to_dict()
        assert d["title"] == "My App"
        assert len(d["tasks"]) == 1

    def test_from_dict_roundtrip(self):
        p = Project("My App", "desc", "2025-01-01")
        p.add_task(Task("Fix bug", "Alex", "complete"))
        restored = Project.from_dict(p.to_dict())
        assert restored.title == "My App"
        assert len(restored.tasks) == 1
        assert restored.tasks[0].status == "complete"


# ═══════════════════════════════════════════════════════════════
# User tests
# ═══════════════════════════════════════════════════════════════

class TestUser:
    def test_create_user(self):
        u = User("Alex", "alex@example.com", "developer")
        assert u.name == "Alex"
        assert u.email == "alex@example.com"
        assert u.role == "developer"
        assert u.projects == []

    def test_default_role(self):
        u = User("Alex", "alex@example.com")
        assert u.role == "developer"

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError):
            u = User("Alex", "not-an-email")
            u.email = "not-an-email"

    def test_add_project(self):
        u = User("Alex", "alex@example.com")
        u.add_project(Project("My App"))
        assert len(u.projects) == 1

    def test_find_project_case_insensitive(self):
        u = User("Alex", "alex@example.com")
        u.add_project(Project("My App"))
        assert u.find_project("my app") is not None
        assert u.find_project("MY APP") is not None

    def test_find_project_missing(self):
        u = User("Alex", "alex@example.com")
        assert u.find_project("Ghost") is None

    def test_remove_project(self):
        u = User("Alex", "alex@example.com")
        u.add_project(Project("My App"))
        assert u.remove_project("My App") is True
        assert len(u.projects) == 0

    def test_remove_project_not_found(self):
        u = User("Alex", "alex@example.com")
        assert u.remove_project("Ghost") is False

    def test_to_dict(self):
        u = User("Alex", "alex@example.com", "manager")
        p = Project("My App")
        p.add_task(Task("Fix bug"))
        u.add_project(p)
        d = u.to_dict()
        assert d["name"] == "Alex"
        assert len(d["projects"]) == 1

    def test_from_dict_roundtrip(self):
        u = User("Alex", "alex@example.com", "manager")
        p = Project("My App", "desc", "2025-01-01")
        p.add_task(Task("Fix bug", "Alex", "complete"))
        u.add_project(p)
        restored = User.from_dict(u.to_dict())
        assert restored.name == "Alex"
        assert restored.role == "manager"
        assert len(restored.projects) == 1
        assert restored.projects[0].tasks[0].status == "complete"

    def test_inheritance_from_person(self):
        from lib.user import Person
        u = User("Alex", "alex@example.com")
        assert isinstance(u, Person)

    def test_str(self):
        u = User("Alex", "alex@example.com", "developer")
        assert "Alex" in str(u)
        assert "developer" in str(u)


# ═══════════════════════════════════════════════════════════════
# Storage tests
# ═══════════════════════════════════════════════════════════════

class TestStorage:
    def test_save_and_load(self, tmp_path, monkeypatch):
        import utils.storage as storage_module
        monkeypatch.setattr(storage_module, "DATA_DIR", str(tmp_path))
        monkeypatch.setattr(storage_module, "DATA_FILE", str(tmp_path / "data.json"))

        u = User("Alex", "alex@example.com", "developer")
        p = Project("My App", "Cool", "2025-12-31")
        p.add_task(Task("Fix bug", "Alex", "complete"))
        u.add_project(p)

        storage_module.save_data([u])
        loaded = storage_module.load_data()

        assert len(loaded) == 1
        assert loaded[0].name == "Alex"
        assert loaded[0].projects[0].title == "My App"
        assert loaded[0].projects[0].tasks[0].status == "complete"

    def test_load_empty_when_no_file(self, tmp_path, monkeypatch):
        import utils.storage as storage_module
        monkeypatch.setattr(storage_module, "DATA_FILE", str(tmp_path / "missing.json"))
        assert storage_module.load_data() == []

    def test_load_malformed_json(self, tmp_path, monkeypatch):
        import utils.storage as storage_module
        bad = tmp_path / "bad.json"
        bad.write_text("{ not valid json !!!")
        monkeypatch.setattr(storage_module, "DATA_FILE", str(bad))
        result = storage_module.load_data()
        assert result == []