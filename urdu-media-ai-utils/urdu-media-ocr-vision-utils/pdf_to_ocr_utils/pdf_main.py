"""
    This will contain the main pdf functionalities.
"""

import os
from datetime import datetime

import cv2

from config import CONFIG, THRESHOLD
from convert_to_lines import page_to_lines, text_to_lines
from convert_to_pages import pdf_to_pages, text_to_pages
from log_utils import create_log_entry, update_log_entry
from predict_and_save import do_prediction, get_model
from text_utils import validate_file_path


def process_pdf_file(pdf_path):
    """
    Process a single PDF file to extract images and lines, perform OCR, and save predictions.
    """

    book_name = os.path.basename(pdf_path).replace(".pdf", "")
    output_dir = f"output/predictions/line_predictions/{book_name}"
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist.

    # Step 1: Convert PDF pages to images
    log_entry = create_log_entry(pdf_path, process="Pdf to Pages")
    update_log_entry(log_entry)
    try:
        page_images = pdf_to_pages(pdf_path, CONFIG['save_page_images'])
        num_pages = len(page_images)
        log_entry["details"] = f"Number of Pages Processed: {num_pages}"
        log_entry["status"] = "Success"
    except Exception as e:
        log_entry["error"] = f"{type(e).__name__}: {str(e)}"
        log_entry["status"] = "Failed"
    update_log_entry(log_entry)  # Finalize the log entry for page extraction

    if CONFIG['extract_lines']:
        # Step 2: Convert pages to lines
        start_time = datetime.now()
        log_entry = create_log_entry(pdf_path, process="Pages to Lines", details=f"Pages: {num_pages}")
        try:
            total_lines = 0
            for page_count, (page_name, page_image) in enumerate(page_images.items()):
                print(f"Extracting Lines from Page {page_count}")
                try:
                    line_images = page_to_lines(page_image, CONFIG['save_line_images'], page_name)
                    total_lines += len(line_images)
                except Exception as e:
                    log_entry["error"] = f"{type(e).__name__}: {str(e)}"
                    log_entry["status"] = "Failed"
                    update_log_entry(log_entry)
                    return  # Exit if there's an error in extracting lines

            # Update log entry to indicate success
            log_entry["status"] = "Success"
            log_entry["details"] = f"Extracted {total_lines} Lines from {num_pages} Pages."
        except Exception as e:
            log_entry["error"] = f"{type(e).__name__}: {str(e)}"
            log_entry["status"] = "Failed"
        log_entry["end_time"] = datetime.now().strftime("%H:%M:%S")
        log_entry["duration"] = str(datetime.strptime(log_entry["end_time"], "%H:%M:%S") - start_time)
        update_log_entry(log_entry)  # Finalize the log entry for line extraction

    if CONFIG['do_predictions']:
        # Step 3: Perform OCR on lines
        start_time = datetime.now()
        log_entry = create_log_entry(pdf_path, process="OCR on Line Images", details=f"Total Lines : {total_lines}")
        model = get_model('configs/CNN_RNN_CTC/MMA-UD.json')

        # Initialize files for saving if BOOK_WISE option is enabled
        if CONFIG['save_book_predictions']:
            book_file_name = f"{book_name}.txt"
            book_save_path = os.path.join(output_dir, f"book_wise/{book_file_name}")
            os.makedirs(os.path.dirname(book_save_path), exist_ok=True)

        try:
            print(f"\n\nPredicting Images ....\n")
            for page_count, (page_name, page_image) in enumerate(page_images.items()):
                print(f"Predicting :  Page {page_count}")
                line_images = page_to_lines(page_image, CONFIG['save_line_images'], page_name)
                page_predictions = []  # Store page-wise predictions temporarily

                for line_count, line_img in enumerate(line_images):
                    try:
                        prediction = do_prediction(line_img)

                        if CONFIG["save_line_predictions"]:
                            # Save predictions line-wise
                            prediction_file_name = f"{page_name.replace('.jpg', '')}_ln{line_count + 1}.txt"
                            save_path = os.path.join(output_dir, f"line_wise/{prediction_file_name}")
                            os.makedirs(os.path.dirname(save_path), exist_ok=True)
                            with open(save_path, 'w', encoding='utf-8') as file:
                                file.write(prediction)

                        if CONFIG["save_page_predictions"]:
                            # Collect page-wise predictions
                            page_predictions.append(prediction)

                        if CONFIG["save_book_predictions"]:
                            # Write to the book-wise file immediately after each line prediction
                            with open(book_save_path, 'a', encoding='utf-8') as book_file:
                                if line_count == 0:
                                    book_file.write(f"\n######## Page {page_count + 1} ########\n")
                                book_file.write(f"{prediction}\n")

                    except Exception as e:
                        log_entry["error"] = f"{type(e).__name__}: {str(e)}"
                        log_entry["status"] = "Failed"
                        update_log_entry(log_entry)
                        return  # Exit if there's an error in performing OCR

                # Write page-wise predictions immediately after the entire page is processed
                if CONFIG["save_page_predictions"] and page_predictions:
                    page_file_name = f"{page_name.replace('.jpg', '')}.txt"
                    save_path = os.path.join(output_dir, f"page_wise/{page_file_name}")
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    with open(save_path, 'w', encoding='utf-8') as file:
                        file.write("\n".join(page_predictions))

            # Update log entry to indicate success
            log_entry["status"] = "Success"
        except Exception as e:
            log_entry["error"] = f"{type(e).__name__}: {str(e)}"
            log_entry["status"] = "Failed"
        log_entry["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry["duration"] = str(datetime.strptime(log_entry["end_time"], "%Y-%m-%d %H:%M:%S") - start_time)
        update_log_entry(log_entry)  # Finalize the log entry for OCR


def process_pdf_directory(pdf_dir):
    """
    Process all PDF files in a directory.
    """

    pdf_files = [os.path.join(pdf_dir, pdf_file) for pdf_file in os.listdir(pdf_dir) if
                 pdf_file.lower().endswith('.pdf')]
    for pdf_path in pdf_files:
        print(f"Processing PDF file {pdf_path}")
        try:
            process_pdf_file(pdf_path)
        except Exception as e:
            log_entry = create_log_entry(pdf_path, process="Processing PDF")
            log_entry["error"] = f"{type(e).__name__}: {str(e)}"
            log_entry["status"] = "Failed"
            update_log_entry(log_entry)


def process_directory_images(directory):
    """
    Process each image in the directory by applying the same logic used for individual images.
    Converts Page images to lines.
    """

    log_entry = create_log_entry(directory, process="Pages to Lines")
    update_log_entry(log_entry)
    file_count = 0
    line_count = 0
    failed_count = 0
    failed_files = []

    output_path = f"/home/cle-dl-05/Desktop/Aroosh/2. Pdf Ocr Pipeline/test_data/3. selected pages for multi-line analysis/"
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    try:
        print(f"Processing : {directory}")
        # List all files in the directory
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)

            # Check if the file is an image
            if validate_file_path(file_path, ('.jpg', '.JPG', '.png', '.PNG', '.jpeg', '.JPEG')):
                print(f"Processing image: {file_path}")
                file_count += 1
            try:
                # Same logic as for an individual page image
                page_lines = page_to_lines(file_path) # line images from pages.
                line_count += len(page_lines)

                for line in page_lines:
                    line_img_name = f"{file_name.replace('.jpg', '')}_ln{line_count + 1}.jpg"
                    save_path = os.path.join(output_path,line_img_name)
                    cv2.imwrite(save_path, line)
            except:
                failed_count+= 1
                failed_files.append(file_name)

        log_entry['status'] = "Success"
        log_entry['details'] = (f"Processed: {file_count} images"
                                f"\n Successful Conversion to Lines for: {file_count-failed_count} pages"
                                f"\n Failed Conversion to Lines for: {failed_count} pages"
                                f"Failed Files: {','.join(failed_files)}")

    except Exception as e:
        log_entry["error"] = f"{type(e).__name__}: {str(e)}"
        log_entry["status"] = "Failed"

    update_log_entry(log_entry)


def process_text_file(txt_path, save=False):
    """
    Process a text file by splitting it into pages and further dividing each page's content into lines.

    Args:
        txt_path (str): Path to the text file.
        save (bool): Whether to save the individual text files and lines to the disk.

    Returns:
        None
    """
    # Convert text file into pages
    text_pages = text_to_pages(txt_path, save=save)

    # Process each page
    for file_name, content in text_pages.items():
        try:
            # Convert the page content into lines and optionally save
            text_to_lines(content, save=save, file_name=file_name)
        except Exception as e:
            print(f"Error processing page {file_name}: {e}")
            continue


def process_text_dir(txt_dir, save=False):
    """
    Process all text files in a given directory. For each text file, split the content into pages
    and then further divide each page's content into lines.

    Args:
        txt_dir (str): Path to the directory containing text files.
        save (bool): Whether to save the processed pages and lines to the disk.

    Returns:
        None
    """
    if not os.path.isdir(txt_dir):
        print(f"Error: {txt_dir} is not a valid directory.")
        return

    # Loop through all the files in the directory
    for file_name in os.listdir(txt_dir):
        file_path = os.path.join(txt_dir, file_name)

        # Only process text files (.txt)
        if os.path.isfile(file_path) and validate_file_path(file_path, ('.txt', '.TXT')):
            try:
                print(f"Processing file: {file_path}")
                process_text_file(file_path, save=save)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                continue

    print("Processing complete.")


if __name__ == "__main__":
    txt_path = "/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/Annotated Books/Hayat-e-Iqbal.pdf" # Hayat-e-Iqbal.txt

    # process_text_file(txt_path)
    process_pdf_file(txt_path, save= True)
