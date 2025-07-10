"""
    This file contains the code to convert page images and text to line images and texts.
"""

import os

import cv2
import numpy as np
from PIL import Image

from .image_utils import image_contours, image_contours_updated
from .text_utils import validate_file_path


def page_to_lines_old(page_img):
    """
        Converts page image to lines based on contours.

         Args:
             img_or_pth (str or np.ndarray or PIL.Image): Path to the image file or image data.

        Returns:
         list: A list of line images extracted from the page image.
    """

    contours = image_contours(page_img)
    line_imgs = []

    for count, contour in enumerate(contours):
        print(f"Processing Line {count}")

        try:
            x, y, w, h = cv2.boundingRect(contour)
            x, y, w, h = (x - 3, y - 3, w + 3, h + 3)  # Adjust padding as needed

            line_image = page_img[y:y + h, x:x + w]

            # Check if line image meets height criteria
            if line_image.shape[0] > 15:
                line_imgs.append(line_image)

        except Exception as e:
            print(f"Error processing line {count}: {e}")
            continue  # Continue with the next contour

    return line_imgs


def page_to_lines_updated(page_img, filter_size = 3.0, kernel_sizes = ((200, 4), (8, 3))):
    """
        Extracts the lines from the page image based on the contours
        enhanced using morphological operations and
        - Otsu's threshold for binarization
        - Guassian Blur for Noise Reduction.

        Args:
             img_or_pth (str or np.ndarray or PIL.Image): Path to the image file or image data.

        Returns:
        list: A list of line images extracted from the page image.
    """

    line_imgs = [] # array to hold detected lines

    sorted_contours = image_contours_updated(page_img, kernel_sizes)

    # Iterate over each sorted contour and save line images
    for contour in sorted_contours:
        x, y, w, h = cv2.boundingRect(contour)
        y_offset = 5

        line_image = page_img[max(0, y - y_offset):y + h + y_offset, x:x + w]

        # Save line image if its height is sufficient
        if line_image.shape[0] > 15:
            line_imgs.append(line_image)

    return line_imgs


def text_to_lines(txt_or_path, save=False, file_name=None):
    """
    Given a path to a page text file or a list of text lines, extract the text and optionally save it to the desired path.

    Args:
        txt_or_path (str or list): Path to the text file or a list of lines.
        save (bool): Whether to save the extracted lines to individual text files.
        file_name (str): Optional file name to use when saving the extracted lines.

    Returns:
        list: A list of lines extracted from the text content.
    """

    lines = []
    book_name = None

    # Process input text or path
    if isinstance(txt_or_path, str):
        if not validate_file_path(txt_or_path, ('.txt', '.TXT')):
            print(f"Error: {txt_or_path} is not a valid Text file.")
            return None

        # Extract book and file name from file path
        book_name = os.path.basename(txt_or_path).split("_")[0]
        file_name = os.path.basename(txt_or_path).replace(".txt", "") if file_name is None else file_name

        try:
            with open(txt_or_path, encoding="utf-8-sig") as file:
                lines = [line for line in file.readlines() if len(line.strip()) > 0]
        except Exception as e:
            print(f"Error reading file {txt_or_path}: {e}")
            return None

    elif isinstance(txt_or_path, list):
        lines = [line for line in txt_or_path if len(line.strip()) > 0]

        if file_name is not None:
            # below only happens if the img_or_pth is image type
            book_name = file_name.split("_")[0]
            file_name = file_name.replace(".txt", "")

    else:
        print("Error: Input must be either a valid text file path or a list of lines.")
        return None

    # Save extracted lines if requested
    if save and book_name and file_name:
        output_dir = os.path.join("output/book_lines/texts", book_name)
        os.makedirs(output_dir, exist_ok=True)

        for count, line in enumerate(lines):
            save_path = os.path.join(output_dir, f"{file_name}_ln{count}.txt")
            try:
                with open(save_path, 'w', encoding='utf-8') as file:
                    file.write(line)
                print(f"Saved line text: {save_path}")
            except Exception as e:
                print(f"Error saving line text {count + 1}: {e}")

    return lines


if __name__ == "__main__":
    img_pth = "/home/cle-dl-05/Desktop/Aroosh/2. Pdf Ocr Pipeline/output/book_Pages/images/Al Jihad Fil Islam/Al Jihad Fil Islam_pg2.jpg"

    txt_path = "/home/cle-dl-05/Desktop/Aroosh/2. Pdf Ocr Pipeline/output/book_Pages/texts/Al Jihad Fil Islam/Al Jihad Fil Islam_pg33.txt"
    # text_to_lines(txt_path)
