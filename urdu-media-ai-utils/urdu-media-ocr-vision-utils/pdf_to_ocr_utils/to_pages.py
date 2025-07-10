import os
import sys
from pdf2image import convert_from_path
from image_utils import is_image_completely_blank


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