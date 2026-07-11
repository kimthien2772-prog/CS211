"""HW 2: MVC To-Do List, model.py
Kim Huynh, 2026-04-10, CS 211
"""

# credits: slides from class (The MVC Pattern)

{"description": "Buy milk", "completed": False}

class Model:
    def __init__(self): 
        self.tasks = []  # starts with empty list of tasks
    
    def add_task(self, description):
        task = {"description": description, "completed": False}  # create new task
        self.tasks.append(task)  # add taks to list

    def get_tasks(self):
        return self.tasks  # return full task list

    def mark_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = True  # mark task as complete
            return True
        return False
    
    def mark_incomplete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = False  # mark task as incomplete
            return True
        return False

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)   # remove task from list
            return True
        return False