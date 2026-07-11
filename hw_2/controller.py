"""HW 2: MVC To-Do List, controller.py
Kim Huynh, 2026-04-10, CS 211
"""

# credits: slides from class (The MVC Pattern)

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            self.view.menu()
            choice = self.view.user_choice() # get user menu choice

# 6 choices from to do list menu
    
            # add task
            if choice == "1":
                description = self.view.task_description()
                self.model.add_task(description)
                self.view.display_message("Task added successfully")
            
            # view tasks
            elif choice == "2":
                tasks = self.model.get_tasks()
                self.view.display_tasks(tasks)
            
            # mark task complete
            elif choice == "3":
                task_num = self.view.task_index()
                if task_num.isdigit():
                    index = int(task_num) - 1
                    if self.model.mark_complete(index):
                        self.view.display_message("Task marked as complete")
                    else:
                        self.view.display_message("Invalid number")
                else:
                    self.view.display_message("Please enter a valid number")
            
            # mark task incomplete
            elif choice == "4":
                task_num = self.view.task_index()
                if task_num.isdigit():
                    index = int(task_num) -1
                    if self.model.mark_incomplete(index):
                        self.view.display_message("Task marked as incomplete")
                    else:
                        self.view.display_message("Invalid number")
                else:
                    self.view.display_message("Please enter a valid number")
            
            # remove task
            elif choice == "5":
                task_num = self.view.task_index()
                if task_num.isdigit():
                    index = int(task_num) - 1
                    if self.model.remove_task(index):
                        self.view.display_message("Task removed successfully")
                    else:
                        self.view.display_message("Invalid number")
                else:
                    self.view.display_message("Please enter a valid number")

            # exit
            elif choice == "6":
                self.view.display_message("Byeee")
                break
            
            # invalid choice
            else: self.view.display_message("Invalid choice maybe try again!")