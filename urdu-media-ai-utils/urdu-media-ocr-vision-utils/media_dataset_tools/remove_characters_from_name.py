"""
    Removes some specified characters from the name of a file.
"""

import os


def rename_files_remove_prefix(directory, phrase_to_remove):
    """
    Removes a specified phrase from the names of all files in a given directory.

    :param directory: Path to the directory containing files.
    :param phrase_to_remove: The phrase to be removed from file names.
    """
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    for file_name in os.listdir(directory):
        old_path = os.path.join(directory, file_name)

        # Ensure it's a file (not a folder)
        if os.path.isfile(old_path) and phrase_to_remove in file_name:
            new_name = file_name.replace(phrase_to_remove, "")
            new_path = os.path.join(directory, new_name)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {file_name} -> {new_name}")


directory_path = "phase-I-vott/all_texts"  # Change this to your actual directory
phrase = "_Done"

rename_files_remove_prefix(directory_path, phrase)
