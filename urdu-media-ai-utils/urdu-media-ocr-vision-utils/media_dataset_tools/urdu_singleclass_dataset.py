import os
import xml.etree.ElementTree as ET
import shutil

def process_xml(xml_path, dest_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Check if there are 'Urdu' elements in the XML file
    urdu_elements = root.findall('.//object[name="Urdu"]')
    if urdu_elements:
        # Create a copy of the root element
        new_root = ET.Element(root.tag, attrib=root.attrib)

        # Copy the elements with name 'Urdu'
        for obj in urdu_elements:
            new_root.append(obj)

        # Save the modified XML to the destination directory
        dest_file = os.path.join(dest_path, os.path.basename(xml_path))
        new_tree = ET.ElementTree(new_root)
        new_tree.write(dest_file)

def process_directory(source_dir, dest_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate over XML files in the source directory
    for file in os.listdir(source_dir):
        if file.endswith('.xml'):
            xml_path = os.path.join(source_dir, file)
            process_xml(xml_path, dest_dir)

if __name__ == "__main__":

    DATASET_DIR = "../../new-dataset"

    for dir in os.listdir(DATASET_DIR):
        main_dir = os.path.join(DATASET_DIR, dir)
        src = os.path.join(main_dir, "annotations")
        dst = os.path.join(main_dir, "annotations_urdu")
        if dir != "AllData":
            process_directory(src,dst)



