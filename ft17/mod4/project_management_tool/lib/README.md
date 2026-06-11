# 🗂 Python Project Management CLI Tool

A command-line tool for managing users, projects, and tasks — built with
Python, `argparse`, OOP, and `rich` for colour-coded terminal output.

---

## Project Structure

```
project-management-cli/
│
├── main.py                  ← CLI entry point (argparse subcommands)
│
├── models/                  ← Domain object definitions
│   ├── __init__.py
│   ├── person.py            ← Base class (inherited by User)
│   ├── user.py              ← User extends Person; owns Projects
│   ├── project.py           ← Project belongs to User; owns Tasks
│   └── task.py              ← Task belongs to Project
│
├── utils/                   ← Shared utilities
│   ├── __init__.py
│   ├── storage.py           ← JSON save/load (persistence layer)
│   ├── display.py           ← Rich-powered terminal output
│   └── helpers.py           ← Lookup helpers (find_user, find_project)
│
├── data/                    ← Auto-generated; holds persisted JSON
│   └── data.json            ← Created automatically on first run
│
├── testing/                 ← Pytest unit tests
│   └── test_models.py
│
├── conftest.py              ← Pytest sys.path setup
├── pytest.ini               ← Pytest configuration
├── requirements.txt         ← Pinned dependencies
├── Pipfile                  ← Pipenv environment definition
├── .gitignore
├── CONTRIBUTING.md
└── LICENSE.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd project-management-cli
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## CLI Commands

### Add a user
```bash
python main.py add-user --name "Alex" --email "alex@example.com" --role "developer"
```

### List all users
```bash
python main.py list-users
```

### Add a project to a user
```bash
python main.py add-project --user "Alex" --title "CLI Tool" \
  --description "Build the CLI" --due-date "2025-12-31"
```

### List a user's projects
```bash
python main.py list-projects --user "Alex"
```

### Add a task to a project
```bash
python main.py add-task --user "Alex" --project "CLI Tool" \
  --title "Implement add-task" --assigned-to "Alex"
```

### List tasks in a project
```bash
python main.py list-tasks --user "Alex" --project "CLI Tool"
```

### Mark a task as complete
```bash
python main.py complete-task --user "Alex" --project "CLI Tool" \
  --title "Implement add-task"
```

### Search projects by keyword
```bash
python main.py search-projects --keyword "CLI"
```

---

## Running Tests

```bash
pytest
```

All 29 tests cover: Task, Project, User model logic, serialisation
roundtrips, helper lookups, and storage (save/load/error handling).

---

## Git Workflow

```bash
# Create a feature branch
git checkout -b feature-automation-tool

# Commit changes with a meaningful message
git add .
git commit -m "Add generate_log function with validation and file I/O"

# Push and open a Pull Request
git push origin feature-automation-tool
```

---

## Dependencies

| Package    | Purpose                          |
|------------|----------------------------------|
| `rich`     | Colour-coded, formatted output   |
| `tabulate` | Tabular data formatting          |
| `pytest`   | Unit testing (dev dependency)    |

---

## Known Issues

- Due dates are stored as plain strings; no date format validation is applied.
- User names must be unique across the whole system.
- Project titles must be unique per user (same title is allowed for different users).