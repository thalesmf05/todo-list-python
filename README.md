# To-Do List in Python

This is a simple command-line To-Do List application built with Python.  
It allows you to add, view, complete, and remove tasks. Tasks are saved in a JSON file so they stay even after you close the program.

## About

I'm currently preparing to start college in Computing, and this is my first real Python project.  
I wanted to create something simple but useful to practice what I've been learning.  
Any feedback is welcome!

## Features

- Add new tasks
- Mark tasks as completed
- Remove tasks
- View current task list
- Tasks saved in a local `tasks.json` file

## How It Works

- The app stores your tasks in a list of dictionaries.
- Each task has a name and a status (completed or not).
- All tasks are saved in a file called `tasks.json`, so you won’t lose them when you exit the program.

## How to Run

1. Make sure you have Python 3 installed.
2. Clone this repository or download the project folder.
3. Open a terminal in the project folder.
4. Run the script:

```bash
python "to-do list.py"
