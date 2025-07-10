import math
import os
import shutil

# from import channels, find_channel, classify_annotation, get_image_height, \
#     channel_names
import xml.etree.ElementTree as ET

from Scripts.Others.common import channels

# === Directory Paths (Update these with your actual dataset paths) ===

# Original dataset directories
IMAGES_DIR = "path/to/your/full_dataset/images"
ANNOT_DIR = "path/to/your/full_dataset/annotations"

# Train/Validation/Test image directories
TRAIN_IMAGES_DIR = "path/to/your/train/images"
VAL_IMAGES_DIR = "path/to/your/val/images"
TEST_IMAGES_DIR = "path/to/your/test/images"

# Train/Validation/Test annotation directories
TRAIN_ANNOT_DIR = "path/to/your/train/annotations"
VAL_ANNOT_DIR = "path/to/your/val/annotations"
TEST_ANNOT_DIR = "path/to/your/test/annotations"



def main():
    channels_data = {}

    Total_Images = len(os.listdir(IMAGES_DIR))
    total_annot = len(os.listdir(ANNOT_DIR))

    for xml_file in os.listdir(ANNOT_DIR):
        channel = (xml_file, channels)

        if channel not in channels_data.keys():
            channels_data[channel] = {}
            channels_data[channel]["top"] = []
            channels_data[channel]["middle"] = []
            channels_data[channel]["bottom"] = []

        img_file = xml_file[:-4] + ".jpg"
        xml_path = os.path.join(ANNOT_DIR, xml_file)
        img_path = os.path.join(IMAGES_DIR, img_file)

        is_image = os.path.exists(img_path)
        is_xml = os.path.exists(xml_path)

        if is_image:
            image_height = get_image_height(img_path)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            is_top = False
            is_middle = False

            for obj in root.iter('object'):
                bbox = obj.find('bndbox')
                ymin = int(bbox.find('ymin').text)
                ymax = int(bbox.find('ymax').text)

                classification = classify_annotation(ymin, image_height)

                if classification == 'above':
                    is_top = True
                elif classification == 'middle':
                    is_middle = True

            if is_top:
                channels_data[channel]['top'].append(img_file)
            elif is_middle:
                channels_data[channel]['middle'].append(img_file)
            else:
                channels_data[channel]['bottom'].append(img_file)

    for channel in channel_names:
        data = channels_data[channel]
        top = data['top']
        middle = data['middle']
        bottom = data['bottom']

        total_images = len(top) + len(middle) + len(bottom)

        total_val_test_images = math.floor(total_images * 0.1)

        top_10_perc = top[:math.floor(len(top) * 0.1)]
        middle_10_perc = middle[:math.floor(len(middle) * 0.1)]

        top_90 = top[math.floor(len(top) * 0.1):]
        middle_90 = middle[math.floor(len(middle) * 0.1):]

        total_20_perc = math.floor(total_images * 0.2)

        train_images = []
        test_images = []
        val_images = []

        val_images.extend(top_10_perc[:math.floor(len(top_10_perc) * 0.5)])
        test_images.extend(top_10_perc[math.floor(len(top_10_perc) * 0.5):])
        val_images.extend(middle_10_perc[:math.floor(len(middle_10_perc) * 0.5)])
        test_images.extend(middle_10_perc[math.floor(len(middle_10_perc) * 0.5):])

        train_images.extend(top_90)
        train_images.extend(middle_90)

        remaining_val  = total_val_test_images-len(val_images)
        remaining_test = total_val_test_images-len(test_images)

        rest_val_images = bottom[:remaining_val]
        rest_test_images = bottom[remaining_val:remaining_val+remaining_test]

        val_images.extend(rest_val_images)
        test_images.extend(rest_test_images)

        rest_train_images = bottom[remaining_val+remaining_test : ]

        train_images.extend(rest_train_images)

        for image_name in val_images:
            xml_filename = image_name[:-4]+".xml"
            image_path = os.path.join(IMAGES_DIR, image_name)
            xml_path = os.path.join(ANNOT_DIR, xml_filename)

            dest_img_path = os.path.join(VAL_IMAGES_DIR, image_name)
            dst_xml_path = os.path.join(VAL_ANNOT_DIR, xml_filename)

            if os.path.exists(image_path) and os.path.exists(xml_path):
                shutil.copy(image_path, dest_img_path)
                shutil.copy(xml_path, dst_xml_path)

        for image_name in train_images:
            xml_filename = image_name[:-4] + ".xml"
            image_path = os.path.join(IMAGES_DIR, image_name)
            xml_path = os.path.join(ANNOT_DIR, xml_filename)

            dest_img_path = os.path.join(TRAIN_IMAGES_DIR, image_name)
            dst_xml_path = os.path.join(TRAIN_ANNOT_DIR, xml_filename)

            if os.path.exists(image_path) and os.path.exists(xml_path):
                shutil.copy(image_path, dest_img_path)
                shutil.copy(xml_path, dst_xml_path)

        for image_name in test_images:
            xml_filename = image_name[:-4] + ".xml"
            image_path = os.path.join(IMAGES_DIR, image_name)
            xml_path = os.path.join(ANNOT_DIR, xml_filename)

            dest_img_path = os.path.join(TEST_IMAGES_DIR, image_name)
            dst_xml_path = os.path.join(TEST_ANNOT_DIR, xml_filename)

            if os.path.exists(image_path) and os.path.exists(xml_path):
                shutil.copy(image_path, dest_img_path)
                shutil.copy(xml_path, dst_xml_path)

if __name__ == "__main__":
    main()
