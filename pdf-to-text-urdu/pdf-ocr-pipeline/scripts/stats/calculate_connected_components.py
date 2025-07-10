import os
import cv2
import pandas as pd
from bookwise_no_of_pages_and_lines import get_book_names, get_page_count, get_line_count

def calculate_connected_components(image_path):
    """
    Calculates the number of connected components in the given image.

    :param image_path: Path to the image file.
    :return: Number of connected components.
    """
    # Read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Threshold the image to binary (you may need to adjust the threshold value)
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

    # Find connected components
    num_labels, _ = cv2.connectedComponents(binary_image)

    # Since the first component is the background, subtract 1
    return num_labels - 1

def process_images_and_store_connected_components(dir_path):
    """
    Processes images to calculate connected components and stores the result in an Excel file.

    :param dir_path: Directory path where the images are stored.
    :return: None
    """
    file_names = os.listdir(dir_path)

    data = []

    for file_name in file_names:
        try:
            parts = file_name.split("_")
            book_name = parts[0]
            page_num = parts[1].replace("pg", "")
            line_num = parts[2].replace("ln", "").replace(".jpg", "")

            # Full path to the image file
            image_path = os.path.join(dir_path, file_name)

            # Calculate connected components
            connected_components = calculate_connected_components(image_path)

            # Append the results to the data list
            data.append({
                "Book Name": book_name,
                "Page Number": page_num,
                "Line Number": line_num,
                "Connected Components": connected_components
            })

        except Exception as e:
            # Print an error message and skip the file
            print(f"Error processing file {file_name}: {e}")
            continue

    # Convert the data to a DataFrame and save it to an Excel file
    df = pd.DataFrame(data)
    output_path = os.path.join("connected_components_train_dataset.xlsx")
    df.to_excel(output_path, index=False)

    print(f"Connected components data saved to {output_path}")

# Example usage
dir_path = "Final Dataset Backup/Test/images"
process_images_and_store_connected_components(dir_path)
