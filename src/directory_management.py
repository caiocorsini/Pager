from pathlib import Path
from os import listdir
import re


# Checks if directory actually contains png files
def have_png_files(directory_path):
    for filename in listdir(directory_path):
        if filename.lower().endswith('.png'):
            return True
    return False


# Sorts the PNG files in natural order
# Natural order takes into account the numeric values embedded in strings rather than sorting lexicographic
def natural_sort_key(filename):
    # Extracts groups of digits or non-digits
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', filename)]


# Gets all PNG files in a given directory
def get_png_files(directory_path):
    path = Path(directory_path)
    png_files = path.glob('*.png')
    png_file_list = sorted([file.name for file in png_files], key=natural_sort_key)
    return png_file_list
