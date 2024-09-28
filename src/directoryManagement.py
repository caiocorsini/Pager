from pathlib import Path
from os import listdir


# Checks if directory actually contains png files
def have_png_files(directory_path):
    for filename in listdir(directory_path):
        if filename.lower().endswith('.png'):
            return True
    return False


# Gets all PNG files in a given directory
def get_png_files(directory_path):
    path = Path(directory_path)
    png_files = path.glob('*.png')
    png_file_list = sorted([file.name for file in png_files])
    return png_file_list
