# utils/display.py
# Pretty-prints users, projects, and tasks using the `rich` library.

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def display_users(users: list) -> None:
    """Print all users in a rich table."""
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="Users", box=box.ROUNDED, show_lines=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Name", style="bold cyan")
    table.add_column("Email", style="blue")
    table.add_column("Role", style="magenta")
    table.add_column("Projects", justify="center")

    for i, user in enumerate(users, 1):
        table.add_row(
            str(i),
            user.name,
            user.email,
            user.role,
            str(len(user.projects)),
        )

    console.print(table)


def display_projects(user) -> None:
    """Print all projects belonging to a user."""
    if not user.projects:
        console.print(f"[yellow]No projects found for '{user.name}'.[/yellow]")
        return

    table = Table(
        title=f"Projects — {user.name}",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", style="bold cyan")
    table.add_column("Description", style="white")
    table.add_column("Due Date", style="blue")
    table.add_column("Progress", justify="center")

    for i, project in enumerate(user.projects, 1):
        total = len(project.tasks)
        done = sum(1 for t in project.tasks if t.status == "complete")
        progress = f"{done}/{total}" if total else "[dim]—[/dim]"
        table.add_row(
            str(i),
            project.title,
            project.description or "[dim]—[/dim]",
            project.due_date or "[dim]—[/dim]",
            progress,
        )

    console.print(table)


def display_tasks(project) -> None:
    """Print all tasks inside a project."""
    if not project.tasks:
        console.print(f"[yellow]No tasks found in project '{project.title}'.[/yellow]")
        return

    table = Table(
        title=f"Tasks — {project.title}",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", style="bold cyan")
    table.add_column("Assigned To", style="blue")
    table.add_column("Status", justify="center")

    STATUS_STYLE = {
        "complete": "[bold green]COMPLETE[/bold green]",
        "pending":  "[yellow]PENDING[/yellow]",
    }

    for i, task in enumerate(project.tasks, 1):
        status_display = STATUS_STYLE.get(task.status, task.status.upper())
        table.add_row(
            str(i),
            task.title,
            task.assigned_to,
            status_display,
        )

    console.print(table)