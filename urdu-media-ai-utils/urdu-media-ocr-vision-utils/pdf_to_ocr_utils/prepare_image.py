"""
    Preparing Line image for line extraction.
"""
import cv2


def preprocess_image_for_line_separation(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Define a kernel for dilation (tune size based on your image characteristics)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))

    # Apply dilation to separate closely spaced lines
    dilated_img = cv2.dilate(binary_img, kernel, iterations=1)

    # cv2.imshow("dilated", dilated_img)
    # cv2.waitKey(3000)

    return dilated_img