import os
import shutil

def create_dataset_structure(directory):

    image_dir = os.path.join(directory,"images")
    annotations_dir = os.path.join(directory,"annotations")

    if not os.path.exists(image_dir):
        os.mkdir(image_dir)

    if not os.path.exists(annotations_dir):
        os.mkdir(annotations_dir)

    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            file_path = os.path.join(directory, filename)
            dst_path = os.path.join(image_dir, filename)
            shutil.copy(file_path, dst_path)

    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory, filename)
            dst_path = os.path.join(annotations_dir, filename)
            shutil.copy(file_path, dst_path)

if __name__ == "__main__":
    train_dir = "data/train"
    test_dir = "data/test"

    # create_dataset_structure(train_dir)
    create_dataset_structure(test_dir)
