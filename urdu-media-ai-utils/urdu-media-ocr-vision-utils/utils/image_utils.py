"""
    This file will contain the image utils
    The functions that will be used to perform some operations on an image.
"""

import cv2


def optimize_image(image):
    """
    Given a Urdu text image strip, it will optimize the image to remove the empty
    background from the left and the right of the image and only use the area that contains the
    text data.

    :param image: Input image as cv2 image array.
    """
    # Convert image to grayscale
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert image to binary if it's not already binary
    _, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Find the coordinates where the black pixels start and end in each dimension
    top = next((i for i, row in enumerate(binary_img) if any(pixel == 0 for pixel in row)), 0)
    bottom = next((i for i, row in enumerate(reversed(binary_img)) if any(pixel == 0 for pixel in row)), 0)
    left = next((i for i, col in enumerate(binary_img.T) if any(pixel == 0 for pixel in col)), 0)
    right = next((i for i, col in enumerate(reversed(binary_img.T)) if any(pixel == 0 for pixel in col)), 0)

    # Crop the image based on the found coordinates
    cropped_image = binary_img[top: len(binary_img) - bottom, left: len(binary_img[0]) - right]

    # Display original and optimized images
    cv2.imshow("Original Image", image)
    cv2.imshow("Optimized Image", cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":

    img_pth = "/home/cle-dl-05/Documents/3.PdfOCR/dataset/Testing_set_1000/images/Al Jihad Fil Islam (Volume 02) SwaneUmri Hazrat Uma80_Line8.jpg"
    image = cv2.imread(img_pth)
    optimize_image(image)
