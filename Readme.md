# 🧾 Urdu OCR & Media Utilities

A modular AI-powered toolkit for processing Urdu PDFs, images, and video content. This repository merges tools from **two real-world projects**:

- `pdf-to-urdu-text`: Django-based OCR API for scanned Urdu PDFs and images.
- `urdu-media-ai-utils`: Utilities for Urdu text annotation, YouTube media downloading, and end-to-end testing.

This consolidated repository streamlines the entire Urdu media processing pipeline — from input to automation-ready outputs — for research, NLP, or product deployment. It is actively maintained and will continue to be updated with new features and improvements.

---

## 🧠 Included Modules

| Module | Source | Description |
|--------|--------|-------------|
| `ocr-api/` | `pdf-to-urdu-text` | OCR on scanned Urdu PDFs/images via Django. Outputs structured line/page text in JSON. |
| `urdu-polygon-line-extractor/` | `urdu-media-ai-utils` | Extracts individual line images using polygon annotations (VoTT) for preprocessing. |
| `video-downloader/` | `urdu-media-ai-utils` | Django REST API & CLI tool to download YouTube videos for offline processing/transcription. |
| `selenium-e2e-tests/` | `urdu-media-ai-utils` | End-to-end Selenium testing simulating multi-user activity across OCR and transcription flows. |

---

## 🚀 Use Cases

- Extract text from Urdu PDFs and images.
- Crop lines from scanned Urdu books using polygon annotations.
- Download and archive Urdu YouTube videos for processing.
- Automate testing of Urdu OCR and media workflows.

---

## 🏗 Project Structure

```bash
urdu-ocr-media-utils/
├── pdf-to-text-urdu/                  # Urdu PDF OCR backend and tools
│   ├── notebooks/                     # Jupyter notebooks for evaluation/testing
│   ├── pdf-ocr-pipeline/              # Main image processing and inference
│   ├── pdf_pipeline_api/              # Django REST API for OCR
│   ├── static/                        # CSS/JS/images for frontend
│   ├── templates/                     # HTML templates for OCR UI
│   ├── images/                        # Sample images
│   ├── logs/                          # OCR logs
│   ├── Readme.md                      # Module-specific docs
│   └── manage.py
├── urdu-media-ocr-vision-utils/       # Utilities: PDF → pages/images and more
├── urdu-polygon-line-extractor/       # Polygon-based line extraction
├── video-downloader/                  # YouTube to .mp4 API
├── selenium-e2e-tests/                # Multi-user automation testing
└── README.md                           # Project overview
```

## 🔧 Setup Instructions
Each module is standalone and contains its own README.md. In general:
Set up a Python virtual environment:
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

## Install dependencies:
```
pip install -r requirements.txt
```
Follow individual module instructions to run servers, scripts, or pipelines.

📸 Previews (Examples)
- OCR Output: Urdu PDF → structured page/line-wise text.
- Polygon Extraction: VoTT-annotated page → cropped lines.
- Video Downloader: YouTube links → local video files.
- Selenium Tests: Simulate login, upload, and transcription workflows.

**Author:** Aroosh Ahmad — AI Engineer (NLP, LLMs, ML Systems) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[GitHub](https://github.com/arushahmd) • [LinkedIn](https://www.linkedin.com/in/arooshahmad-data/)
