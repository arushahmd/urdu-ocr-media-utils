import os
import csv
import xml.etree.ElementTree as ET
from ArooshScripts.utils.common import channel_names, get_image_height, classify_annotation

MAIN_DIR = "new-dataset"

def main():
    channel_data = {}
    image_lists = {}

    for channel in channel_names:
        channel_dir = os.path.join(MAIN_DIR, channel)
        annotation_dir = os.path.join(channel_dir, "annotations_urdu")
        images_dir = os.path.join(channel_dir, "images")

        if os.path.exists(channel_dir):
            if channel not in channel_data.keys():
                channel_data[channel] = {'total_top_images': 0,
                                         'total_middle_images': 0,
                                         'total_bottom_images': 0,
                                         'total_images': 0
                                         }
                image_lists[channel] = {'top_images': [], 'middle_images': [], 'bottom_images': []}

            for xml_file in os.listdir(annotation_dir):
                img_file = xml_file[:-4] + ".jpg"
                xml_path = os.path.join(annotation_dir, xml_file)
                img_path = os.path.join(images_dir, img_file)

                is_image = os.path.exists(img_path)
                is_xml = os.path.exists(xml_path)

                if is_image:
                    image_height = get_image_height(img_path)
                    tree = ET.parse(xml_path)
                    root = tree.getroot()

                    channel_data[channel]['total_images'] += 1

                    for obj in root.iter('object'):
                        bbox = obj.find('bndbox')
                        ymin = int(bbox.find('ymin').text)
                        ymax = int(bbox.find('ymax').text)

                        annotation_height = ymax - ymin
                        classification = classify_annotation(ymin, image_height)

                        if classification == "above":
                            channel_data[channel]['total_top_images'] += 1
                            image_lists[channel]['top_images'].append(img_file)
                        elif classification == "low":
                            channel_data[channel]['total_bottom_images'] += 1
                            image_lists[channel]['bottom_images'].append(img_file)
                        elif classification == "middle":
                            channel_data[channel]['total_middle_images'] += 1
                            image_lists[channel]['middle_images'].append(img_file)

            channel_file_path = f"new-dataset/{channel}_image_stats.csv"
            header = ["Top Images", "Middle Images", "Bottom Images"]
            data = image_lists[channel]

            with open(channel_file_path, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)

                # Write header
                csv_writer.writerow(header)

                # Find the maximum number of items in any list
                max_items = max(len(data["top_images"]), len(data["middle_images"]), len(data["bottom_images"]))

                # Write rows
                for i in range(max_items):
                    row = [
                        data["top_images"][i] if i < len(data["top_images"]) else "",
                        data["middle_images"][i] if i < len(data["middle_images"]) else "",
                        data["bottom_images"][i] if i < len(data["bottom_images"]) else "",
                    ]
                    csv_writer.writerow(row)

    stats_file_path = "new-dataset/channel_image_count_stats.csv"
    stats_header = ["Channel Name", "Top Images", "Middle Images", "Bottom Images", "Total Images"]
    channel_stats = []


    for channel_name, stats in channel_data.items():
        row = [channel_name, stats["total_top_images"], stats["total_middle_images"], stats["total_bottom_images"], stats['total_images']]
        channel_stats.append(row)

    with open(stats_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write header
        csv_writer.writerow(stats_header)

        # Write rows
        csv_writer.writerows(channel_stats)







if __name__ == "__main__":
    main()
