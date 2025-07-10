import os
from PIL import Image


def check_and_move_images(main_folder_path):
    images_folder_path = os.path.join(main_folder_path, 'images')
    texts_folder_path = os.path.join(main_folder_path, 'texts')
    problematic_folder_path = os.path.join(main_folder_path, 'problematic')

    problematic_images_folder = os.path.join(problematic_folder_path, 'images')
    problematic_texts_folder = os.path.join(problematic_folder_path, 'texts')

    # Ensure the directories exist
    if not os.path.exists(problematic_images_folder):
        os.makedirs(problematic_images_folder)
    if not os.path.exists(problematic_texts_folder):
        os.makedirs(problematic_texts_folder)

    for filename in os.listdir(images_folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(images_folder_path, filename)
            text_filename = os.path.splitext(filename)[0] + '.txt'
            text_path = os.path.join(texts_folder_path, text_filename)

            try:
                # Try to open the image
                with Image.open(image_path) as img:
                    img.verify()
            except (IOError, SyntaxError) as e:
                # If it fails, move the image and text to the problematic folder
                print(f'Problematic file found: {image_path}')
                os.rename(image_path, os.path.join(problematic_images_folder, filename))

                if os.path.exists(text_path):
                    os.rename(text_path, os.path.join(problematic_texts_folder, text_filename))


if __name__ == '__main__':
    main_folder_path = "/home/cle-dl-05/Documents/38u.PdfOCR/2.Datasets/2.Training/3.New Dataset 39.645k"
    check_and_move_images(main_folder_path)
