import os
import csv

# Define the folder containing the jpg files
folder_path = '/media/cle-nb-183/New Volume/CLE/Testing Data/2. Selected 100 Pages/WP_50 pages'

# Define the CSV file to be created
output_csv = 'output.csv'

# Function to extract book name and page number from the filename
def extract_book_info(file_name):
    try:
        # Remove the .jpg extension
        file_name = os.path.splitext(file_name)[0]
        # Split the name into book-name and page-number
        book_name, page_number = file_name.split('_')
        return book_name, page_number
    except ValueError:
        return None, None

# List to store the extracted data
data = []

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.jpg'):
        book_name, page_number = extract_book_info(file_name)
        if book_name and page_number:
            data.append([book_name, page_number])

# Write the data to a CSV file
with open(output_csv, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    # Write the header
    writer.writerow(["Book Name", "Page Number"])
    # Write the rows of data
    writer.writerows(data)

print(f"CSV file '{output_csv}' has been created successfully.")
