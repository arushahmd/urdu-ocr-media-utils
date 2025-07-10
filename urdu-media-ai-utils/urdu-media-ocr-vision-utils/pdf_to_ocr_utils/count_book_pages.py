import os
import pandas as pd

# Function to count pages in each book folder
def count_pages_in_books(main_folder):
    book_page_counts = []  # List to hold book names and their page counts

    # Iterate through each subfolder in the main folder
    for book_name in os.listdir(main_folder):
        book_path = os.path.join(main_folder, book_name)

        # Check if it's a directory
        if os.path.isdir(book_path):
            # Count .jpg files in the book folder
            page_count = len([file for file in os.listdir(book_path) if file.lower().endswith('.jpg')])
            book_page_counts.append({'Book Name': book_name, 'No. of Pages': page_count})

    # Create a DataFrame and save it to a CSV file
    df = pd.DataFrame(book_page_counts)
    output_csv_path = os.path.join(main_folder, 'ip_book_page_counts.csv')
    df.to_csv(output_csv_path, index=False)

    print(f"CSV file created: {output_csv_path}")

# Specify the path to the main folder
main_folder_path = '/home/cle-dl-05/Desktop/Aroosh/2. Pdf Ocr Pipeline/output/book_pages/images/IP'  # Change this to your main folder path
count_pages_in_books(main_folder_path)
