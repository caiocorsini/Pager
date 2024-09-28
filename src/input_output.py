def take_input():
    choice = input("Select your option: ")
    if choice not in {'1', '2', '3', '4', '0'}:
        print("\nInvalid option.\nChoose again.\n")
        return -1
    return choice


def show_menu():
    print("Select what you want to do:")
    print("[1] Generate printable paired pdf file.")
    print("[2] Generate separate printable paired pdf files.")
    print("[3] Generate reader pdf file.")
    print("[4] Help.")
    print("[0] Exit program.")


def menu_input():
    choice = -1
    while choice == -1:
        show_menu()
        choice = take_input()
    return choice
