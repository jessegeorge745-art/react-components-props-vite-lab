from task_manager.validation import (
    validate_task_title,
    validate_task_description,
    validate_due_date
)


def add_task(tasks, title, description, due_date):

    if not validate_task_title(title):
        return

    if not validate_task_description(description):
        return

    if not validate_due_date(due_date):
        return

    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False
    }

    tasks.append(task)
    print("Task added successfully.")


def mark_task_as_complete(tasks, task_index):

    if len(tasks) == 0:
        print("No tasks available.")
        return

    if 0 <= task_index < len(tasks):
        tasks[task_index]["completed"] = True
        print("Task marked as complete.")
    else:
        print("Invalid task number.")


def view_pending_tasks(tasks):

    pending_tasks = [task for task in tasks if not task["completed"]]

    if len(pending_tasks) == 0:
        print("No pending tasks.")
        return

    print("\nPending Tasks:")

    for i, task in enumerate(pending_tasks, start=1):
        print(
            f"{i}. {task['title']} - "
            f"{task['description']} "
            f"(Due: {task['due_date']})"
        )


def calculate_progress(tasks):

    if len(tasks) == 0:
        return 0

    completed_tasks = sum(
        1 for task in tasks if task["completed"]
    )

    progress = (completed_tasks / len(tasks)) * 100

    return progress