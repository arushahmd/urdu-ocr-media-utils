import json
import os
from xml.etree.ElementTree import Element, SubElement, ElementTree

def create_pascal_voc_xml(file_name, image_width, image_height, regions):
    """
    :param file_name: name of the image file in the vott file
    :param image_width: width of the image
    :param image_height: heigght of the image
    :param regions: the regions for the bounding boxes
    :return: a single xml file , annotated in coco format

    Makes a single xml file from the vott given the file name, in the vott annotated json file
    """
    root = Element("annotation")

    folder = SubElement(root, "folder")
    folder.text = "images"

    filename = SubElement(root, "filename")
    filename.text = file_name

    size = SubElement(root, "size")
    width = SubElement(size, "width")
    width.text = str(image_width)

    height = SubElement(size, "height")
    height.text = str(image_height)

    for region in regions:
        object_elem = SubElement(root, "object")
        name = SubElement(object_elem, "name")
        name.text = region["tags"][0]

        if name.text not in ('L', 'He', 'H'):
            name.text = "Urdu"

        bndbox = SubElement(object_elem, "bndbox")
        xmin = SubElement(bndbox, "xmin")
        xmin.text = str(int(region["boundingBox"]["left"]))

        ymin = SubElement(bndbox, "ymin")
        ymin.text = str(int(region["boundingBox"]["top"]))

        xmax = SubElement(bndbox, "xmax")
        xmax.text = str(int(region["boundingBox"]["left"] + region["boundingBox"]["width"]))

        ymax = SubElement(bndbox, "ymax")
        ymax.text = str(int(region["boundingBox"]["top"] + region["boundingBox"]["height"]))

    tree = ElementTree(root)
    return tree

def convert_vott_to_xml(base_path):
    """
    :param base_path: base path of the main json file ( vott annotations )
    :return: None

    This function takes the base path, then troll the subdirectories, and creates
    the xml file for each image, reading it's annotation from the main json file.
    """
    dirs = os.listdir(base_path)

    for dir in dirs:
        dir_path = os.path.join(base_path, dir)

        if os.path.isdir(dir_path):
            sub_dirs = os.listdir(dir_path)

            for sub_dir in sub_dirs:
                sub_dir_path = os.path.join(dir_path,sub_dir)
                if os.path.isdir(sub_dir_path):
                    json_files = [f for f in os.listdir(sub_dir_path) if f.endswith(".json")]

                    for json_file in json_files:
                        json_file_path = os.path.join(sub_dir_path, json_file)
                        with open(json_file_path, encoding='utf-8-sig') as file:
                            data = json.load(file)
                            assets = data["assets"]

                            for asset_id in assets:
                                asset_obj = assets[asset_id]
                                asset = asset_obj['asset']
                                file_name = asset["name"]
                                image_width = asset["size"]["width"]
                                image_height = asset["size"]["height"]
                                regions = asset_obj["regions"]

                                tree = create_pascal_voc_xml(file_name, image_width, image_height, regions)

                                # Save the XML file
                                xml_file_path = os.path.join(sub_dir_path, f'{os.path.splitext(file_name)[0]}.xml')
                                tree.write(xml_file_path)

def delete_file(dir_path, ext):
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):
            if file.endswith(ext):
                file_path = os.path.join(dir_path, file)
                os.remove(file_path)

def delete_xml(base_path):
    """
    :param base_path: the path where the xml files are present
    :return: None

    Deletes all the xml files from the base_path directory, and sub-directories.
    """
    dirs = os.listdir(base_path)

    for dir in dirs:
        dir_path = os.path.join(base_path, dir)
        delete_file(dir_path, ".xml")


if __name__ == "__main__":
    base_path = "dataset"
    convert_vott_to_xml(base_path)
    # delete_xml(base_path)