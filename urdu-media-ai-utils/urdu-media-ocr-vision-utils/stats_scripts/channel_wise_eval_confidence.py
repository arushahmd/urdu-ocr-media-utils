import csv
import os
import torch
import cv2
from ArooshScripts.utils.common import collect_all_images, find_channel, channels, get_target_boxes
from models.create_fasterrcnn_model import create_model
from utils.transforms import infer_transforms, resize

NUM_CLASSES = 2
DEVICE = 0
RESIZE_TO = None

def load_model(args):
    checkpoint = torch.load(args['weights'], map_location=args['device'])
    # Remove the "module." prefix from keys if it exists.
    state_dict = checkpoint['model_state_dict']
    if any(key.startswith('module.') for key in state_dict.keys()):
        state_dict = {key.replace('module.', ''): value for key, value in state_dict.items()}

    NUM_CLASSES = checkpoint['data']['NC']
    CLASSES = checkpoint['data']['CLASSES']

    build_model = create_model[str(args['model'])]
    model = build_model(num_classes=NUM_CLASSES, coco_model=False)
    model.load_state_dict(state_dict)

    model.to(DEVICE).eval()

    return model

def main(args):
    images = collect_all_images(args['image_dir'])

    # Dictionary to store channel-wise images
    channel_images_dict = {channel: [] for channel in channels}
    # Dictionary to store channel-wise 6. statistics
    channel_stats = {
        channel: {'total_images': 0, 'total_annotations': 0, 'total_predicted_boxes': 0}
        for channel in channels
    }

    model = load_model(args)

    for image_path in images:
        image_name = image_path.split("/")[-1]
        channel = find_channel(image_name, channels)

        # Check if the channel is in the predefined channels list
        if channel in channels:
            channel_images_dict[channel].append(image_path)

            # Perform inference
            orig_image = cv2.imread(image_path)
            frame_height, frame_width, _ = orig_image.shape
            if args['imgsz'] is not None:
                RESIZE_TO = args['imgsz']
            else:
                RESIZE_TO = frame_width
            image_resized = resize(orig_image, RESIZE_TO, square=args['square_img'])
            image = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
            image = infer_transforms(image)
            image = torch.unsqueeze(image, 0)

            with torch.no_grad():
                outputs = model(image.to(args['device']))

            pred_boxes = outputs[0]['boxes'].cpu().numpy()
            pred_scores = outputs[0]['scores'].cpu().numpy()

            # Construct XML file name by replacing the image extension with '.xml'
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            xml_name = image_name + '.xml'

            # Construct the full path to the XML file
            xml_path = os.path.join(args['annotation_dir'], xml_name)

            if os.path.exists(xml_path):
                # Get target boxes and labels
                target_boxes, _ = get_target_boxes(xml_path)

                # Update 6. statistics based on confidence scores
                channel_stats[channel]['total_images'] += 1
                channel_stats[channel]['total_annotations'] += len(target_boxes)
                channel_stats[channel]['total_predicted_boxes'] += len(pred_boxes)

    # Create and save CSV file
    csv_filename = '../6. statistics/channel_statistics.csv'
    csv_filepath = os.path.join(args['save_dir'], csv_filename)

    # Clear the CSV file if it already exists
    if os.path.exists(csv_filepath):
        os.remove(csv_filepath)

    # Open the CSV file for writing data
    with open(csv_filepath, 'w', newline='') as csvfile:
        fieldnames = ['Channel', 'Total_Images', 'Total_Annotations', 'Total_Predicted_Boxes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        for channel, stats in channel_stats.items():
            writer.writerow({
                'Channel': channel,
                'Total_Images': stats['total_images'],
                'Total_Annotations': stats['total_annotations'],
                'Total_Predicted_Boxes': stats['total_predicted_boxes']
            })

if __name__ == "__main__":
    args = {
        'image_dir': '../data/headlinedataset/test/images',
        'annotation_dir': '../data/headlinedataset/test/annotations_urdu',
        'config': '../data_configs/urdu_test.yaml',
        'model': 'fasterrcnn_resnet50_fpn_v2',
        'save_dir': '/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/FRCNN_PYTORCH_PIPELINE/ArooshScripts',
        'weights': '../outputs/training/urdu_text_exp1/last_model_state.pth',
        'confidence_threshold': 80,  # Set your confidence threshold here
        'iou_threshold': 0.5,  # Set your IoU threshold here
        'imgsz': None,
        'device': 'cuda:0',
        'square_img': False,
    }

    main(args)
