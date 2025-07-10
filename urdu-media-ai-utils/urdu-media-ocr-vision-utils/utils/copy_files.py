import os
import shutil


def copy_files(source_folder, destination_folder):
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # List all files in the source folder
    files = os.listdir(source_folder)

    # Copy each file to the destination folder
    for file_name in files:
        full_file_name = os.path.join(source_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, destination_folder)
            print(f"Copied: {full_file_name} to {destination_folder}")


def move_to_misc(image_folder, text_folder):
    # Create 'misc' folder in the root directory of images and text folders
    root_folder = os.path.commonpath([image_folder, text_folder])
    misc_folder = os.path.join(root_folder, 'misc')


    if not os.path.exists(misc_folder):
        os.makedirs(misc_folder)

    # Get lists of image and text file names without extensions
    image_files = {os.path.splitext(file)[0] for file in os.listdir(image_folder) if file.endswith('.jpg')}
    text_files = {os.path.splitext(file)[0] for file in os.listdir(text_folder) if file.endswith('.txt')}

    # Find mismatched files
    mismatched_images = image_files - text_files
    mismatched_texts = text_files - image_files

    total_misc_imgs = len(mismatched_images)
    total_misc_txts = len(mismatched_texts)

    # Move mismatched images to 'misc' folder
    for image in mismatched_images:
        image_path = os.path.join(image_folder, image + '.jpg')
        shutil.move(image_path, misc_folder)
        print(f"Moved image: {image_path} to {misc_folder}")

    # Move mismatched texts to 'misc' folder
    for text in mismatched_texts:
        text_path = os.path.join(text_folder, text + '.txt')
        shutil.move(text_path, misc_folder)
        print(f"Moved text: {text_path} to {misc_folder}")

    print(f"Total Misc Images : {total_misc_imgs}")
    print(f"Total Misc Texts : {total_misc_txts}")


if __name__ == "__main__":

    copy_files = False
    remove_misc = True

    if copy_files:

        source_img_folders = [
            "/media/cle-nb-183/New Volume/Pdf Dataset/Hira_Correct/correct_data/images",
            "/media/cle-nb-183/New Volume/Pdf Dataset/Iqra_correct/Images",
            "/media/cle-nb-183/New Volume/Pdf Dataset/Javeria_Correct/correct images",
            "/media/cle-nb-183/New Volume/Pdf Dataset/Abiha_correct data(5 july final verfication)/distribution3/correct_data/images"
        ]

        source_txt_folders = [
            "/media/cle-nb-183/New Volume/Pdf Dataset/Hira_Correct/correct_data/texts",
            "/media/cle-nb-183/New Volume/Pdf Dataset/Iqra_correct/texts",
            "/media/cle-nb-183/New Volume/Pdf Dataset/Javeria_Correct/correct texts",
            "/media/cle-nb-183/New Volume/Pdf Dataset/Abiha_correct data(5 july final verfication)/distribution3/correct_data/texts"
        ]

        dest_img_folder = "/media/cle-nb-183/New Volume/Pdf Dataset/Verified Data/images"
        dest_txt_folder = "/media/cle-nb-183/New Volume/Pdf Dataset/Verified Data/texts"

        for img_folder in source_img_folders:
            copy_files(img_folder, dest_img_folder)

        for txt_folder in source_txt_folders:
            copy_files(txt_folder, dest_txt_folder)

    if remove_misc:
        img_folder = "/media/cle-nb-183/New Volume/Pdf Dataset/Verified Data/images"
        txt_folder = "/media/cle-nb-183/New Volume/Pdf Dataset/Verified Data/texts"
        move_to_misc(img_folder, txt_folder)


