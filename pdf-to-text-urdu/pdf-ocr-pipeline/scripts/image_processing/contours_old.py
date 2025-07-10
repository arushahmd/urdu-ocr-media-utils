import cv2
import os


def image_contours(image, image_path):
    """
    Extract text contours from image using OpenCV.
    Returns sorted contours based on y-coordinate.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image_path = os.path.join(output_directory, f'gray_{os.path.basename(image_path)}')
    cv2.imwrite(gray_image_path, gray) # Save grayscale image
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    bw_image_path = os.path.join(output_directory, f'bw_{os.path.basename(image_path)}')
    cv2.imwrite(bw_image_path, bw)  # Save thresholded image

    # Define kernel size for morphological operations
    kernel_size = (200, 10)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

    # Perform morphological closing operation
    bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    # Find contours for each text line
    contours, _ = cv2.findContours(bw_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours to select those whose width is at least 3 times their height
    filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3]) >= 3.0]

    # Sort contours based on y-coordinate
    sorted_contours = sorted(filtered_contours, key=lambda contour: cv2.boundingRect(contour)[1])

    return sorted_contours


def process_image(image_path, output_dir, count_start=1):
    """
    Process an image, extract line contours using the image_contours logic,
    and save the extracted line images.
    """
    # Read the page image
    page_img = cv2.imread(image_path)

    # Check if the image is loaded correctly
    if page_img is None:
        print(f"Error: Could not load image {image_path}.")
        return

    # Extract the book name from the image path
    book_name = os.path.basename(image_path).split("_")[0]
    print(f"Processing: {os.path.basename(image_path)} | Book name: {book_name}")

    # Save the original image
    original_image_path = os.path.join(output_dir, f'original_{os.path.basename(image_path)}')
    cv2.imwrite(original_image_path, page_img)

    # Initialize count for naming output images
    count = count_start

    # Use the same contour extraction logic from `image_contours`
    sorted_contours = image_contours(page_img, image_path)

    # Prepare a list to hold the extracted line images
    line_imgs = []

    # Create a text file to store operation specifications
    specs_file_path = os.path.join(output_dir, f'{book_name}_specs.txt')
    with open(specs_file_path, 'w') as specs_file:
        specs_file.write(f"Image processing specifications for {book_name}\n")
        specs_file.write(f"Image Name: {os.path.basename(image_path)}\n")

    # Iterate over each sorted contour and extract line images
    for contour in sorted_contours:
        try:
            # Get bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)
            y_offset = 5  # Adjust this offset as needed

            # Extract the line image using the bounding box
            line_image = page_img[max(0, y - y_offset):y + h + y_offset, x:x + w]

            # Check if the height of the line image meets the criteria
            if line_image.shape[0] > 15:
                # Append the line image to the list
                line_imgs.append(line_image)

                # Create the filename with zero-padded numbers for better sorting
                # line_image_path = f'{book_name}_ln{count:03d}.jpg'
                # save_path = os.path.join(output_dir, line_image_path)

                # Save the extracted line image
                # cv2.imwrite(save_path, line_image)

                # Write the image path to the specs file
                # with open(specs_file_path, 'a') as specs_file:
                #     specs_file.write(f"Line {count:03d}: {save_path}\n")

                count += 1
            else:
                print(f"Line image height too small, skipped: {line_image.shape[0]} pixels.")

            # Draw the contour on the original image
            cv2.rectangle(page_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        except Exception as e:
            print(f"Error processing contour: {e}")
            continue  # Continue with the next contour

    # Save the image with contours drawn using the original name
    contour_image_path = os.path.join(output_dir, f'contoured_{os.path.basename(image_path)}')
    cv2.imwrite(contour_image_path, page_img)
    print(f"Saved image with contours: {contour_image_path}")

    # Output the total number of line images extracted
    with open(specs_file_path, 'a') as specs_file:
        specs_file.write(f"\nTotal number of lines extracted: {len(line_imgs)}\n")

    return count  # Return the updated count for line numbering

def process_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Initialize count
    count_start = 1

    # Iterate over all jpg images in the input directory
    for image_file in os.listdir(input_dir):
        if image_file.endswith('.jpg'):
            image_path = os.path.join(input_dir, image_file)
            count_start = process_image(image_path, output_dir, count_start)

# Example usage
input_directory = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/2. selected 100 pages/WP_50 pages'  # Set your input directory here
output_directory = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/3. analysis/2. Old Technique Analysis/2. pre processing/1.wp'  # Set your output directory here

process_directory(input_directory, output_directory)
