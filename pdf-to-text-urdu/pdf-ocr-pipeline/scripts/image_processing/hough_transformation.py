import cv2
import os
import numpy as np

# Load the image
image_path = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/6. analysis/3. selected pages for multi-line analysis/test_page/Hayat-e-Iqbal_pg15.jpg'
image = cv2.imread(image_path)

output_path = "/media/cle-nb-183/New Volume/CLE/2. Testing Data/6. analysis/3. selected pages for multi-line analysis/hough"
os.makedirs(output_path, exist_ok=True)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection (Canny)
edges = cv2.Canny(gray, 50, 150)

# Use Hough Transform to detect lines
lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)

# Draw detected lines on the original image
if lines is not None:
    for rho, theta in lines[:, 0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Create a window with a specific name
cv2.namedWindow('Detected Lines', cv2.WINDOW_NORMAL)

# Resize the window to 700x500 pixels
cv2.resizeWindow('Detected Lines', 700, 500)

# Show the result
cv2.imshow('Detected Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
