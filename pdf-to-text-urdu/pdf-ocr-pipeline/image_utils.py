"""
    Contains all the utilities regarding the images.
"""
import os

import cv2
import numpy as np
from PIL.Image import Image

from .text_utils import validate_file_path


def read_image(img_or_pth, file_name=None):
    page_img = None
    book_name = None
    file_name = None

    # Load the image
    if isinstance(img_or_pth, str):
        if not validate_file_path(img_or_pth, ('.jpg', '.JPG', '.png', '.bmp', '.tiff')):
            print(f"Error: {img_or_pth} is not a valid Image file.")
            return None

        if os.path.isfile(img_or_pth):
            page_img = cv2.imread(img_or_pth)
            book_name = os.path.basename(img_or_pth).split("_")[0]
            file_name = os.path.basename(img_or_pth).replace(".jpg", "").replace(".JPG", "").replace(".png",

                                                                                                     "").replace(".bmp",
                                                                                                                 "").replace(
                ".tiff", "")
            return page_img, book_name, file_name
        else:
            raise FileNotFoundError(f"The file path {img_or_pth} does not exist.")

    elif isinstance(img_or_pth, np.ndarray):
        page_img = img_or_pth
        if file_name is not None:
            # below only happens if the img_or_pth is image type
            book_name = file_name.split("_")[0]
            file_name = file_name.replace(".jpg", "")

        return page_img, book_name, file_name

    elif isinstance(img_or_pth, Image.Image):
        page_img = np.array(img_or_pth)
        if page_img.ndim == 3 and page_img.shape[2] == 3:
            page_img = cv2.cvtColor(page_img, cv2.COLOR_RGB2BGR)
            if file_name is not None:
                # below only happens if the img_or_pth is image type
                book_name = file_name.split("_")[0]
                file_name = file_name.replace(".jpg", "")

        return page_img, book_name, file_name

    else:
        raise ValueError("Unsupported input type. Must be a file path, NumPy array, or PIL Image.")


def is_image_completely_blank(image):
    """
    Check if an image is completely blank (white).

    Args:
        image (PIL.Image.Image): Image object.

    Returns:
        bool: True if image is completely blank, False otherwise.
    """
    grayscale_image = image.convert("L")
    extrema = grayscale_image.getextrema()
    return extrema == (255, 255)


def image_contours(image):
    """
    Extract text contours from image using OpenCV.
    Returns sorted contours based on y-coordinate.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Define kernel size for morphological operations
    kernel_size = (200, 10)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

    # Perform morphological closing operation
    bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    # Find contours for each text line
    contours, _ = cv2.findContours(bw_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours to select those whose width is at least 3 times its height
    filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3]) >= 3.0]

    # Sort contours based on y-coordinate
    sorted_contours = sorted(filtered_contours, key=lambda contour: cv2.boundingRect(contour)[1])

    return sorted_contours


def image_contours_with_saving(image_path, output_dir):
    """
    Process the image and save each step's result.
    Also, save the final image with contours drawn on it.

    Parameters:
        image_path: Path to the input image.
        output_dir: Directory to save the intermediate and final images.
    """
    # Read the image
    image = cv2.imread(image_path)
    file_name = image_path.split("/")[-1].replace(".jpg", "")

    # Step 1: Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    save_image(gray, f"{file_name}_grayscale", output_dir)

    # Step 2: Apply Gaussian Blur
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    save_image(blur, f"{file_name}_blurred", output_dir)

    # Step 3: Apply binary threshold using OTSU's method
    _, bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    save_image(bw, f"{file_name}_binary_threshold", output_dir)

    # Step 4: Morphological closing operation
    kernel_size = (200, 10)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
    save_image(bw_closed, f"{file_name}_closing", output_dir)

    # Step 5: Find contours for each text line
    contours, _ = cv2.findContours(bw_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 6: Filter contours where width is at least 3 times its height
    filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3]) >= 3.0]

    # Step 7: Sort contours based on y-coordinate (top to bottom)
    sorted_contours = sorted(filtered_contours, key=lambda contour: cv2.boundingRect(contour)[1])

    contour_image = image.copy()

    for contour in sorted_contours:
        # Get the bounding box coordinates for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Draw a rectangle around each contour on the original image
        cv2.rectangle(contour_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save the final image with rectangles drawn around the contours
    save_image(contour_image, f"{file_name}_contours", output_dir)

    # return sorted_contours


def process_image_morphology(page_img, kernel_sizes):
    """
    Applies morphological operations (closing and opening) to the given image.

    Args:
        page_img (np.ndarray): The input image (as a NumPy array).
        kernel_sizes (tuple): Tuple containing kernel sizes for closing and opening operations.

    Returns:
        tuple: A tuple containing the grayscale image, binary image, morphologically closed image,
               and morphologically opened image.
    """

    # Convert to grayscale
    # Assuming page_img is your input image
    if len(page_img.shape) == 3 and page_img.shape[2] == 3:  # Check if the image is color (BGR)
        # Convert to grayscale
        gray = cv2.cvtColor(page_img, cv2.COLOR_BGR2GRAY)
    else:
        gray = page_img  # Already grayscale, no conversion needed

    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # Binarize the image (using Otsu's threshold, inverted binary)
    bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel_size_close = kernel_sizes[0]  # kernel size for closing
    kernel_size_open = kernel_sizes[1]  # kernel size for opening

    # Perform morphological closing to connect text lines
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size_close)
    bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel_close)

    # Perform morphological opening to separate closely spaced lines
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size_open)
    bw_separated = cv2.morphologyEx(bw_closed, cv2.MORPH_OPEN, kernel_open)

    return gray, bw, bw_closed, bw_separated


def image_contours_updated(page_img, kernel_sizes):
    """
    Finds and returns sorted contours from the processed image.

    Args:
        page_img (np.ndarray): Input image as a NumPy array.
        kernel_sizes (tuple): Tuple containing kernel sizes for morphological operations.

    Returns:
        list: Sorted contours based on width-to-height ratio and y-coordinate.
    """
    _, _, _, bw_separated = process_image_morphology(page_img, kernel_sizes)

    # Find contours in the separated image
    contours, _ = cv2.findContours(bw_separated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on width-to-height ratio
    filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3]) >= 3.0]

    # Sort contours by y-coordinate
    sorted_contours = sorted(filtered_contours, key=lambda contour: cv2.boundingRect(contour)[1])

    return sorted_contours


def get_contour_morph_images(page_img, kernel_sizes=None):
    """
    Returns the original image, grayscale image, binary image, closed (morphologically closed) image,
    opened (morphologically opened) image, and the original image with contours drawn.

    Args:
        img_or_pth (str or np.ndarray): Path to the image file or image data.
        kernel_sizes (tuple): Tuple containing kernel sizes for morphological closing and opening.

    Returns:
        tuple: A tuple containing the original image, grayscale image, binary image,
               morphologically closed image, morphologically opened image,
               and original image with contours drawn.
    """

    # Kernel sizes for morphological operations (if not provided)
    if kernel_sizes is None:
        kernel_sizes = ((200, 4), (8, 3))  # Default values

    # Process the image using morphological operations
    gray, bw, bw_closed, bw_separated = process_image_morphology(page_img, kernel_sizes)

    # Save a copy of the original image for drawing contours later
    original_contoured_image = page_img.copy()

    # Find contours in the separated image
    contours = image_contours_updated(page_img, kernel_sizes)

    # Draw the contours on the original contoured image
    cv2.drawContours(original_contoured_image, contours, -1, (0, 255, 0), 2)

    # Return all the requested images as a tuple
    return page_img, gray, bw, bw_closed, bw_separated, original_contoured_image


def save_line_images(line_images, file_name, save_path):
    """
        Given line images and save path along with file name saves the lines
    """

    prefix = file_name.replace(".jpg", '')

    for count, line_img in enumerate(line_images):
        file_name = f"{prefix}_ln{count + 1}.jpg"
        file_save_pth = os.path.join(save_path, file_name)
        # save the line image
        cv2.imwrite(file_save_pth, line_img)
        print(f"Saved {file_name}")


def save_contour_morph_images(images, file_name, save_path):
    """
    Saves the images of various stages (grayscale, binary, morphologically closed, etc.)
    with corresponding suffixes to differentiate them.

    Args:
        images (list of np.ndarray): A list of images to be saved.
        file_name (str): The original file name (without extension) for the image.
        save_path (str, optional): Directory path where images will be saved. Defaults to None.
    """

    os.makedirs(save_path, exist_ok=True)

    print(f"Saving pre processed images for {file_name}")

    # Suffixes corresponding to each image stage
    suffixes = ['_original', '_gray', '_bw', '_bw_closed', '_bw_separated', '_contours']

    # Create the save path if it doesn't exist
    if save_path and not os.path.exists(save_path):
        os.makedirs(save_path)

    # Iterate over images and save them with the corresponding suffix
    for img, suffix in zip(images, suffixes):
        # Construct the new file name with the suffix
        new_file_name = f"{file_name.replace('.jpg', '')}{suffix}.jpg"

        # Full path where the image will be saved
        if save_path:
            save_file_path = os.path.join(save_path, new_file_name)
        else:
            save_file_path = new_file_name

        # Save the image
        cv2.imwrite(save_file_path, img)

    print(f"Images saved in {save_path if save_path else 'current directory'} with corresponding suffixes.")


def save_image(image, step_name, output_dir):
    """
    Save the image with the given step name in the specified output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, f"{step_name}.png")
    cv2.imwrite(output_path, image)


if __name__ == "__main__":
    image_path = "/media/cle-nb-183/New Volume/CLE/2. Testing Data/2. selected 100 pages/WP_50 pages/Aab-e-Hiyat_pg4.jpg"
    output_dir = "/media/cle-nb-183/New Volume/CLE/2. Testing Data/7. analysis/2. Old Technique Analysis/3. pre processing/1.wp"
    image_contours_with_saving(image_path, output_dir)
