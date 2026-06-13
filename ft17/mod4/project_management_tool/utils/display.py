# utils/display.py
# Pretty terminal output using the `rich` library.

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

STATUS_STYLE = {
    "complete":    "[bold green]✔ COMPLETE[/bold green]",
    "in-progress": "[bold yellow]⟳ IN-PROGRESS[/bold yellow]",
    "pending":     "[dim]○ PENDING[/dim]",
}


def display_users(users: list) -> None:
    """Print all users in a rich table."""
    if not users:
        console.print(Panel("[yellow]No users found. Use [bold]add-user[/bold] to create one.[/yellow]"))
        return

    table = Table(title="👥  All Users", box=box.ROUNDED, show_lines=True, highlight=True)
    table.add_column("#",        style="dim",       width=4,  justify="right")
    table.add_column("Name",     style="bold cyan")
    table.add_column("Email",    style="blue")
    table.add_column("Role",     style="magenta")
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
    """Print all projects for a user."""
    if not user.projects:
        console.print(Panel(
            f"[yellow]No projects for [bold]{user.name}[/bold]. "
            f"Use [bold]add-project --user \"{user.name}\"[/bold] to create one.[/yellow]"
        ))
        return

    table = Table(
        title=f"📁  Projects — {user.name}",
        box=box.ROUNDED, show_lines=True, highlight=True,
    )
    table.add_column("#",           style="dim",       width=4, justify="right")
    table.add_column("Title",       style="bold cyan")
    table.add_column("Description", style="white",     max_width=35)
    table.add_column("Due Date",    style="blue",      justify="center")
    table.add_column("Progress",    justify="center")

    for i, project in enumerate(user.projects, 1):
        total = len(project.tasks)
        done  = sum(1 for t in project.tasks if t.status == "complete")
        if total == 0:
            progress = "[dim]—[/dim]"
        elif done == total:
            progress = f"[bold green]{done}/{total}[/bold green]"
        else:
            progress = f"[yellow]{done}/{total}[/yellow]"

        table.add_row(
            str(i),
            project.title,
            project.description or "[dim]—[/dim]",
            project.due_date    or "[dim]—[/dim]",
            progress,
        )
    console.print(table)


def display_tasks(project) -> None:
    """Print all tasks in a project."""
    if not project.tasks:
        console.print(Panel(
            f"[yellow]No tasks in [bold]{project.title}[/bold]. "
            f"Use [bold]add-task --project \"{project.title}\"[/bold] to add one.[/yellow]"
        ))
        return

    table = Table(
        title=f"✅  Tasks — {project.title}",
        box=box.ROUNDED, show_lines=True, highlight=True,
    )
    table.add_column("#",           style="dim",  width=4, justify="right")
    table.add_column("Title",       style="bold cyan")
    table.add_column("Assigned To", style="blue")
    table.add_column("Status",      justify="center")

    for i, task in enumerate(project.tasks, 1):
        table.add_row(
            str(i),
            task.title,
            task.assigned_to,
            STATUS_STYLE.get(task.status, task.status.upper()),
        )
    console.print(table)