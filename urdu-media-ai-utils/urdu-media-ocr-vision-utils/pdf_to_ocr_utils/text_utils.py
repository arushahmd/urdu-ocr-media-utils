"""
    All utilities regarding text
"""

import os
import re


def page_number_from_text_line(line):
    """
    Extract the page number from a line starting with '#'.

    Args:
        line (str): The line containing the page number.

    Returns:
        int: The extracted page number.
    """
    match = re.search(r'[#-]+(\d+)[#-]+', line)
    return int(match.group(1)) if match else None


def page_num_from_filename(file_name):
    """
    Extract page numbers from filename.

    Filename format:
        ** {book_name}_pg{page_number}.{extension}
    """
    pattern = r"_pg(\d+)"
    match = re.search(pattern, file_name)

    if match:
        page_number = int(match.group(1))  # match page number to int
        return page_number
    else:
        return None


def validate_file_path(file_path, valid_extensions):
    """
    Validate if the file path is valid and if the file has one of the allowed extensions.

    Args:
        file_path (str): Path of the file to validate.
        valid_extensions (tuple): Allowed file extensions (e.g., ('.pdf', '.PDF')).

    Returns:
        bool: True if the file path is valid and has the correct extension, False otherwise.
    """
    return os.path.isfile(file_path) and file_path.lower().endswith(valid_extensions)
