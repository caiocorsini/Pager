from os import path

from PIL import Image, ImageDraw, ImageFont

# Constants for page generation and image processing
# A4 paper in vertical position dimensions in pixels.
A4_PAPER_WIDTH = 2480
A4_PAPER_HEIGHT = 3508

# Dimensions of a single page in pixels. Vertical position.
SINGLE_PAGE_WIDTH = 1754
SINGLE_PAGE_HEIGHT = 2480

# X and Y coordinates of the page number, if it is a single page.
PAGE_N_X_POS_SINGLE = 877
PAGE_N_Y_POS_SINGLE = 2400

# X and Y coordinates of the page numbers if it is a paired page. Only the X position differ.
PAGE_N_X_LEFT_POS_DOUBLE = 877
PAGE_N_X_RIGHT_POS_DOUBLE = 2631
PAGE_N_Y_POS_DOUBLE = 2400

# X position of the two images in a paired page.
IMAGE_LEFT_POS_PAIRED = 0
IMAGE_RIGHT_POS_PAIRED = 1754

# Font attributes: font, family and color.
PAGE_N_FONT_SIZE = 50
FONT_FAMILY = "arial.ttf"
BLACK = (0, 0, 0)

# Default output file name.
READER_PDF_OUTPUT_FILE_NAME = "output_single_pages"

# So that it doesn't write the page number in cover and the like.
COVER_PAGE_COUNT = 2
END_PAGE_COUNT = 3


def write_pg_num_simple(img, page_number):
    """
    Writes the page number on the image, for single image pages, excluding cover and title pages.

    Args:
        img: The image object where the number will be drawn.
        page_number: The page number to be written.
    """
    draw = ImageDraw.Draw(img)
    pg_num = str(page_number - COVER_PAGE_COUNT)  # -2 since the cover and title pages do not count
    font = ImageFont.truetype(FONT_FAMILY, PAGE_N_FONT_SIZE)
    text_color = BLACK
    position = (PAGE_N_X_POS_SINGLE, PAGE_N_Y_POS_SINGLE)
    draw.text(position, pg_num, fill=text_color, font=font)


def generate_reader_pdf(png_file_list, directory_path):
    """
    Generates a reader file, that is, a file with multiple pages that contain only a single image each.

    Args:
        png_file_list: List containing the paths of all image file names that will be processed.
        directory_path: path of the directory containing all images.
    """
    images = []
    print("\nFiles are being processed...")
    for i in range(len(png_file_list)):  # Process each image file individually
        img_path = f"{directory_path}/{png_file_list[i]}"
        img = Image.open(img_path).convert('RGB')
        img = img.resize((SINGLE_PAGE_WIDTH, SINGLE_PAGE_HEIGHT))
        if COVER_PAGE_COUNT < i < len(png_file_list) - END_PAGE_COUNT:  # 2 < i < 3
            write_pg_num_simple(img, i)
        images.append(img)
    # Once all images have processed they are all merged into a single .pdf file of multiple pages
    pdf_path = f"{directory_path}/{READER_PDF_OUTPUT_FILE_NAME}.pdf"
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f"PDF created at: {pdf_path}\n")


def write_pg_num_double(paired_page, page_number, side):
    """
    Writes the page number on the image, for paired image pages, excluding cover and title pages.

    Args:
        paired_page: The image object of the paired page where the page numbers will be drawn.
        page_number: The page number to be written.
        side: the side in which the number should be written: left or right.
    """
    draw = ImageDraw.Draw(paired_page)
    font = ImageFont.truetype(FONT_FAMILY, PAGE_N_FONT_SIZE)
    text_color = BLACK
    x_position = 0
    if side == "left":
        x_position = PAGE_N_X_LEFT_POS_DOUBLE
    elif side == "right":
        x_position = PAGE_N_X_RIGHT_POS_DOUBLE
    position = (x_position, PAGE_N_Y_POS_DOUBLE)
    draw.text(position, page_number, fill=text_color, font=font)


def paste_images(page, to_be_pasted, side):
    """
    Pastes an image into a page.

    Args:
        page: The page in which the images will be pasted into
        to_be_pasted: The image that will be pasted in the page.
        side: the side in which the number should be written: left or right.
    """
    to_be_pasted = to_be_pasted.resize((int(A4_PAPER_HEIGHT // 2), int(A4_PAPER_WIDTH)), Image.LANCZOS)
    if side == "left":
        position = IMAGE_LEFT_POS_PAIRED
    elif side == "right":
        position = IMAGE_RIGHT_POS_PAIRED
    else:
        raise ValueError("Side must be 'left' or 'right'.")
    page.paste(to_be_pasted, (position, 0))


def generate_printable_pdf(png_file_list, directory_path):
    """
    Generates a printable file, that is, a file with multiple pages that contain two image per page.
    Customized so that the pages can be printed like a classic comic book.

    Args:
        png_file_list: List containing the paths of all image file names that will be processed.
        directory_path: path of the directory containing all images.
    """
    paired_pages = []
    n = len(png_file_list)
    print("\nFiles are being processed...")

    inverted = True  # To invert the sides the images get pasted, so that it can be printed like a comic book.
    for i in range(n//2):
        # Create a new blank A4 image. Height and width are inverted since the A4 paper is in horizontal position here.
        img = Image.new('RGB', (A4_PAPER_HEIGHT, A4_PAPER_WIDTH), color='white')

        if not inverted:
            img_left = Image.open(path.join(directory_path, png_file_list[i]))
            img_right = Image.open(path.join(directory_path, png_file_list[n-i-1]))
            left_page_num = i - COVER_PAGE_COUNT
            right_page_num = n - i - END_PAGE_COUNT
        else:
            img_left = Image.open(path.join(directory_path, png_file_list[n-i-1]))
            img_right = Image.open(path.join(directory_path, png_file_list[i]))
            left_page_num = n - i - END_PAGE_COUNT
            right_page_num = i - COVER_PAGE_COUNT

        paste_images(img, img_left, "left")
        paste_images(img, img_right, "right")

        # Condition so that no page numbers are written in the cover, the back cover and the likes.
        if i-COVER_PAGE_COUNT > 0:
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
