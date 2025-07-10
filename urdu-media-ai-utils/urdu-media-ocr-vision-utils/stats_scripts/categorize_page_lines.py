import os
import pandas as pd
from collections import defaultdict

def count_line_images(base_folder):
    # Dictionary to hold counts
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    # Traverse through each category folder
    for category in os.listdir(base_folder):
        category_path = os.path.join(base_folder, category)
        if os.path.isdir(category_path):  # Check if it is a folder
            for filename in os.listdir(category_path):
                if filename.endswith('.jpg'):
                    # Split the filename to extract book name and page number
                    parts = filename.split('_')
                    if len(parts) >= 3:
                        book_name = parts[0]
                        page_number = parts[1][2:]  # Skip 'pg'
                        data[book_name][page_number][category] += 1

    # Prepare the DataFrame
    rows = []
    for book_name, pages in data.items():
        for page_number, categories in pages.items():
            total_lines = sum(categories.values())
            row = {
                'Book Name': book_name,
                'Page Number': page_number,
                'Total No of Lines': total_lines
            }
            row.update(categories)  # Add category counts to the row
            rows.append(row)

    # Create DataFrame from rows
    df = pd.DataFrame(rows).fillna(0)

    # Convert count columns to integers
    count_columns = df.columns[3:]  # All columns after the first three
    df[count_columns] = df[count_columns].astype(int)

    return df

def save_to_csv(df, output_file):
    # Save DataFrame to a CSV file
    df.to_csv(output_file, index=False)

def main():
    # Directly specify the base folder and output file paths
    base_folder = '/media/cle-nb-183/New Volume/CLE/Testing Data/3. Categorized Line Data/Word Processed'  # Base folder path
    output_file = '/media/cle-nb-183/New Volume/CLE/Testing Data/codes/output.csv'  # Desired output file path

    line_counts = count_line_images(base_folder)
    save_to_csv(line_counts, output_file)
    print(f"Line counts saved to {output_file}")

if __name__ == "__main__":
    main()

