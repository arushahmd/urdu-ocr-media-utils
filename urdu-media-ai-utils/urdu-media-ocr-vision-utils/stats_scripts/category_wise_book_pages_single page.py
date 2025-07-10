import os
import re
import pandas as pd

# Define the base folder and output CSV file paths
base_folder = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/3. categorized line data/Scanned'  # Base folder containing category subfolders
output_csv_path = 'ip_category_based_page_names.csv'  # Path to save the CSV file

# Initialize an empty list to store data
data = []

# Regex pattern to extract book name and page number from filenames
filename_pattern = re.compile(r'(?P<book_name>.+)_pg(?P<page_number>\d+)_ln\d+\.jpg')

# Traverse the base folder
for category in os.listdir(base_folder):
    category_path = os.path.join(base_folder, category)
    
    if os.path.isdir(category_path):  # Check if it's a folder (category)
        # Traverse files in the category folder
        for file_name in os.listdir(category_path):
            if file_name.endswith('.jpg'):  # Only process .jpg files
                match = filename_pattern.match(file_name)
                
                if match:
                    book_name = match.group('book_name')
                    page_number = match.group('page_number')
                    
                    # Append the information as a row in the data list
                    data.append({
                        'Category': category,
                        'Book Name': book_name,
                        'Page Number': page_number
                    })

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv(output_csv_path, index=False)

print(f"CSV file generated and saved at: {output_csv_path}")
