import cv2
import os
import numpy as np

# Load the image and extract lines
image_path = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/6. analysis/3. selected pages for multi-line analysis/test_page/Hayat-e-Iqbal_pg15.jpg'
output_dir = "/media/cle-nb-183/New Volume/CLE/2. Testing Data/6. analysis/3. selected pages for multi-line analysis/contour/1"
os.makedirs(output_dir, exist_ok=True)

# Read the page image
page_img = cv2.imread(image_path)

# Check if the image is loaded correctly
if page_img is None:
    print("Error: Could not load image.")
    exit()

# Extract the book name from the image path
book_name = os.path.basename(image_path).split("_")[0]
print(f"Book name extracted: {book_name}")

# Initialize count for naming output images
count = 1

# Convert to grayscale
gray = cv2.cvtColor(page_img, cv2.COLOR_BGR2GRAY)
print("Converted image to grayscale.")

# Save grayscale image
gray_image_path = os.path.join(output_dir, f'{book_name}_gray.jpg')
cv2.imwrite(gray_image_path, gray)

# Apply Gaussian blur
blur = cv2.GaussianBlur(gray, (3, 3), 0)
print("Applied Gaussian blur.")

# Binarize the image (invert binary)
bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
print("Binarized the image.")

# Save binary image
bw_image_path = os.path.join(output_dir, f'{book_name}_binary.jpg')
cv2.imwrite(bw_image_path, bw)

# Show the binary image for debugging
cv2.imshow("Binary Image", bw)
cv2.resizeWindow("Binary Image", 700, 500)
cv2.waitKey(3000)

# Define kernel size for morphological operations
kernel_size_close = (200, 4)  # Adjust the kernel size for better separation
kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size_close)

# Perform morphological closing operation to connect text lines
bw_closed = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel_close)
print("Performed morphological closing.")

# Save closed image
closed_image_path = os.path.join(output_dir, f'{book_name}_closed.jpg')
cv2.imwrite(closed_image_path, bw_closed)

# Show the image after closing operation for debugging
cv2.imshow("Closed Image", bw_closed)
cv2.resizeWindow("Closed Image", 700, 500)
cv2.waitKey(3000)

# Perform morphological opening operation to separate closely spaced lines
kernel_size_open = (8, 3)  # Vertical kernel for opening
kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size_open)
bw_separated = cv2.morphologyEx(bw_closed, cv2.MORPH_OPEN, kernel_open)
print("Performed morphological opening.")

# Save separated image
separated_image_path = os.path.join(output_dir, f'{book_name}_separated.jpg')
cv2.imwrite(separated_image_path, bw_separated)

# Show the image after opening operation for debugging
cv2.imshow("Separated Image", bw_separated)
cv2.resizeWindow("Separated Image", 700, 500)
cv2.waitKey(3000)

# Find contours in the binary image
contours, _ = cv2.findContours(bw_separated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Contours found: {len(contours)}")

# Filter contours based on width-to-height ratio
filtered_contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3]) >= 3.0]
print(f"Filtered contours: {len(filtered_contours)} based on width-to-height ratio.")

# Sort contours based on y-coordinate
sorted_contours = sorted(filtered_contours, key=lambda contour: cv2.boundingRect(contour)[1])
print("Sorted contours based on their y-coordinate.")

# Prepare a list to hold the extracted line images
line_imgs = []

# Create a text file to store operation specifications
specs_file_path = os.path.join(output_dir, f'{book_name}_specs.txt')
with open(specs_file_path, 'w') as specs_file:
    specs_file.write(f"Image processing specifications for {book_name}\n")
    specs_file.write(f"Image Name: {os.path.basename(image_path)}\n")
    specs_file.write(f"Grayscale Image: {gray_image_path}\n")
    specs_file.write(f"Binary Image: {bw_image_path}\n")
    specs_file.write(f"Closing Kernel Size: {kernel_size_close}\n")
    specs_file.write(f"Closed Image: {closed_image_path}\n")
    specs_file.write(f"Opening Kernel Size: {kernel_size_open}\n")
    specs_file.write(f"Separated Image: {separated_image_path}\n")
    specs_file.write("\nExtracted Line Images:\n")

# Iterate over each sorted contour
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
            line_image_path = f'{book_name}_ln{count:03d}.jpg'
            save_path = os.path.join(output_dir, line_image_path)

            # Save the extracted line image
            cv2.imwrite(save_path, line_image)
            print(f"Saved line image: {save_path}")

            # Write the image path to the specs file
            with open(specs_file_path, 'a') as specs_file:
                specs_file.write(f"Line {count:03d}: {save_path}\n")

            count += 1
        else:
            print(f"Line image height too small, skipped: {line_image.shape[0]} pixels.")

    except Exception as e:
        print(f"Error processing contour: {e}")
        continue  # Continue with the next contour

# Output the total number of line images extracted
with open(specs_file_path, 'a') as specs_file:
    specs_file.write(f"\nTotal number of lines extracted: {len(line_imgs)}\n")

print(f"{len(line_imgs)} line images extracted and saved.")

# Close all OpenCV windows
cv2.destroyAllWindows()
