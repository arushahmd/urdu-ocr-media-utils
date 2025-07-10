"""
    This file contains all the file utilities used for the pdf ocr data
    which is extracted from pdf books.

    The pdf ocr is being trained for urdu language, and the below functions are made in a way
    to be used for urdu language but some can be used for other languages too.
"""

import os
import random
import shutil
import csv
import numpy as np

import cv2


def copy_images_and_txt(src_image_folder, src_txt_folder, dest_image_folder, dest_txt_folder, min_width=100, max_files=None):
    """
    Copies images and their corresponding text files from source folders to destination folders
    if the images meet a specified minimum width requirement. Records filenames and error messages
    of problematic files in a CSV file.

    Parameters:
    src_image_folder (str): Path to the source folder containing image files.
    src_txt_folder (str): Path to the source folder containing text files.
    dest_image_folder (str): Path to the destination folder where valid images will be copied.
    dest_txt_folder (str): Path to the destination folder where corresponding text files will be copied.
    min_width (int): Minimum width (in pixels) that an image must have to be copied. Default is 100.
    max_files (int, optional): Maximum number of image-text pairs to copy. If None, all valid pairs are copied.

    Returns:
    None
    """

    # Create the destination folders if they don't exist
    os.makedirs(dest_image_folder, exist_ok=True)
    os.makedirs(dest_txt_folder, exist_ok=True)

    # Create a CSV file to store the filenames of problematic files
    with open('../problematic_files_old.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'Error Message'])

        # Get the list of text files in the source text folder
        txt_files = os.listdir(src_txt_folder)

        file_count = 0  # Counter for the number of copied files

        # Iterate over all files in the source image folder
        for filename in os.listdir(src_image_folder):
            if max_files is not None and file_count >= max_files:
                break

            if filename.endswith((".jpg", ".jpeg", ".png")):
                # Get the full path of the image file
                src_image_path = os.path.join(src_image_folder, filename)

                try:
                    # Read the image dimensions
                    image_width = get_image_width(src_image_path)

                    # Check if the image width is greater than the minimum width and if there's a corresponding text file
                    if image_width > min_width and filename[:-4] + '.txt' in txt_files:
                        # Copy the image to the destination folder
                        dest_image_path = os.path.join(dest_image_folder, filename)
                        shutil.copyfile(src_image_path, dest_image_path)

                        # Copy corresponding text file from src_txt_folder to dest_txt_folder
                        txt_filename = os.path.splitext(filename)[0] + ".txt"
                        src_txt_path = os.path.join(src_txt_folder, txt_filename)
                        dest_txt_path = os.path.join(dest_txt_folder, txt_filename)
                        shutil.copyfile(src_txt_path, dest_txt_path)
                        print(f"Copied {filename} and {txt_filename}")

                        file_count += 1  # Increment the counter
                except Exception as e:
                    # If an error occurs, write the filename and error message to the CSV file
                    csvwriter.writerow([filename, str(e)])
                    print(f"Error processing {filename}: {e}")


def copy_images_and_txt_excluding_folders(src_image_folder, src_txt_folder, dest_image_folder, dest_txt_folder, exclude_folders, min_width=100, max_files=None):
    """
    Copies images and their corresponding text files from source folders to destination folders
    if the images meet a specified minimum width requirement and are not in the excluded folders.
    Records filenames and error messages of problematic files in a CSV file.

    Parameters:
    src_image_folder (str): Path to the source folder containing image files.
    src_txt_folder (str): Path to the source folder containing text files.
    dest_image_folder (str): Path to the destination folder where valid images will be copied.
    dest_txt_folder (str): Path to the destination folder where corresponding text files will be copied.
    exclude_folders (list): List of folders to exclude images from.
    min_width (int): Minimum width (in pixels) that an image must have to be copied. Default is 100.
    max_files (int, optional): Maximum number of image-text pairs to copy. If None, all valid pairs are copied.

    Returns:
    None
    """

    # Create the destination folders if they don't exist
    os.makedirs(dest_image_folder, exist_ok=True)
    os.makedirs(dest_txt_folder, exist_ok=True)

    # Create a CSV file to store the filenames of problematic files
    with open('../problematic_files_old.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'Error Message'])

        # Get the list of text files in the source text folder
        txt_files = os.listdir(src_txt_folder)

        file_count = 0  # Counter for the number of copied files

        # Iterate over all files in the source image folder
        for filename in os.listdir(src_image_folder):
            if max_files is not None and file_count >= max_files:
                break

            if filename.endswith((".jpg", ".jpeg", ".png")):
                # Get the full path of the image file
                src_image_path = os.path.join(src_image_folder, filename)

                # Check if the image is in the excluded folders
                if any(os.path.join(folder, filename) in src_image_path for folder in exclude_folders):
                    continue

                try:
                    # Read the image dimensions
                    image_width = get_image_width(src_image_path)

                    # Check if the image width is greater than the minimum width and if there's a corresponding text file
                    if image_width > min_width and filename[:-4] + '.txt' in txt_files:
                        # Copy the image to the destination folder
                        dest_image_path = os.path.join(dest_image_folder, filename)
                        shutil.copyfile(src_image_path, dest_image_path)

                        # Copy corresponding text file from src_txt_folder to dest_txt_folder
                        txt_filename = os.path.splitext(filename)[0] + ".txt"
                        src_txt_path = os.path.join(src_txt_folder, txt_filename)
                        dest_txt_path = os.path.join(dest_txt_folder, txt_filename)
                        shutil.copyfile(src_txt_path, dest_txt_path)
                        print(f"Copied {filename} and {txt_filename}")

                        file_count += 1  # Increment the counter
                except Exception as e:
                    # If an error occurs, write the filename and error message to the CSV file
                    csvwriter.writerow([filename, str(e)])
                    print(f"Error processing {filename}: {e}")


def copy_data_with_height(params):
    """
    Given the images and texts path of the destination and the src folders,
    Will check for images with height between range 95-100 and then move them
    to destination image and text folder.

    If the images and texts folder for destination does not exist first create them.
    Copy only those images, for which we have corresponding texts, as we want to copy pair of image and corresponding text.
    If Image name is Aina Khan-e-Iqbal7_Line2.jpg the corresponding text file in the text folder will be named as Aina Khan-e-Iqbal7_Line2.txt.

    :param params: Dictionary containing source and destination paths and quantity of pairs to copy
    :return: None
    """

    def get_image_height(image_path):
        """
        Get the height of an image.

        :param image_path: Path to the image file
        :return: Height of the image
        """
        from PIL import Image
        with Image.open(image_path) as img:
            return img.height

    # Create destination directories if they don't exist
    dest_images_dir = params['destination_images']
    dest_texts_dir = params['destination_texts']
    os.makedirs(dest_images_dir, exist_ok=True)
    os.makedirs(dest_texts_dir, exist_ok=True)

    # Get the list of all image and text files
    all_images = os.listdir(params['source_images'])
    all_texts = os.listdir(params['source_texts'])

    # Get the common image and text pairs
    common_pairs = set(os.path.splitext(image)[0] for image in all_images).intersection(
        os.path.splitext(text)[0] for text in all_texts)

    print(f"Common Pairs contains : \n\n {common_pairs}")

    # Shuffle the list to randomly select images
    common_pairs = list(common_pairs)
    random.shuffle(common_pairs)

    # Number of pairs to copy
    num_pairs = min(int(params['quantity']), len(common_pairs))

    # Counter to keep track of copied pairs
    copied_pairs = 0

    # Iterate through shuffled list of common pairs
    for filename in common_pairs:
        image_path = os.path.join(params['source_images'], filename + ".jpg")
        text_path = os.path.join(params['source_texts'], filename + ".txt")

        # Check if the image height is between 95 and 100
        try:
            image_height = get_image_height(image_path)
        except Exception as e:
            print(f"Error getting height of {filename}: {e}")
            continue

        if 95 <= image_height <= 100:
            # Move image to destination directory
            shutil.copy(image_path, dest_images_dir)
            # Move corresponding text file to destination directory
            shutil.copy(text_path, dest_texts_dir)
            copied_pairs += 1
            print(f"Copied {filename}")

        if copied_pairs == num_pairs:
            break

    if copied_pairs < num_pairs:
        print(f"Warning: There are only {copied_pairs} available image-text pairs, "
              f"but you specified to copy {num_pairs}.")


def copy_with_confirmation(
        source_images_dir,
        source_texts_dir,
        dest_images_dir,
        dest_texts_dir,
        faulty_images_dir,
        faulty_texts_dir,
        removed_images_dir,
        removed_texts_dir,
        copy_to_faulty=True,
        copy_to_removed=False,
        num_pairs=None):
    """
    Copy image-text pairs from source directories to destination directories with confirmation.

    Given source and destination directories for images and texts, this function finds common pairs,
    opens the images, shows the content of corresponding text files as labels,
    and asks the user for confirmation to copy, skip, or remove the pair.
    If the user chooses to remove, both the image and the text file are removed from the source directories.

    :param source_images_dir: Path to the directory containing source images
    :param source_texts_dir: Path to the directory containing source text files
    :param dest_images_dir: Path to the directory where images will be copied
    :param dest_texts_dir: Path to the directory where text files will be copied
    :param faulty_images_dir: Path to the directory where faulty images will be moved
    :param faulty_texts_dir: Path to the directory where faulty text files will be moved
    :param removed_images_dir: Path to the directory where removed images will be moved
    :param removed_texts_dir: Path to the directory where removed text files will be moved
    :param copy_to_faulty: Boolean indicating whether to copy to faulty directories
    :param copy_to_removed: Boolean indicating whether to copy to removed directories
    :param num_pairs: Number of image-text pairs to process, if None, copy as much as available
    :return: None
    """
    # Create destination directories if they don't exist
    for directory in [dest_images_dir, dest_texts_dir, faulty_images_dir, faulty_texts_dir, removed_images_dir, removed_texts_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Get the list of all image and text files
    all_images = os.listdir(source_images_dir)
    all_texts = os.listdir(source_texts_dir)

    # Get the common image and text pairs
    common_pairs = set(os.path.splitext(image)[0] for image in all_images).intersection(
        os.path.splitext(text)[0] for text in all_texts)

    # Shuffle the list to randomly select pairs
    common_pairs = list(common_pairs)

    # Number of pairs to process
    num_pairs = min(num_pairs, len(common_pairs)) if num_pairs is not None else len(common_pairs)

    # Counter to keep track of copied, moved to faulty, and removed pairs
    copied_pairs = 0
    faulty_pairs = 0
    removed_pairs = 0
    skipped_pairs = 0

    # Iterate through shuffled list of common pairs
    for filename in common_pairs[:num_pairs]:
        image_path = os.path.join(source_images_dir, filename + ".jpg")
        text_path = os.path.join(source_texts_dir, filename + ".txt")

        # Check if destination files already exist
        dest_img_pth = os.path.join(dest_images_dir, filename + ".jpg")
        dest_txt_pth = os.path.join(dest_texts_dir, filename + ".txt")
        faulty_img_pth = os.path.join(faulty_images_dir, filename + ".jpg")
        faulty_txt_pth = os.path.join(faulty_texts_dir, filename + ".txt")
        removed_img_pth = os.path.join(removed_images_dir, filename + ".jpg")
        removed_txt_pth = os.path.join(removed_texts_dir, filename + ".txt")

        if os.path.exists(dest_img_pth) or os.path.exists(dest_txt_pth):
            print(f"Skipped {filename} because it already exists in the destination directories")
            skipped_pairs += 1
            continue

        content = None
        image = cv2.imread(image_path)

        # Read the text content
        with open(text_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()

        # Show image with text content as label
        cv2.imshow(f"Image : ", image)
        print(f"Content : {content}")

        # Wait for user input
        key = cv2.waitKey(0) & 0xFF

        # Process user input
        if key == ord('y'):
            # Copy image and text file to destination directories
            shutil.copy(image_path, dest_img_pth)
            shutil.copy(text_path, dest_txt_pth)
            copied_pairs += 1
            print(f"Copied {filename} to destination directories")
        elif key == ord('n'):
            if copy_to_faulty:
                # Move image and text file to faulty directories
                shutil.move(image_path, faulty_img_pth)
                shutil.move(text_path, faulty_txt_pth)
                faulty_pairs += 1
                print(f"Moved {filename} to faulty directories")
            else:
                print(f"Skipped {filename}")
                skipped_pairs += 1
        elif key == ord('r'):
            if copy_to_removed:
                # Move image and text file to removed directories
                shutil.move(image_path, removed_img_pth)
                shutil.move(text_path, removed_txt_pth)
                removed_pairs += 1
                print(f"Moved {filename} to removed directories")
            else:
                print(f"Skipped {filename}")
                skipped_pairs += 1
        else:
            print(f"Skipped {filename}")
            skipped_pairs += 1

        # Close image window
        cv2.destroyAllWindows()

        # Display summary after each action
        print(f"Copied : {copied_pairs} Moved to faulty {faulty_pairs} Moved to removed {removed_pairs} Skipped {skipped_pairs}")

    print("\nFinal Summary:")
    print(f"Copied : {copied_pairs} Moved to faulty {faulty_pairs} Moved to removed {removed_pairs} Skipped {skipped_pairs}")


def view_and_remove_pairs(main_dir):
    """
    View image-text pairs from source directories and remove them based on user input.

    Given the main directory path containing folders for images and texts, this function iterates through
    the image and text pairs, showing each image and the content of its corresponding text file.
    If the user chooses to remove a pair, both the image and the text file are removed from their respective directories.

    :param main_dir: Path to the main directory containing folders for images and texts
    :return: None
    """
    source_images_dir = os.path.join(main_dir, "images")
    source_texts_dir = os.path.join(main_dir, "texts")

    # Get the list of all image and text files
    all_images = sorted(os.listdir(source_images_dir))
    all_texts = sorted(os.listdir(source_texts_dir))

    # Counter to keep track of removed pairs
    removed_pairs = 0

    for i, image_name in enumerate(all_images):
        image_path = os.path.join(source_images_dir, image_name)
        text_name = os.path.splitext(image_name)[0] + ".txt"
        text_path = os.path.join(source_texts_dir, text_name)

        # Read the text content
        with open(text_path, 'r', encoding='utf-8-sig') as file:
            text_content = file.read()

        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to read image {image_path}")
            continue

        # Show image with text content as label
        cv2.imshow("Image with Text", image)
        print(f"Text Content: {text_content}")

        # Wait for user input
        key = cv2.waitKey(0) & 0xFF

        # Process user input
        if key == ord('d') or key == 81:  # 'd' or left arrow key
            # Remove both image and text file from source directories
            os.remove(image_path)
            os.remove(text_path)
            removed_pairs += 1
            print(f"Removed {image_name} and its corresponding text file from source directories")
        elif key == ord('s') or key == 83:  # 's' or right arrow key
            print(f"Skipped {image_name}")

        # Close image window
        cv2.destroyAllWindows()

    print("\nSummary:")
    print(f"Removed {removed_pairs} image-text pairs")


def remove_page_number(directory):
    """
    Remove the '_Page' from the names of all files in the given directory.

    Given a directory containing files with names like 'Aina Khan e Iqbal_Page1_Line1.txt',
    this function will remove the '_Page' part from the names and rename the files accordingly.

    :param directory: Path to the directory containing files to be renamed
    :return: None
    """
    # Iterate through files in the directory
    for filename in os.listdir(directory):
        # Check if the filename contains '_Page'
        if "_Page" in filename:
            # Remove the '_Page' part and rename the file
            new_filename = filename.replace("_Page", "")
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"Renamed: {filename} -> {new_filename}")


def get_image_width(image_path):
    import cv2
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    # Check if the image was loaded successfully
    if image is None:
        # If not, return None
        return None
    # Get the width of the image
    height, width, _ = image.shape
    return width


def delete_problematic_files(csv_file, src_pth):
    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        print(f"CSV file '{csv_file}' not found.")
        return

    src_img_pth = os.path.join(src_pth, "images")
    src_txt_pth = os.path.join(src_pth, "texts")


    # Open the CSV file and read problematic filenames and their error messages
    with open(csv_file, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row
        for row in csvreader:
            filename, error_message = row
            image_file = filename.split(',')[0]
            image_file = os.path.join(src_img_pth,image_file)
            if os.path.isfile(image_file):
                os.remove(image_file)
                print(f"Deleted image file: {image_file}")
            else:
                print(f"Image file not found: {image_file}")
            txt_file = os.path.splitext(filename)[0] + ".txt"
            txt_file = os.path.join(src_txt_pth, txt_file)
            if os.path.isfile(txt_file):
                os.remove(txt_file)
                print(f"Deleted text file: {txt_file}")
            else:
                print(f"Text file not found: {txt_file}")


def delete_Pages(images_dir, texts_dir):
    """
    Given the images and texts dir, will traverse the images directory
    and remove all the images that do not contain the word 'Line' in their names,
    as those images contain full page not single Lines.
    Also will search in the text folder to check if for the images we need to remove, if any .txt file
    exists remove that too.
    If image name is Arooj-e-Iqbal333_Line2.jpg the text file for the image in texts directory will be
    with name Arooj-e-Iqbal333_Line2.txt

    :param images_dir: Directory containing images
    :param texts_dir: Directory containing corresponding text files
    :return: None
    """

    print("Checking for page files...")

    # Iterate through images directory
    for filename in os.listdir(images_dir):
        if "Line" not in filename:
            # If the word 'Line' is not in the filename, delete the image
            print(f"Page image found with name  {filename}")
            os.remove(os.path.join(images_dir, filename))

            # Remove corresponding text file, if exists
            text_filename = os.path.splitext(filename)[0] + ".txt"
            text_path = os.path.join(texts_dir, text_filename)
            if os.path.exists(text_path):
                print(f"Corresponding text file found with name {text_filename}")
                os.remove(text_path)
            print(f"Removed Files.")


def refine_images(images_dir, texts_dir):
    """
    Given the images and the texts path, will check the images which are corrupt,
    do not open or any other error occurs and will remove those images and their corresponding text files.
    If image name is, Aina Khan-e-Iqbal23_Line14.jpg, the corresponding text file in texts_dir will have name,
    Aina Khan-e-Iqbal23_Line14.txt.

    If the corresponding text file exists remove it too.

    :param images_dir: Directory containing images
    :param texts_dir: Directory containing corresponding text files
    :return: None
    """
    # Iterate through images directory
    for filename in os.listdir(images_dir):
        image_path = os.path.join(images_dir, filename)
        text_filename = os.path.splitext(filename)[0] + ".txt"
        text_path = os.path.join(texts_dir, text_filename)

        try:
            # Attempt to open the image to check if it's corrupt
            image = cv2.imread(image_path)
            cv2.imshow("Image", image)
            cv2.waitKey(100)
        except Exception as e:
            print(f"Image == {filename} == is corrupted and will be removed.")
            # If image is corrupt or can't be opened, remove it
            os.remove(image_path)
            # Also remove corresponding text file if it exists
            if os.path.exists(text_path):
                print(f"Text File == {text_filename} == found and will be removed.")
                os.remove(text_path)


def open_image(image_path):
    try:
        image = cv2.imread(image_path)
        cv2.imshow(f"Image : {image.shape}", image)
        cv2.waitKey(0)
    except Exception as e:
        print("The image was corrupt.")


def get_pages_dataset_paths(main_dir):

    """
        Simply give the path of the images and the texts of the given directory.
    """

    images_dir = os.path.join(main_dir, "Pictures")
    texts_dir = os.path.join(main_dir, "Text")

    page_images_dir = os.path.join(images_dir, "Pages")
    page_texts_dir = os.path.join(texts_dir, "Pages")

    img_names = os.listdir(page_images_dir)

    images = [os.path.join(page_images_dir, imagename) for imagename in img_names]
    texts = [os.path.join(page_texts_dir, textname) for textname in os.listdir(page_texts_dir)] #

    return images, texts


def create_pages_dataset(dirs, dest_images_dir, dest_texts_dir):
    """
    Copies pages and their associated texts to specific directories.

    Args:
        dirs (list): List of directories containing images and texts.
        dest_images_dir (str): Destination directory for images.
        dest_texts_dir (str): Destination directory for texts.
    """
    if not os.path.exists(dest_images_dir):
        os.makedirs(dest_images_dir)
    if not os.path.exists(dest_texts_dir):
        os.makedirs(dest_texts_dir)

    for directory in dirs:
        print(f"Working on {directory}.")
        image_paths, text_paths = get_pages_dataset_paths(directory)
        print("Copying Files.")
        for img_path, text_path in zip(image_paths, text_paths):
            if os.path.exists(img_path):
                img_filename = os.path.basename(img_path)
                shutil.copy(img_path, os.path.join(dest_images_dir, img_filename))
            if os.path.exists(text_path):
                text_filename = os.path.basename(text_path)
                shutil.copy(text_path, os.path.join(dest_texts_dir, text_filename))


def count_lines_from_text_data(texts_dir):
    """
        Given the directory containing .txt files it will count the number of text lines in each .txt file
        and return back the total count i.e. total number of text lines collectively in all the files in the
        given directory.
    """

    file_names = os.listdir(texts_dir)

    for filename in file_names:
        # first extract all the pdf data and convert it to desired pages format.
        pass

def count_images_for_book(directory, book_name, extension):
    total_images = 0

    for filename in os.listdir(directory):
        if filename.lower().startswith(book_name.lower()) and filename.lower().endswith(extension.lower()):
            total_images += 1

    return total_images


all_images_dir = "ocr-data/images"
all_texts_dir = "ocr-data/texts"

#================= FLAGS ====================#

DELETE_PAGES = False # Delete page images from given directories.
CHECK_FOR_PAGES = False # Checks if a corresponding image directory have page images.
DELETE_PROBLAMETIC = False # delete files that do not have image and text pair, with only image or only text.
COPY_FILES = True # Copy images and their corresponding text files from given directory to destination directory.
OPEN_IMAGE = False # Function try to open a single image, and if it is corrupt print that it is corrupt.
REFINE_IMAGES = False # This flag is used to remove the corrupt images and their corresponding text files.

COPY_FILES_HEIGHT_RANGE = False # will use the function to copy images with height between range 95 - 110
COPY_WITH_CONFIRMATION = False
VIEW_AND_REMOVE = False
CREATE_PAGES_DATASET = False
COUNT_IMAGES_FOR_BOOKS = False


COPY_WITH_EXCLUSION = False

#================= FLAGS ====================#


if __name__ == "__main__":

    if DELETE_PAGES:
        """Delete page images from given directories."""
        delete_Pages(all_images_dir, all_texts_dir)

    if COPY_FILES:
        """Copy images and their corresponding text files from given directory to destination directory."""
        # Copy images and corresponding text files
        src_image_folder = "ocr-main-data/raw-data/images"
        src_txt_folder = "ocr-main-data/raw-data/texts"
        dest_image_folder = "ocr-main-data/new-data/images"
        dest_txt_folder = "ocr-main-data/new-data/texts"
        copy_images_and_txt(src_image_folder, src_txt_folder, dest_image_folder, dest_txt_folder, max_files=100)

    if COPY_WITH_EXCLUSION:
        """Copy images and their corresponding text files from given directory to destination directory."""
        # Copy images and corresponding text files
        src_image_folder = "ocr-main-data/images"
        src_txt_folder = "ocr-main-data/texts"
        dest_image_folder = "ocr/test-data/images"
        dest_txt_folder = "ocr/test-data/texts"

        excluded_folders = [
            "ocr-data/images/old",
            "ocr-data/images/old"
        ]

        copy_images_and_txt_excluding_folders(src_image_folder, src_txt_folder, dest_image_folder, dest_txt_folder,
                                              excluded_folders, min_width=100, max_files=2500)

    if DELETE_PROBLAMETIC:
        """Take the main folder containing the images and texts folder, and traverse to delete problematic files."""
        # delete_problematic_files(csv_file_pth, src_folder)

    if OPEN_IMAGE:
        img_pth = "line-data/Line18.jpg"
        # img_pth = os.path.join(all_images_dir, "Aina Khan-e-Iqbal7_Line2.jpg")
        open_image(img_pth)

    if REFINE_IMAGES:
        """ Refine Images, remove corrupt images and their corresponding text files from given image and text directories."""
        refine_images(all_images_dir, all_texts_dir)

    if COPY_FILES_HEIGHT_RANGE:
        "Number of pixels can serve as a measure here too."
        params = {
            "source_images": all_images_dir,
            "source_texts": all_texts_dir,
            "destination_images": "test-data/images",
            "destination_texts": "test-data/texts",
            "quantity": 1000
        }
        copy_data_with_height(params)

    if COPY_WITH_CONFIRMATION:
        dest_images_dir = "correct-data/images"
        dest_texts_dir = "correct-data/texts"

        faulty_images_dir = "incorrect-data/images"
        faulty_texts_dir = "incorrect-data/texts"

        removed_images_dir = "removed-data/images"
        removed_texts_dir = "removed-data/texts"

        copy_with_confirmation(all_images_dir, all_texts_dir, dest_images_dir, dest_texts_dir, faulty_images_dir, faulty_texts_dir, removed_images_dir, removed_texts_dir)

    if VIEW_AND_REMOVE:
        main_dir = "training-set-(1000)"
        view_and_remove_pairs(main_dir)

    if CREATE_PAGES_DATASET:
        dirs = [
            "books-data/Aina Khan e Iqbal",
            "books-data/Al Jihad Fil Islam (Volume 02) SwaneUmri Hazrat Uma",
            "books-data/Andaz-e-Mehrmana Iqbal kiTasanif per Nai Roshni",
            "books-data/Arooj-e-Iqbal",
            "books-data/Darbar-e-Akbari",
            "books-data/Hayat-e-Iqbal",
            "books-data/Hikmat-e-Iqbal"
                ]
        dest_images_dir = "page-images/images"
        dest_texts_dir = "page-images/texts"
        create_pages_dataset(dirs, dest_images_dir, dest_texts_dir)

    if COUNT_IMAGES_FOR_BOOKS:
        # Book names and their corresponding keywords in file names
        book_names = {
            # "Aina Khan-e-Iqbal": "Aina Khan-e-Iqbal", # name in jpg images
            "Aina Khan e Iqbal": "Aina Khan e Iqbal",
            "Al Jihad Fil Islam (Volume 02) SwaneUmri Hazrat Uma": "Al Jihad Fil Islam",
            "Andaz-e-Mehrmana Iqbal kiTasanif per Nai Roshni": "Andaz-e-Mehrmana Iqbal",
            "Arooj-e-Iqbal": "Arooj-e-Iqbal",
            "Darbar-e-Akbari": "Darbar-e-Akbari",
            "Hayat-e-Iqbal": "Hayat-e-Iqbal",
            "Hikmat-e-Iqbal": "Hikmat-e-Iqbal"
        }

        # Desired file extension
        desired_extension = ".txt"  # Specify the desired extension here

        directory_path = "page-images/texts"

        # Count images for each book
        for book_name, keyword in book_names.items():
            total_images = count_images_for_book(directory_path, keyword, desired_extension)
            # print(f"Total images for {book_name}: {total_images}")
            print(f"{book_name} : {total_images} Pages")



