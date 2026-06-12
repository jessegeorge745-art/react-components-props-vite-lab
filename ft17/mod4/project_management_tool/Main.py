#!/usr/bin/env python3
# main.py
# Entry point for the Project Management CLI Tool.
#
# Usage examples:
#   python main.py add-user --name "Alex" --email "alex@example.com"
#   python main.py add-project --user "Alex" --title "My Project"
#   python main.py add-task --user "Alex" --project "My Project" --title "Fix bug"
#   python main.py complete-task --user "Alex" --project "My Project" --title "Fix bug"
#   python main.py list-users
#   python main.py list-projects --user "Alex"
#   python main.py list-tasks --user "Alex" --project "My Project"

import argparse
import sys

from lib.user import User
from lib.project import Project
from lib.task import Task
from utils.storage import load_users, save_users
from utils.display import print_success, print_error, show_users, show_projects, show_tasks


# ── Helper ────────────────────────────────────────────────────────────────────

def find_user(users, name):
    """Return a user by name (case-insensitive), or None."""
    for user in users:
        if user.name.lower() == name.lower():
            return user
    return None


# ── Command handlers ──────────────────────────────────────────────────────────

def cmd_add_user(args, users):
    if find_user(users, args.name):
        print_error(f"A user named '{args.name}' already exists.")
        return

    user = User(name=args.name, email=args.email, role=args.role)
    users.append(user)
    save_users(users)
    print_success(f"User '{user.name}' created.")


def cmd_list_users(args, users):
    show_users(users)


def cmd_add_project(args, users):
    user = find_user(users, args.user)
    if not user:
        print_error(f"No user named '{args.user}' found. Use add-user first.")
        return

    if user.find_project(args.title):
        print_error(f"'{args.user}' already has a project called '{args.title}'.")
        return

    project = Project(title=args.title, description=args.description, due_date=args.due_date)
    user.add_project(project)
    save_users(users)
    print_success(f"Project '{project.title}' added to '{user.name}'.")


def cmd_list_projects(args, users):
    user = find_user(users, args.user)
    if not user:
        print_error(f"No user named '{args.user}' found.")
        return
    show_projects(user)


def cmd_add_task(args, users):
    user = find_user(users, args.user)
    if not user:
        print_error(f"No user named '{args.user}' found.")
        return

    project = user.find_project(args.project)
    if not project:
        print_error(f"No project titled '{args.project}' found for '{args.user}'.")
        return

    task = Task(title=args.title, assigned_to=args.assigned_to)
    project.add_task(task)
    save_users(users)
    print_success(f"Task '{task.title}' added to '{project.title}'.")


def cmd_list_tasks(args, users):
    user = find_user(users, args.user)
    if not user:
        print_error(f"No user named '{args.user}' found.")
        return

    project = user.find_project(args.project)
    if not project:
        print_error(f"No project titled '{args.project}' found for '{args.user}'.")
        return

    show_tasks(project)


def cmd_complete_task(args, users):
    user = find_user(users, args.user)
    if not user:
        print_error(f"No user named '{args.user}' found.")
        return

    project = user.find_project(args.project)
    if not project:
        print_error(f"No project titled '{args.project}' found for '{args.user}'.")
        return

    if project.complete_task(args.title):
        save_users(users)
        print_success(f"Task '{args.title}' marked as complete.")
    else:
        print_error(f"No task titled '{args.title}' found in '{args.project}'.")


# ── Parser ────────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="project-cli",
        description="Project Management CLI Tool",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # add-user
    p = sub.add_parser("add-user", help="Create a new user.")
    p.add_argument("--name",  required=True, help="User's full name.")
    p.add_argument("--email", required=True, help="User's email address.")
    p.add_argument("--role",  default="developer", help="User's role (default: developer).")

    # list-users
    sub.add_parser("list-users", help="List all users.")

    # add-project
    p = sub.add_parser("add-project", help="Add a project to a user.")
    p.add_argument("--user",        required=True, help="Name of the user.")
    p.add_argument("--title",       required=True, help="Project title.")
    p.add_argument("--description", default="",    help="Project description.")
    p.add_argument("--due-date",    default="",    dest="due_date", help="Due date (YYYY-MM-DD).")

    # list-projects
    p = sub.add_parser("list-projects", help="List all projects for a user.")
    p.add_argument("--user", required=True, help="Name of the user.")

    # add-task
    p = sub.add_parser("add-task", help="Add a task to a project.")
    p.add_argument("--user",        required=True, help="Name of the user.")
    p.add_argument("--project",     required=True, help="Project title.")
    p.add_argument("--title",       required=True, help="Task title.")
    p.add_argument("--assigned-to", default="Unassigned", dest="assigned_to", help="Assignee name.")

    # list-tasks
    p = sub.add_parser("list-tasks", help="List all tasks in a project.")
    p.add_argument("--user",    required=True, help="Name of the user.")
    p.add_argument("--project", required=True, help="Project title.")

    # complete-task
    p = sub.add_parser("complete-task", help="Mark a task as complete.")
    p.add_argument("--user",    required=True, help="Name of the user.")
    p.add_argument("--project", required=True, help="Project title.")
    p.add_argument("--title",   required=True, help="Task title.")

    return parser


# ── Entry point ───────────────────────────────────────────────────────────────

COMMANDS = {
    "add-user":      cmd_add_user,
    "list-users":    cmd_list_users,
    "add-project":   cmd_add_project,
    "list-projects": cmd_list_projects,
    "add-task":      cmd_add_task,
    "list-tasks":    cmd_list_tasks,
    "complete-task": cmd_complete_task,
}

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    users = load_users()

    handler = COMMANDS.get(args.command)
    if handler:
        handler(args, users)
    else:
        print_error(f"Unknown command: {args.command}")
        sys.exit(1)