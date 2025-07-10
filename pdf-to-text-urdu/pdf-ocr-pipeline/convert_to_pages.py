import cv2
import numpy as np
import os
import sys
from pdf2image import convert_from_path, convert_from_bytes

from .image_utils import is_image_completely_blank


def pdf_to_pages(pdf_data, save=False, book_name=""):
    """
    Convert each page of a PDF (from binary data) to an OpenCV image.

    Args:
        pdf_data (bytes): Binary data of the PDF file.
        save (bool): Whether to save the extracted page images to individual files.
        book_name (str): Optional name for the book if saving is enabled.

    Returns:
        dict: A dictionary where the key is the image filename and the value is the OpenCV image.
    """
    useful_images = {}

    if not book_name:
        book_name = "extracted_pdf"  # Default name if not provided

    print(f"Extracting Pages from: {book_name}.pdf")

    if save:
        output_dir = os.path.join("output/book_pages/images", book_name)
        os.makedirs(output_dir, exist_ok=True)

    # Convert PDF pages to images from binary data.
    try:
        images = convert_from_bytes(pdf_data)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return {}

    total_pages = len(images)

    for index, image in enumerate(images):
        page_number = index + 1
        sys.stdout.write(f"\rProcessing page {page_number}/{total_pages}")
        sys.stdout.flush()
        print(f"\rProcessing page {page_number}/{total_pages}")

        try:
            if is_image_completely_blank(image):
                print(f"\nPage {page_number} is completely blank. Skipping.")
                continue

            open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            page_name = f"{book_name}_pg{page_number}.jpg"
            useful_images[page_name] = open_cv_image

            if save:
                image_save_path = os.path.join(output_dir, page_name)
                cv2.imwrite(image_save_path, open_cv_image)
                print(f"Saved image: {image_save_path}")

        except Exception as e:
            print(f"\nError processing page {page_number}: {e}")

    return useful_images

if __name__ == "__main__":
    pass
    # pdf_path = "/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/Annotated Books/Al Jihad Fil Islam.pdf"
    # pdf_to_pages(pdf_path)

