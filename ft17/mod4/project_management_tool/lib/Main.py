#!/usr/bin/env python3
# main.py
# CLI entry point for the Project Management Tool.
#
# Usage:
#   python main.py <command> [options]
#   python main.py --help

import argparse
import sys

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import load_users, save_users
from utils.helpers import find_user, find_project
from utils.display import (
    display_users,
    display_projects,
    display_tasks,
    print_success,
    print_error,
    print_info,
    console,
)


# ══════════════════════════════════════════════════════════════════════════════
# Command handlers — one function per subcommand
# ══════════════════════════════════════════════════════════════════════════════

def cmd_add_user(args, users: list[User]):
    """add-user: Create a new user and persist to storage."""
    if find_user(users, args.name):
        print_error(f"A user named '{args.name}' already exists.")
        return

    try:
        user = User(name=args.name, email=args.email, role=args.role)
    except ValueError as e:
        print_error(str(e))
        return

    users.append(user)
    save_users(users)
    print_success(f"User '{user.name}' created (ID #{user.id}).")


def cmd_list_users(args, users: list[User]):
    """list-users: Display all registered users in a Rich table."""
    display_users(users)


def cmd_add_project(args, users: list[User]):
    """add-project: Add a new project to a specific user."""
    user = find_user(users, args.user)
    if not user:
        print_error(f"No user named '{args.user}' found. Add them first with add-user.")
        return

    try:
        project = Project(
            title=args.title,
            description=args.description or "",
            due_date=args.due_date or "",
        )
        user.add_project(project)
    except (ValueError, TypeError) as e:
        print_error(str(e))
        return

    save_users(users)
    print_success(f"Project '{project.title}' added to '{user.name}' (ID #{project.id}).")


def cmd_list_projects(args, users: list[User]):
    """list-projects: Show all projects that belong to a user."""
    user = find_user(users, args.user)
    if not user:
        print_error(f"No user named '{args.user}' found.")
        return
    display_projects(user)


def cmd_add_task(args, users: list[User]):
    """add-task: Add a task to a specific project."""
    user = find_user(users, args.user)
    if not user:
        print_error(f"No user named '{args.user}' found.")
        return

    project = find_project(user, args.project)
    if not project:
        print_error(f"No project titled '{args.project}' found for '{user.name}'.")
        return

    try:
        task = Task(title=args.title, assigned_to=args.assigned_to or "Unassigned")
        project.add_task(task)
    except (ValueError, TypeError) as e:
        print_error(str(e))
        return

    save_users(users)
    print_success(
        f"Task '{task.title}' added to project '{project.title}' (ID #{task.id})."
    )


def cmd_list_tasks(args, users: list[User]):
    """list-tasks: Show all tasks inside a project."""
    user = find_user(users, args.user)
    if not user:
        print_error(f"No user named '{args.user}' found.")
        return

    project = find_project(user, args.project)
    if not project:
        print_error(f"No project titled '{args.project}' found for '{user.name}'.")
        return

    display_tasks(project)


def cmd_complete_task(args, users: list[User]):
    """complete-task: Mark a named task inside a project as complete."""
    user = find_user(users, args.user)
    if not user:
        print_error(f"No user named '{args.user}' found.")
        return

    project = find_project(user, args.project)
    if not project:
        print_error(f"No project titled '{args.project}' found for '{user.name}'.")
        return

    if project.complete_task(args.title):
        save_users(users)
        print_success(f"Task '{args.title}' marked as complete.")
    else:
        print_error(
            f"No task titled '{args.title}' found in project '{project.title}'."
        )


def cmd_search_projects(args, users: list[User]):
    """search-projects: Find all projects (across all users) matching a keyword."""
    keyword = args.keyword.lower()
    found = False

    for user in users:
        matches = [p for p in user.projects if keyword in p.title.lower()]
        if matches:
            found = True
            print_info(f"User: {user.name}")
            for project in matches:
                console.print(f"  •  {project}")

    if not found:
        print_error(f"No projects found matching '{args.keyword}'.")


# ══════════════════════════════════════════════════════════════════════════════
# Argument parser
# ══════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="project-cli",
        description="🗂  Python Project Management CLI Tool",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # ── add-user ─────────────────────────────────────────────────────────────
    p = sub.add_parser("add-user", help="Create a new user.")
    p.add_argument("--name",  required=True, help="Full name of the user.")
    p.add_argument("--email", required=True, help="Email address of the user.")
    p.add_argument("--role",  default="developer", help="Role (default: developer).")

    # ── list-users ────────────────────────────────────────────────────────────
    sub.add_parser("list-users", help="List all registered users.")

    # ── add-project ───────────────────────────────────────────────────────────
    p = sub.add_parser("add-project", help="Add a project to a user.")
    p.add_argument("--user",        required=True, help="Owner's name.")
    p.add_argument("--title",       required=True, help="Project title.")
    p.add_argument("--description", default="",   help="Short description.")
    p.add_argument("--due-date",    default="",   dest="due_date",
                   help="Due date in YYYY-MM-DD format.")

    # ── list-projects ─────────────────────────────────────────────────────────
    p = sub.add_parser("list-projects", help="List all projects for a user.")
    p.add_argument("--user", required=True, help="Name of the user.")

    # ── add-task ──────────────────────────────────────────────────────────────
    p = sub.add_parser("add-task", help="Add a task to a project.")
    p.add_argument("--user",        required=True, help="Owner's name.")
    p.add_argument("--project",     required=True, help="Project title.")
    p.add_argument("--title",       required=True, help="Task title.")
    p.add_argument("--assigned-to", default="Unassigned", dest="assigned_to",
                   help="Assignee name.")

    # ── list-tasks ────────────────────────────────────────────────────────────
    p = sub.add_parser("list-tasks", help="List all tasks in a project.")
    p.add_argument("--user",    required=True, help="Owner's name.")
    p.add_argument("--project", required=True, help="Project title.")

    # ── complete-task ─────────────────────────────────────────────────────────
    p = sub.add_parser("complete-task", help="Mark a task as complete.")
    p.add_argument("--user",    required=True, help="Owner's name.")
    p.add_argument("--project", required=True, help="Project title.")
    p.add_argument("--title",   required=True, help="Title of the task to complete.")

    # ── search-projects ───────────────────────────────────────────────────────
    p = sub.add_parser("search-projects", help="Search all projects by keyword.")
    p.add_argument("--keyword", required=True, help="Keyword to match against project titles.")

    return parser


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

COMMAND_MAP = {
    "add-user":        cmd_add_user,
    "list-users":      cmd_list_users,
    "add-project":     cmd_add_project,
    "list-projects":   cmd_list_projects,
    "add-task":        cmd_add_task,
    "list-tasks":      cmd_list_tasks,
    "complete-task":   cmd_complete_task,
    "search-projects": cmd_search_projects,
}

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    # Load persisted state before every command
    users = load_users()

    handler = COMMAND_MAP.get(args.command)
    if handler:
        handler(args, users)
    else:
        print_error(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)