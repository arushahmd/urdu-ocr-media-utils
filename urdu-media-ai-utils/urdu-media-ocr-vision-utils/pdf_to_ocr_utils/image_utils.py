"""
    Contains all the utilities regarding the images.
"""

import cv2


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
    if len(image.shape) == 3:  # Image has 3 channels (BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image  # Image is already grayscale

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

