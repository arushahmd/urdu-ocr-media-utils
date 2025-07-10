import os

from ArooshScripts.utils.common import collect_all_images, find_channel, channels, get_target_boxes, calculate_iou
from models.create_fasterrcnn_model import create_model
from utils.transforms import infer_transforms, resize
import torch
import cv2

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
    channel_stats = {channel: {'iou_sum': 0, 'target_boxes': 0, 'above_threshold': 0} for channel in channels}

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

            # Construct XML file name by replacing the image extension with '.xml'
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            xml_name = image_name + '.xml'

            # Construct the full path to the XML file
            xml_path = os.path.join(args['annotation_dir'], xml_name)

            if os.path.exists(xml_path):
                # Get target boxes and labels
                target_boxes, _ = get_target_boxes(xml_path)

                # Calculate IoU and update 6. statistics
                for pred_box in pred_boxes:
                    iou_values = [calculate_iou(pred_box, target_box) for target_box in target_boxes]
                    max_iou = max(iou_values, default=0.0)
                    channel_stats[channel]['iou_sum'] += max_iou
                    channel_stats[channel]['target_boxes'] += len(target_boxes)
                    if max_iou >= args['threshold']:
                        channel_stats[channel]['above_threshold'] += 1

    print(f"CHANNEL \t\t\t IMAGES \t\t  AVG_IoU  \t\t PREDICTED_BOXES")

    # Print or use the channel-wise image lists and 6. statistics as needed
    for channel, images_list in channel_images_dict.items():
        avg_iou = channel_stats[channel]['iou_sum'] / len(images_list) if len(images_list) > 0 else 0.0

        print(f"{channel} \t\t {len(images_list)} \t\t {avg_iou:.4f} \t\t "
              f"\t\t {channel_stats[channel]['above_threshold']}")

if __name__ == "__main__":
    args = {
        'image_dir': 'balanced-image-data/train/images',
        'annotation_dir': 'balanced-image-data/train/annotations_urdu',
        'config': '../data_configs/urdu_test.yaml',
        'model': 'fasterrcnn_resnet50_fpn_v2',
        'save_dir': '../data/headlinedataset/inference/urdu_txt_exp1',
        'weights': '../outputs/training/urdu_text_exp1/last_model_state.pth',
        'threshold': 0.7,
        'imgsz': None,
        'device': 'cuda:0',
        'square_img': False,
    }

    main(args)
