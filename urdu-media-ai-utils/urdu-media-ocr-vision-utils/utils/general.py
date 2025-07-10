import csv
import os
import cv2
import numpy as np
import torch
import xml.etree.ElementTree as ET

from ArooshScripts.utils.common import calculate_iou
from ArooshScripts.utils.config import DEVICE
from models.create_fasterrcnn_model import create_model
from ArooshScripts.utils.transforms import infer_transforms, resize

def get_xml_stats(xml_path):
    """
    given a cml file path returns,
        - the boxes
        - their scores
        - labels
    Args:
        xml_path:
    """
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
def get_img_box_stats(img_path, xml_path, model):

    threshold = 0.8
    predictions = get_predictions(img_path, model)
    pred_boxes = predictions[0]['boxes']
    pred_scores = predictions[0]['scores']
    boxes, labels = get_xml_stats(xml_path)

    total_annot = len(boxes)
    total_pred = len(pred_boxes)
    stats = {
        "total_annotated_boxes": total_annot,
        "total_predicted_boxes": total_pred,
        "correct_preds": 0, # where iou is greater threshold
        "missing_preds": 0,
        "extra_preds": 0, # are they false positives ? No
    }

    for box in boxes:
        for pred in pred_boxes:
            iou = calculate_iou(box,pred)
            if iou > threshold:
                stats['correct_preds'] +=1

    correct_pred = stats['correct_preds']

    if total_pred > total_annot:
        stats['extra_preds'] = total_pred - total_annot
    elif total_pred < total_annot:
        stats['missing_preds'] = total_annot - total_pred

    return stats, predictions
def get_predictions(img_path, model):
    """
    Given an image path and model will return the predicted boxes
    Returns:
    """
    orig_image = cv2.imread(img_path)
    frame_height, frame_width, _ = orig_image.shape

    RESIZE_TO = frame_width

    # In our case square needs to be False by default
    image_resized = resize(
        orig_image, RESIZE_TO, square=False
    )
    image = image_resized.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = infer_transforms(image)
    image = torch.unsqueeze(image, 0)  # Add batch dimension.

    with torch.no_grad():
        predictions = model(image.to(DEVICE))

    return predictions
def load_weights_model(weights):
    """
    Given weights model path and model name returns a model
    Returns:
    """
    checkpoint = torch.load(weights, map_location=DEVICE)
    state_dict = checkpoint['model_state_dict']
    if any(key.startswith('module.') for key in state_dict.keys()):
        state_dict = {key.replace('module.', ''): value for key, value in state_dict.items()}

    NUM_CLASSES = checkpoint['data']['NC']
    CLASSES = checkpoint['data']['CLASSES']

    build_model = create_model[checkpoint['model_name']]
    model = build_model(num_classes=NUM_CLASSES, coco_model=False)
    model.load_state_dict(state_dict)
    model.to(DEVICE).eval()

    return model
def append_to_csv(csv_file, row):
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(row)
