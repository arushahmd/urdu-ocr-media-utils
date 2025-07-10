# 🧾 Urdu OCR & Media Utilities

A modular AI-powered toolkit for processing Urdu PDFs, images, and video content. This repository combines tools originally developed across **two real-world projects**:

- 📄 `pdf-to-urdu-text`: A Django-based OCR API for converting scanned Urdu PDFs and images into structured text.
- 🧪 `urdu-media-ai-utils`: Utility modules for Urdu text annotation, YouTube media downloading, and end-to-end testing.

These components were merged to streamline the entire Urdu media processing pipeline — from input to automation-ready outputs — for research, NLP tasks, or product deployment.

---

## 🧠 What’s Included

| Module | Source | Description |
|--------|--------|-------------|
| `ocr-api/` | from `pdf-to-urdu-text` | Perform OCR on scanned Urdu PDFs or image files via a Django backend. Returns structured line-by-line or page-by-page text in JSON. |
| `urdu-polygon-line-extractor/` | from `urdu-media-ai-utils` | Extracts individual line images from Urdu book pages using polygon annotations (VoTT). Supports OCR pipeline preprocessing. |
| `video-downloader/` | from `urdu-media-ai-utils` | A Django REST API and CLI tool to download YouTube videos for offline processing and transcription. |
| `selenium-e2e-tests/` | from `urdu-media-ai-utils` | End-to-end Selenium testing suite for simulating multi-user activity across transcription and OCR platforms. |

---

## 🚀 Use Cases

- 🔍 Urdu PDF & image text extraction via OCR
- ✂️ Annotation-based line cropping for scanned Urdu books
- 📥 Download and archive Urdu YouTube videos for transcription or processing
- 🧪 UI-based test automation for Urdu OCR and media systems

---

## 🏗 Project Structure

```bash
## 🏗 Project Structure

```bash
urdu-ocr-media-utils/
├── pdf-to-text-urdu/                    # Urdu PDF OCR backend and tools
│   ├── notebooks/                       # Jupyter notebooks for OCR evaluation and testing
│   ├── pdf-ocr-pipeline/                # Main image processing and model inference code
│   ├── pdf_pipeline_api/                # Django REST API for performing OCR
│   ├── static/                          # Static assets (CSS/JS/images for frontend)
│   ├── templates/                       # OCR utility UI (HTML templates)
│   ├── images/                          # Sample images for testing
│   ├── logs/                            # Logs generated during OCR
│   ├── Readme.md                        # Module-specific documentation
│   └── manage.py
├── urdu-media-ocr-vision-utils     # utilities, pdf to pages and images and more
├── urdu-polygon-line-extractor/    # Extract polygon-annotated line images
├── video-downloader/               # YouTube to .mp4 API
├── selenium-e2e-tests/             # Multi-user automation testing
└── README.md                       # Project overview

```

🔧 Setup Instructions
Each module is standalone and includes its own README.md.
In general:

Set up a virtual environment

```
Run pip install -r requirements.txt
```
Follow the module instructions to run servers, scripts, or pipelines

📸 Previews (Examples)
- 🧾 OCR Output: Urdu PDF → page-wise/line-wise structured text
- ✂️ Polygon Extraction: VoTT-annotated Urdu page → cropped lines
- 📥 Video Downloader: YouTube links → local video files
- 🧪 Selenium UI Tests: Simulate login, upload, and transcription steps

### ✅ What's Improved
- Clear mention of **both original repos**
- Strong positioning of this as a **consolidated OCR + media system**
- Highlights real-world use cases, structure, and modularity
- Still simple to navigate and professional in tone

Let me know if you'd like to:
- Add example screenshots or links to notebooks
- Convert this to a `README.md` file and push it for you
- Localize to Urdu/English hybrid for audience in Pakistan or Urdu-speaking researchers

## 👨‍💻 Author
**Aroosh Ahmad**
AI Engineer | Python Developer | Urdu NLP & CV Enthusiast

<p align="left"> <a href="https://linkedin.com/in/arooshahmad-data"> <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" /> </a> <a href="https://github.com/arooshahmad-data"> <img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white" /> </a> <a href="https://www.kaggle.com/arooshahmad"> <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=flat&logo=kaggle&logoColor=white" /> </a> </p>

✨ This is an actively evolving repository focused on real-world Urdu NLP, OCR, and automation systems.
Contributions, feedback, and collaboration are welcome.




