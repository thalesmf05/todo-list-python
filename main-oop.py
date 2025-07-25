import datetime
import json 
from operator import index
import os


# Validate user input for menu options
def user_input_validation(user_input, max_index, min_index, context):
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

class Task:
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
    
    def add_task(self,task):
        self.tasks.append(task)

    def remove_task(self,index):
        
        removed_task = self.tasks.pop(index - 1)
        


    def complete_task(self,index):
        pass
    
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

t = Task("Go shooping", False, datetime.datetime.now())
todo = ToDoList()
todo.add_task(t)
todo.show_tasks()
remove_input = input("choose one to remove: ")

user_input_validation(remove_input,)




