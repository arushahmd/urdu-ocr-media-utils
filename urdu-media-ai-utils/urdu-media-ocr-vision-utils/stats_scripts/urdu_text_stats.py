"""
    given a directory path calculates the following stats.
        ** Total Number of image and text files
        ** Total Number of characters, ligatures, words in all files
        ** Average number of characters, ligatures and words in each line.
"""
import os
import csv
from text_utils import extract_ligatures
from config import all_books_line_data, stats_path


def number_of_characters_and_ligatures(content):
    """
    Given Urdu text content, calculates the number of characters and ligatures.

    Args:
        content (str): Urdu text content.

    Returns:
        tuple: Number of characters, number of ligatures.
    """
    number_of_characters = len(content)
    ligatures = extract_ligatures(content)
    number_of_ligatures = len(ligatures)

    return number_of_characters, number_of_ligatures


def count_words(content):
    """
    Counts the number of words in the given text content.

    Args:
        content (str): Urdu text content.

    Returns:
        int: Number of words.
    """
    words = content.split()
    return len(words)


def dir_urdu_text_stats(dir_path, csv_output_path):
    """
    Given a directory path, calculates the following stats and saves them to a CSV file:
    ** Total Number of characters, ligatures, words in all files
    ** Average number of characters, ligatures, and words per file.

    Args:
        dir_path (str): Path to the directory containing text files.
        csv_output_path (str): Path to save the CSV file with the stats.
    """
    total_characters = 0
    total_ligatures = 0
    total_words = 0
    total_files = 0

    # Iterate through all .txt files in the directory
    for text_file in os.listdir(dir_path):
        if text_file.endswith('.txt'):
            total_files += 1
            with open(os.path.join(dir_path, text_file), encoding='utf-8') as file:
                content = file.read().strip()

                characters, ligatures = number_of_characters_and_ligatures(content)
                words = count_words(content)

                total_characters += characters
                total_ligatures += ligatures
                total_words += words

    average_characters_per_file = total_characters / total_files if total_files > 0 else 0
    average_ligatures_per_file = total_ligatures / total_files if total_files > 0 else 0
    average_words_per_file = total_words / total_files if total_files > 0 else 0

    # Save the stats to a CSV file
    with open(csv_output_path, 'w', newline='', encoding='utf-8') as csvfile:

        # csvwriter = csv.writer(csvfile)
        # csvwriter.writerow(['Total Files', 'Total Characters', 'Total Ligatures', 'Total Words',
        #                     'Average Characters per File', 'Average Ligatures per File', 'Average Words per File'])
        # csvwriter.writerow([total_files, total_characters, total_ligatures, total_words,
        #                     average_characters_per_file, average_ligatures_per_file, average_words_per_file])

        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Metric', 'Value'])
        csvwriter.writerow(['Total Files', total_files])
        csvwriter.writerow(['Total Characters', total_characters])
        csvwriter.writerow(['Total Ligatures', total_ligatures])
        csvwriter.writerow(['Total Words', total_words])
        csvwriter.writerow(['Average Characters per File', average_characters_per_file])
        csvwriter.writerow(['Average Ligatures per File', average_ligatures_per_file])
        csvwriter.writerow(['Average Words per File', average_words_per_file])

    print(f"Statistics saved to {csv_output_path}")


# Example usage
if __name__ == "__main__":
    text_dir = os.path.join(all_books_line_data, "texts")
    dir_urdu_text_stats(text_dir, stats_path)


