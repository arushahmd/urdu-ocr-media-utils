import os
import csv
from collections import defaultdict

"""
This script counts the number of image files in a specified directory that share a common prefix,
representing the book name and page number (e.g., "Iqbal aur Qurratulain Hyder_pg28").
It saves the counts to a CSV file, allowing easy tracking of how many images correspond to each
book and page combination.

The expected naming format for image files is:
    <Book_Name>_pg<page_number>_ln<line_number>.jpg
    e.g., "Iqbal aur Qurratulain Hyder_pg28_ln27.jpg"

Usage:
1. Set the `directory_path` variable to the path of the folder containing the images.
2. Run the script. It will generate a CSV file with the counts of images for each prefix.
"""


def count_files_by_prefix(directory):
    """
    Count the number of image files with a specific prefix (book name and page number)
    in the given directory.

    Args:
        directory (str): Path to the directory containing image files.

    Returns:
        dict: A dictionary with prefixes as keys and counts as values.
    """
    prefix_count = defaultdict(int)

    # List all files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(('.jpg', '.jpeg', '.png')):  # Check for image files
            # Extract the prefix (book name and page number)
            prefix = '_'.join(file_name.split('_')[:-1])  # Exclude the last part (_lnXX.jpg)
            prefix_count[prefix] += 1

    return prefix_count

def save_counts_to_csv(counts, output_file):
    """
    Save the prefix counts to a CSV file.

    Args:
        counts (dict): A dictionary with prefixes and their counts.
        output_file (str): The path for the output CSV file.
    """
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Prefix', 'Count'])  # Header

        for prefix, count in counts.items():
            writer.writerow([prefix, count])

def main(directory, output_file):
    """
    Main function to count files by prefix and save to a CSV.

    Args:
        directory (str): Path to the directory containing image files.
        output_file (str): The path for the output CSV file.
    """
    counts = count_files_by_prefix(directory)
    save_counts_to_csv(counts, output_file)
    print(f"Counts saved to {output_file}")

if __name__ == "__main__":
    # Set the directory path and output CSV file name
    directory_path = "/media/cle-nb-183/New Volume/CLE/2. Testing Data/7. analysis/3. selected pages for multi-line analysis/1. New Technique Analysis/1. lines/2. ip"  # Change this to your directory
    output_csv = "/media/cle-nb-183/New Volume/CLE/2. Testing Data/7. analysis/3. selected pages for multi-line analysis/1. New Technique Analysis/3. Stats/ip_lines_count.csv"  # Output CSV file name

    main(directory_path, output_csv)
