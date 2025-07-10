import os

import cv2
import numpy as np

from ArooshScripts.utils.common import collect_all_files, combine_paths, get_target_boxes, draw_boxes_with_iou, \
    calculate_iou, channels, channel_names, find_channel
from ArooshScripts.utils.config import CLASSES
from ArooshScripts.utils.general import get_img_box_stats, load_weights_model, append_to_csv, get_predictions
from ArooshScripts.utils.annotations import inference_annotations, convert_detections


def infer_images_with_stats(img_dir, annot_dir, weights_path, img_save_dir, get_stats = False, save_images = False):
    images = collect_all_files(img_dir,["*.jpg"])

    header_written = False
    with open(os.path.join(img_save_dir, "results.csv"), 'w', newline='') as csv_file:
        for img_name in images:
            image_path = combine_paths(img_dir, img_name)
            xml_name = img_name[:-4] + ".xml"
            xml_path = combine_paths(annot_dir, xml_name)

            if os.path.exists(image_path) and os.path.exists(xml_path):
                model = load_weights_model(weights_path)

                image_stats, predictions = get_img_box_stats(image_path, xml_path, model)

                t = image_stats['total_annotated_boxes']
                p = image_stats['total_predicted_boxes']
                c = image_stats['correct_preds']
                m = image_stats['missing_preds']
                e = image_stats['extra_preds']

                image_name = img_name[:-4] + str(f"_t{t}_p{p}_c{c}_m{m}_e{e}") + ".jpg"


                channel_list = channels
                channel_dict = {channel: {
                    'total_annotated_boxes':0,
                    'total_predicted_boxes':0,
                    'correct_preds':0,
                    'missing_preds':0,
                    'extra_preds':0
                } for channel in channel_names}

                if get_stats:
                    if not header_written:
                        header = list(image_stats.keys())
                        header.insert(0, "Channel Name")
                        append_to_csv(csv_file, header)
                        header_written = True

                channel_name = find_channel(img_name, channels)

                channel_dict[channel_name]['total_annotated_boxes'] += t
                channel_dict[channel_name]['total_predicted_boxes'] += p
                channel_dict[channel_name]['correct_preds'] += m
                channel_dict[channel_name]['missing_preds'] += c
                channel_dict[channel_name]['extra_preds'] += e

                if save_images:
                    predictions = get_predictions(image_path, model)
                    pred_boxes = predictions[0]['boxes'].cpu().numpy()
                    pred_labels = predictions[0]['labels'].cpu().numpy()

                    image = cv2.imread(image_path)
                    target_boxes, _ = get_target_boxes(xml_path)

                    box_ious = []

                    COLORS = {'pred': (255, 145, 0), 'conf' :(170, 59, 255),'target': (0, 0, 0), 'iou': (255, 145, 0)}  # Adjusted colors

                    if len(pred_boxes) != 0:
                        for box in pred_boxes:
                            box_ious.append(max(list([calculate_iou(box, target_box) for target_box in target_boxes])))

                    image_predicted = draw_boxes_with_iou(image, pred_boxes,target_boxes,pred_labels, box_ious, predictions, COLORS, threshold=0.7 )
                    # cv2.imshow("Image", image_predicted)
                    # cv2.waitKey(0)

                    cv2.imwrite(
                            combine_paths(img_save_dir, image_name),
                            image_predicted)
                    # cv2.destroyAllWindows()


if __name__ == "__main__":
    # TODO: move these all variables to config file and read using config class object
    image_path = "/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/FRCNN_PYTORCH_PIPELINE/data/headlinedataset/script_test"
    xml_path = "/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/FRCNN_PYTORCH_PIPELINE/data/headlinedataset/script_test"

    images_dir = "/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/FRCNN_PYTORCH_PIPELINE/ArooshScripts/Comparative_testing_all/images"
    annotation_dir = "/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/FRCNN_PYTORCH_PIPELINE/ArooshScripts/Comparative_testing_all/images"
    weights_path = "/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/FRCNN_PYTORCH_PIPELINE/outputs/training/urdu_text_balanced/best_model.pth"
    img_save_dir = "/home/cle-dl-05/Desktop/ArooshWork/FRCNN_PYTORCH/FRCNN_PYTORCH_PIPELINE/ArooshScripts/Comparative_testing_all/exp3"
    # csv_path = combine_paths(img_save_dir, "urdu_bal_75_stats_exp1_T.csv")

    infer_images_with_stats(images_dir, annotation_dir, weights_path, img_save_dir, get_stats=False, save_images=True)

    print("Done")

    # row = list(image_stats.values())
    # row.insert(0, str(image_name))
    # append_to_csv(csv_file, row)

