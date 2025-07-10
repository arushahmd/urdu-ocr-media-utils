"""
    Will contain configurations like,
        ** Directory and File Paths
        ** Variables
"""
import os

raw_data_folder_path = "/media/cle-nb-183/New Volume/Pdf Dataset/Dataset"
all_books_line_data = os.path.join(raw_data_folder_path, "Verified Data")
stats_path = "/media/cle-nb-183/New Volume/Pdf Dataset/scripts/stats/stats_verified_data_(W_L_C).csv"


pdf_files_dir_path = "/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/Annotated Books"

pdf_pages_images_and_texts_dir_path = "/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/1.All Books Combined Pagewise Data"
pdf_books_lines_data_dir_path = "/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/2.All Books Combined Linewise Data"

stats_dir_path = "/home/cle-dl-05/Documents/3.PdfOCR/3.Scripts/pdf_dataset_creation_scripts/stats"

dataset_path_25k_images = "/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/2.Training/2.New Dataset 25k"
dataset_25k_stats = "/home/cle-dl-05/Documents/3.PdfOCR/3.Scripts/pdf_dataset_creation_scripts/stats/dataset_25k_stats.csv"

train_path = "/home/cle-dl-05/Documents/3.PdfOCR/1.Code/1.Code_v1/1.Train/data/MMA-UD/train"

book_name_prefixes = [
    # contains the name prefixes of pdf books and their corresponding text files.
    'Aina Khan-e-Iqbal',
    'Al Jihad Fil Islam',
    'Andaz-e-Mehrmana',
    'Arooj-e-Iqbal',
    'Darbar-e-Akbari',
    'Hayat-e-Iqbal',
    'Hazrat Abu Bakar Siddique',
    'Hikmat-e-Iqbal',
    'Hiyat-e-Muhammad(SAW)'
]

'/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/1.All Books Combined Pagewise Data/texts/Hayat-e-Iqbal_pg15.txt'

