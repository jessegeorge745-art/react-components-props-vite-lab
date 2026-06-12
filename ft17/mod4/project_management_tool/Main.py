# main.py
# CLI entry point for the Project Management Tool.

import argparse
from lib.user import User
from lib.project import Project
from lib.task import Task
from utils.storage import load_data, save_data
from utils.display import (
    display_users,
    display_projects,
    display_tasks,
)


def get_args():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Project Management CLI Tool",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ── add-user ──────────────────────────────────────────────
    p = sub.add_parser("add-user", help="Add a new user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=True)
    p.add_argument("--role", default="developer")

    # ── list-users ────────────────────────────────────────────
    sub.add_parser("list-users", help="List all users")

    # ── add-project ───────────────────────────────────────────
    p = sub.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True, help="User name")
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--due-date", default="")

    # ── list-projects ─────────────────────────────────────────
    p = sub.add_parser("list-projects", help="List projects for a user")
    p.add_argument("--user", required=True)

    # ── add-task ──────────────────────────────────────────────
    p = sub.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--user", required=True)
    p.add_argument("--project", required=True, help="Project title")
    p.add_argument("--title", required=True)
    p.add_argument("--assigned-to", default="Unassigned")

    # ── list-tasks ────────────────────────────────────────────
    p = sub.add_parser("list-tasks", help="List tasks in a project")
    p.add_argument("--user", required=True)
    p.add_argument("--project", required=True)

    # ── complete-task ─────────────────────────────────────────
    p = sub.add_parser("complete-task", help="Mark a task as complete")
    p.add_argument("--user", required=True)
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)

    return parser.parse_args()


def main():
    args = get_args()
    users = load_data()

    # ── add-user ──────────────────────────────────────────────
    if args.command == "add-user":
        if any(u.email.lower() == args.email.lower() for u in users):
            print(f"[!] A user with email '{args.email}' already exists.")
            return
        user = User(args.name, args.email, args.role)
        users.append(user)
        save_data(users)
        print(f"[+] User '{args.name}' added successfully.")

    # ── list-users ────────────────────────────────────────────
    elif args.command == "list-users":
        display_users(users)

    # ── add-project ───────────────────────────────────────────
    elif args.command == "add-project":
        user = next((u for u in users if u.name.lower() == args.user.lower()), None)
        if not user:
            print(f"[!] User '{args.user}' not found.")
            return
        if user.find_project(args.title):
            print(f"[!] Project '{args.title}' already exists for '{args.user}'.")
            return
        project = Project(args.title, args.description, args.due_date)
        user.add_project(project)
        save_data(users)
        print(f"[+] Project '{args.title}' added to user '{args.user}'.")

    # ── list-projects ─────────────────────────────────────────
    elif args.command == "list-projects":
        user = next((u for u in users if u.name.lower() == args.user.lower()), None)
        if not user:
            print(f"[!] User '{args.user}' not found.")
            return
        display_projects(user)

    # ── add-task ──────────────────────────────────────────────
    elif args.command == "add-task":
        user = next((u for u in users if u.name.lower() == args.user.lower()), None)
        if not user:
            print(f"[!] User '{args.user}' not found.")
            return
        project = user.find_project(args.project)
        if not project:
            print(f"[!] Project '{args.project}' not found for user '{args.user}'.")
            return
        if project.find_task(args.title):
            print(f"[!] Task '{args.title}' already exists in project '{args.project}'.")
            return
        task = Task(args.title, args.assigned_to)
        project.add_task(task)
        save_data(users)
        print(f"[+] Task '{args.title}' added to project '{args.project}'.")

    # ── list-tasks ────────────────────────────────────────────
    elif args.command == "list-tasks":
        user = next((u for u in users if u.name.lower() == args.user.lower()), None)
        if not user:
            print(f"[!] User '{args.user}' not found.")
            return
        project = user.find_project(args.project)
        if not project:
            print(f"[!] Project '{args.project}' not found for user '{args.user}'.")
            return
        display_tasks(project)

    # ── complete-task ─────────────────────────────────────────
    elif args.command == "complete-task":
        user = next((u for u in users if u.name.lower() == args.user.lower()), None)
        if not user:
            print(f"[!] User '{args.user}' not found.")
            return
        project = user.find_project(args.project)
        if not project:
            print(f"[!] Project '{args.project}' not found for user '{args.user}'.")
            return
        if project.complete_task(args.title):
            save_data(users)
            print(f"[✓] Task '{args.title}' marked as complete.")
        else:
            print(f"[!] Task '{args.title}' not found in project '{args.project}'.")


if __name__ == "__main__":
    main()