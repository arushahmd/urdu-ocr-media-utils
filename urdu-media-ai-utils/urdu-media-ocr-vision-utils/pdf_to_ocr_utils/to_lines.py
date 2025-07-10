import os
import cv2
import numpy as np
from PIL import Image

from image_utils import image_contours, preprocess_image_for_line_separation


def validate_file_path(file_path, valid_extensions):
    """
    Validate if the file path is valid and if the file has one of the allowed extensions.

    Args:
        file_path (str): Path of the file to validate.
        valid_extensions (tuple): Allowed file extensions (e.g., ('.pdf', '.PDF')).

    Returns:
        bool: True if the file path is valid and has the correct extension, False otherwise.
    """
    return os.path.isfile(file_path) and file_path.lower().endswith(valid_extensions)


def page_to_lines(img_or_pth, save=False, file_name=None):
    """
    Extract line images from the original image based on contours.
    Filters out lines based on minimum height criteria.

    Args:
        img_or_pth (str or np.ndarray or PIL.Image): Path to the image file or image data.
        save (bool): Whether to save the extracted line images to individual files.

    Returns:
        list: A list of line images extracted from the page image.
    """

    book_name = None

    # Load the image
    if isinstance(img_or_pth, str):
        if not validate_file_path(img_or_pth, ('.jpg', '.JPG', '.png', '.bmp', '.tiff')):
            print(f"Error: {img_or_pth} is not a valid Image file.")
            return None

        if os.path.isfile(img_or_pth):
            page_img = cv2.imread(img_or_pth)
            new_image = preprocess_image_for_line_separation(page_img)
            cv2.imshow("img", new_image)
            cv2.waitKey(3000)
            if save:
                book_name = os.path.basename(img_or_pth).split("_")[0]
                file_name = os.path.basename(img_or_pth).replace(".jpg", "").replace(".JPG", "").replace(".png",
                                                                                                         "").replace(
                    ".bmp", "").replace(".tiff", "")
        else:
            raise FileNotFoundError(f"The file path {img_or_pth} does not exist.")

    elif isinstance(img_or_pth, np.ndarray):
        page_img = img_or_pth
        if file_name is not None:
            # below only happens if the img_or_pth is image type
            book_name = file_name.split("_")[0]
            file_name = file_name.replace(".jpg", "")

    elif isinstance(img_or_pth, Image.Image):
        page_img = np.array(img_or_pth)
        if page_img.ndim == 3 and page_img.shape[2] == 3:
            page_img = cv2.cvtColor(page_img, cv2.COLOR_RGB2BGR)
            if file_name is not None:
                # below only happens if the img_or_pth is image type
                book_name = file_name.split("_")[0]
                file_name = file_name.replace(".jpg", "")

    else:
        raise ValueError("Unsupported input type. Must be a file path, NumPy array, or PIL Image.")

    # Prepare for saving if needed
    if save and book_name and file_name:
        # output_dir = os.path.join("output/book_lines/images", book_name)
        output_dir = "/media/cle-nb-183/New Volume/CLE/fonts_guide"
        os.makedirs(output_dir, exist_ok=True)

    count = 1
    contours = image_contours(new_image)
    line_imgs = []

    # Draw the contours on the image for visualization
    contoured_image = new_image.copy()  # Create a copy of the image to draw contours
    cv2.drawContours(contoured_image, contours, -1, (0, 255, 0), 2)  # Draw contours in green color

    # Display the image with drawn contours
    cv2.imshow("Contoured Image", contoured_image)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()

    for contour in contours:
        print(f"Processing Line {count}")

        try:
            x, y, w, h = cv2.boundingRect(contour)
            x, y, w, h = (x - 3, y - 3, w + 3, h + 3)  # Adjust padding as needed

            line_image = page_img[y:y + h, x:x + w]

            # Check if line image meets height criteria
            if line_image.shape[0] > 15:
                line_imgs.append(line_image)

                if save:
                    save_path = os.path.join(output_dir, f"{file_name}_ln{count}.jpg")
                    cv2.imwrite(save_path, line_image)

                count += 1

        except Exception as e:
            print(f"Error processing line {count}: {e}")
            continue  # Continue with the next contour

    if line_imgs == []:
        return [page_img]

    return line_imgs
