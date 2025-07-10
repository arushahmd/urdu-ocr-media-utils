"""
Traverse a directory, process JSON annotation files, and convert them to YOLO format.
"""

import os
import json


def convert_vott_to_yolo(input_folder, output_folder):
    """
    Converts VoTT JSON annotations to YOLO format.

    :param input_folder: Path to the folder containing VoTT JSON files.
    :param output_folder: Path where YOLO annotations will be saved.
    """
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_folder, file_name)
            print(f"Processing file: {file_name}")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Check if "asset" and necessary keys exist
                if "asset" not in data or "name" not in data["asset"] or "size" not in data["asset"]:
                    print(f"Skipping {file_name} (missing 'asset' or 'size' key).")
                    continue

                # Get dynamic image width and height
                img_width = data["asset"]["size"]["width"]
                img_height = data["asset"]["size"]["height"]

                # Ensure valid width and height
                if img_width <= 0 or img_height <= 0:
                    print(f"Skipping {file_name} (invalid image dimensions).")
                    continue

                # Create YOLO annotation file
                image_name = data["asset"]["name"].replace(".jpg", ".txt")
                txt_output_path = os.path.join(output_folder, image_name)

                with open(txt_output_path, "w") as yolo_file:
                    for region in data.get("regions", []):
                        if "boundingBox" not in region:
                            print(f"Skipping region in {file_name} (missing 'boundingBox').")
                            continue  # Skip invalid bounding boxes

                        bbox = region["boundingBox"]
                        x_center = (bbox["left"] + bbox["width"] / 2) / img_width
                        y_center = (bbox["top"] + bbox["height"] / 2) / img_height
                        bbox_width = bbox["width"] / img_width
                        bbox_height = bbox["height"] / img_height

                        yolo_file.write(f"0 {x_center} {y_center} {bbox_width} {bbox_height}\n")

                print(f"Converted: {file_name} -> {image_name}")

            except json.JSONDecodeError:
                print(f"Skipping {file_name} (invalid JSON format).")
            except Exception as e:
                print(f"Error processing {file_name}: {e}. Skipping.")


input_json_folder = "/media/cle-nb-183/New Volume/Aroosh/1.Finals/1.Data/3. DiachronicFinalData/3.Annotated(phaseI-vott-annotated)/1.AllData/all_jsons"  # Change this to your actual JSON folder path
output_yolo_folder = "/media/cle-nb-183/New Volume/Aroosh/1.Finals/1.Data/3. DiachronicFinalData/3.Annotated(phaseI-vott-annotated)/1.AllData/yolo"  # Change this to your desired output folder

convert_vott_to_yolo(input_json_folder, output_yolo_folder)
