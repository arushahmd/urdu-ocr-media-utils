import os
import pandas as pd
from collections import defaultdict

def get_book_names(dir_or_filenames):
    """
    Given a directory or list of filenames, this function extracts and returns the unique book names.
    The naming convention is assumed to be <book_name>_pg<page no>_ln<line no>.jpg.

    :param dir_or_filenames: Directory of images or a list of filenames.
    :return: Set of unique book names.
    """
    if isinstance(dir_or_filenames, list):
        file_names = dir_or_filenames
    else:
        file_names = os.listdir(dir_or_filenames)

    book_names = set(file_name.split("_")[0] for file_name in file_names)
    return book_names


def get_page_count(file_names):
    """
    Calculates the number of unique pages for each book.

    :param file_names: List of filenames.
    :return: Dictionary with book names as keys and the number of unique pages as values.
    """
    page_count = defaultdict(set)

    for file_name in file_names:
        parts = file_name.split("_")
        book_name = parts[0]
        page_num = parts[1].replace("pg", "")
        page_count[book_name].add(page_num)

    # Convert sets to their lengths to get the count of unique pages
    page_count = {book: len(pages) for book, pages in page_count.items()}
    return page_count


def get_line_count(file_names):
    """
    Calculates the total number of lines for each book.

    :param file_names: List of filenames.
    :return: Dictionary with book names as keys and the total number of lines as values.
    """
    line_count = defaultdict(int)

    for file_name in file_names:
        book_name = file_name.split("_")[0]
        line_count[book_name] += 1

    return line_count


def get_lines_per_page(file_names):
    """
    Calculates the number of lines per page for each book.

    :param file_names: List of filenames.
    :return: Dictionary with keys as (book_name, page_num) and values as the number of lines on that page.
    """
    lines_per_page = defaultdict(int)

    for file_name in file_names:
        parts = file_name.split("_")
        book_name = parts[0]
        page_num = parts[1].replace("pg", "")
        lines_per_page[(book_name, page_num)] += 1

    return lines_per_page


def save_book_pages_and_lines(dir_path):
    """
    Calculates and saves the number of pages and lines for each book to an Excel file.

    :param dir_path: Directory path where the images are stored.
    :return: None
    """
    file_names = os.listdir(dir_path)

    book_names = get_book_names(file_names)
    page_counts = get_page_count(file_names)
    line_counts = get_line_count(file_names)

    # Prepare data for Excel
    data = {
        "Book Name": list(book_names),
        "No of Pages": [page_counts.get(book, 0) for book in book_names],
        "No of Lines": [line_counts.get(book, 0) for book in book_names]
    }

    df = pd.DataFrame(data)

    # Save the data to an Excel file
    output_path = os.path.join("book_pages_and_lines_train_dataset.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Book pages and lines data saved to {output_path}")


def save_lines_per_page(dir_path):
    """
    Calculates and saves the number of lines per page for each book to an Excel file.

    :param dir_path: Directory path where the images are stored.
    :return: None
    """
    file_names = os.listdir(dir_path)
    lines_per_page = get_lines_per_page(file_names)

    # Prepare data for Excel
    lines_per_page_data = {
        "Book Name": [book for (book, page) in lines_per_page.keys()],
        "Page Number": [page for (book, page) in lines_per_page.keys()],
        "No of Lines": list(lines_per_page.values())
    }

    df_lines_per_page = pd.DataFrame(lines_per_page_data)

    # Save the data to an Excel file
    output_path_lines = os.path.join("book_lines_per_page_test_dataset.xlsx")
    df_lines_per_page.to_excel(output_path_lines, index=False)
    print(f"Lines per page data saved to {output_path_lines}")


if __name__ == "__main__":

    from config import dir_path, calculate_pages_and_lines, calculate_lines_per_page

    # Call the specific functions based on the flags
    if calculate_pages_and_lines:
        save_book_pages_and_lines(dir_path)

    if calculate_lines_per_page:
        save_lines_per_page(dir_path)
