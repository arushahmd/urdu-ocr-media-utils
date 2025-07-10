import csv
import os
from datetime import datetime
from datetime import timedelta

import cv2
import numpy as np
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from pdf_ocr_pipeline.convert_to_lines import page_to_lines_updated
from pdf_ocr_pipeline.convert_to_pages import pdf_to_pages
from pdf_ocr_pipeline.predict_and_save import get_model, do_pred
from pdf_pipeline_api.config import DEBUG


def view_utility_page(request):
    return render(request, "utility_page.html")


LOG_FILE_PATH = "logs/ocr_process_log.csv"

LOG_COLUMNS = ["File Name", "Process", "Start Time", "End Time", "Duration", "Status"]


# Initialize the log file (create if not exists, write headers)
def initialize_log_file():
    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=LOG_COLUMNS)
            writer.writeheader()


# Append a log entry
def log_entry(file_name, process, start_time, end_time, status):
    duration = end_time - start_time  # Calculate duration as a timedelta object
    duration_str = str(duration)  # Convert to string in HH:MM:SS format

    # Ensure duration is formatted as HH:MM:SS, even if it's less than one hour.
    if isinstance(duration, timedelta):
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"

    with open(LOG_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=LOG_COLUMNS)
        writer.writerow({
            "File Name": file_name,
            "Process": process,
            "Start Time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "End Time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Duration": duration_str,
            "Status": status
        })


class PerformOcr(APIView):
    permission_classes = [AllowAny]  # No authorization required
    parser_classes = [MultiPartParser, FormParser]  # Ensures correct parsing for file uploads

    def __init__(self):
        self.model = get_model('pdf_ocr_pipeline/configs/CNN_RNN_CTC/MMA-UD.json')
        self.width_thres = 40
        self.height_thres = 50
        self.DEBUG = DEBUG  # Toggle debug mode for saving files
        self.output_folder = "output"  # Base output folder
        self.log_file = "output/ocr_process_log.csv"

        initialize_log_file()

    def get(self, request, *args, **kwargs):
        """
        No GET implementation for now.
        """
        return Response({"message": "GET request not supported for this endpoint."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE,
                              description="Upload a file (.pdf, .png, .jpg)")
        ],
        responses={
            200: 'File uploaded successfully',
            400: 'Invalid file type or no file provided',
        }
    )

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        file_extension = file.name.split('.')[-1].lower()
        if file_extension not in ['pdf', 'png', 'jpg', 'jpeg']:
            return Response({"error": "Unsupported file type. Only .pdf, .png, .jpg files are allowed."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Process the file based on its type
        if file_extension in ['png', 'jpg', 'jpeg']:
            return self.process_image(file)
        elif file_extension == 'pdf':
            return self.process_pdf(file)

    def save_debug_files(self, base_folder, sub_folder, file_name, content, is_image=False):
        """Helper function to save debug files."""
        save_path = os.path.join(base_folder, sub_folder)
        os.makedirs(save_path, exist_ok=True)
        file_path = os.path.join(save_path, file_name)
        if is_image:
            cv2.imwrite(file_path, content)  # Save image
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)  # Save text

    def process_image(self, file):
        """Process an image file and return OCR results."""
        image_data = file.read()  # Read the image file into memory
        img_cv2 = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)  # Decode into OpenCV image

        file_name = os.path.splitext(file.name)[0]
        output_base = os.path.join(self.output_folder, os.path.splitext(file.name)[0])

        # 1. Extract Lines from the Page
        print("Extracting Lines ......")
        start_time = datetime.now()
        try:
            line_images = page_to_lines_updated(img_cv2)
            end_time = datetime.now()
            log_entry(file_name, "Page to Lines", start_time, end_time, "Success")
            print(f"Extracted {len(line_images)} Lines.")
        except Exception as e:
            end_time = datetime.now()
            log_entry(file_name, "Page to Lines", start_time, end_time, "Failure")
            print(f"Failed to extract lines. Exception: {e}")
            return Response({"error": "Failed to extract lines from the image."},
                            status=status.HTTP_400_BAD_REQUEST)

        # 2. If No Lines Detected, Return Error
        if not line_images:
            return Response({"error": "OCR failed to detect any text in the image."},
                            status=status.HTTP_400_BAD_REQUEST)

        # 3. OCR on Each Line
        predicted_data = {}
        start_time = datetime.now()

        for count, line_image in enumerate(line_images):
            print(f"Processing Line {count + 1}...")
            height, width, _ = line_image.shape

            if height > 25 and width > 70:
                if self.DEBUG:
                    self.save_debug_files(output_base, "lines", f"line_{count + 1}.png", line_image, is_image=True)

                try:
                    line_start_time = datetime.now()
                    prediction = do_pred(line_image, self.model)
                    line_end_time = datetime.now()

                    predicted_data[f'line_{count + 1}'] = prediction
                    log_entry(file_name, f"OCR on Line {count + 1}", line_start_time, line_end_time, "Success")

                    if self.DEBUG:
                        self.save_debug_files(output_base, "predictions", f"line_{count + 1}.txt", prediction)
                except Exception as e:
                    print(f"Prediction failed for Line {count + 1}. Exception: {e}")
                    # Log the failure for this line but continue processing the next line
                    continue
            else:
                print("Image to small to be processed!.")

        end_time = datetime.now()
        log_entry(file_name, "OCR", start_time, end_time, "Success")

        return Response({
            "file": file.name,
            "predicted_text": predicted_data
        }, status=status.HTTP_200_OK)

    def process_pdf(self, file):
        """Process a PDF file and return OCR results."""
        pdf_data = file.read()
        file_name = os.path.splitext(file.name)[0]
        output_base = os.path.join(self.output_folder, file_name)
        predicted_data = {}

        # Initialize variables for storing extracted text
        full_text_output = []
        page_texts = {}  # Store page-wise text separately

        # 1. Extract Pages
        print("Extracting Pages...")
        try:
            start_time = datetime.now()
            page_images = pdf_to_pages(pdf_data, save=False, book_name=file_name)
            end_time = datetime.now()
            log_entry(file_name, "PDF to Pages", start_time, end_time, "Success")
            print(f"Extracted {len(page_images)} pages from the PDF.")

            # Save extracted pages
            if self.DEBUG:
                for page_name, page_image in page_images.items():
                    self.save_debug_files(output_base, "pages", f"{page_name}.png", page_image, is_image=True)
        except Exception as e:
            end_time = datetime.now()
            log_entry(file_name, "PDF to Pages", start_time, end_time, "Failure")
            print(f"Failed to extract pages from the PDF. Exception: {e}")
            return Response({"error": "Failed to process PDF to pages."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Process Each Page
        for count, (page_name, page_image) in enumerate(page_images.items(), start=1):
            print(f"Processing Page {count}...")

            # Extract Lines from Page
            print(f"Extracting Lines from Page {count}...")
            try:
                start_time = datetime.now()
                line_images = page_to_lines_updated(page_image)
                end_time = datetime.now()
                log_entry(file_name, f"Page {count} to Lines", start_time, end_time, "Success")
                print(f"Extracted {len(line_images)} lines from Page {count}.")

                if self.DEBUG:
                    for line_index, line_image in enumerate(line_images):
                        self.save_debug_files(output_base, "lines", f"{page_name}_line_{line_index + 1}.png",
                                              line_image,
                                              is_image=True)
            except Exception as e:
                end_time = datetime.now()
                log_entry(file_name, f"Page {count} to Lines", start_time, end_time, "Failure")
                print(f"Failed to extract lines from Page {count}. Exception: {e}")
                continue

            # Skip pages with no detected lines
            if not line_images:
                predicted_data[page_name] = {"error": "No text detected in this page."}
                continue

            # Perform OCR on Each Line
            page_predictions = {}
            page_text = []  # Start collecting text for the current page
            for line_count, line_image in enumerate(line_images, start=1):
                if line_image.shape[0] < self.width_thres or line_image.shape[1] < self.height_thres:
                    print(f"Skipping Line {line_count} of Page {count} due to insufficient dimensions.")
                    continue

                try:
                    start_time = datetime.now()
                    prediction = do_pred(line_image, self.model)
                    end_time = datetime.now()
                    log_entry(file_name, f"Line {line_count} OCR on Page {count}", start_time, end_time, "Success")
                    page_predictions[f"line_{line_count}"] = prediction
                    page_text.append(prediction)  # Append line prediction to the page text

                    if self.DEBUG:
                        self.save_debug_files(output_base, "predictions", f"{page_name}_line_{line_count}.txt",
                                              prediction)
                except Exception as e:
                    end_time = datetime.now()
                    log_entry(file_name, f"Line {line_count} OCR on Page {count}", start_time, end_time, "Failure")
                    print(f"Failed OCR for Line {line_count} of Page {count}. Exception: {e}")
                    continue

            # Save page text
            page_texts[page_name] = "\n".join(page_text)  # Join all lines for the page
            predicted_data[page_name] = page_predictions

            # Save full page text if DEBUG is enabled
            if self.DEBUG:
                self.save_debug_files(output_base, "page_texts", f"{page_name}.txt", page_texts[page_name])

            # Add the page text to the full text output
            full_text_output.append(page_texts[page_name])

        # Save the full extracted text of the entire document to a text file
        try:
            full_text_filename = os.path.join(output_base, f"{file_name}.txt")
            with open(full_text_filename, 'w') as full_text_file:
                full_text_file.write("\n\n".join(full_text_output))  # Join pages with double newline
            print(f"Full extracted text saved to {full_text_filename}.")
        except Exception as e:
            print(f"Failed to save full text file. Exception: {e}")

        # Save page-wise text to individual files
        try:
            page_text_folder = os.path.join(output_base, "page_texts")
            os.makedirs(page_text_folder, exist_ok=True)
            for page_name, page_text in page_texts.items():
                page_file_path = os.path.join(page_text_folder, f"{page_name}.txt")
                with open(page_file_path, 'w') as page_file:
                    page_file.write(page_text)
            print("Page-wise texts saved successfully.")
        except Exception as e:
            print(f"Failed to save page-wise text files. Exception: {e}")

        # Final Logging and Return Response
        print("All pages processed successfully.")
        return Response({
            "file": file.name,
            "predicted_data": predicted_data
        }, status=status.HTTP_200_OK)


def download_scope_document(request):
    # Construct the file path from the static folder
    filename = 'PDF OCR Pipeline Scope.docx'
    file_path = os.path.join(settings.BASE_DIR, 'static', 'files', filename)

    # Check if the file exists
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        # Handle file not found
        return HttpResponse("File not found", status=404)
