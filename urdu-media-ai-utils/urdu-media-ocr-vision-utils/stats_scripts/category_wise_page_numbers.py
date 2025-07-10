import os
import re
import pandas as pd

# Function to extract book name and page number from the filename
def extract_book_and_page(filename):
    match = re.match(r"(.+)_pg(\d+)_ln\d+\.jpg", filename)
    if match:
        book_name = match.group(1)
        page_number = int(match.group(2))
        return book_name, page_number
    return None, None

# Function to process the base folder and aggregate results
def process_base_folder(base_dir):
    # Create a dictionary to store results
    results = {'Category': [], 'Book Name': [], 'Page Numbers': [], 'Comments': []}
    book_page_folder = {}

    # Traverse through all category folders in the base directory
    for category in os.listdir(base_dir):
        category_path = os.path.join(base_dir, category)
        if os.path.isdir(category_path):  # Ensure it's a folder
            # Traverse the files inside the category folder
            for file in os.listdir(category_path):
                if file.endswith('.jpg'):  # Only process .jpg files
                    book_name, page_number = extract_book_and_page(file)
                    if book_name and page_number:
                        if (book_name, category) not in book_page_folder:
                            book_page_folder[(book_name, category)] = {
                                'page_numbers': set(),
                                'folders': set()
                            }
                        book_page_folder[(book_name, category)]['page_numbers'].add(page_number)
                        book_page_folder[(book_name, category)]['folders'].add(category)

    # Convert book_page_folder data into the results dictionary
    for (book_name, category), data in book_page_folder.items():
        results['Category'].append(category)
        results['Book Name'].append(book_name)
        results['Page Numbers'].append(', '.join(map(str, sorted(data['page_numbers']))))
        results['Comments'].append(', '.join(data['folders']))

    # Convert results to a DataFrame
    return pd.DataFrame(results)

# Main function to process the base folder and save to CSV
def main(base_folder, output_csv_path):
    # Process the base folder and get aggregated results
    aggregated_data = process_base_folder(base_folder)

    # Save the final result to a CSV file
    aggregated_data.to_csv(output_csv_path, index=False)
    print(f"Aggregated data saved to: {output_csv_path}")

# Example usage
if __name__ == "__main__":
    base_folder = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/3. categorized line data/Word Processed'  # Base folder containing category subfolders
    output_csv_path = 'wp_category_based_page_names.csv'  # Path to save the CSV file

    main(base_folder, output_csv_path)
