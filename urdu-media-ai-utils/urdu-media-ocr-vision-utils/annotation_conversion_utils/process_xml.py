import os




def process_directory(directory):
    """
        Delete those jpgs and their xml which donot have any bounding box
    """
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(directory, filename)
            if not has_object_tag(xml_file_path):
                jpeg_file_name = filename[:-4]+".jpg"
                jpeg_file_path = os.path.join(directory, jpeg_file_name)
                print(f"Deleting {xml_file_path}")
                print(f"Deleting {jpeg_file_path}")
                os.remove(xml_file_path)
                os.remove(jpeg_file_path)

def process_jpegs(directory):
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            xml_file = filename[:-4]+".xml"
            xml_path = os.path.join(directory,xml_file)
            jpg_path = os.path.join(directory,filename)
            if (xml_file[:-4] == filename[:-4]):
                if not os.path.exists(jpg_path) or not os.path.exists(xml_path):
                    if os.path.exists(jpg_path):
                        os.remove(jpg_path)
                    if os.path.exists(xml_path):
                        os.remove(xml_path)

                    count += 1
        print(f"Files Deleted {count}")


if __name__ == "__main__":
    # Specify the directory path
    # trolls_directory = "/home/cle-dl-05/Desktop/Aroosh Work/headlinedataset/train"
    trolls_directory = "/home/cle-dl-05/Desktop/Aroosh Work/headlinedataset/test"

    # Process the directory
    # process_directory(trolls_directory)

    # 
    process_jpegs(trolls_directory)


