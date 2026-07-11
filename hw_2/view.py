"""HW 2: MVC To-Do List, view.py
Kim Huynh, 2026-04-10, CS 211
"""

class View:

    def menu(self):
        print("\n--- To-Do List Menu ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Mark Task as Incomplete")
        print("5. Remove Task")
        print("6. Exit")

    def user_choice(self):
        return input("Enter your choice (1-6): ")
    
    def task_description(self):
        return input("Enter task description: ")
    
    def task_index(self):
        return input("Enter task number: ")
    
    # display tasks
    def display_tasks(self, tasks):
        if not tasks:
            print("No tasks found.")
        else:
            print("\nTasks:")
            for i, task in enumerate(tasks, start=1):
                status = "Complete" if task["completed"] else "Incomplete"
                print(f"{i}. {task['description']} - {status}")
    
    def display_message(self, message):
        print(message)