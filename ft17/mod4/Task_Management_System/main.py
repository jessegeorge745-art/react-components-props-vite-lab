from task_manager.task_utils import (
    add_task,
    mark_task_as_complete,
    view_pending_tasks,
    calculate_progress
)


tasks = []


while True:

    print("\n===== TASK MANAGEMENT SYSTEM =====")
    print("1. Add Task")
    print("2. Mark Task as Complete")
    print("3. View Pending Tasks")
    print("4. Track Progress")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        title = input("Enter task title: ")
        description = input("Enter task description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")

        add_task(tasks, title, description, due_date)

    elif choice == "2":

        if len(tasks) == 0:
            print("No tasks available.")
        else:
            print("\nTasks:")

            for i, task in enumerate(tasks):
                status = "Completed" if task["completed"] else "Pending"
                print(f"{i}. {task['title']} ({status})")

            try:
                task_index = int(
                    input("Enter task number to complete: ")
                )
                mark_task_as_complete(tasks, task_index)
            except ValueError:
                print("Please enter a valid number.")

    elif choice == "3":

        view_pending_tasks(tasks)

    elif choice == "4":

        progress = calculate_progress(tasks)

        print(f"Progress: {progress:.2f}% completed")

    elif choice == "5":

        print("Exiting Task Management System...")
        break

    else:
        print("Invalid choice. Please try again.")