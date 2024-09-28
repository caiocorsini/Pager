from sys import argv
from directoryManagement import have_png_files, get_png_files
from input_output import menu_input


def main():

    file_directory_path = ""
    if len(argv) < 2:
        print("Please, type in the path to the files you want to work on.")
    elif len(argv) > 2:
        print("Too many arguments.")
    else:
        file_directory_path = argv[1]
        print(f"\nWorking under the following path:\n{file_directory_path}\n")

    if not have_png_files(file_directory_path):
        print("Chosen file has no PNG files.\n")
        return 1

    png_file_list = get_png_files(file_directory_path)
    choice = menu_input()

    if choice == '0':
        print("\nThanks for using my program!\n")
        return 0


if __name__ == "__main__":
    main()
