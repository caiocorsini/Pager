from sys import argv
import time as t

from directory_management import get_png_files, have_png_files
from input_output import argument_input, menu_input
from pdf_processing import generate_printable_pdf, generate_reader_pdf


def main():
    file_directory_path = argument_input(argv)

    # Verification in case the chosen directory has no PNG files.
    if not have_png_files(file_directory_path):
        print("Chosen file has no PNG files.\n")
        return 1

    png_file_list = get_png_files(file_directory_path)

    choice = 'a'
    while choice != '0':
        choice = menu_input()  # Takes input from user

        start_time = t.time()  # Starts counting the runtime
        if choice == '1':
            generate_printable_pdf(png_file_list, file_directory_path)

        if choice == '2':
            generate_reader_pdf(png_file_list, file_directory_path)

        # Runtime is only shown if user used one of the functions of the program
        if choice != '0':
            end_time = t.time()  # Time when the function stopped running
            print(f"Runtime: {round(end_time - start_time,2)} seconds.\n")  # Prints runtime

    print("\nThanks for using my program!\U0001F609")  # prints winking emoji
    return 0


if __name__ == "__main__":  # Calls main function
    main()
