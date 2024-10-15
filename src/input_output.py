import os
import tkinter as tk
from tkinter import filedialog


# Takes user input and returns it
def take_input():
    choice = input("Select your option: ")
    if choice not in {'1', '2', '3', '0'}:
        print("\nInvalid option.\nChoose again.\n")
        return -1
    return choice


# Basic menu to show to the user
def show_menu():
    print("Select what you want to do:")
    print("[1] Paired pages.")
    print("[2] Single pages")
    print("[3] Help.")
    print("[0] Exit program.")


# Shows menu and returns input. Uses two functions for that
def menu_input():
    choice = -1
    while choice == -1:
        show_menu()
        choice = take_input()
    return choice


# Analyses the arguments written by the user
def argument_input(argv):
    if len(argv) < 2:
        root = tk.Tk()
        root.withdraw()  # User selects directory manually in case no path argument has been passed initially
        return tk.filedialog.askdirectory()
    elif len(argv) > 2:
        print("\nToo many arguments.\n")
        exit()
    else:
        if argv[1] == "current":
            file_directory_path = os.getcwd()
            print(f"\nWorking under the current working directory:\n{file_directory_path}\n")
            return file_directory_path
        file_directory_path = argv[1]
        print(f"\nWorking under the following path:\n{file_directory_path}\n")
        return file_directory_path
