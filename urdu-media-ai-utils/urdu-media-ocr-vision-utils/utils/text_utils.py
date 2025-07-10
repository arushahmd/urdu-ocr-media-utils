"""
    Contains utility functions related to text data.
"""

import os

from config import book_name_prefixes, pdf_files_dir_path

def minus_to_hash_in_text_data(text_path):
    """
        Replaces the minus (-) sign with the hash (#) so that all the text files
        have the same notation for the page number,

        Like, #########3########, where 3 is the page number.
    """
    with open(text_path, encoding='utf-8-sig') as file:
        lines = file.readlines()

        updated_lines = [line.replace("-", "#") for line in lines]
        updated_lines = [line.replace("Page", "") for line in lines]

        with open(text_path, 'w', encoding='utf-8-sig') as file:
            file.writelines(updated_lines)

# ligatures = []
def extract_ligatures(text):
    """
        This script will extract ligatures from a urdu text
    """
    # Calling class that will read the config file and set values
    non_joiners = ['آ', 'ا', 'د', 'ڈ', 'ذ', 'ر', 'ڑ', 'ز', 'ژ', 'ں', 'و', 'ے', '\"', '،', '(', ')', '؟', '۔', '!',
                   ':']  # Getting value of non_joiners from config file
    ligatures = []
    ligatures_return = []
    words = text.split(' ')  # Splitting sentence by space to get words from sentence
    for word in words:  # Iterating the words to separate ligatures
        ligature = ''
        for char in word:  # Iterating characters of a word
            if char not in non_joiners:  # If char is not non_joiner it will be concatenated
                ligature += char
            else:
                # If char is a non_joiner it will concatenate and from next char new ligature will start
                ligature += char
                ligatures.append(ligature)
                ligatures_return.append(ligature)
                ligature = ''
        if ligature != '':
            # If ligature got no non_joiner whole will be considered as a ligature
            ligatures.append(ligature)
            ligatures_return.append(ligature)

    return ligatures_return


if __name__ =="__main__":
    for book_name in book_name_prefixes:
        txt_pth = os.path.join(pdf_files_dir_path, f"{book_name}.txt")
        minus_to_hash_in_text_data(txt_pth)




