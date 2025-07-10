"""
    This file helps to calculate the stats for pdf dataset.

    Stats may include
        ** No of pages
        ** No of Lines
        ** No of ligatures
        ** No of characters
        ** No of Average character per line
        ** No of Average Ligatures per line
        ** No of Average words per line
"""

import re
import os
import csv

from config import book_name_prefixes, all_books_line_data

"""
    Stats I need:
        1.Book Wise
            ** No of Line images per book (Correct and Verified).
            ** No of Characters and Ligatures for each book.
"""

def bookwise_stats(directory_path):
    """
        Calculates the number of images and lines separating them based on the prefix of the image name.
        Calculates the number of characters and ligaures based on the prefix of the text file.
    """
    if os.path.exists(directory_path):
        images_dir = os.path.join(directory_path, "images")
        texts_dir = os.path.join(directory_path, "texts")

        images = os.listdir(images_dir)
        texts = os.listdir(texts_dir)

        if(len(images) == len(texts)):
            print("Found Equal Number of Images and Texts.")
        else:
            print("Number of Images and Texts is not Equal."
                  f"\nNumber of Images: {len(images)}"
                  f"\nNumber of Texts: {len(texts)}")
    else:
        print("The folder path is incorrect. Make sure the folder exists.")
    pass

def calculate_stats(directory_path, output_csv):
    total_chars = 0
    total_ligatures = 0
    total_words = 0
    total_files = 0
    total_lines = 0

    # Open CSV file for writing
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Filename', 'Total Characters', 'Total Ligatures', 'Total Words', 'Total Lines']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate over files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):  # Process only text files
                total_files += 1
                file_path = os.path.join(directory_path, filename)

                try:
                    # Read text content
                    with open(file_path, mode='r', encoding='utf-8-sig') as f:
                        text = f.read()

                    # Calculate total characters
                    num_chars = len(text)
                    total_chars += num_chars

                    # Count lines in the text
                    # Count as one line (since there are no explicit '\n' characters)
                    num_lines = 1
                    total_lines += num_lines

                    # Find ligatures (connected sequences of characters)
                    ligatures = []
                    for match in re.finditer(r'[\u0600-\u06FF]+', text):
                        ligature = match.group(0)
                        ligatures.extend(list(ligature))  # Split ligature into individual characters
                    num_ligatures = len(ligatures)
                    total_ligatures += num_ligatures

                    # Split text into words (separated by spaces, punctuation, etc.)
                    words = re.findall(r'[\u0600-\u06FF]+', text)
                    num_words = len(words)
                    total_words += num_words

                    # Write file-specific stats to CSV
                    writer.writerow({'Filename': filename,
                                     'Total Characters': num_chars,
                                     'Total Ligatures': num_ligatures,
                                     'Total Words': num_words,
                                     'Total Lines': num_lines})

                except Exception as e:
                    print(f"Error processing file {filename}: {str(e)}")

        # Write aggregated totals to CSV
        writer.writerow({'Filename': 'Total',
                         'Total Characters': total_chars,
                         'Total Ligatures': total_ligatures,
                         'Total Words': total_words,
                         'Total Lines': total_lines})

    # Print confirmation
    print(f"Aggregated statistics saved to {output_csv}")


if __name__ == "__main__":
    texts_path = os.path.join(all_books_line_data, "texts")
    output_csv = '/scripts/stats/dataset_stats_verified_data(W_L_C).csv'
    calculate_stats(texts_path, output_csv)
    # bookwise_stats(all_books_line_data)