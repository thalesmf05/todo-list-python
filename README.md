# To-Do List CLI in Python

Hey there! This is my simple command-line To-Do List app, built from scratch as a way to practice Python while getting ready for college in Computing.

This project has two versions:
- **v1:** My very first version, all in a single file, focused on getting things working (even if a bit messy 😅).
- **v2:** A more modular, object-oriented version, aiming to write cleaner and more professional code.

I’m sharing both versions here to show my learning path, not just the “final result”. If you’re a recruiter, teacher, or just curious, check below for a comparison!

---

## 🚀 What Does It Do?

- Add, view, complete, and remove tasks right from the terminal
- Tasks get saved in a local JSON file (`tasks.json`) so nothing is lost when you close the program
- View your tasks in a nice formatted table (v2)

---

## 🛠️ How To Run

**1.** Make sure you have Python 3 installed.

**2.** Clone or download this repo.

**3.** Open your terminal, navigate to the project folder.

**4.** To run the latest (v2):
```bash
python main.py
```
*(If you want to check v1, look for the `main.py` inside the `v1` folder)*

---

## 🤔 Why Two Versions? (My Learning Path)

### v1: First Steps

- Everything in a single file (`main.py`)
- Used basic functions and Python lists/dicts to keep things simple
- Just wanted to make it work! (…but it got messy quickly)
- Adding new features was hard, and fixing bugs would make things even more tangled

### v2: Leveling Up

- Broke the code into modules: `task.py`, `task_manager.py`, `utils.py`
- Switched to Object-Oriented Programming (OOP): now I have `Task` and `TaskManager` classes
- Responsibilities are separated: one file for task data, one for managing tasks, another for the UI/menus
- The code is **way** easier to read, maintain, and expand
- Added more user-friendly menus, better error handling, and a table to display tasks
- Prepared the code to add more advanced features in the future (like deadlines, priorities, etc.)

---

## 📈 What Did I Learn?

- How to organize a real project in Python (not just scripts)
- The difference between procedural and OOP code (and why OOP rocks for bigger projects)
- How to serialize/deserialize objects using JSON
- The basics of user input validation and building a menu system
- How to separate concerns (and why this makes your life much easier)

---

## 🗺️ Next Steps

I’m currently working on:
- Allowing users to mark or remove **multiple tasks at once** (batch input)
- Adding deadlines, priorities, or categories for tasks
- Writing automated tests for core features (so I can refactor without fear!)

---

## 👋 Final Notes

This project is still a work in progress, but I’m really proud of how much I learned already.  
If you have any suggestions, feedback, or just want to chat about code, feel free to open an issue or reach out!

Thanks for checking out my project!