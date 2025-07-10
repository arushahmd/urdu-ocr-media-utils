"""
    Convert the pages data to lines,
        ** Extract line images from each page image
        ** Extracts the line content from the text file, for each page image.
"""

import os
import shutil
import cv2
import re
import pandas as pd

from config import pdf_pages_images_and_texts_dir_path, pdf_books_lines_data_dir_path, stats_path

"""
    Goals:
          Read the image and text files for each page, then
            ** Extract line images from page images
            ** Extract line texts for each page
            ** Save the page images and text files with corresponding name.
            
    Naming: {book_name}_pg{page number}_ln{line number}.{jpg/txt}
"""

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
        page_number = int(match.group(1)) # match page number to int
        return page_number
    else:
        # Return None or raise an error if the pattern is not found
        return None

def linewise_text_from_text_file(file_path):
    """
        Given the text file returns the content of text file as lines.
    """

    with open(file_path, encoding="utf-8-sig") as file:
        lines = file.readlines()
        lines = [line for line in lines if len(str(line)) > 10] # if line will be empty it's length will be 0.
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

def page_to_lines_image_and_text(dir_path, output_path, stats_path):
    """
        Convert the page images and text to line images and text and store to
        corresponding text files.
    """
    images_dir = os.path.join(dir_path,"images")
    texts_dir = os.path.join(dir_path,"texts")

    if not (os.path.exists(images_dir) and os.path.exists(texts_dir)):
        print("Check your directory paths. One or both of the paths is incorrect or does not exist.")
        return None

    print("For some books some first pages have issues in annotation. "
          "\nSo Some pages will be skipped for each book.")

    # image_file_names = os.list_dir(images_dir)
    text_file_names = os.listdir(texts_dir)

    error_files_log = {}
    saved_files = []

    file_names = [filename[:-4] for filename in text_file_names if filename.__contains__("Hayat-e-Iqbal")]

    for filename in file_names:
        image_file_pth = os.path.join(images_dir, f"{filename}.jpg")
        text_file_pth = os.path.join(texts_dir, f"{filename}.txt")

        page_number = page_num_from_filename(filename)

        # Skip first 4 pages for each book.
        if page_number is None:  # If page number not extracted keep track of such files.
            error_files_log[filename] = dict()
            error_files_log[filename]["Error"] = "Enable to Extract File Number Page Number."
            continue
        elif page_number < 5:
            print(f"Skipping Page Number {page_number}.")
            continue

        page_image = cv2.imread(image_file_pth)

        image_lines = lines_from_page_image(page_image)
        text_lines = linewise_text_from_text_file(text_file_pth)

        if not len(image_lines) == len(text_lines):
            print(f"For {filename} Number of Line images does not equal to number of line texts."
                  f"\nLine Images: {len(image_lines)} \nText Lines: {len(text_lines)}")
            if filename not in error_files_log:
                error_files_log[filename] = dict()
            error_files_log[filename]["Line Images"] = len(image_lines)
            error_files_log[filename]["Text Lines"] = len(text_lines)
            continue

        for number in range(len(image_lines)):
            image = image_lines[number]
            text = text_lines[number]

            # list indexing starts from one, but we need naming to start from 1.
            img_file_name = f"{filename}_ln{number+1}.jpg"
            txt_file_name = f"{filename}_ln{number+1}.txt"

            images_out_pth = os.path.join(output_path, "images")
            texts_out_pth = os.path.join(output_path, "texts")

            if not (os.path.exists(images_out_pth) and os.path.exists(texts_out_pth)):
                remove_recreate_dir(images_out_pth)
                remove_recreate_dir(texts_out_pth)

            image_save_path = os.path.join(images_out_pth, img_file_name)
            text_save_path = os.path.join(texts_out_pth, txt_file_name)

            if image.shape[0] is None or image.shape[1] is None or image.shape[0] is 0 or image.shape[1] is 0:
                if filename not in error_files_log:
                    error_files_log[filename] = dict()
                error_files_log[filename]["Image Error"] = "One of the image dimensions was None or 0."
                continue

            saved_files.append(f"{filename}_ln{number}")
            # save the line image and the text
            cv2.imwrite(image_save_path, image)
            with open(text_save_path,'w', encoding="utf-8-sig") as file:
                file.writelines(text)


    # Save stats files.
    # df = pd.DataFrame.from_dict(error_files_log, orient='index')
    # df.to_csv(os.path.join(stats_path, 'error_files_while_page_to_line_conversion_stats.csv'))
    #
    # saved_files_df = pd.DataFrame(saved_files, columns=["File Names"])
    # saved_files_df.to_excel(os.path.join(stats_path, 'files_saved_while_page_to_line_conversion_stats.xlsx'),
    #                         index=False)
    # saved_files_df.to_csv(os.path.join(stats_path, 'files_saved_while_page_to_line_conversion_stats.csv'), index=False)


if __name__ == "__main__":
    """
        The average height of black lines is 5-10 px, means I need lines that have height below 10px.
        Some Pages have no annotations, means they have text, but the text is either like an indexing table
        or like a appendix, for those there is no annotations text in the text file contianing all the text data
        for the full pdf book.
        ==> so we will only take those page images and also those pages which has annotated text, only convert those to line images
            and skip all others.
    """

    page_to_lines_image_and_text(pdf_pages_images_and_texts_dir_path, pdf_books_lines_data_dir_path, stats_path)







