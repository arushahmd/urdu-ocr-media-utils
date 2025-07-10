import os
import shutil


def move_paired_images_texts(images_folder, texts_folder, output_folder):
    """
    Moves paired images and text files to a new structured folder.

    :param images_folder: Path to the folder containing images.
    :param texts_folder: Path to the folder containing text files.
    :param output_folder: Path to the new folder where paired files will be moved.
    """
    # Create output subfolders
    output_images_folder = os.path.join(output_folder, "images")
    output_texts_folder = os.path.join(output_folder, "texts")
    os.makedirs(output_images_folder, exist_ok=True)
    os.makedirs(output_texts_folder, exist_ok=True)

    # Get sets of image and text file names (without extensions)
    image_names = {os.path.splitext(f)[0] for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))}
    text_names = {os.path.splitext(f)[0] for f in os.listdir(texts_folder) if f.lower().endswith('.txt')}

    # Find common pairs
    common_files = image_names & text_names

    # Move paired files
    for file_name in common_files:
        image_src = os.path.join(images_folder, file_name + ".jpg")  # Change extension if needed
        text_src = os.path.join(texts_folder, file_name + ".txt")

        image_dest = os.path.join(output_images_folder, file_name + ".jpg")
        text_dest = os.path.join(output_texts_folder, file_name + ".txt")

        if os.path.exists(image_src) and os.path.exists(text_src):
            shutil.move(image_src, image_dest)
            shutil.move(text_src, text_dest)
            print(f"Moved: {file_name}.jpg and {file_name}.txt")

    print("Pair moving completed.")


# Example usage
images_path = "phase-I-vott/all_images"
texts_path = "phase-I-vott/all_texts"
output_path = "phase-I-vott/yolo_training_ready_data"

move_paired_images_texts(images_path, texts_path, output_path)
