"""
This script is designed to distribute image and text files into specified directories based on certain criteria.
It can also check for duplicate files across these directories.

In short create buckets of images and texts and place them in the specified folder,
Folders are named as,
    - distribution 1, distribution 2, ... , distribution n.


The main functionalities include:
1. Distributing images and corresponding text files into a specified number of directories, ensuring that the width of the images exceeds a minimum value.
2. Creating the necessary directory structure for the distributions.
3. Checking for duplicate files across the distribution directories.

Functions:
- get_image_width(image_path): Returns the width of the given image.
- create_dir_structure(base_path, distribution_count): Creates the required directory structure for the distributions.
- distribute_files(src_image_folder, src_txt_folder, base_dest_dir, distribution_count, min_width): Distributes image and text files into the specified number of directories.
- check_duplicates(base_dest_dir, distribution_count): Checks for duplicate files across the distribution directories.
- main(main_folder, distribution_count, min_width, check_dist): The main function to either distribute files or check for duplicates.

Example usage:
- To distribute files: Set check_dist to False.
- To check for duplicates: Set check_dist to True.
"""


import os
import shutil
import random
import cv2
from collections import defaultdict

def get_image_width(image_path):
    """
    Given the path to an image file, returns the width of the image.

    Args:
        image_path (str): Path to the image file.

    Returns:
        int: Width of the image in pixels.
    """
    image = cv2.imread(image_path)
    if image is not None:
        height, width, channels = image.shape
        return width
    else:
        raise FileNotFoundError(f"Image not found: {image_path}")

def create_dir_structure(base_path, distribution_count):
    """
    Creates the directory structure for distributions.
    """
    for i in range(1, distribution_count + 1):
        dist_dir = os.path.join(base_path, f'distribution{i}')
        images_dir = os.path.join(dist_dir, 'images')
        texts_dir = os.path.join(dist_dir, 'texts')
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(texts_dir, exist_ok=True)

def distribute_files(src_image_folder, src_txt_folder, base_dest_dir, distribution_count=4, min_width=100):
    """
    Distributes images and texts into the specified number of parts.
    """
    # Get list of image files
    image_files = [f for f in os.listdir(src_image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(image_files)  # Shuffle the files to ensure random distribution

    total_files = len(image_files)
    files_per_distribution = total_files // distribution_count
    remaining_files = total_files % distribution_count

    create_dir_structure(base_dest_dir, distribution_count)

    # Distribute files across distributions
    current_index = 0
    for i in range(distribution_count):
        dist_dir = os.path.join(base_dest_dir, f'distribution{i+1}')
        images_dir = os.path.join(dist_dir, 'images')
        texts_dir = os.path.join(dist_dir, 'texts')

        if remaining_files > 0:
            num_files = files_per_distribution + 1
            remaining_files -= 1
        else:
            num_files = files_per_distribution

        for _ in range(num_files):
            if current_index < total_files:
                filename = image_files[current_index]
                current_index += 1
                try:
                    src_image_path = os.path.join(src_image_folder, filename)
                    image_width = get_image_width(src_image_path)

                    if image_width > min_width:
                        # Copy the image to the destination folder
                        dest_image_path = os.path.join(images_dir, filename)
                        shutil.copyfile(src_image_path, dest_image_path)

                        # Copy corresponding text file from src_txt_folder to dest_txt_folder
                        txt_filename = os.path.splitext(filename)[0] + ".txt"
                        src_txt_path = os.path.join(src_txt_folder, txt_filename)
                        if os.path.exists(src_txt_path):
                            dest_txt_path = os.path.join(texts_dir, txt_filename)
                            shutil.copyfile(src_txt_path, dest_txt_path)
                            print(f"Copied {filename} and {txt_filename} to distribution{i+1}")

                except Exception as e:
                    print(f"Error processing {filename}: {e}")

def check_duplicates(base_dest_dir, distribution_count):
    """
    Checks for duplicate files across distributions.
    """
    file_locations = defaultdict(list)

    # Iterate through each distribution to collect file paths
    for i in range(1, distribution_count + 1):
        images_dir = os.path.join(base_dest_dir, f'distribution{i}', 'images')
        for filename in os.listdir(images_dir):
            file_locations[filename].append(f'distribution{i}')

    # Find and print files that exist in more than one distribution
    duplicates = {filename: locations for filename, locations in file_locations.items() if len(locations) > 1}

    if duplicates:
        print("Duplicate files found:")
        for filename, locations in duplicates.items():
            print(f"{filename} found in {', '.join(locations)}")
    else:
        print("No duplicate files found.")

# Main function to either distribute files or check for duplicates
def main(main_folder, distribution_count=4, min_width=100, check_dist=False):
    src_image_folder = os.path.join(main_folder, 'images')
    src_txt_folder = os.path.join(main_folder, 'texts')
    base_dest_dir = os.path.join(main_folder, 'distributions')

    if check_dist:
        check_duplicates(base_dest_dir, distribution_count)
    else:
        distribute_files(src_image_folder, src_txt_folder, base_dest_dir, distribution_count, min_width)

# Example usage
main_folder = '../new-dataset'
distribution_count = 4
min_width = 100
check_dist = True  # Set to True to check for duplicates

main(main_folder, distribution_count, min_width, check_dist)
