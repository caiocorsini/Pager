import os
import tkinter as tk
from tkinter import filedialog

# Directory that will be worked on can be chosen via GUI (tkinter) or via CLI (argv)
# TODO maybe add red text in some parts like this print("\033[31mThis text is red!\033[0m")


# Takes user input and returns it
def take_input():
    """
    Takes numerical input from user and returns it.

    Returns:
        Choice as a numerical char, or -1 if it was an invalid option
    """
    choice = input("Select your option: ")
    if choice not in {'1', '2', '3', '0'}:
        print("\nInvalid option.\nChoose again.\n")
        return -1
    return choice


def show_menu():
    """
    Prints the menu.
    """
    print("Select what you want to do:")
    print("[1] Paired pages.")
    print("[2] Single pages")
    print("[3] Help.")
    print("[0] Exit program.")


def menu_input():
    """
    Helper function to call the show_menu() and take_input() functions.

    Returns:
        User choice as a numerical char
    """
    choice = -1
    while choice == -1:  # -1 represents an invalid input
        show_menu()
        choice = take_input()
    return choice


# Analyses the arguments written by the user.
def argument_input(argv):
    """
    Chooses which directory will be worked on. Via CLI (argv) or GUI.
    If no argv is written, choice is going to be with GUI.

    Args:
        argv: CLI argument

    Returns:
        str: Directory path
    """
    # Choosing using GUI
    if len(argv) < 2:
        root = tk.Tk()
        root.withdraw()  # User selects directory manually in case no path argument has been passed initially
        return tk.filedialog.askdirectory()
    elif len(argv) > 2:
        print("\nToo many arguments.\n")
        exit()
    else:  # Choosing using CLI
        if argv[1] == "current":
            file_directory_path = os.getcwd()
            print(f"\nWorking under the current working directory:\n{file_directory_path}\n")
            return file_directory_path
        file_directory_path = argv[1]
        print(f"\nWorking under the following path:\n{file_directory_path}\n")
        return file_directory_path
