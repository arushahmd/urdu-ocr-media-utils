"""
    Removes the image if it is corrupted.
"""

import os
import cv2
import shutil
import pandas as pd

from config import dataset_path_25k_images


def is_corrupt(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None or image.shape[0] == 0 or image.shape[1] == 0:
            return True
    except Exception as e:
        return True
    return False


def remove_corrupt_images(image_dir, text_dir, corrupted_dir):
    if not os.path.exists(corrupted_dir):
        os.makedirs(corrupted_dir)

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            image_path = os.path.join(image_dir, filename)
            text_filename = os.path.splitext(filename)[0] + '.txt'
            text_path = os.path.join(text_dir, text_filename)

            if is_corrupt(image_path):
                # Move the corrupt image
                corrupted_image_path = os.path.join(corrupted_dir, filename)
                shutil.move(image_path, corrupted_image_path)

                # Move the corresponding text file if it exists
                if os.path.exists(text_path):
                    corrupted_text_path = os.path.join(corrupted_dir, text_filename)
                    shutil.move(text_path, corrupted_text_path)
                print(f"Moved corrupted image and text file: {filename}")


def list_corrupt_images(image_dir):
    corrupt_images = []

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            image_path = os.path.join(image_dir, filename)

            if is_corrupt(image_path):
                corrupt_images.append(filename)

    df = pd.DataFrame(corrupt_images, columns=["Corrupt Images"])
    print(df)

# Example usage:
# remove_corrupt_images("path/to/image/dir", "path/to/text/dir", "path/to/corrupted/dir")
list_corrupt_images(os.path.join(dataset_path_25k_images,"images"))
