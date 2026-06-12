# utils/display.py
# Terminal output using the rich package for clean, readable tables.

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def print_success(msg):
    console.print(f"[bold green]✔  {msg}[/bold green]")


def print_error(msg):
    console.print(f"[bold red]✘  {msg}[/bold red]")


def print_info(msg):
    console.print(f"[bold cyan]ℹ  {msg}[/bold cyan]")


def show_users(users):
    """Display all users in a table."""
    if not users:
        print_info("No users found.")
        return

    table = Table(title="Users", box=box.ROUNDED)
    table.add_column("Name", style="bold white")
    table.add_column("Email", style="cyan")
    table.add_column("Role", style="magenta")
    table.add_column("Projects", justify="right")

    for user in users:
        table.add_row(user.name, user.email, user.role, str(len(user.projects)))

    console.print(table)


def show_projects(user):
    """Display all projects for a user in a table."""
    if not user.projects:
        print_info(f"No projects found for '{user.name}'.")
        return

    table = Table(title=f"Projects — {user.name}", box=box.ROUNDED)
    table.add_column("Title", style="bold white")
    table.add_column("Description", style="white")
    table.add_column("Due Date", style="yellow")
    table.add_column("Progress", style="green")

    for project in user.projects:
        total = len(project.tasks)
        done = sum(1 for t in project.tasks if t.status == "complete")
        table.add_row(
            project.title,
            project.description or "—",
            project.due_date or "—",
            f"{done}/{total} complete",
        )

    console.print(table)


def show_tasks(project):
    """Display all tasks for a project in a table."""
    if not project.tasks:
        print_info(f"No tasks found for '{project.title}'.")
        return

    table = Table(title=f"Tasks — {project.title}", box=box.ROUNDED)
    table.add_column("Title", style="bold white")
    table.add_column("Assigned To", style="cyan")
    table.add_column("Status", style="magenta")

    for task in project.tasks:
        color = "green" if task.status == "complete" else "yellow"
        table.add_row(
            task.title,
            task.assigned_to,
            f"[{color}]{task.status.upper()}[/{color}]",
        )

    console.print(table)