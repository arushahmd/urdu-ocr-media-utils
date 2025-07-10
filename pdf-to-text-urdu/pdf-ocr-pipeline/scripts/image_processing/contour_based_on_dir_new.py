# Updated the name of folders to be like, kernel(200,3)_morph(8,3)

import cv2
import os
import numpy as np


def process_image(image_path, output_base_dir, kernel_variations):
    # Read the page image
    page_img = cv2.imread(image_path)

    # Check if the image is loaded correctly
    if page_img is None:
        print(f"Error: Could not load image: {image_path}")
        return

    # Extract the image name without extension
    image_name = os.path.basename(image_path).split('.')[0]

    # Create a folder for the current image inside the output directory
    image_output_dir = os.path.join(output_base_dir, image_name)
    os.makedirs(image_output_dir, exist_ok=True)

    # Convert to grayscale
    gray = cv2.cvtColor(page_img, cv2.COLOR_BGR2GRAY)
    gray_image_path = os.path.join(image_output_dir, f'{image_name}_gray.jpg')
    cv2.imwrite(gray_image_path, gray)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # Binarize the image (invert binary)
    bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    bw_image_path = os.path.join(image_output_dir, f'{image_name}_binary.jpg')
    cv2.imwrite(bw_image_path, bw)

    # Save original binary image with contours
    original_contoured_image = page_img.copy()

    # Define kernel variations for morphological operations
    for kernel_size_close, kernel_size_open in kernel_variations:
        # Create folder named based on kernel sizes
        variation_output_dir = os.path.join(image_output_dir, f'kernel({kernel_size_close[0]},{kernel_size_close[1]})_morph({kernel_size_open[0]},{kernel_size_open[1]})')
        os.makedirs(variation_output_dir, exist_ok=True)

        # Perform morphological closing to connect text lines
        kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size_close)
        bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel_close)
        closed_image_path = os.path.join(variation_output_dir, f'{image_name}_closed.jpg')
        cv2.imwrite(closed_image_path, bw_closed)

        # Perform morphological opening to separate closely spaced lines
        kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size_open)
        bw_separated = cv2.morphologyEx(bw_closed, cv2.MORPH_OPEN, kernel_open)
        separated_image_path = os.path.join(variation_output_dir, f'{image_name}_separated.jpg')
        cv2.imwrite(separated_image_path, bw_separated)

        # Find contours in the separated image
        contours, _ = cv2.findContours(bw_separated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on the original image
        contoured_image = original_contoured_image.copy()
        cv2.drawContours(contoured_image, contours, -1, (0, 255, 0), 2)
        contoured_image_path = os.path.join(variation_output_dir, f'{image_name}_contoured.jpg')
        cv2.imwrite(contoured_image_path, contoured_image)

        # Filter contours based on width-to-height ratio
        filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3]) >= 3.0]

        # Sort contours by y-coordinate
        sorted_contours = sorted(filtered_contours, key=lambda contour: cv2.boundingRect(contour)[1])

        # Initialize count for line images
        count = 1
        specs_file_path = os.path.join(variation_output_dir, f'{image_name}_specs.txt')

        # Write operation specs to file
        with open(specs_file_path, 'w') as specs_file:
            specs_file.write(f"Image processing specs for {image_name} (Kernel Variation {kernel_size_close}, {kernel_size_open})\n")
            specs_file.write(f"Grayscale Image: {gray_image_path}\n")
            specs_file.write(f"Binary Image: {bw_image_path}\n")
            specs_file.write(f"Closing Kernel Size: {kernel_size_close}\n")
            specs_file.write(f"Closed Image: {closed_image_path}\n")
            specs_file.write(f"Opening Kernel Size: {kernel_size_open}\n")
            specs_file.write(f"Separated Image: {separated_image_path}\n")
            specs_file.write(f"Contoured Image: {contoured_image_path}\n")
            specs_file.write("\nExtracted Line Images:\n")

            # Iterate over each sorted contour and save line images
            for contour in sorted_contours:
                x, y, w, h = cv2.boundingRect(contour)
                y_offset = 5

                line_image = page_img[max(0, y - y_offset):y + h + y_offset, x:x + w]

                # Save line image if its height is sufficient
                if line_image.shape[0] > 15:
                    line_image_path = f'{image_name}_ln{count:03d}.jpg'
                    save_path = os.path.join(variation_output_dir, line_image_path)
                    cv2.imwrite(save_path, line_image)

                    # Write to specs file
                    specs_file.write(f"Line {count:03d}: {save_path}\n")

                    count += 1


# Function to process either a single image or all images in a directory
def process_images(input_path, output_dir, kernel_variations):
    if os.path.isfile(input_path):
        process_image(input_path, output_dir, kernel_variations)
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(input_path, filename)
                process_image(image_path, output_dir, kernel_variations)


# Kernel variations for closing and opening with the requested filters
kernel_variations = [
    ((200, 4), (10, 4)),
    ((200, 4), (20, 5)),
    ((200, 4), (30, 5)),
    ((150, 4), (10, 4)),
    ((150, 4), (20, 5)),
    ((100, 4), (10, 4)),
    ((50, 4), (20, 5)),
]

# Example usage
input_path = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/6. analysis/3. selected pages for multi-line analysis/all_pages'
output_dir = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/6. analysis/3. selected pages for multi-line analysis/contour'
process_images(input_path, output_dir, kernel_variations)
