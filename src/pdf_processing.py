from PIL import Image, ImageDraw, ImageFont
from os import path

A4_PAPER_WIDTH = 2480
A4_PAPER_HEIGHT = 3508

SINGLE_PAGE_WIDTH = 1754
SINGLE_PAGE_HEIGHT = 2480

PAGE_N_X_POS_SINGLE = 877
PAGE_N_Y_POS_SINGLE = 2400

PAGE_N_X_LEFT_POS_DOUBLE = 877
PAGE_N_X_RIGHT_POS_DOUBLE = 2631
PAGE_N_Y_POS_DOUBLE = 2400

IMAGE_LEFT_POS_PAIRED = 0
IMAGE_RIGHT_POS_PAIRED = 1754

PAGE_N_FONT_SIZE = 50
FONT_FAMILY = "arial.ttf"

BLACK = (0, 0, 0)

READER_PDF_OUTPUT_FILE_NAME = "readerPages"


def write_pg_num_simple(img, number):
    draw = ImageDraw.Draw(img)
    pg_num = str(number - 2)
    font = ImageFont.truetype(FONT_FAMILY, PAGE_N_FONT_SIZE)
    text_color = BLACK
    position = (PAGE_N_X_POS_SINGLE, PAGE_N_Y_POS_SINGLE)
    draw.text(position, pg_num, fill=text_color, font=font)


def generate_reader_pdf(png_file_list, directory_path):
    images = []
    print("\nFiles are being processed...")
    for i in range(len(png_file_list)):
        img_path = f"{directory_path}/{png_file_list[i]}"
        img = Image.open(img_path).convert('RGB')
        img = img.resize((SINGLE_PAGE_WIDTH, SINGLE_PAGE_HEIGHT))
        if 2 < i < len(png_file_list) - 3:
            write_pg_num_simple(img, i)
        images.append(img)
    pdf_path = f"{directory_path}/{READER_PDF_OUTPUT_FILE_NAME}.pdf"
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f"PDF created at: {pdf_path}\n")


def write_pg_num_double(paired_page, number, side):
    draw = ImageDraw.Draw(paired_page)
    font = ImageFont.truetype(FONT_FAMILY, PAGE_N_FONT_SIZE)
    text_color = BLACK
    x_position = 0
    if side == "left":
        x_position = PAGE_N_X_LEFT_POS_DOUBLE
    elif side == "right":
        x_position = PAGE_N_X_RIGHT_POS_DOUBLE
    position = (x_position, PAGE_N_Y_POS_DOUBLE)
    draw.text(position, number, fill=text_color, font=font)


def paste_images(img, to_be_pasted, side):
    to_be_pasted = to_be_pasted.resize((int(A4_PAPER_HEIGHT//2), int(A4_PAPER_WIDTH)), Image.LANCZOS)
    if side == "left":
        position = IMAGE_LEFT_POS_PAIRED
    elif side == "right":
        position = IMAGE_RIGHT_POS_PAIRED
    else:
        raise ValueError("Side must be 'left' or 'right'.")
    img.paste(to_be_pasted, (position, 0))
    pass


def generate_printable_pdf(png_file_list, directory_path):
    paired_pages = []
    n = len(png_file_list)
    print("\nFiles are being processed...")

    inverted = True
    for i in range(n//2):
        # Create a new blank A4 image
        img = Image.new('RGB', (A4_PAPER_HEIGHT, A4_PAPER_WIDTH), color='white')

        if not inverted:
            img_left = Image.open(path.join(directory_path, png_file_list[i]))
            img_right = Image.open(path.join(directory_path, png_file_list[n-i-1]))
            left_page_num = i - 2
            right_page_num = n - i - 3
        else:
            img_left = Image.open(path.join(directory_path, png_file_list[n-i-1]))
            img_right = Image.open(path.join(directory_path, png_file_list[i]))
            left_page_num = n - i - 3
            right_page_num = i - 2

        paste_images(img, img_left, "left")
        paste_images(img, img_right, "right")

        if i-2 > 0:
            write_pg_num_double(img, str(left_page_num), "left")
            write_pg_num_double(img, str(right_page_num), "right")

        paired_pages.append(img)

        # Inverts the position of the images and page number of the next iteration
        inverted = not inverted

    output_pdf_path = path.join(directory_path, "output.pdf")
    if paired_pages:
        paired_pages[0].save(output_pdf_path, save_all=True, append_images=paired_pages[1:])
        print(f"PDF successfully created at {output_pdf_path}\n")
    else:
        print("No images were processed.")
