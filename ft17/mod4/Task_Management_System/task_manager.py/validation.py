from datetime import datetime


def validate_task_title(title):
    if len(title.strip()) == 0:
        print("Error: Task title cannot be empty.")
        return False
    return True


def validate_task_description(description):
    if len(description.strip()) == 0:
        print("Error: Task description cannot be empty.")
        return False
    return True


def validate_due_date(due_date):
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
        return True
    except ValueError:
        print("Error: Due date must be in YYYY-MM-DD format.")
        return False