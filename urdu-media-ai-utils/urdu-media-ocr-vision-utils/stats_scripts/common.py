import os
import re
import csv
import cv2
import xml.etree.ElementTree as ET
import glob as glob

# 'ARY News': [(351, 509)],
# '24 News': [(510, 690)],

channels = {
    'Geo News': [(32, 350), (691, 800)],
    'GNN News': [(1074, 1165), (1805, 1824)],
    '92 News': [(1166, 1255), (1825, 1854), (2077, 2086)],
    'Dunya News': [(1256, 1346), (1855, 1884), (2067, 2076)],
    'Dawn News': [(982, 1073), (1885, 2066)],
    # 'Lahore News': [(1715, 1804), (2107, 2126)],
    'Neo News': [(1621, 1711), (2087, 2106)],
    'Bol News': [(801, 890)],
}

channel_names = ['Geo News', 'GNN News', '92 News', 'Dunya News', \
                 'Dawn News', 'Neo News', 'Bol News'] # 'Lahore News'

def collect_all_images(dir_test):
    """
    Function to return a list of image paths.

    :param dir_test: Directory containing images or single image path.

    Returns:
        test_images: List containing all image paths.
    """
    test_images = []
    if os.path.isdir(dir_test):
        image_file_types = ['*.jpg', '*.jpeg', '*.png', '*.ppm']
        for file_type in image_file_types:
            test_images.extend(glob.glob(f"{dir_test}/{file_type}"))
    else:
        test_images.append(dir_test)
    return test_images

def get_target_boxes(xml_path):

    if os.path.exists(xml_path):

        # Initialize empty lists for boxes and labels
        boxes = []
        labels = []

        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Iterate over all object elements in the XML
        for obj in root.findall('object'):
            # Extract bounding box coordinates
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)

            # Extract label
            label = obj.find('name').text

            # Append bounding box and label to the lists
            boxes.append((xmin, ymin, xmax, ymax))
            labels.append(label)

    return boxes, labels

def calculate_iou(box1, box2):
    # Calculate intersection coordinates
    xmin_int = max(box1[0], box2[0])
    ymin_int = max(box1[1], box2[1])
    xmax_int = min(box1[2], box2[2])
    ymax_int = min(box1[3], box2[3])

    # Calculate intersection area
    intersection_area = max(0, xmax_int - xmin_int) * max(0, ymax_int - ymin_int)

    # Calculate union area
    area_box1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area_box2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = area_box1 + area_box2 - intersection_area

    # Calculate IoU
    iou = intersection_area / union_area if union_area > 0 else 0.0

    return iou

def draw_boxes_with_iou(image, pred_boxes, target_boxes, labels, ious, colors, threshold=0.85):


    for target_box, label in zip(target_boxes, labels):
        cv2.rectangle(image, (int(target_box[0]), int(target_box[1])),
                      (int(target_box[2]), int(target_box[3])), colors['target'], 5)
        # label_text = f"Ground Truth"
        # cv2.putText(image, label_text, (int(target_box[0]), int(target_box[1]) - 5),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors['target'], 4)

    for pred_box, iou in zip(pred_boxes, ious):
        if iou >= threshold:
            # Draw only if IoU is greater than or equal to 0.75
            cv2.rectangle(image, (int(pred_box[0]), int(pred_box[1])),
                          (int(pred_box[2]), int(pred_box[3])), colors['iou'], 2)
            # Display IoU score on the prediction
            iou_text = f"IoU: {iou:.2f}"
            cv2.putText(image, iou_text, (int(pred_box[0]), int(pred_box[1]) - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors['iou'], 3)
            # cv2.putText(image, 'Prediction', (int(pred_box[0]), int(pred_box[1]) - 3),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors['iou'], 5)

    return image

def extract_video_id(file_name):
    match = re.search(r'V(\d+)', file_name)
    if match:
        return int(match.group(1))
    return None

def find_channel(file_name, channels):
    video_id = extract_video_id(file_name)
    if video_id is not None:
        for channel, ranges in channels.items():
            for start, end in ranges:
                if start <= video_id <= end:
                    return channel
    return None

def classify_annotation(y_min, image_height):
    upper_threshold = 0.25 * image_height
    lower_threshold = 0.75 * image_height


    if y_min < upper_threshold:
        return 'above'
    elif y_min > lower_threshold:
        return 'low'
    else:
        return 'middle'

def get_image_height(image_path):
    # Assuming the image height is needed and the image file extension is '.jpg'
    if image_path.endswith('.jpg'):
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                return img.size[1]  # Index 1 corresponds to the height
        except Exception as e:
            print(f"Error reading image {image_path}: {e}")

    return 0  # Return 0 if image height cannot be obtained

def process_xml(file_path, channels, channel_counts, image_dir):
    tree = ET.parse(file_path)
    root = tree.getroot()

    channel = find_channel(file_path, channels)
    if channel is not None:
        channel_counts[channel]['total'] += 1

        image_file = os.path.splitext(os.path.basename(file_path))[0] + '.jpg'
        image_path = os.path.join(image_dir, image_file)
        image_height = get_image_height(image_path)

        for obj in root.iter('object'):
            bbox = obj.find('bndbox')
            ymin = int(bbox.find('ymin').text)
            ymax = int(bbox.find('ymax').text)

            annotation_height = ymax - ymin
            classification = classify_annotation(ymin, image_height)

            # Update the counts
            channel_counts[channel][classification] += 1

            # Update the top, middle, bottom counts
            if classification == 'above':
                channel_counts[channel]['top'] += 1
            elif classification == 'middle':
                channel_counts[channel]['middle'] += 1
            elif classification == 'low':
                channel_counts[channel]['bottom'] += 1

def count_files_in_channels(directory, channels, image_dir):
    channel_counts = {channel: {'low': 0, 'above': 0, 'middle': 0, 'top': 0, 'bottom': 0, 'total': 0} for channel in channels}
    unique_channels = set()  # Track unique channels

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Check if it's a file and not a directory
        if os.path.isfile(file_path) and file_name.endswith('.xml'):
            channel = find_channel(file_name, channels)
            if channel:
                unique_channels.add(channel)
                process_xml(file_path, channels, channel_counts, image_dir)

    # Calculate top, middle, bottom counts across all channels
    total_top = sum(counts['top'] for counts in channel_counts.values())
    total_middle = sum(counts['middle'] for counts in channel_counts.values())
    total_bottom = sum(counts['bottom'] for counts in channel_counts.values())

    return channel_counts, len(unique_channels), total_top, total_middle, total_bottom


def flatten_dict(d, parent_key='', sep='_'):
    """
    Flatten a nested dictionary by joining keys with the specified separator.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def create_csv(data, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        # Flatten the first item in data to get fieldnames
        flattened_data = flatten_dict(next(iter(data), {}))
        fieldnames = list(flattened_data.keys()) if flattened_data else []

        if fieldnames:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for item in data.values():
                flattened_item = flatten_dict(item)
                writer.writerow(flattened_item)
        else:
            print("Data is empty. No CSV file created.")
