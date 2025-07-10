"""
    This file contains the whole functionality to convert pdf to page images
    and then the page images to lines.

    1. Convert a pdf file to pages
    2. Convert a page to Lines
"""

import os
import re
import shutil
import sys

import cv2
import numpy as np
import pandas as pd
from pdf2image import convert_from_path


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


def pdf_to_page_images(pdf_path):
    """
    Convert each page of a PDF to an image and save it in the specified output directory.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        dict: A dictionary where the key is the image filename and the value is the image.
    """
    useful_images = {}

    # Extract the name of the book from the PDF filename
    book_name = pdf_path.split("/")[-1].replace(".pdf", "")

    print(f"Processing {book_name}")

    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    # Get the total number of pages in the PDF
    total_pages = len(images)

    # Process each page with tqdm progress bar
    for index, image in enumerate(images):
        page_number = index + 1

        # Print the progress on the same line (page_number/total_pages)
        sys.stdout.write(f"\rProcessing page {page_number}/{total_pages}")
        sys.stdout.flush()

        # Check if the image is blank
        if is_image_completely_blank(image):
            print(f"\nPage {page_number} is completely blank. Skipping.")
        else:
            # Generate the filename for the image
            filename = f"{book_name}_pg{page_number}.jpg"

            # Add the image to the useful_images dictionary
            useful_images[filename] = image

    print()  # Print a new line after all pages are processed

    # Return the dictionary of useful images
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


def pages_from_book_txt(txt_path):
    """
    Read the text from a text file and separate the text for each page and save to a text file for each page.

    Args:
        txt_path (str): Path of the text file containing the text content of the book.
        book_name (str): Name of the book, the text file belongs to.

    Returns:
        dict: A dictionary where the key is the text filename and the value is the text content.
    """
    with open(txt_path, 'r', encoding='utf-8-sig') as file:
        content = file.readlines()

    book_name = txt_path.split("/")[-1].replace(".txt", "")

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
        pages (dict): Dictionary where the key is the name of the text file and
                      the value is the text content of the page.
        output_dir (str): Output directory to save the text files.
    """
    for key, content in pages.items():
        file_path = os.path.join(output_dir, str(key))
        with open(file_path, 'w', encoding='utf-8-sig') as file:
            file.write('\n'.join(content))


def save_image_pages(page_images, output_dir):
    """
    Given the dictionary of the page image and image name, saves it to the
    specified output directory.

    Args:
        page_images (dict): A dictionary where key is the name of the file with extension
                            and the value is the image content.
    """
    for key, image in page_images.items():
        image.save(os.path.join(output_dir, str(key)))  # image is a PIL <image>


def remove_recreate_dir(dir_pth):
    """ Remove directory if exists and then create it. """
    if os.path.exists(dir_pth):
        shutil.rmtree(dir_pth)
    os.makedirs(dir_pth)


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


def linewise_text_from_text_file(file_path):
    """
    Given the text file returns the content of text file as lines.
    """
    with open(file_path, encoding="utf-8-sig") as file:
        lines = file.readlines()
        lines = [line for line in lines if len(line.strip()) > 0]  # filter out empty lines
        return lines


def image_contours(image):
    """
    Extract text contours from image using OpenCV.
    Returns sorted contours based on y-coordinate.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Define kernel size for morphological operations
    kernel_size = (200, 10)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

    # Perform morphological closing operation
    bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    # Find contours for each text line
    contours, _ = cv2.findContours(bw_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours to select those whose width is at least 3 times its height
    filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3]) >= 3.0]

    # Sort contours based on y-coordinate
    sorted_contours = sorted(filtered_contours, key=lambda contour: cv2.boundingRect(contour)[1])

    return sorted_contours


def lines_from_page_image(image):
    """
        Extract line images from the original image based on contours.
        Filters out lines based on minimum height criteria.
    """
    contours = image_contours(image)

    line_imgs = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        x, y, w, h = (x - 3, y - 3, w + 3, h + 3)  # Add padding

        line_image = image[y:y + h, x:x + w]

        # Check if line image meets height criteria
        if line_image.shape[0] > 15:
            line_imgs.append(line_image)

    return line_imgs


def pdf_to_pages(path, extract_images=True, extract_texts=False):
    """
    Convert PDFs to images and texts, and save them in corresponding directories.

    Args:
        path (str): Can be a path to a pdf or a directory containing the pdfs
        extract_images (bool): Flag to determine if images should be extracted and saved.
        extract_texts (bool): Flag to determine if texts should be extracted and saved.

    Note:
        ** Main issue is for some pages which have Arabic and English text,
           so we do not have the annotation in the text file, so these images
           should be removed to be added in the main data.

        ** There can be a possibility that there is text data but for that, the
           page image is not being extracted from the PDF.
    """

    main_output_dir = "Output/Book Pages"

    if os.path.exists(main_output_dir):
        shutil.rmtree(main_output_dir)
    os.makedirs(main_output_dir)

    stats = {}

    if os.path.isdir(path):
        pdf_files = [f for f in os.listdir(path) if f.lower().endswith('.pdf')]
    elif os.path.isfile(path) and path.lower().endswith('.pdf'):
        pdf_files = [path]
    else:
        raise ValueError("Provided path is neither a directory of PDFs nor a single PDF file.")

    for pdf_file in pdf_files:
        pdf_pth = os.path.join(path, pdf_file) if os.path.isdir(path) else path
        pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]

        print(f"============== Working on {pdf_name} ==============")

        # Create book-specific directory inside the Output folder
        book_output_dir = os.path.join(main_output_dir, pdf_name)
        output_images_dir = os.path.join(book_output_dir, "images")
        output_texts_dir = os.path.join(book_output_dir, "texts")

        misc_images_dir = os.path.join(book_output_dir, "Misc", "images")
        misc_texts_dir = os.path.join(book_output_dir, "Misc", "texts")

        # Create the required directories
        for dir_path in [output_images_dir, output_texts_dir, misc_images_dir, misc_texts_dir]:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
            os.makedirs(dir_path)

        book_pdf_pth = pdf_pth
        book_txt_pth = book_pdf_pth.replace(".pdf", ".txt")
        # book_txt_pth = os.path.join(path, f"{pdf_name}.txt") if os.path.isdir(path) else f"{pdf_name}.txt"

        image_keys = set()
        text_keys = set()

        if extract_images:
            print(f"============== Extracting Images ==============")
            page_images = pdf_to_page_images(book_pdf_pth)
            image_keys = set([key[:-4] for key in page_images.keys()])

        if extract_texts:
            print(f"============== Extracting Text ==============")
            page_texts = pages_from_book_txt(book_txt_pth)
            text_keys = set([key[:-4] for key in page_texts.keys()])

        mutual_keys = image_keys & text_keys if extract_images and extract_texts else image_keys if extract_images else text_keys if extract_texts else set()

        misc_image_keys = [key for key in image_keys if key not in mutual_keys]
        misc_text_keys = [key for key in text_keys if key not in mutual_keys]

        filtered_page_images = {f"{key}.jpg": page_images[f"{key}.jpg"] for key in
                                mutual_keys} if extract_images else {}
        misc_page_images = {f"{key}.jpg": page_images[f"{key}.jpg"] for key in
                            misc_image_keys} if extract_images else {}

        filtered_page_texts = {f"{key}.txt": page_texts[f"{key}.txt"] for key in mutual_keys} if extract_texts else {}
        misc_page_texts = {f"{key}.txt": page_texts[f"{key}.txt"] for key in misc_text_keys} if extract_texts else {}

        # Store stats.
        stats[pdf_name] = {
            'total_images': len(image_keys) if extract_images else 0,
            'total_texts': len(text_keys) if extract_texts else 0,
            'misc_images': len(misc_image_keys) if extract_images else 0,
            'misc_texts': len(misc_text_keys) if extract_texts else 0,
            'total_relevant_data': len(mutual_keys)
        }

        if extract_images:
            save_image_pages(filtered_page_images, output_images_dir)
            save_image_pages(misc_page_images, misc_images_dir)
        if extract_texts:
            save_text_pages(filtered_page_texts, output_texts_dir)
            save_text_pages(misc_page_texts, misc_texts_dir)

    df = pd.DataFrame.from_dict(stats, orient='index')
    df.to_csv(os.path.join(main_output_dir, 'Bookwise_Pages.csv'))


def pdf_text_2_page_text(pdf_text_path):
    pass


def page_to_lines(path, extract_images=True, extract_texts=False):
    """
    Convert the page images and text to line images and text and store them in
    corresponding text files based on flags.

    Args:
        path (str): Directory path containing the book's page images and texts.
        extract_images (bool): Flag to determine if line images should be extracted and saved.
        extract_texts (bool): Flag to determine if line texts should be extracted and saved.
    """
    # Define output paths
    book_name = os.path.basename(path)
    main_output_dir = os.path.join("../Output", "Book Lines", book_name)
    images_out_pth = os.path.join(main_output_dir, "images")
    texts_out_pth = os.path.join(main_output_dir, "texts")

    # Create main output directory if it doesn't exist
    if not os.path.exists(main_output_dir):
        os.makedirs(main_output_dir)
        print(f"Created main output directory: {main_output_dir}")
    if extract_images and not os.path.exists(images_out_pth):
        os.makedirs(images_out_pth)
        print(f"Created images output directory: {images_out_pth}")
    if extract_texts and not os.path.exists(texts_out_pth):
        os.makedirs(texts_out_pth)
        print(f"Created texts output directory: {texts_out_pth}")

    images_dir = os.path.join(path, "images")
    texts_dir = os.path.join(path, "texts")

    if not (os.path.exists(images_dir) and os.path.exists(texts_dir)):
        print("Check your directory paths. One or both of the paths is incorrect or does not exist.")
        return None

    print("For some books, some first pages have issues in annotation. "
          "So some pages will be skipped for each book.")

    text_file_names = os.listdir(texts_dir)
    error_files_log = {}
    saved_files = []

    # Get list of image files
    file_names = [filename[:-4] for filename in os.listdir(images_dir) if filename.lower().endswith('.jpg')]

    print(f"Found {len(file_names)} files to process.")

    for filename in file_names:
        print(f"Processing {filename}...")

        image_file_pth = os.path.join(images_dir, f"{filename}.jpg")
        text_file_pth = os.path.join(texts_dir, f"{filename}.txt")

        page_number = page_num_from_filename(filename)

        # Skip first 4 pages for each book.
        if page_number is None:  # If page number not extracted keep track of such files.
            error_files_log[filename] = {"Error": "Unable to Extract Page Number."}
            print(f"Skipping {filename}: Unable to extract page number.")
            continue
        elif page_number < 5:
            print(f"Skipping Page Number {page_number} from {filename}.")
            continue

        page_image = cv2.imread(image_file_pth)

        if extract_images or extract_texts:
            image_lines = lines_from_page_image(page_image) if extract_images else []
            text_lines = linewise_text_from_text_file(text_file_pth) if extract_texts else []

            if extract_images and extract_texts:
                if len(image_lines) != len(text_lines):
                    print(f"For {filename}, number of line images does not equal number of line texts."
                          f"\nLine Images: {len(image_lines)} \nText Lines: {len(text_lines)}")
                    error_files_log[filename] = {
                        "Line Images": len(image_lines),
                        "Text Lines": len(text_lines)
                    }
                    continue

            if extract_images:
                print(f"Extracting line images for {filename}...")
                for number in range(len(image_lines)):
                    image = image_lines[number]
                    img_file_name = f"{filename}_ln{number + 1}.jpg"
                    image_save_path = os.path.join(images_out_pth, img_file_name)
                    if image.shape[0] == 0 or image.shape[1] == 0:
                        error_files_log.setdefault(filename, {})["Image Error"] = "One of the image dimensions was 0."
                        print(f"Error saving {img_file_name}: Image dimensions are zero.")
                        continue
                    cv2.imwrite(image_save_path, image)
                    print(f"Saved image: {img_file_name}")

            if extract_texts:
                print(f"Extracting line texts for {filename}...")
                for number in range(len(text_lines)):
                    text = text_lines[number]
                    txt_file_name = f"{filename}_ln{number + 1}.txt"
                    text_save_path = os.path.join(texts_out_pth, txt_file_name)
                    with open(text_save_path, 'w', encoding="utf-8-sig") as file:
                        file.writelines(text)
                    print(f"Saved text: {txt_file_name}")

            # Record saved files
            saved_files.extend([f"{filename}_ln{number + 1}" for number in range(len(image_lines))])
            saved_files.extend([f"{filename}_ln{number + 1}" for number in range(len(text_lines))])

    # Save stats files.
    print("Saving error log and file stats...")
    df_errors = pd.DataFrame.from_dict(error_files_log, orient='index')
    df_errors.to_csv(os.path.join(main_output_dir, 'error_files_while_page_to_line_conversion_stats.csv'))

    saved_files_df = pd.DataFrame(saved_files, columns=["File Names"])
    # saved_files_df.to_excel(os.path.join(main_output_dir, 'files_saved_while_page_to_line_conversion_stats.xlsx'),
    #                         index=False)
    saved_files_df.to_csv(os.path.join(main_output_dir, 'Pages_To_Lines.csv'),
                          index=False)

    print(f"Processing complete. Stats saved to {os.path.join(main_output_dir, 'Pages_To_Lines.csv')}")


def pdf_to_pages_and_lines(path, extract_images=True, extract_texts=False, model=None, predict=False):
    """
    Convert PDFs to images and texts, and then convert those pages to line images and texts,
    saving them in corresponding directories based on flags.

    Args:
        path (str): Can be a path to a PDF or a directory containing PDFs.
        extract_images (bool): Flag to determine if images should be extracted and saved.
        extract_texts (bool): Flag to determine if texts should be extracted and saved.
        model (object): Model to use for predictions if predict flag is True.
        predict (bool): Flag to determine if predictions on line images should be performed.
    """
    main_output_dir = "Output/Book Pages"

    if os.path.exists(main_output_dir):
        shutil.rmtree(main_output_dir)
    os.makedirs(main_output_dir)

    stats = {}

    if os.path.isdir(path):
        # List all files in the directory with .pdf or .PDF extension
        pdf_files = [f for f in os.listdir(path) if f.endswith(('.pdf', '.PDF'))]
    elif os.path.isfile(path) and path.endswith(('.pdf', '.PDF')):
        # If it's a single file, check if it ends with .pdf or .PDF
        pdf_files = [path]
    else:
        raise ValueError("Provided path is neither a directory of PDFs nor a single PDF file.")

    for pdf_file in pdf_files:
        pdf_pth = os.path.join(path, pdf_file) if os.path.isdir(path) else path
        pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]

        print(f"============== Working on {pdf_name} ==============")

        # Create book-specific directory inside the Output folder
        book_output_dir = os.path.join(main_output_dir, pdf_name)
        output_images_dir = os.path.join(book_output_dir, "images")
        output_texts_dir = os.path.join(book_output_dir, "texts")
        output_pred_dir = os.path.join(book_output_dir, "Predicted Text")
        misc_images_dir = os.path.join(book_output_dir, "Misc", "images")
        misc_texts_dir = os.path.join(book_output_dir, "Misc", "texts")

        # Create the required directories
        for dir_path in [output_images_dir, output_texts_dir, output_pred_dir, misc_images_dir, misc_texts_dir]:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
            os.makedirs(dir_path)

        book_pdf_pth = pdf_pth
        book_txt_pth = book_pdf_pth.replace(".pdf", ".txt")

        image_keys = set()
        text_keys = set()

        if extract_images:
            print(f"============== Extracting Images ==============")
            page_images = pdf_to_page_images(book_pdf_pth)
            image_keys = set([key[:-4] for key in page_images.keys()])

        if extract_texts:
            print(f"============== Extracting Text ==============")
            page_texts = pages_from_book_txt(book_txt_pth)
            text_keys = set([key[:-4] for key in page_texts.keys()])

        mutual_keys = image_keys & text_keys if extract_images and extract_texts else image_keys if extract_images else text_keys if extract_texts else set()

        misc_image_keys = [key for key in image_keys if key not in mutual_keys]
        misc_text_keys = [key for key in text_keys if key not in mutual_keys]

        filtered_page_images = {f"{key}.jpg": page_images[f"{key}.jpg"] for key in
                                mutual_keys} if extract_images else {}
        misc_page_images = {f"{key}.jpg": page_images[f"{key}.jpg"] for key in
                            misc_image_keys} if extract_images else {}

        filtered_page_texts = {f"{key}.txt": page_texts[f"{key}.txt"] for key in mutual_keys} if extract_texts else {}
        misc_page_texts = {f"{key}.txt": page_texts[f"{key}.txt"] for key in misc_text_keys} if extract_texts else {}

        # Store stats.
        stats[pdf_name] = {
            'total_images': len(image_keys) if extract_images else 0,
            'total_texts': len(text_keys) if extract_texts else 0,
            'misc_images': len(misc_image_keys) if extract_images else 0,
            'misc_texts': len(misc_text_keys) if extract_texts else 0,
            'total_relevant_data': len(mutual_keys)
        }

        if extract_images:
            save_image_pages(filtered_page_images, output_images_dir)
            save_image_pages(misc_page_images, misc_images_dir)
        if extract_texts:
            save_text_pages(filtered_page_texts, output_texts_dir)
            save_text_pages(misc_page_texts, misc_texts_dir)

        # Process pages to lines
        if extract_images or extract_texts:
            print(f"============== Processing Lines for {pdf_name} ==============")
            page_to_lines(book_output_dir, extract_images=extract_images, extract_texts=extract_texts)

        # Perform predictions on line images if the flag is set
        if predict:
            from predict_and_save import do_prediction

            print(f"============== Making Predictions for {pdf_name} ==============")
            for key, pil_image in filtered_page_images.items():
                print(f"Predicting {key[:-4]}")

                open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                page_lines_images = lines_from_page_image(open_cv_image)


                # Create or open a text file to save predictions for the page
                prediction_file_path = os.path.join(output_pred_dir, str(key.replace(".jpg", ".txt")))
                with open(prediction_file_path, "w") as pred_file:
                    for line_image in page_lines_images:
                        prediction = do_prediction(line_image)

                        # Write the prediction to the file
                        pred_file.write(prediction + "\n")

                print(f"Predictions saved to {prediction_file_path}")

    # Save the 6. statistics as a CSV file
    df = pd.DataFrame.from_dict(stats, orient='index')
    df.to_csv(os.path.join(main_output_dir, 'Bookwise_Pages.csv'))
    print(f"Stats saved to {os.path.join(main_output_dir, 'Bookwise_Pages.csv')}")


