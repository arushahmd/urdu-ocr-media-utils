"""
    The following script is written to create a pdf ocr dataset
    from pdf books, so that we have almost equal disctribution of
    data from all the available books.

    There are two possibilities
        ** Take a specific number of images from each book.
        ** Take a percentage of the total data from each book.
"""
import os
import math
import shutil

import cv2

from config import book_name_prefixes, pdf_books_lines_data_dir_path, dataset_path_25k_images, train_path
from pages_data_to_lines import remove_recreate_dir

def dataset_with_percentage(dir_path, percentage=60):
    """
        Get the desired percentage of the data for each pdf book
        given the percentage.

        Args:
            dir_path (str): path of the directory which contains the images and texts directory
            percentage (int): the percentage to take from each book's data
            book_name_prefixes (list -> str): list of book names, which are a part of file names.
                                              ** Not used as an argument for now, rather imported.
    """

    images_dir = os.path.join(dir_path, "images")
    texts_dir = os.path.join(dir_path, "texts")

    # dest_image_path = os.path.join(dataset_path_25k_images, "images")
    # dest_text_path = os.path.join(dataset_path_25k_images, "texts")

    dest_image_path = os.path.join(train_path, "images")
    dest_text_path = os.path.join(train_path, "texts")

    remove_recreate_dir(dest_image_path)
    remove_recreate_dir(dest_text_path)

    files = dict()

    #create an empty list for each book, to store files later.
    for book_name in book_name_prefixes:
        files[book_name] = []

    image_files = os.listdir(images_dir)

    for image_name in image_files:
    # for (image_name, text_name) in zip(image_files, text_files):
        # print(f"Image File: {image} \nText File: {text}")
        img_prefix = image_name.split("_")[0]
        files[img_prefix].append(image_name)


    for key, value in files.items(): # value is a list of images
        print(f"Working on {key} "
              f"\nTotal Files : {len(value)}")

        if book_name not in ['Andaz-e-Mehrmana','Arooj-e-Iqbal', 'Hayat-e-Iqbal']:
            number_of_files_to_take = math.floor((percentage * len(value)) / 100)
        else:
            number_of_files_to_take = len(value)

        desired_percentage_images = value[:number_of_files_to_take]
        total_files_copied = 0

        for image_name in desired_percentage_images:
            img_prefix = image_name.split("_")[0]
            text_file_name = f"{image_name[:-4]}.txt"

            text_file = os.path.join(texts_dir, text_file_name)

            if os.path.exists(text_file):

                shutil.copy(os.path.join(images_dir,image_name), os.path.join(dest_image_path,image_name))
                shutil.copy(text_file, os.path.join(dest_text_path,text_file_name))

                total_files_copied += 1
        print(f"Total Copied: {total_files_copied}")

if __name__ == "__main__":
    dataset_with_percentage(pdf_books_lines_data_dir_path)


