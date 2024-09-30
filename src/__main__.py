from sys import argv
from directory_management import have_png_files, get_png_files
from input_output import menu_input, argument_input
from pdf_processing import generate_reader_pdf, generate_printable_pdf


def main():
    file_directory_path = argument_input(argv)

    # Verification in case the chosen directory has no PNG files.
    if not have_png_files(file_directory_path):
        print("Chosen file has no PNG files.\n")
        return 1

    png_file_list = get_png_files(file_directory_path)

    choice = 'a'
    while choice != '0':
        choice = menu_input()

        if choice == '1':
            generate_printable_pdf(png_file_list, file_directory_path)

        if choice == '3':
            generate_reader_pdf(png_file_list, file_directory_path)

    print("\nThanks for using my program!\n")
    return 0


if __name__ == "__main__":
    main()
