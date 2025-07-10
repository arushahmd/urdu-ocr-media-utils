import os
import random
import shutil

def copy_all_data(base_path,dst_path):
    """
    :param base_path: the path of the base directory containing sub folders for images
    :param dst_path: the destination directory where the files to be copied
    :return: copies files from sub directories to a single directory
    """
    dir_list = os.listdir(base_path)

    for dir_name in dir_list:
        dir_path = os.path.join(base_path, dir_name)
        sub_dirs = os.listdir(dir_path)

        for sub_dir in sub_dirs:
            sub_dir_path = os.path.join(dir_path, sub_dir)

            # Check if sub_dir_path is a directory
            if os.path.isdir(sub_dir_path):
                jpegs = [f for f in os.listdir(sub_dir_path) if f.endswith(".jpg")]
                xmls = [f for f in os.listdir(sub_dir_path) if f.endswith(".xml")]

                for jpg in jpegs:
                    src =  os.path.join(sub_dir_path,jpg)
                    dst =  os.path.join(dst_path,jpg)
                    if not os.path.exists(dst):
                        shutil.copy(src,dst)

                for xml in xmls:
                    src =  os.path.join(sub_dir_path,xml)
                    dst = os.path.join(dst_path, xml)
                    if not os.path.exists(dst):
                        shutil.copy(src, dst)

def create_dataset(base_path, train_pth, test_pth):
    jpegs = [f for f in os.listdir(base_path)  if f.endswith(".jpg")]
    sample_data = random.sample(jpegs,2000)
    train_samples_count = (len(sample_data) * 80) / 100
    for i, jpg_name in enumerate(sample_data):
        xml_name = jpg_name[:-4]+".xml"
        jpg_src_path = os.path.join(base_path, jpg_name)
        xml_src_path = os.path.join(base_path, xml_name)
        if i < train_samples_count:
            jpg_dst_path = os.path.join(train_pth, jpg_name)
            xml_dst_path = os.path.join(train_pth, xml_name)
        else:
            jpg_dst_path = os.path.join(test_pth, jpg_name)
            xml_dst_path = os.path.join(test_pth, xml_name)
        if os.path.exists(jpg_src_path) and os.path.exists(xml_src_path):
            if not os.path.exists(jpg_dst_path) and not os.path.exists(xml_dst_path):
                shutil.copy(jpg_src_path, jpg_dst_path)
                shutil.copy(xml_src_path, xml_dst_path)

if __name__ == "__main__":

    # paths for the directory with all data
    base_path = "ocr-data"
    train_pth = "/train"
    test_pth = "/headlinedataset/test"

    create_dataset(base_path, train_pth, test_pth)
