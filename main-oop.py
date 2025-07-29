import datetime
import json 
import os 
class Task: #done
    def __init__(self, description, completed, time):
        self.description = description
        self.completed = completed
        self.time = time 
    
    def mark_completed(self):
        self.completed = True

    def to_dict(self):
       return {
           "description": self.description,
           "completed": self.completed,
           "time": self.time.isoformat()
       }
    @classmethod
    def from_dict(cls, data):
        description = data["description"]
        completed = data["completed"]
        time = datetime.datetime.fromisoformat(data["time"])
        return cls(description, completed, time)
    
class ToDoList:
    def __init__(self):
        self.tasks = []
    
    def get_tasks(self):
        return self.tasks
    
    def add_task(self,task):
        self.tasks.append(task)

    def remove_task(self,index):
        try:
            removed = self.tasks.pop(index - 1)
            return removed
        except IndexError:
            return None

    def complete_task(self,index):
        try:
            completed_task = todo_list.tasks[index - 1].completed = True
            return completed_task
        except IndexError:
            return None
    
    def show_tasks(self):
        if not self.tasks:
            print("No tasks in the list.")
            return
        
        for index,task in enumerate(self.tasks, start=1):
            status = "✅" if task.completed else "❌"
            print(f"{index}. {task.description} - {status}")
            

    def save_to_file(self, filename):
        pass 

    def load_from_file(self,filename):
        pass 

todo_list = ToDoList()

# Valide user input          
def validate_user_input(user_input, max_index, min_index, context):
    try:
        user_input = int(user_input)
        if not (min_index <= user_input <= max_index):
            if context != "remove":
                print(f"Invalid option. Please only number beetwen {min_index} - {max_index}.") #if been used in remove, it will not print the message
            return None
    except ValueError:
        if context != "remove": #if been used in remove, it will not print the message
            print("Invalid option. Please try again.")
        return None
    else:
        return user_input
# Display a list of options and return the chosen one
def show_options(prompt, question, options):
    if prompt is not None:
        print(prompt)
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")
    while True:
        choice = input(question)
        validated = validate_user_input(choice, len(options), 1, "show_options")
        if validated is not None:
            return validated
        
# Validate user input for menu options
def show_main_menu():
    to_do_list = todo_list.get_tasks()    
    while True:
        option = show_options("----------- Menu -----------", "Choose one: ",["View Tasks", "Add Task", "Complete Task", "Remove Task", "Exit"])
        if option == 1:
            todo_list.show_tasks()
        elif option == 2:
            print("Add task") #TODO add task
        elif option == 3:
            handle_complete(to_do_list)
        elif option == 4:
            handle_remove(to_do_list) 
        elif option == 5:
            print("exit app") #TODO exit app
        
    
def handle_remove(todo_list):
    RED = "\033[31m"
    RESET = "\033[0m"
    
    while True:
        max_index = len(todo_list.get_tasks())
        remove_input = input("Choose one option to remove: ") #TODO create option to get more inputs at once 
        index = validate_user_input(remove_input, max_index, 1, "remove")
        
        if index is not None: # input is valid
            task_to_remove = todo_list.tasks[index - 1]
            confirm = input(f"Press ENTER to {RED}delete{RESET} '{task_to_remove.description}', or any other key to cancel: ")
            if confirm == "":
                removed_task = todo_list.remove_task(index)
                if removed_task is not None:
                    print(f"{task_to_remove.description} was removed!")
                else:
                    print("Unexpected error. Removal cancelled")
            else:
                print("Deletion cancelled")
        else:
            print("Invalid index. No tasks deleted")

def handle_complete(todo_list):
    GREEN = "\033[92m"
    RESET = "\033[0m"
    
    while True: 
        max_index = len(todo_list.get_tasks())
        complete_input = input("Choose one to mark as completed: ") #TODO same as remove_tasks
        index = validate_user_input(complete_input, max_index, 1, "complete")
        if index is not None:
            task_to_complete = todo_list.tasks[index - 1]
            confirm = input(f"Press ENTER to {GREEN}complete{RESET} '{task_to_complete.description}', or any other key to cancel: ")
            if confirm == "":
                completed_task = todo_list.complete_task(index)
                if completed_task is not None:
                    print(f"{task_to_complete.description} completed sucessifuly!!")
                else:
                    print("UnUnexpected error. Action cancelled ")
            else:
                print("Action cancelled")
        else:
            print("Invalid index. No tasks completed")

t = Task("oi", False, datetime.datetime.now())
todo = ToDoList()
todo.add_task(t)

# Start the program
if __name__ == "__main__":
    show_main_menu()







