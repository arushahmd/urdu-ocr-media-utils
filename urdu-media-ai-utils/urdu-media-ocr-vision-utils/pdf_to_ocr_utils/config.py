# /home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/Annotated Books/
# /home/cle-dl-05/Desktop/Aroosh/2. Pdf Ocr Pipeline/output/book_pages/images/Al Jihad Fil Islam.pdf

PATH = "/media/cle-nb-183/New Volume/CLE/fonts.png" # path to pdf file or directory Darbar-e-Akbari_pg6.jpg
# PATH = "/home/cle-dl-05/Documents/3.PdfOCR/2.Datasets/1.Raw/Annotated Books/Aina Khan-e-Iqbal.pdf"
TEXT_PATH = "" # path to text file or directory

book_metadata_file = "output/books_metadata/Fatawa-Qasmia-Vol-01.xlsx"

DEBUG = False

# Given a path of directory will look into it for pdf files or images based on
# the below flags, to know what file format to search for, .pdf or images.
PROCESS_PDFS =  False
PROCESS_IMGS = True
OCR = False
THRESHOLD = 35

CONFIG = {
    # 'extract_pages': True,
    'extract_lines': False,
    'save_page_images': False,
    'save_line_images': True,
    'do_predictions': False, # if this is true then the predictions will be done and saved based on below flags.
    'save_line_predictions': True,
    'save_page_predictions': True,
    'save_book_predictions': False
}











