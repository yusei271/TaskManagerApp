import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

tasks = load_tasks()

def show_tasks():
    if len(tasks) == 0:

        print("No tasks found")
    else:
        for task in tasks:
            print(f"{task['id']}: {task['title']}")

def add_task(title):
    task = {
        "id": len(tasks),
        "title": title
    }
    tasks.append(task)
    print(f"added task: {title}")
    save_tasks()

def remove_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            print(f"removed task: {task['title']}")
            return
    print("Task not found")
    save_tasks()

while True:
    print("\n1: Show all tasks / 2: Add a task / 3: Remove a task / 4: Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        show_tasks()
    elif choice == "2":
        title = input("Enter the task title: ")
        add_task(title)
    elif choice == "3":
        task_id = int(input("Enter the task id to remove: "))
        remove_task(task_id)
    elif choice == "4":
        break