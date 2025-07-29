import datetime

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