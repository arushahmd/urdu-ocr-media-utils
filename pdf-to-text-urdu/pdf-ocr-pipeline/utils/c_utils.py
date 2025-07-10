import os
import PyPDF2
import pdfplumber
import pandas as pd
import re
from config import book_metadata_file


def create_metadata_file():
    """Create an empty metadata file with the necessary columns."""
    data = {
        'book_name': [],
        'category': [],  # Add a column for category
        'no. of pages': [],
        'font': [],
        'font_size': [],
        'color': []
    }

    df = pd.DataFrame(data)
    df.to_excel(book_metadata_file, index=False, engine='openpyxl')
    print(f"Created metadata file at: \n\t\t{book_metadata_file}")


def classify_color(color):
    """Classify color based on RGB or grayscale values."""
    if color == (0, 0, 0) or color == 0:  # Black (can be represented as (0,0,0) or just 0)
        return 'Black and White'
    return 'Colorful'


def clean_font_name(fontname):
    """Remove the prefix like 'ABCDEE+' from the font name."""
    return re.sub(r'^[A-Z]+[0-9]*\+', '', fontname)


def append_metadata_to_file(book_name, category, num_pages, fonts_str, font_sizes_str, color_status):
    """Append metadata to the Excel file."""
    if not os.path.exists(book_metadata_file):
        create_metadata_file()

    # Read the existing metadata file
    df = pd.read_excel(book_metadata_file, engine='openpyxl')

    # Append the new data
    new_data = {
        'book_name': [book_name],
        'category': [category],
        'no. of pages': [num_pages],
        'font': [fonts_str],
        'font_size': [font_sizes_str],
        'color': [color_status]
    }

    new_df = pd.DataFrame(new_data)

    # Append the new data and save
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_excel(book_metadata_file, index=False, engine='openpyxl')


def write_book_metadata(pdf_path, category):
    """Extract metadata from a PDF and append to the metadata file."""
    fonts = set()
    font_sizes = set()
    is_colorful = False

    book_name = os.path.basename(pdf_path)

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        print(f"Number of pages in {book_name}: {num_pages}")

    with pdfplumber.open(pdf_path) as pdf:
        for count, page in enumerate(pdf.pages):
            # Extract the text objects from the page
            for obj in page.extract_words(extra_attrs=['fontname', 'size', 'non_stroking_color']):
                # Clean font names and add to the set
                cleaned_font = clean_font_name(obj['fontname'])
                fonts.add(cleaned_font)

                # Round off font sizes and add to the set
                rounded_size = round(obj['size'])
                font_sizes.add(rounded_size)

                # Classify color to determine if the book is colorful or black and white
                color_classification = classify_color(obj['non_stroking_color'])
                print(f"Color at Page {count} : {color_classification}")
                if color_classification == 'Colorful':
                    is_colorful = True  # If any color appears, mark the book as colorful

            # only check first 15 pages rather the whole book.
            if count == 15:
                break

    # Convert sets to comma-separated strings
    fonts_str = ', '.join(sorted(fonts))  # Sorting for readability
    font_sizes_str = ', '.join(map(str, sorted(font_sizes)))  # Sorting for readability
    color_status = 'Colorful' if is_colorful else 'Black and White'

    # Append the extracted metadata to the metadata file
    append_metadata_to_file(book_name, category, num_pages, fonts_str, font_sizes_str, color_status)

    print(f"Metadata for {book_name} has been added to the file.")


def process_pdf_directory(directory_path):
    """Traverse through a directory and extract metadata for all PDF files."""
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                category = os.path.basename(root)  # The folder name is treated as the category
                print(f"Processing {pdf_path} in category {category}...")
                write_book_metadata(pdf_path, category)


if __name__ == "__main__":
    directory_path = "/media/cle-dl-05/03206245-1c77-474b-9a20-806f99b21f20/home/cle-dl-05/Documents/2.DataSets/2.OCR test data for all categories/1.Books"
    process_pdf_directory(directory_path)
