from PyPDF2 import PdfMerger
from PIL import Image, ImageDraw, ImageFont

A4_PAPER_WIDTH = 2480
A4_PAPER_HEIGHT = 3508

SINGLE_PAGE_WIDTH = 1754
SINGLE_PAGE_HEIGHT = 2480

PAGE_N_X_POS_SINGLE = 877
PAGE_N_Y_POS_SINGLE = 2400

PAGE_N_FONT_SIZE = 50

BLACK = (0, 0, 0)

READER_PDF_OUTPUT_FILE_NAME = "readerPages"

def write_pg_num_simple(img, number):
    draw = ImageDraw.Draw(img)
    pg_num = str(number - 2)
    font = ImageFont.truetype("arial.ttf", PAGE_N_FONT_SIZE)
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
    print(f"PDF created at: {pdf_path}")
