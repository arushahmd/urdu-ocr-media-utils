import os
import shutil

def delete_files_not_in_base_folder(base_folder, target_folder):
    base_files = set(os.listdir(base_folder))
    
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.abspath(root) != os.path.abspath(base_folder) and file not in base_files:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

# Example usage:
base_folder = '/home/cle-dl-05/Documents/2.DataSets/TEST SET/4. train_25k images/test/texts'
target_folder = '/home/cle-dl-05/Documents/1.OCR/2.TestOCR_LM/predictions'

delete_files_not_in_base_folder(base_folder, target_folder)
