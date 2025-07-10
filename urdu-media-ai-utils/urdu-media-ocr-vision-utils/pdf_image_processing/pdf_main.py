import yaml
from pdf_to_page_images_and_text import pdf_main
from scripts.pages_data_to_lines import page_to_lines_image_and_text

yaml_file_path = "D:/PdfOcr/Pdf Dataset/scripts/config.yaml"

with open(yaml_file_path, 'r') as file:
    data = yaml.safe_load(file)

if data["EXTRACT_PAGES"]:
    """
        Save Path is where images and the texts will be saved, this folder will have images and texts directories
    """
    pdf_main(data["PDF_PATH"], data["book_name_prefixes"], data["SAVE_PATH"])
else:
    """
        Used to Extract Line Images and Corresponding Text From Page Images and Texts.
    """

    page_to_lines_image_and_text(data["DIR_IMAGES_TEXTS_MAIN"], data["LINE_DATA_SAVE_PATH"], data["STATS_LINE_DATA"])