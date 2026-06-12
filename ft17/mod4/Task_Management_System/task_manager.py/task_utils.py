tasks = []

def add_task(title, description, due_date):
    if (validate_task_title(title) and 
        validate_task_description(description) and 
        validate_due_date(due_date)):

        new_task = {
            "title": title.strip(),
            "description": description.strip(),
            "due_date": due_date.strip(),
            "completed": False
        }
        tasks.append(new_task)
        print("Task added successfully!")
        return True
    else:
        return False

def mark_task_as_complete(index, tasks=tasks):
    try:
        idx = int(index) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["completed"] = True
            print("Task marked as complete!")
            return True
        else:
            print("Invalid task index.")
            return False
    except ValueError:
        print("Please enter a valid numeric index.")
        return False

def view_pending_tasks(tasks=tasks):
    pending = [t for t in tasks if not t["completed"]]
    if len(pending) == 0:
        print("No pending tasks found.")
        return

    print("\n--- Pending Tasks ---")
    for idx, task in enumerate(tasks):
        if not task["completed"]:
            print(f"{idx + 1}. Title: {task['title']} | Due: {task['due_date']}")
    print("--------------------")

def calculate_progress(tasks=tasks):
    if len(tasks) == 0:
        return 0.0

    completed_count = len([t for t in tasks if t["completed"]])
    progress = (completed_count / len(tasks)) * 100
    return progress