"""
    Converts the pdf books to images page wise with their corresponding text for each page.
    For each page image, we have a .txt file containing the text for that particular page image lines.
"""

import os
import shutil
import cv2
import re
import pandas as pd
from pdf2image import convert_from_path

from config import book_name_prefixes, pdf_files_dir_path, pdf_pages_images_and_texts_dir_path

"""
    Goal:
        given the prefixes of book names and the directories where they reside
        convert the pdf to page images, converting each pdf page to a jpg image 
        and also form their text files, extracting the text from the full book 
        text file into separate text file for each page.
        
    What is needed from pdf ?.
        1. All images in images folder and all texts in texts folder for all books ?.
        2. Each book's data in a separate folder with the book name ?.
"""

def is_image_completely_blank(image):
    """
    Check if an image is completely blank (white).

    Args:
        image (PIL.Image.Image): Image object.

    Returns:
        bool: True if image is completely blank, False otherwise.
    """
    grayscale_image = image.convert("L")
    extrema = grayscale_image.getextrema()
    return extrema == (255, 255)


def pdf_to_page_images(pdf_path, book_name):
    """
    Convert each page of a PDF to an image and save it in the specified output directory.

    Args:
        pdf_path (str): Path to the PDF file.
        book_name (str): Name of the book (used for naming the image files).

    returns:
            A dictionary where the key is the image filename and the value is the image.
    """
    useful_images = {}

    images = convert_from_path(pdf_path)
    for index, image in enumerate(images):
        page_number = index + 1
        if is_image_completely_blank(image):
            print(f"Image {page_number} is completely blank. Skipping.")
        else:
            filename = f"{book_name}_pg{page_number}.jpg"
            useful_images[filename] = image

    return useful_images


def extract_page_number(line):
    """
    Extract the page number from a line starting with '#'.
    Args:
        line (str): The line containing the page number.
    Returns:
        int: The extracted page number.
    """
    match = re.search(r'[#-]+(\d+)[#-]+', line)
    return int(match.group(1)) if match else None


def pages_from_book_txt(txt_path, book_name):
    """
    Read the text from a text file and separate the text for each page and save to a text file for each page.

    Args:
        txt_path (str): path of the text file containing the text content of the book.
        book_name (str): name of the book, the text file belongs to.
    Returns:
            A dictionary where the key is the text filename and the value is the text content.

    """
    with open(txt_path, 'r', encoding='utf-8-sig') as file:
        content = file.readlines()

    pages = {}
    page_content = []
    page_no = None
    for line in content:
        line_modified = line.strip()
        if line_modified.startswith("#") or line_modified.startswith("-"):
            if page_no is not None:
                # Save the previous page content
                if page_content:  # Only save if page_content is not empty
                    pages[f"{book_name}_pg{page_no}.txt"] = page_content
                page_content = []
            page_no = extract_page_number(line_modified)
        else:
            if line_modified != '' and not line_modified.isspace():
                page_content.append(line_modified)

    # Save the last page content
    if page_no is not None and page_content:
        pages[f"{book_name}_pg{page_no}.txt"] = page_content

    return pages


def save_text_pages(pages, output_dir):
    """
    Save each page's text content into separate TXT files.

    Args:
        pages (dict): dictionary where the key is the name of the text file and
                      the value is the text content of the page
        output_dir (str): output directory to save the text files
    """

    # Key is in the form, {book_name}_pg{page_number}.txt
    for key, content in pages.items():
        file_path = os.path.join(output_dir, str(key))
        with open(file_path, 'w', encoding='utf-8-sig') as file:
            file.write('\n'.join(content))


def save_image_pages(page_images, output_dir):
    """
        Given the dictionary of the page image and image name, saves it to the
        specified output directory.

        page_images (dict) : a dictionary where key is the name of the file with extension
                             and the value is the image content.
    """
    for key, image in page_images.items():
        image.save(os.path.join(output_dir, str(key))) # image is a PIL <image>

def pdf_main(pdfs_dir, book_names, output_dir):
    """

    Args:
        pdfs_dir (str): Path where all the pdf book files and their corresponding text files are located.
        book_names (list-> str): A list that contains the book names.
        output_dir (str): Directories where we want to save the extracted page images and text data.

    ==> Note:
            **  Main issue is for some pages which have arabic and english text,
                so we do not have the annotation,in the text file, so these images
                should be removed to be added in the main data.

            **  There can be a possibility that there is text data but for that the
                page image is not being extracted from the pdf.
    """

    output_images_dir = os.path.join(output_dir, "images")
    output_texts_dir = os.path.join(output_dir, "texts")

    misc_images_dir = os.path.join(output_dir, "Misc/images")
    misc_texts_dir = os.path.join(output_dir, "Misc/texts")


    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)
    os.makedirs(output_images_dir)
    os.makedirs(output_texts_dir)
    os.makedirs(misc_images_dir)
    os.makedirs(misc_texts_dir)

    # Will contain the total number of the images for each book, which had the corresponding text data.
    stats = {}

    for book_name in book_names:
        print(f"============== Working on {book_name} ==============")

        book_pdf_pth = os.path.join(pdfs_dir,f"{book_name}.pdf")
        book_txt_pth = os.path.join(pdfs_dir,f"{book_name}.txt")

        print(f"============== Extracting Images ==============")
        page_images = pdf_to_page_images(book_pdf_pth, book_name)
        image_keys = set(page_images.keys())
        image_keys = set([key[:-4] for key in image_keys])

        print(f"============== Extracting Text ==============")
        page_texts = pages_from_book_txt(book_txt_pth, book_name)
        text_keys = set(page_texts.keys())
        text_keys = set([key[:-4] for key in text_keys])

        mutual_keys = image_keys & text_keys  # or use page_keys.intersection(text_keys)
        misc_image_keys = [key for key in image_keys if key not in mutual_keys]
        misc_text_keys = [key for key in text_keys if key not in mutual_keys]

        filtered_page_images = {f"{key}.jpg": page_images[f"{key}.jpg"] for key in mutual_keys}
        filtered_page_texts = {f"{key}.txt": page_texts[f"{key}.txt"] for key in mutual_keys}

        misc_page_images = {f"{key}.jpg": page_images[f"{key}.jpg"] for key in misc_image_keys}
        misc_page_texts = {f"{key}.txt": page_texts[f"{key}.jpg"] for key in misc_text_keys}

        # store stats.
        stats[book_name] = dict()
        stats[book_name]['total_images'] = len(image_keys)
        stats[book_name]['total_texts'] = len(image_keys)
        stats[book_name]['misc_images'] = len(misc_image_keys)
        stats[book_name]['misc_texts'] = len(misc_text_keys)
        stats[book_name]['total_relevant_data'] = len(mutual_keys)

        save_image_pages(filtered_page_images, output_images_dir)
        save_text_pages(filtered_page_texts, output_texts_dir)

        save_image_pages(misc_page_images, misc_images_dir)
        save_text_pages(misc_page_texts, misc_texts_dir)

    df = pd.DataFrame.from_dict(stats, orient='index')
    df.to_csv(os.path.join(output_dir, 'pdfocr_data_bookwise_pagewise_stats.csv'))


if __name__ == "__main__":
    pdf_main(pdf_files_dir_path, book_name_prefixes,pdf_pages_images_and_texts_dir_path)










