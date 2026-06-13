#!/usr/bin/env python3
# main.py
# CLI entry point for the Project Management Tool.
# Usage: python main.py <command> [options]

import argparse
import logging
import sys

from lib.user import User
from lib.project import Project
from lib.task import Task
from utils.storage import load_data, save_data
from utils.display import (
    console,
    display_users,
    display_projects,
    display_tasks,
)

# ── logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s | %(name)s | %(message)s",
)


# ── CLI definition ────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="🗂  Project Management CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py add-user      --name "Alex" --email "alex@example.com" --role developer
  python main.py list-users
  python main.py add-project   --user "Alex" --title "My App" --due-date 2025-12-31
  python main.py list-projects --user "Alex"
  python main.py add-task      --user "Alex" --project "My App" --title "Fix bug" --assigned-to "Alex"
  python main.py list-tasks    --user "Alex" --project "My App"
  python main.py complete-task --user "Alex" --project "My App" --title "Fix bug"
  python main.py update-task   --user "Alex" --project "My App" --title "Fix bug" --status in-progress
  python main.py delete-user   --name "Alex"
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="<command>")

    # ── add-user ──────────────────────────────────────────────
    p = sub.add_parser("add-user", help="Create a new user")
    p.add_argument("--name",  required=True, help="Full name")
    p.add_argument("--email", required=True, help="Email address")
    p.add_argument("--role",  default="developer",
                   choices=["developer", "manager", "admin", "designer", "tester"],
                   help="User role (default: developer)")

    # ── list-users ────────────────────────────────────────────
    sub.add_parser("list-users", help="List all users")

    # ── delete-user ───────────────────────────────────────────
    p = sub.add_parser("delete-user", help="Remove a user")
    p.add_argument("--name", required=True)

    # ── add-project ───────────────────────────────────────────
    p = sub.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user",        required=True, help="Owner's name")
    p.add_argument("--title",       required=True)
    p.add_argument("--description", default="")
    p.add_argument("--due-date",    default="", metavar="YYYY-MM-DD")

    # ── list-projects ─────────────────────────────────────────
    p = sub.add_parser("list-projects", help="List projects for a user")
    p.add_argument("--user", required=True)

    # ── delete-project ────────────────────────────────────────
    p = sub.add_parser("delete-project", help="Remove a project from a user")
    p.add_argument("--user",    required=True)
    p.add_argument("--project", required=True)

    # ── add-task ──────────────────────────────────────────────
    p = sub.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--user",        required=True)
    p.add_argument("--project",     required=True)
    p.add_argument("--title",       required=True)
    p.add_argument("--assigned-to", default="Unassigned")

    # ── list-tasks ────────────────────────────────────────────
    p = sub.add_parser("list-tasks", help="List tasks in a project")
    p.add_argument("--user",    required=True)
    p.add_argument("--project", required=True)

    # ── complete-task ─────────────────────────────────────────
    p = sub.add_parser("complete-task", help="Mark a task as complete")
    p.add_argument("--user",    required=True)
    p.add_argument("--project", required=True)
    p.add_argument("--title",   required=True)

    # ── update-task ───────────────────────────────────────────
    p = sub.add_parser("update-task", help="Update a task's status or assignee")
    p.add_argument("--user",        required=True)
    p.add_argument("--project",     required=True)
    p.add_argument("--title",       required=True)
    p.add_argument("--status",      choices=["pending", "in-progress", "complete"])
    p.add_argument("--assigned-to")

    # ── delete-task ───────────────────────────────────────────
    p = sub.add_parser("delete-task", help="Remove a task from a project")
    p.add_argument("--user",    required=True)
    p.add_argument("--project", required=True)
    p.add_argument("--title",   required=True)

    return parser


# ── helper: look up user ──────────────────────────────────────────────────────
def _get_user(users: list, name: str):
    user = next((u for u in users if u.name.lower() == name.lower()), None)
    if not user:
        console.print(f"[red][!] User '{name}' not found.[/red]")
        sys.exit(1)
    return user


def _get_project(user, title: str):
    project = user.find_project(title)
    if not project:
        console.print(f"[red][!] Project '{title}' not found for user '{user.name}'.[/red]")
        sys.exit(1)
    return project


def _get_task(project, title: str):
    task = project.find_task(title)
    if not task:
        console.print(f"[red][!] Task '{title}' not found in project '{project.title}'.[/red]")
        sys.exit(1)
    return task


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    parser = build_parser()
    args = parser.parse_args()
    users = load_data()

    # ── add-user ──────────────────────────────────────────────
    if args.command == "add-user":
        if any(u.email.lower() == args.email.lower() for u in users):
            console.print(f"[red][!] Email '{args.email}' is already registered.[/red]")
            sys.exit(1)
        try:
            user = User(args.name, args.email, args.role)
        except ValueError as e:
            console.print(f"[red][!] {e}[/red]")
            sys.exit(1)
        users.append(user)
        save_data(users)
        console.print(f"[green][+] User '{args.name}' added successfully.[/green]")

    # ── list-users ────────────────────────────────────────────
    elif args.command == "list-users":
        display_users(users)

    # ── delete-user ───────────────────────────────────────────
    elif args.command == "delete-user":
        user = _get_user(users, args.name)
        users.remove(user)
        save_data(users)
        console.print(f"[green][✓] User '{args.name}' deleted.[/green]")

    # ── add-project ───────────────────────────────────────────
    elif args.command == "add-project":
        user = _get_user(users, args.user)
        if user.find_project(args.title):
            console.print(f"[red][!] Project '{args.title}' already exists for '{args.user}'.[/red]")
            sys.exit(1)
        try:
            project = Project(args.title, args.description, args.due_date)
        except ValueError as e:
            console.print(f"[red][!] {e}[/red]")
            sys.exit(1)
        user.add_project(project)
        save_data(users)
        console.print(f"[green][+] Project '{args.title}' added to '{args.user}'.[/green]")

    # ── list-projects ─────────────────────────────────────────
    elif args.command == "list-projects":
        user = _get_user(users, args.user)
        display_projects(user)

    # ── delete-project ────────────────────────────────────────
    elif args.command == "delete-project":
        user = _get_user(users, args.user)
        if not user.remove_project(args.project):
            console.print(f"[red][!] Project '{args.project}' not found.[/red]")
            sys.exit(1)
        save_data(users)
        console.print(f"[green][✓] Project '{args.project}' deleted.[/green]")

    # ── add-task ──────────────────────────────────────────────
    elif args.command == "add-task":
        user    = _get_user(users, args.user)
        project = _get_project(user, args.project)
        if project.find_task(args.title):
            console.print(f"[red][!] Task '{args.title}' already exists in '{args.project}'.[/red]")
            sys.exit(1)
        try:
            task = Task(args.title, args.assigned_to)
        except ValueError as e:
            console.print(f"[red][!] {e}[/red]")
            sys.exit(1)
        project.add_task(task)
        save_data(users)
        console.print(f"[green][+] Task '{args.title}' added to project '{args.project}'.[/green]")

    # ── list-tasks ────────────────────────────────────────────
    elif args.command == "list-tasks":
        user    = _get_user(users, args.user)
        project = _get_project(user, args.project)
        display_tasks(project)

    # ── complete-task ─────────────────────────────────────────
    elif args.command == "complete-task":
        user    = _get_user(users, args.user)
        project = _get_project(user, args.project)
        if project.complete_task(args.title):
            save_data(users)
            console.print(f"[green][✓] Task '{args.title}' marked as complete.[/green]")
        else:
            console.print(f"[red][!] Task '{args.title}' not found.[/red]")
            sys.exit(1)

    # ── update-task ───────────────────────────────────────────
    elif args.command == "update-task":
        user    = _get_user(users, args.user)
        project = _get_project(user, args.project)
        task    = _get_task(project, args.title)
        if args.status:
            try:
                task.status = args.status
            except ValueError as e:
                console.print(f"[red][!] {e}[/red]")
                sys.exit(1)
        if args.assigned_to:
            task.assigned_to = args.assigned_to
        save_data(users)
        console.print(f"[green][✓] Task '{args.title}' updated.[/green]")

    # ── delete-task ───────────────────────────────────────────
    elif args.command == "delete-task":
        user    = _get_user(users, args.user)
        project = _get_project(user, args.project)
        if project.remove_task(args.title):
            save_data(users)
            console.print(f"[green][✓] Task '{args.title}' deleted.[/green]")
        else:
            console.print(f"[red][!] Task '{args.title}' not found.[/red]")
            sys.exit(1)


if __name__ == "__main__":
    main()