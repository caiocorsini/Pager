from sys import argv
from directory_management import have_png_files, get_png_files
from input_output import menu_input, argument_input


def main():
    file_directory_path = argument_input(argv)

    # Verification if choses directory has no PNG files.
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
