# Project Management CLI Tool

A simple command-line tool for managing users, projects, and tasks.
Built with Python, `argparse`, and `rich`.

---

## Project Structure

```
project-management-cli/
│
├── main.py                  ← CLI entry point
│
├── lib/                     ← Core classes
│   ├── __init__.py
│   ├── user.py              ← User class
│   ├── project.py           ← Project class
│   └── task.py              ← Task class
│
├── utils/                   ← Helper functions
│   ├── __init__.py
│   ├── storage.py           ← Save and load data (JSON)
│   └── display.py           ← Terminal output (rich tables)
│
├── data/                    ← Auto-created on first run
│   └── data.json
│
├── testing/
│   └── test_project_management.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── Pipfile
├── .gitignore
├── CONTRIBUTING.md
└── LICENSE.md
```

---

## Setup

```bash
# Clone and enter the project
git clone <your-repo-url>
cd project-management-cli

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Commands

```bash
# Add a user
python main.py add-user --name "Alex" --email "alex@example.com" --role "developer"

# List all users
python main.py list-users

# Add a project to a user
python main.py add-project --user "Alex" --title "My Project" --description "Build it" --due-date "2025-12-31"

# List projects for a user
python main.py list-projects --user "Alex"

# Add a task to a project
python main.py add-task --user "Alex" --project "My Project" --title "Fix bug" --assigned-to "Alex"

# List tasks in a project
python main.py list-tasks --user "Alex" --project "My Project"

# Mark a task as complete
python main.py complete-task --user "Alex" --project "My Project" --title "Fix bug"
```

---

## Running Tests

```bash
pytest
```

---

## Git Workflow

```bash
git checkout -b feature-automation-tool
git add .
git commit -m "Add project management CLI"
git push origin feature-automation-tool
```