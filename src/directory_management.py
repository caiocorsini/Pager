from os import listdir
from pathlib import Path
import re


def have_png_files(directory_path):
    """
    Checks if given directory actually contains png files

    Args:
        directory_path: The path of the directory to check if it has png files

    Returns:
        True or False
    """
    for filename in listdir(directory_path):
        if filename.lower().endswith('.png'):
            return True
    return False


# Natural order takes into account the numeric values embedded in strings rather than sorting lexicographic
def natural_sort_key(filename):
    """
    Sorts the PNG files in natural order

    Args:
        filename: vector that will be sorted

    Returns:
        sorted files naturally
    """
    # Extracts groups of digits or non-digits
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', filename)]


def get_png_files(directory_path):
    """
    Extracts all PNG files in a given directory

    Args:
        directory_path: The path of the directory to get png files

    Returns:
        vector with all png files
    """

    path = Path(directory_path)
    png_files = path.glob('*.png')
    png_file_list = sorted([file.name for file in png_files], key=natural_sort_key)
    return png_file_list
