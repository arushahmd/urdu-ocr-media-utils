"""
    This is the main file that will run the following operations

    1. Extract the page images given the pdf file
    2. Extract lines from each page image
    3. Copy files of images and texts per Book from the given folder
"""

import os
import re
import time
from datetime import datetime

import cv2

from config import PATH, TEXT_PATH, DEBUG, CONFIG, PROCESS_PDFS, PROCESS_IMGS, OCR
from convert_to_lines import page_to_lines
from log_utils import initialize_csv, create_log_entry, update_log_entry
from pdf_main import process_pdf_file, process_pdf_directory, process_text_file, process_text_dir, \
    process_directory_images
from predict_and_save import do_prediction
from text_utils import validate_file_path

def clean_filename(file_name):
    # Use a regex to match '_ln<number>' and remove it
    return re.sub(r'_ln\d+', '', file_name)

if __name__ == "__main__":
    initialize_csv()

    if os.path.isfile(PATH) and validate_file_path(PATH, ('.pdf', '.PDF')):
        process_pdf_file(PATH)
        if TEXT_PATH is not None and TEXT_PATH != "":
            process_text_file(TEXT_PATH, DEBUG)

    elif validate_file_path(PATH, ('.jpg', '.JPG','.png','.PNG', '.jpeg', '.JPEG')):
        page_lines = page_to_lines(PATH)
        page_predictions = []

        output_path = "output/predictions/image_predictions"
        # Ensure the output directory exists
        os.makedirs(output_path, exist_ok=True)

        for line_count, line in enumerate(page_lines):
            try:
                # Perform prediction on the line image
                prediction = do_prediction(line)

                if CONFIG["save_line_predictions"]:
                    # line_out_dir = f"{output_path}/line_wise/"
                    line_out_dir = "/media/cle-nb-183/New Volume/CLE/fonts_guide"
                    os.makedirs(line_out_dir, exist_ok=True)

                    # Extract the filename from the PATH and check if '_ln' is already in it
                    file_name = PATH.split("/")[-1].replace(".jpg", "").replace(".JPG", "")

                    # Only append '_ln{line_count+1}' if '_ln' is not already in the filename
                    if '_ln' not in file_name:
                        line_img_name = f'{file_name}_ln{line_count + 1}.txt'
                    else:
                        line_img_name = f'{file_name}.txt'

                    # Write the prediction to the output file
                    with open(f"{line_out_dir}{line_img_name}", 'w') as file:
                        file.write(prediction)
                        print(f"Prediction saved for {line_img_name}: {prediction}")

                if CONFIG["save_page_predictions"]:
                    page_predictions.append(prediction)

            except Exception as e:
                # Print the error message and the file that caused the issue
                print(f"Exception occurred while processing Line {line_count + 1}: {e}")
                continue

        if CONFIG["save_page_predictions"]:
            file_name = PATH.split("/")[-1].replace(".jpg", "").replace(".JPG", "")
            file_name = clean_filename(file_name)

            page_out_dir = f"{output_path}/page_wise/"
            os.makedirs(page_out_dir, exist_ok=True)

            with open(os.path.join(page_out_dir, file_name), 'w') as file:
                for prediction in page_predictions:
                    file.write(prediction + '\n')

            print(f"\nPredictions saved for Page {file_name}")


    elif os.path.isdir(PATH):
        if PROCESS_PDFS:
            process_pdf_directory(PATH)
            if TEXT_PATH is not None and TEXT_PATH != "":
                process_text_dir(TEXT_PATH, DEBUG)

        if PROCESS_IMGS:
            process_start_time = datetime.now().strftime("%H:%M:%S")
            process_directory_images(PATH)

        if OCR:
            # Log start time
            start_time = time.time()
            log_entry = create_log_entry(PATH, process="OCR on Lines")

            output_path = os.path.join("output", "predictions", "line_predictions",
                                       os.path.basename(os.path.dirname(PATH)))
            os.makedirs(output_path, exist_ok=True)

            successful_count = 0
            failed_count = 0
            img_files = os.listdir(PATH)
            total = len(img_files)

            for i, file in enumerate(img_files):
                save_path = os.path.join(output_path, file.replace("jpg", "txt"))
                if os.path.exists(save_path):
                    print(f"Prediction already exists for {file}")
                else:
                    print(f"{i + 1}/{total} Processing: {file}")  # Show progress

                    try:
                        print(f"Predicting {file}")
                        image_path = os.path.join(PATH, file)
                        image = cv2.imread(image_path)

                        if image is None:
                            raise Exception(f"Failed to read image: {file}")

                        prediction = do_prediction(image)

                        with open(save_path, "w") as f:
                            f.write(prediction + '\n')
                        print(f"Saved prediction at: {save_path}")
                        successful_count += 1

                    except Exception as e:
                        print(f"Failed on file {file}: {e}")
                        failed_count += 1
                        continue  # Continue to the next file

            # Log end time and duration
            end_time = time.time()
            duration = end_time - start_time

            log_entry['status'] = "successful" if successful_count > 0 else "failed"
            log_entry['details'] = (f"Processed {total} line images\n"
                                    f"Successful: {successful_count}\n"
                                    f"Failed: {failed_count}\n"
                                    f"Duration: {duration:.2f} seconds")  # Log the duration

            update_log_entry(log_entry)

            # Print start and end time
            print(f"Process started at: {time.ctime(start_time)}")
            print(f"Process ended at: {time.ctime(end_time)}")
            print(f"Total duration: {duration:.2f} seconds")
