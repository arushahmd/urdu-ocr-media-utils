import os
import shutil
import math

from config import book_name_prefixes, pdf_books_lines_data_dir_path, dataset_path_25k_images, train_path
from pages_data_to_lines import remove_recreate_dir

def get_image_and_text_files(dir_path):
    images_dir = os.path.join(dir_path, "images")
    texts_dir = os.path.join(dir_path, "texts")

    image_files = os.listdir(images_dir)
    text_files = os.listdir(texts_dir)

    return images_dir, texts_dir, image_files, text_files


def copy_files(book_name, images_dir, texts_dir, dest_image_path, dest_text_path, number_of_files_to_take):
    files_copied = 0
    image_files = [f for f in os.listdir(images_dir) if f.startswith(book_name)]

    for image_name in image_files[:number_of_files_to_take]:
        text_file_name = f"{image_name[:-4]}.txt"
        text_file_path = os.path.join(texts_dir, text_file_name)

        if os.path.exists(text_file_path):
            shutil.copy(os.path.join(images_dir, image_name), os.path.join(dest_image_path, image_name))
            shutil.copy(text_file_path, os.path.join(dest_text_path, text_file_name))
            files_copied += 1

    return files_copied


def dataset_with_equal_numbers(dir_path, book_data, total_count=25000):
    """
        Get the desired number of files from each pdf book to reach a total count.

        Args:
            dir_path (str): path of the directory which contains the images and texts directory
            book_data (dict): dictionary with book names as keys and the number of files to take as values
            total_count (int): the target total count of files
    """

    images_dir, texts_dir, image_files, text_files = get_image_and_text_files(dir_path)

    # dest_image_path = os.path.join(dataset_path_25k_images, "images")
    # dest_text_path = os.path.join(dataset_path_25k_images, "texts")

    dest_image_path = os.path.join(train_path, "images")
    dest_text_path = os.path.join(train_path, "texts")

    remove_recreate_dir(dest_image_path)
    remove_recreate_dir(dest_text_path)

    total_files_copied = 0

    for book_name, num_files in book_data.items():
        if total_files_copied >= total_count:
            break

        files_to_take = min(num_files, total_count - total_files_copied)
        files_copied = copy_files(book_name, images_dir, texts_dir, dest_image_path, dest_text_path, files_to_take)
        total_files_copied += files_copied

        print(f"Working on {book_name} "
              f"\nTotal Files : {len([f for f in image_files if f.startswith(book_name)])}"
              f"\nTotal Copied: {files_copied}")

    print(f"\nTotal files copied: {total_files_copied}")


# Dictionary with book names as keys and the number of files to take as values
book_data = {
    "Aina Khan-e-Iqbal": 1154,
    "Al Jihad Fil Islam": 1000,
    "Andaz-e-Mehrmana": 520,
    "Arooj-e-Iqbal": 109,
    "Darbar-e-Akbari": 7500,
    "Hayat-e-Iqbal": 0,
    "Hazrat Abu Bakar Siddique": 3400,
    "Hikmat-e-Iqbal": 5000,
    "Hiyat-e-Muhammad(SAW)": 3317
}

dataset_with_equal_numbers(pdf_books_lines_data_dir_path ,book_data)