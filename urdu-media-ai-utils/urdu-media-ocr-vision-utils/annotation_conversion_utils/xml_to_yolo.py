import os
import xml.etree.ElementTree as ET
import cv2  # Make sure to install OpenCV: pip install opencv-python

def xml_to_yolo(xml_path, dest_txt_dir, image_dir):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    image_filename = os.path.splitext(os.path.basename(xml_path))[0]  # Get the image filename without extension
    dest_txt_path = os.path.join(dest_txt_dir, f"{image_filename}.txt")

    # Generate the image path by replacing the extension
    image_path = os.path.join(image_dir, f"{image_filename}.jpg")  # Assuming images are in JPG format

    # Read the image to get its dimensions
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    with open(dest_txt_path, "w") as txt_file:
        for object_elem in root.findall("object"):
            name_elem = object_elem.find("name")
            if name_elem is not None and name_elem.text == "Urdu":
                bndbox_elem = object_elem.find("bndbox")

                xmin = int(bndbox_elem.find("xmin").text)
                ymin = int(bndbox_elem.find("ymin").text)
                xmax = int(bndbox_elem.find("xmax").text)
                ymax = int(bndbox_elem.find("ymax").text)

                # Calculate normalized coordinates
                x_center = (xmin + xmax) / (2.0 * width)
                y_center = (ymin + ymax) / (2.0 * height)
                box_width = (xmax - xmin) / width
                box_height = (ymax - ymin) / height

                # Write YOLO format to the text file
                txt_file.write(f"0 {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

# Replace 'source_xml_dir', 'dest_txt_dir', and 'image_dir' with your actual directories
source_xml_dir = "/Datasets/MAINTESTDATA/annotations"
dest_txt_dir = "/Datasets/MAINTESTDATA/labels"
image_dir = "/Datasets/MAINTESTDATA/images"

# Ensure the destination directory exists
os.makedirs(dest_txt_dir, exist_ok=True)

# Process each XML file in the source directory
files = os.listdir(source_xml_dir)
for i, xml_filename in enumerate(files):
    if xml_filename.endswith(".xml"):
        print(f" {i}/{len(files)} Working on {xml_filename}")
        xml_path = os.path.join(source_xml_dir, xml_filename)
        xml_to_yolo(xml_path, dest_txt_dir, image_dir)
