import datetime

class Task:
    """
    Represents a single to-do task.
    Stores description, completion status, and creation time.
    Handles (de)serialization for saving/loading.
    """
    def __init__(self, description, completed, time):
        # Task description (string)
        self.description = description
        # Boolean: True if the task is completed, False otherwise
        self.completed = completed
        # Creation timestamp (datetime object)
        self.time = time 
    
    def mark_completed(self):
        """
        Marks this task as completed.
        """
        self.completed = True

    def to_dict(self):
        """
        Converts the Task object to a dictionary for JSON serialization.
        """
        return {
            "description": self.description,
            "completed": self.completed,
            "time": self.time.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Task object from a dictionary (usually loaded from JSON).
        """
        description = data["description"]
        completed = data["completed"]
        time = datetime.datetime.fromisoformat(data["time"])
        return cls(description, completed, time)
