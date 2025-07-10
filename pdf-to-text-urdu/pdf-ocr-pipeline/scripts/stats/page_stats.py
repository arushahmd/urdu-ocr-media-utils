import os
import pandas as pd
import cv2
import re
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import sys

def count_lines(text):
    """ Count the number of lines in the given text. """
    return len(text.splitlines())

def process_text_file(txt_file_path):
    """ Process a single text file to extract page numbers and count lines. """
    results = []
    current_page_number = None
    content_lines = []
    book_name = os.path.splitext(os.path.basename(txt_file_path))[0]  # Extract book name from file name

    with open(txt_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#########') and line.endswith('##########'):
                # Extract page number from the hash line
                try:
                    page_number = int(line.strip('#'))
                    if current_page_number is not None:
                        # Save the content lines of the previous page
                        page_content = "\n".join(content_lines)
                        num_lines = count_lines(page_content)
                        if num_lines > 0:
                            results.append((book_name, current_page_number, num_lines))

                    # Reset for new page
                    current_page_number = page_number
                    content_lines = []
                except ValueError:
                    print(f"Warning: Could not convert '{line}' to an integer. Skipping this line.")
                    continue
            else:
                content_lines.append(line)

        # Save the content lines of the last page
        if current_page_number is not None:
            page_content = "\n".join(content_lines)
            num_lines = count_lines(page_content)
            if num_lines > 0:
                results.append((book_name, current_page_number, num_lines))

    return results

def process_all_text_files(directory):
    """ Process all text files in the given directory and return results. """
    all_results = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            txt_file_path = os.path.join(directory, filename)
            file_results = process_text_file(txt_file_path)
            all_results.extend(file_results)

    return all_results

def image_contours(image):
    """ Extract text contours from image using OpenCV. """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel_size = (200, 10)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(bw_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3]) >= 3.0]
    sorted_contours = sorted(filtered_contours, key=lambda contour: cv2.boundingRect(contour)[1])

    return sorted_contours

def lines_from_page_image(image):
    """ Extract line images from the original image based on contours. """
    contours = image_contours(image)
    line_imgs = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        x, y, w, h = (x - 3, y - 3, w + 3, h + 3)  # Add padding
        line_image = image[y:y + h, x:x + w]
        if line_image.shape[0] > 15:
            line_imgs.append(line_image)

    return line_imgs

def is_image_completely_blank(image):
    """ Check if an image is completely blank (white). """
    grayscale_image = image.convert("L")
    extrema = grayscale_image.getextrema()
    return extrema == (255, 255)

def pdf_to_page_images(pdf_path):
    """ Convert each page of a PDF to an image and return a dictionary of useful images. """
    useful_images = {}
    book_name = os.path.splitext(os.path.basename(pdf_path))[0]
    images = convert_from_path(pdf_path)
    total_pages = len(images)

    for index, image in enumerate(images):
        page_number = index + 1
        sys.stdout.write(f"\rProcessing page {page_number}/{total_pages}")
        sys.stdout.flush()
        if is_image_completely_blank(image):
            print(f"\nPage {page_number} is completely blank. Skipping.")
        else:
            filename = f"{book_name}_pg{page_number}.jpg"
            useful_images[filename] = image

    print()  # Print a new line after all pages are processed
    return useful_images


def extract_lines_from_pdf(pdf_path):
    """ Extract number of lines from each page of a PDF. """
    images = pdf_to_page_images(pdf_path)
    results = []
    book_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for filename, image in images.items():
        lines = lines_from_page_image(np.array(image))
        num_lines = len(lines)

        # Extract the page number from the filename using regex
        match = re.search(r'pg(\d+)', filename)
        if match:
            page_number = int(match.group(1))
            results.append((book_name, page_number, num_lines))
        else:
            print(f"Warning: Could not extract page number from filename '{filename}'.")

    return results

def pages_from_book_txt(txt_path):
    """ Read the text from a text file and separate the text for each page. """
    with open(txt_path, 'r', encoding='utf-8-sig') as file:
        content = file.readlines()

    book_name = os.path.splitext(os.path.basename(txt_path))[0]
    pages = {}
    page_content = []
    page_no = None
    for line in content:
        line_modified = line.strip()
        if line_modified.startswith("#") or line_modified.startswith("-"):
            if page_no is not None:
                if page_content:
                    pages[f"{book_name}_pg{page_no}.txt"] = page_content
                page_content = []
            try:
                page_no = int(line_modified.strip('#'))
            except ValueError:
                print(f"Warning: Could not convert '{line_modified}' to an integer. Skipping this page.")
                page_no = None
                continue
        else:
            if line_modified:
                page_content.append(line_modified)

    if page_no is not None and page_content:
        pages[f"{book_name}_pg{page_no}.txt"] = page_content

    return pages

def update_excel_with_comparisons(excel_file_path, txt_directory, pdf_directory):
    """ Update the Excel file with line counts from text and extracted from PDF images. """
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(excel_file_path, engine='openpyxl')

        # Process all text files and PDF files in the given directories
        txt_results = process_all_text_files(txt_directory)
        pdf_results = []
        for filename in os.listdir(pdf_directory):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(pdf_directory, filename)
                pdf_results.extend(extract_lines_from_pdf(pdf_path))

        # Create DataFrames for the extracted data
        text_df = pd.DataFrame(txt_results, columns=['Book Name', 'Page Number', 'Text Number of Lines'])
        pdf_df = pd.DataFrame(pdf_results, columns=['Book Name', 'Page Number', 'Utility Number of Lines'])

        # Merge the extracted data with the existing DataFrame
        updated_df = pd.merge(df, text_df, on=['Book Name', 'Page Number'], how='left')
        updated_df = pd.merge(updated_df, pdf_df, on=['Book Name', 'Page Number'], how='left')

        # Save the updated DataFrame back to the Excel file
        updated_df.to_excel(excel_file_path, index=False, engine='openpyxl')
        print(f"Excel file updated with line counts: {excel_file_path}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Empty data error: {e}")
    except pd.errors.ParserError as e:
        print(f"Parser error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example usage
excel_file_path = 'page_line_counts_extracted.xlsx'
txt_directory = '/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/Annotated Books'
pdf_directory = '/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/Annotated Books'
update_excel_with_comparisons(excel_file_path, txt_directory, pdf_directory)
