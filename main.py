import json
import os

# Save the task list to a JSON file
def save_tasks(to_do_list):
    with open("tasks.json", "w") as file:
        json.dump(to_do_list, file)


# Load the task list from a JSON file
def load_tasks():
    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Failed to load tasks. File is corrupted.")
            return []
    return []


#Pause the code for better user understanding
def pause():
    input("Press Enter to continue...")


# Print all tasks with status icons
def show_to_do_list(to_do_list):
    if not to_do_list:
        print("No tasks added yet.")
        return False
    print("-------- To-Do List --------")
    for index, task in enumerate(to_do_list, start=1):
        status = "✅" if task["completed"] else "❌"
        print(f"{index}. {task['task']} - {status}")
    return True

# Check if the task already exists in the list
def task_already_added(to_do_list, new_task):
    for task in to_do_list:
        if task["task"].lower().strip() == new_task.lower().strip():
            return True
    return False


# Validate user input for menu options
def user_input_validation(user_input, max_value, min_value, context):
    try:
        user_input = int(user_input)
        if not (min_value <= user_input <= max_value):
            if context != "remove":
                print("Invalid option. Please try again.") #if been used in remove, it will not print the message
            return None
    except ValueError:
        if context != "remove": #if been used in remove, it will not print the message
            print("Invalid option. Please try again.")
        return None
    else:
        return user_input


# Display a list of options and return the chosen one
def show_options(prompt, options):
    print(prompt)
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")
    while True:
        choice = input("Choose one: ")
        validated = user_input_validation(choice, len(options), 1, "menu")
        if validated is not None:
            return validated


# Flow to add a new task to the list
def add_task_flow(to_do_list):
    while True:
        new_task = input("Enter a task: ")
        if task_already_added(to_do_list, new_task):
            print("This task is already on the list!")
            continue
        dic_task = {"task": new_task.strip(), "completed": False}
        to_do_list.append(dic_task)
        save_tasks(to_do_list)
        print("Task added!")
        option = show_options("What next?", ["Add another", "View list", "Back to main menu"])
        if option == 1:
            continue
        elif option == 2:
            view_list(to_do_list)
        elif option == 3:
            show_main_menu()


# Collect multiple inputs for marking or removing tasks
def collect_multiple_inputs(action, to_do_list):
    try:
        valid_indices = []
        invalid_inputs = []
        remove_option_input = input(f"Enter one or more task numbers to {action}, separated by space: ").strip().split()
        for option in remove_option_input:
            try:
                validated = user_input_validation(option, len(to_do_list), 1, "remove")
                if validated is not None:
                    valid_indices.append(validated)
                else:
                    invalid_inputs.append(option)
            except ValueError:
                invalid_inputs.append(option)
        if valid_indices:
            return valid_indices, invalid_inputs
        else:
            print("Invalid input. Please enter a valid task number.")
            return [], invalid_inputs
    except Exception as e:
        print("Invalid input. Please enter numbers only.")
        return [], []


# Flow to mark a task as completed
def mark_task_completed(to_do_list):
    while True:
        if not show_to_do_list(to_do_list):
            return
        valid_indices, invalid_inputs = collect_multiple_inputs("complete", to_do_list)
        for mark_complete in valid_indices:
            if to_do_list[mark_complete - 1]["completed"]:
                print(f"Task '{to_do_list[mark_complete - 1]['task']}' is already completed.")
                continue
            if mark_complete is not None:
                to_do_list[mark_complete - 1]["completed"] = True
                save_tasks(to_do_list)
                print(f"Task '{to_do_list[mark_complete - 1]['task']}' marked as completed!")
        if invalid_inputs:
            print(f"Invalid inputs: {', '.join(invalid_inputs)}. Please try again.")
        option = show_options("What next?", ["View New list", "Mark another", "Back to main menu"])
        if option == 1:
            view_list(to_do_list)
        elif option == 2:
            continue
        elif option == 3:
            show_main_menu()


# Flow to remove a task from the list
def remove_task(to_do_list):
    while True:
        if not show_to_do_list(to_do_list):
            return
        valid_indices, invalid_inputs = collect_multiple_inputs("remove", to_do_list)
        if valid_indices:
            # Sort indices in descending order to avoid shifting issues
            for remove_option in sorted(valid_indices, reverse=True):
                confirm = input(f"Are you sure you want to remove '{to_do_list[remove_option - 1]['task']}'? (yes/no): ").strip().lower()
                if confirm == "yes":
                    del to_do_list[remove_option - 1]
                    save_tasks(to_do_list)
                    print("Task removed!")
                elif confirm == "no":
                    print("Task removal cancelled.")
            if not valid_indices:
                print("Removal cancelled.")
            # If there are invalid inputs, inform the user 
            if invalid_inputs:
                print(f"Invalid inputs: {', '.join(invalid_inputs)}. Please try again.")
            if len(to_do_list) >= 1:
                option = show_options("What next?", ["View new list", "Remove another", "Back to main menu"])
                if option == 1:
                    view_list(to_do_list)
                elif option == 2:
                    continue
                elif option == 3:
                    return
            else:
                print("No more tasks. Going back to main menu.")
                show_main_menu()

# View task list and choose what to do with tasks
def view_list(to_do_list):
    if not show_to_do_list(to_do_list):
        return
    while True:
        option = show_options("Modify Tasks:", ["Mark task as completed", "Remove task", "Back to main menu"])
        if option == 1:
            mark_task_completed(to_do_list)
        elif option == 2:
            remove_task(to_do_list)
        elif option == 3:
            show_main_menu()

#Make sure user wants to exit the program
def exit_confirmation():
    while True:
        exit_conf = input("Are you sure you want to exit the program? (yes/no): ").strip().lower()
        if exit_conf in ["yes", "y"]:
            print("\nThank you for using the To-Do List app. Goodbye!")
            exit()
        elif exit_conf in ["no", "n"]:
            input("\nExit cancelled. Press ENTER to return to the main menu.")
            show_main_menu()
            break
        else:
            print("\nInvalid input. Please type 'yes' or 'no'.")


# Display the main menu and control the app flow
def show_main_menu():
    to_do_list = load_tasks()
    while True:
        if not to_do_list:
            option = show_options("----------- Menu -----------", ["Add Task", "Exit"])
            if option == 1:
                add_task_flow(to_do_list)
            elif option == 2:
                exit_confirmation()
        else:
            option = show_options("----------- Menu -----------", ["View Tasks", "Add Task", "Complete Task", "Remove Task", "Exit"])
            if option == 1:
                view_list(to_do_list)
            elif option == 2:
                add_task_flow(to_do_list)
            elif option == 3:
                mark_task_completed(to_do_list)
            elif option == 4:
                remove_task(to_do_list)
            elif option == 5:
                choice = input("Do you want to keep your tasks saved in 'tasks.json'? (yes/no): ").strip().lower()
                if choice in ["no", "n"]:
                    if os.path.exists("tasks.json"):
                        try:
                            if input("Press ENTER to confirm deletion of 'tasks.json': ").strip() == "":
                                os.remove("tasks.json")
                                print("tasks.json deleted.")
                            else:
                                print("Deletion cancelled.")
                        except Exception as e:
                            print(f"Error deleting file: {e}")
                elif choice in ["yes", "y"]:
                    print("Tasks will be kept.")
                else:
                    print("Invalid input. Please try again.")
                exit_confirmation()


# Start the program
if __name__ == "__main__":
    show_main_menu()



