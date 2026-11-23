"""Simple command-line To-Do List app.

Tasks are saved in a file called tasks.json, so they are still
there the next time you run the program.
"""

import json
import os

FILE_NAME = "tasks.json"


def load_tasks():
    """Read tasks from the file. Returns an empty list if none exist."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            tasks = json.load(file)
        if isinstance(tasks, list):
            return tasks
    except (json.JSONDecodeError, OSError):
        pass
    print("Could not read saved tasks. Starting with an empty list.")
    return []


def save_tasks(tasks):
    """Write the current tasks to the file."""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def show_tasks(tasks):
    """Print all tasks with their numbers and status."""
    if not tasks:
        print("\nYour to-do list is empty.")
        return
    print("\nYour tasks:")
    for number, task in enumerate(tasks, start=1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"  {number}. {status} {task['title']}")


def add_task(tasks):
    """Ask for a title and add a new task."""
    title = input("Enter the new task: ").strip()
    if not title:
        print("Task cannot be empty.")
        return
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"Added: {title}")


def ask_task_index(tasks, action):
    """Ask for a task number. Returns its list index, or None if invalid."""
    if not tasks:
        print("\nYour to-do list is empty.")
        return None
    show_tasks(tasks)
    choice = input(f"\nEnter the task number to {action}: ").strip()
    if not choice.isdigit():
        print("Please enter a valid number.")
        return None
    number = int(choice)
    if number < 1 or number > len(tasks):
        print("That task number does not exist.")
        return None
    return number - 1


def complete_task(tasks):
    """Mark a task as done."""
    index = ask_task_index(tasks, "mark as done")
    if index is None:
        return
    tasks[index]["done"] = True
    save_tasks(tasks)
    print(f"Completed: {tasks[index]['title']}")


def delete_task(tasks):
    """Remove a task from the list."""
    index = ask_task_index(tasks, "delete")
    if index is None:
        return
    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Deleted: {removed['title']}")


def show_menu():
    """Print the main menu."""
    print("\n===== TO-DO LIST =====")
    print("1. View tasks")
    print("2. Add a task")
    print("3. Mark a task as done")
    print("4. Delete a task")
    print("5. Exit")


def main():
    tasks = load_tasks()
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
