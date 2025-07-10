import os
import shutil

# Define paths
# where the images sub folders are
base_folder = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/4. categorized line data/2. new categorization/1. wp'  # Base folder with jpg files (sub-folders are categories)
txt_folder = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/7. analysis/1. New Technique Analysis/4. predictions/1. wp'             # Folder with txt files

# where to save, can be the same as images, if you want to take text files into the same sub folders as images
output_folder = '/media/cle-nb-183/New Volume/CLE/2. Testing Data/4. categorized line data/2. new categorization/1. wp'            # Third folder where the txt files will be copied into category sub-folders

# Function to create the corresponding sub-folder and copy the txt file
def copy_txt_file(category, file_name):
    # Create the sub-folder inside the output folder
    category_folder_path = os.path.join(output_folder, category)
    os.makedirs(category_folder_path, exist_ok=True)

    # Construct the full paths for the txt file and its destination
    txt_file_src = os.path.join(txt_folder, file_name)
    txt_file_dest = os.path.join(category_folder_path, file_name)

    # Copy the txt file if it exists
    if os.path.exists(txt_file_src):
        shutil.copy(txt_file_src, txt_file_dest)
        print(f"Copied: {txt_file_src} -> {txt_file_dest}")
    else:
        print(f"TXT file does not exist: {txt_file_src}")

# Loop through the base folder and process sub-folders (categories)
for category in os.listdir(base_folder):
    category_folder = os.path.join(base_folder, category)
    
    if os.path.isdir(category_folder):  # Check if it's a sub-folder
        # Loop through the .jpg files in the category folder
        for file_name in os.listdir(category_folder):
            if file_name.endswith('.jpg'):
                # Get the corresponding .txt file name (replace .jpg with .txt)
                txt_file_name = file_name.replace('.jpg', '.txt')

                # Copy the txt file to the appropriate category sub-folder in the output folder
                copy_txt_file(category, txt_file_name)

print("Sorting and copying completed.")
