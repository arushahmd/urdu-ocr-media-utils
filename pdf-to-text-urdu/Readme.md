
# Developer Guide for OCR API

## Overview
The `api/perform_ocr` endpoint allows users to perform OCR (Optical Character Recognition) on uploaded files. It supports both image and PDF files, returning the extracted text for each line or page within the file.

## API Endpoint

- **URL**: `api/perform_ocr`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Supported File Types**: `.pdf`, `.png`, `.jpg`, `.jpeg`

### Permissions
This endpoint does not require authentication or authorization (`AllowAny` permission), allowing public access for testing and development purposes.

## Request Parameters

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `file`    | File | Yes      | The file to process. Supported formats: `.pdf`, `.png`, `.jpg`, `.jpeg` |

## Example Request

### Using `curl`
```bash
curl -X POST "http://<your_domain>/api/perform_ocr" \
     -F "file=@/path/to/your/file.pdf"
```

### Using Python `requests`
```python
import requests

url = "http://<your_domain>/api/perform_ocr"
file_path = "/path/to/your/file.png"

with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": file})

print(response.json())
```

## API Environment

user ```ocr_tf1``` python environment to run this project. 

## Run API 
run the command 

``` python manage.py runserver 0.0.0.0:8000```
http://127.0.0.1:8000/utility/
or 

then to access use, 

```
http://10.0.0.12:8000/<your-url>
```
or
```
http://10.10.38.24:8000/<your-url>
```

## URLS:

```'utility/'``` : to run the utility page UI locally. 
```'api/perform_ocr/'```: to access api services.
```'download_scope_document/'```: to download the scope document
```'swagger/'```: to run swagger UI.

## Responses

### Success Responses
The API will return a JSON response containing either a single line prediction or predictions for multiple lines/pages.

#### Image File (`.png`, `.jpg`, `.jpeg`)
If the uploaded file is an image, the response will contain predicted text for each detected line.

- **Example Response (Single Line)**:
  ```json
  {
      "message": "File: image.png\nPredicted Text: This is the recognized text from the image."
  }
  ```

- **Example Response (Multiple Lines)**:
  ```json
  {
      "file": "image.png",
      "predicted_data": {
          "line_1": "First line of detected text.",
          "line_2": "Second line of detected text."
      }
  }
  ```

#### PDF File (`.pdf`)
If the uploaded file is a PDF, the response will contain OCR results for each page, with line-by-line predictions for each page.

- **Example Response**:
  ```json
  {
      "file": "document.pdf",
      "predicted_data": {
          "page_1": {
              "line_1": "First line of text from page 1.",
              "line_2": "Second line of text from page 1."
          },
          "page_2": {
              "line_1": "First line of text from page 2."
          }
      }
  }
  ```

### Error Responses
The following are possible error responses returned by the API.

| Status Code | Error                    | Description                                                              |
|-------------|--------------------------|--------------------------------------------------------------------------|
| 400         | `No file uploaded.`      | No file was provided in the request.                                     |
| 400         | `Unsupported file type`  | The uploaded file format is not supported. Only `.pdf`, `.png`, `.jpg`, and `.jpeg` are allowed. |
| 405         | `GET request not supported` | This endpoint does not support `GET` requests; use `POST` for file uploads. |

- **Example Error Response**:
  ```json
  {
      "error": "Unsupported file type. Only .pdf, .png, .jpg files are allowed."
  }
  ```

## Additional Notes

- **File Size Limit**: Ensure that the uploaded file meets any server-imposed size limits.
- **Response Time**: Large PDFs or images with many lines may take longer to process due to OCR complexity.
- **Usage in Applications**: Suitable for integration in web and mobile applications where OCR functionality is needed for image and document analysis.

