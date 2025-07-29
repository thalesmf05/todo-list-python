import datetime
import json
from .task import Task

class TaskManager:
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
            self.tasks[index - 1].completed = True
            return self.tasks[index - 1]
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
        with open(filename, 'w') as f:
            tasks_dict = [task.to_dict() for task in self.tasks]
            json.dump(tasks_dict, f, indent=4)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                tasks_dict = json.load(f)
                self.tasks = [Task.from_dict(task) for task in tasks_dict]
        except FileNotFoundError:
            self.tasks = []


