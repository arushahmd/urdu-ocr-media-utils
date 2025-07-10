import os
import pandas as pd

def count_pages_per_book(base_folder):
    # Dictionary to store the book name and unique page counts
    book_page_counts = {}

    # Traverse through the folder to count pages for each book
    for filename in os.listdir(base_folder):
        if filename.endswith('.jpg'):
            # Split the filename to extract book name and page number
            parts = filename.split('_')
            if len(parts) >= 2:
                book_name = parts[0]
                page_number = parts[1][2:]  # Skip 'pg' and get the number

                # Initialize set for pages if not already for the book
                if book_name not in book_page_counts:
                    book_page_counts[book_name] = set()

                # Add the page number to the set (automatically handles uniqueness)
                book_page_counts[book_name].add(page_number)

    # Prepare data for CSV
    data = []
    for book_name, pages in book_page_counts.items():
        data.append({
            'Book Name': book_name,
            'Total Pages': len(pages)  # Count of unique pages
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    return df

def save_to_csv(df, output_file):
    # Save DataFrame to a CSV file
    df.to_csv(output_file, index=False)

def main():
    # Directly specify the base folder and output file paths
    base_folder = '/media/cle-nb-183/New Volume/CLE/Testing Data/2. Selected 100 Pages/WP_50 pages'  # Update with your base folder path
    output_file = '/media/cle-nb-183/New Volume/CLE/Testing Data/codes/wp_book_pages.csv'  # Update with your desired output file path

    # Count pages per book
    page_counts = count_pages_per_book(base_folder)

    # Save the result as CSV
    save_to_csv(page_counts, output_file)

    print(f"Page counts saved to {output_file}")

if __name__ == "__main__":
    main()
