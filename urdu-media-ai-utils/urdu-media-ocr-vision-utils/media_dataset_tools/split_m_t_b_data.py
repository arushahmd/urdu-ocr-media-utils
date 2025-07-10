import os
import pandas as pd
import numpy as np
import shutil
from collections import Counter
from FRCNN_PYTORCH_PIPELINE.ArooshScripts.common import channels
import random

# === Main Dataset Directory (Update these paths before use) ===

# Root directory where your full dataset is stored
MAIN_DIR = "path/to/your/main/dataset"

# Destination directory for organized or balanced dataset
DEST_DIR = "path/to/your/balanced_output_directory"    # e.g., for saving balanced dataset

TARGET_IMAGE_COUNT = 500

from sklearn.model_selection import train_test_split

def select_balanced_images(channel_stats):
    selected_images = []

    top = channel_stats['Top Images'].tolist()
    middle = channel_stats['Middle Images'].tolist()
    bottom = channel_stats['Bottom Images'].tolist()

    common_t_m_b = set(top).intersection(set(middle), set(bottom))

    # Select an equal number of images from each list
    min_count = min(len(top), len(middle), len(bottom))
    selected_images.extend(top[:min_count])
    selected_images.extend(middle[:min_count])
    selected_images.extend(bottom[:min_count])

    # Calculate the remaining count needed
    remaining_count = TARGET_IMAGE_COUNT - len(selected_images)

    # Fill the remaining count from middle and bottom
    common_m_b = set(middle).union(set(bottom))
    selected_images.extend(list(common_m_b)[:remaining_count])

    # Fill any remaining count with NaN
    selected_images.extend([np.nan] * max(0, remaining_count - len(selected_images)))

    # Remove NaN values
    selected_images = [img for img in selected_images if not pd.isna(img)]

    return selected_images[:TARGET_IMAGE_COUNT]

def select_balanced_images_split(channel_stats):
    selected_train_images = []
    selected_val_images = []
    selected_test_images = []

    top = channel_stats['Top Images'].tolist()
    middle = channel_stats['Middle Images'].tolist()
    bottom = channel_stats['Bottom Images'].tolist()

    # Calculate the index for splitting based on percentages
    top_split_index = int(len(top) * 0.8)
    middle_split_index = int(len(middle) * 0.8)
    bottom_split_index = int(len(bottom) * 0.8)

    # Split top images into train, test, and validation sets
    top_train = top[:top_split_index]
    top_val = top[top_split_index:int(len(top) * 0.9)]
    top_test = top[int(len(top) * 0.9):]

    # Split middle images into train, test, and validation sets
    middle_train = middle[:middle_split_index]
    middle_val = middle[middle_split_index:int(len(middle) * 0.9)]
    middle_test = middle[int(len(middle) * 0.9):]

    # Split bottom images into train, test, and validation sets
    bottom_train = bottom[:bottom_split_index]
    bottom_val = bottom[bottom_split_index:int(len(bottom) * 0.9)]
    bottom_test = bottom[int(len(bottom) * 0.9):]

    # Combine the sets for training, validation, and testing
    selected_train_images.extend(top_train)
    selected_train_images.extend(middle_train)
    selected_train_images.extend(bottom_train)

    selected_val_images.extend(top_val)
    selected_val_images.extend(middle_val)
    selected_val_images.extend(bottom_val)

    selected_test_images.extend(top_test)
    selected_test_images.extend(middle_test)
    selected_test_images.extend(bottom_test)

    return selected_train_images, selected_val_images, selected_test_images

def selected_images_all(channel_stats):
    selected_images = []
    top = channel_stats['Top Images'].tolist()
    middle = channel_stats['Middle Images'].tolist()
    bottom = channel_stats['Bottom Images'].tolist()

    common_t_m_b = set(top).intersection(set(middle), set(bottom))

    selected_images.extend(top)
    selected_images.extend(middle)
    selected_images.extend(bottom)

    return list(set(selected_images))

def main():
    for channel in channels:
        # Construct the CSV file path for each channel
        channel_file_path = os.path.join(MAIN_DIR, f"{channel}_image_stats.csv")
        if os.path.exists(channel_file_path):
            # Read the CSV file into a DataFrame
            channel_stats = pd.read_csv(channel_file_path)

            # Select a balanced set of unique images for the channel
            # selected_images = selected_images_all(channel_stats)
            selected_images = select_balanced_images(channel_stats)

            # train_images, val_images, test_images = select_balanced_images_split(channel_stats)


            channel_images_path = os.path.join(MAIN_DIR, channel, "images")
            channel_annots_path = os.path.join(MAIN_DIR, channel, "annotations_urdu")

            dst_images_path = os.path.join(DEST_DIR, "images")
            dst_annots_path = os.path.join(DEST_DIR, "annotations_urdu")

            # Copy the selected unique images to the destination directory
            for image_name in selected_images:
                xml_name = image_name[:-4] + ".xml"
                xml_path = os.path.join(channel_annots_path, xml_name)
                image_path = os.path.join(channel_images_path, image_name)

                dst_image_path = os.path.join(dst_images_path, image_name)
                dst_xml_path = os.path.join(dst_annots_path, xml_name)


                if os.path.exists(xml_path) and os.path.exists(image_path):
                    shutil.copy(xml_path, dst_xml_path)
                    shutil.copy(image_path, dst_image_path)




if __name__ == "__main__":
    main()
