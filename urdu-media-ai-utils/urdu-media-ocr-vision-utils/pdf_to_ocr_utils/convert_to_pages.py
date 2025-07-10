"""
    This file contains the code to convert pdf and text files to pages.
"""

import os
import sys
from pdf2image import convert_from_path

from image_utils import is_image_completely_blank
from text_utils import page_number_from_text_line, validate_file_path


def pdf_to_pages(pdf_path, save=False):
    """
    Convert each page of a PDF to an image and save it in the specified output directory.

    Args:
        pdf_path (str): Path to the PDF file.
        save (bool): Whether to save the extracted page images to individual files.

    Returns:
        dict: A dictionary where the key is the image filename and the value is the image.
    """

    useful_images = {}

    # Extract the name of the book from the PDF filename.
    book_name = os.path.basename(pdf_path).replace(".pdf", "")
    print(f"Extracting Pages from: {book_name}.pdf")

    if save:
        # Create a folder for the book inside the output directory
        output_dir = os.path.join("output/book_pages/images", book_name)
        os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist.

    # Convert PDF pages to images.
    try:
        images = convert_from_path(pdf_path)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return {}

    # Get the total number of pages in the PDF.
    total_pages = len(images)

    # Process each page with tqdm progress bar.
    for index, image in enumerate(images):
        page_number = index + 1

        # Print the progress on the same line (page_number/total_pages).
        sys.stdout.write(f"\rProcessing page {page_number}/{total_pages}")
        sys.stdout.flush()

        try:
            # Check if the image is blank.
            if is_image_completely_blank(image):
                print(f"\nPage {page_number} is completely blank. Skipping.")
                continue

            # Generate the filename for the image.
            page_name = f"{book_name}_pg{page_number}.jpg"

            # Add the image to the useful_images dictionary.
            useful_images[page_name] = image

            if save:
                # Save the image to the book's directory.
                image_save_path = os.path.join(output_dir, page_name)
                image.save(image_save_path, 'JPEG')
                print(f"Saved image: {image_save_path}")

        except Exception as e:
            print(f"\nError processing page {page_number}: {e}")

    # Return the dictionary of useful images.
    return useful_images


def text_to_pages(txt_path, save=False):
    """
    Read the text from a text file, separate the text for each page, and optionally save each page's text content.

    Args:
        txt_path (str): Path of the text file containing the text content of the book.
        save (bool): Whether to save the text for each page to individual text files.

    Returns:
        dict: A dictionary where the key is the text filename and the value is the text content.
    """

    # Check if the file path is valid and has a .txt extension.
    if not validate_file_path(txt_path, ('.txt', '.TXT')):
        print(f"Error: {txt_path} is not a valid text file.")
        return {}

    try:
        with open(txt_path, 'r', encoding='utf-8-sig') as file:
            content = file.readlines()
    except Exception as e:
        print(f"Error reading file {txt_path}: {e}")
        return {}

    # Extract book name from the txt file path
    book_name = os.path.basename(txt_path).replace(".txt", "")

    # If save=True, create the output directory for text pages
    if save:
        output_dir = os.path.join("output/book_pages/texts", book_name)
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

    pages = {}
    page_content = []
    page_no = None

    for line in content:
        try:
            line_modified = line.strip()

            # Detect new page by identifying lines starting with "#" or "-"
            if line_modified.startswith("#") or line_modified.startswith("-"):
                if page_no is not None and page_content:
                    file_name = f"{book_name}_pg{page_no}.txt"
                    pages[file_name] = page_content

                    # Save the page content if save=True
                    if save:
                        try:
                            with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as file:
                                file.write("\n".join(page_content))
                            print(f"Saved page text: {file_name}")
                        except Exception as e:
                            print(f"Error saving page {page_no}: {e}")

                # Reset for the new page
                page_no = page_number_from_text_line(line_modified)
                page_content = []

            else:
                # Add valid text lines to the page content
                if line_modified:
                    page_content.append(line_modified)

        except Exception as e:
            print(f"Error processing line: {e}")
            continue

    # Save the last page content if necessary
    if page_no is not None and page_content:
        file_name = f"{book_name}_pg{page_no}.txt"
        pages[file_name] = page_content

        if save:
            try:
                with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as file:
                    file.write("\n".join(page_content))
                print(f"Saved page text: {file_name}")
            except Exception as e:
                print(f"Error saving page {page_no}: {e}")

    return pages



if __name__ == "__main__":
    # pdf_path = "/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/Annotated Books/Al Jihad Fil Islam.pdf"
    # pdf_to_pages(pdf_path)
    text_pth = "/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/Annotated Books/Al Jihad Fil Islam.txt"
    text_to_pages(text_pth)
