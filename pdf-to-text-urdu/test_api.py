import requests

# url = "http://127.0.0.1:8020/api/perform_ocr"
url = "http://10.10.38.24:8000/api/perform_ocr"
file_path = "/media/cle-nb-183/New Volume/CLE/pdf_pipeline_api/Hiyat-e-Muhammad(SAW)_pg239_ln11.jpg"

with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": file})

print(response.json())