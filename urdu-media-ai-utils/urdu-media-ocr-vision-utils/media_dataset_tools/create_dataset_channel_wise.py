import os
import shutil

from FRCNN_PYTORCH_PIPELINE.ArooshScripts.common import channels, find_channel

MAIN_DATASET_DIR = "../Main_Dataset"
NEW_DATASET = "../NewDataset"

def main():
    dir_list = os.listdir(MAIN_DATASET_DIR)
    for dir in dir_list:
        dir_path = os.path.join(MAIN_DATASET_DIR, dir,"vott-json-export") # the directory with images
        channel = find_channel(dir, channels)
        channel_dir = os.path.join(NEW_DATASET, str(channel))
        images_dir = os.path.join(channel_dir, "images")
        annotation_dir = os.path.join(channel_dir, "annotations")
        if not os.path.exists(channel_dir):
            os.mkdir(channel_dir)
        if not os.path.exists(images_dir):
            os.mkdir(images_dir)
        if not os.path.exists(annotation_dir):
            os.mkdir(annotation_dir)
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if file_name.endswith('.jpg'):
                file_dst_path = os.path.join(images_dir, file_name)
                shutil.copy(file_path, file_dst_path)
            if file_name.endswith('.xml'):
                file_dst_path = os.path.join(annotation_dir, file_name)
                shutil.copy(file_path, file_dst_path)

if __name__ == "__main__":
    main()

