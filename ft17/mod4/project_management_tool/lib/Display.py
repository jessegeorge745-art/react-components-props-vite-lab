# utils/display.py
# All terminal output is centralised here using the `rich` PyPi package.
# Keeping output logic in one place makes it easy to restyle the whole app.

from rich.console import Console
from rich.table import Table
from rich import box

from models.user import User
from models.project import Project

console = Console()


# ------------------------------------------------------------------ #
# Convenience print helpers
# ------------------------------------------------------------------ #

def print_success(msg: str):
    """Print a green success message."""
    console.print(f"[bold green]✔  {msg}[/bold green]")


def print_error(msg: str):
    """Print a red error message."""
    console.print(f"[bold red]✘  {msg}[/bold red]")


def print_info(msg: str):
    """Print a cyan informational message."""
    console.print(f"[bold cyan]ℹ  {msg}[/bold cyan]")


def print_warning(msg: str):
    """Print a yellow warning message."""
    console.print(f"[bold yellow]⚠  {msg}[/bold yellow]")


# ------------------------------------------------------------------ #
# Table display helpers
# ------------------------------------------------------------------ #

def display_users(users: list[User]):
    """Render all users in a formatted Rich table."""
    if not users:
        print_warning("No users found.")
        return

    table = Table(title="Registered Users", box=box.ROUNDED, highlight=True)
    table.add_column("ID",       style="dim",        width=5)
    table.add_column("Name",     style="bold white")
    table.add_column("Email",    style="cyan")
    table.add_column("Role",     style="magenta")
    table.add_column("Projects", justify="right")

    for user in users:
        table.add_row(
            str(user.id),
            user.name,
            user.email,
            user.role,
            str(len(user.projects)),
        )

    console.print(table)


def display_projects(user: User):
    """Render all projects for a given user in a formatted Rich table."""
    if not user.projects:
        print_warning(f"No projects found for '{user.name}'.")
        return

    table = Table(
        title=f"Projects for {user.name}",
        box=box.ROUNDED,
        highlight=True,
    )
    table.add_column("ID",          style="dim",        width=5)
    table.add_column("Title",       style="bold white")
    table.add_column("Description", style="white")
    table.add_column("Due Date",    style="yellow")
    table.add_column("Progress",    style="green")

    for project in user.projects:
        table.add_row(
            str(project.id),
            project.title,
            project.description or "—",
            project.due_date    or "—",
            project.completion_summary,
        )

    console.print(table)


def display_tasks(project: Project):
    """Render all tasks for a given project in a formatted Rich table."""
    if not project.tasks:
        print_warning(f"No tasks found for project '{project.title}'.")
        return

    table = Table(
        title=f"Tasks in '{project.title}'",
        box=box.ROUNDED,
        highlight=True,
    )
    table.add_column("ID",          style="dim",   width=5)
    table.add_column("Title",       style="bold white")
    table.add_column("Assigned To", style="cyan")
    table.add_column("Status",      style="magenta")

    for task in project.tasks:
        status_style = "green" if task.status == "complete" else "yellow"
        table.add_row(
            str(task.id),
            task.title,
            task.assigned_to,
            f"[{status_style}]{task.status.upper()}[/{status_style}]",
        )

    console.print(table)