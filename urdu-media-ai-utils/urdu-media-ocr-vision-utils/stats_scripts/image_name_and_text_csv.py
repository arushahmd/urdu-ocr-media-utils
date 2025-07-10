import os
import csv

def create_csv_from_images_and_text(folder_path, output_csv, threshold):
    # List to store image-text pairs
    data = []

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is an image (.jpg)
        if file_name.endswith(".jpg"):
            # Get the base name (without extension) to find corresponding text file
            base_name = os.path.splitext(file_name)[0]
            text_file = base_name + ".txt"
            
            # Full path for the text file
            text_file_path = os.path.join(folder_path, text_file)
            
            # Check if the corresponding text file exists
            if os.path.exists(text_file_path):
                # Read the text from the .txt file
                with open(text_file_path, 'r', encoding='utf-8') as txt_file:
                    recognized_text = txt_file.read().strip()
                
                # Determine the status based on the length of the recognized text
                status = "good" if len(recognized_text) >= threshold else "bad"
                
                # Add image name, recognized text, and status to the data list
                data.append([file_name, recognized_text, status])
            else:
                print(f"Warning: No corresponding text file found for {file_name}")

    # Write the data to a CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow(["image name", "recognized text", "status"])
        # Write rows for each image-text pair
        writer.writerows(data)

    print(f"CSV file '{output_csv}' created successfully.")

# Example usage
folder_path = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/3. analysis/1. New Technique Analysis/5. categorized data/2. ip/colored'  # Replace with your folder path
file_name = "colored good bad status.csv"
output_csv = f'/media/cle-nb-183/New Volume/CLE/2. Testing Data/3. analysis/1. New Technique Analysis/3. Stats/2. ip/good bad status/{file_name}'  # Replace with the desired output CSV file path
threshold = 10  # Set your threshold here
create_csv_from_images_and_text(folder_path, output_csv, threshold)

