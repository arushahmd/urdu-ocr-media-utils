# 🧾 Urdu OCR & Media Utilities

A modular toolkit for processing Urdu PDFs, images, and video content using AI-powered tools — including OCR APIs, polygon-based annotation extractors, YouTube video downloaders, and Selenium-based end-to-end testing workflows. Built to support real-world Urdu media processing, automation, and research tasks.

---

## 🧠 What’s Included

| Module | Description |
|--------|-------------|
| `ocr-api/` | Perform OCR on scanned Urdu PDFs or image files via a FastAPI/Django backend. Returns structured line-by-line or page-by-page text. |
| `urdu-polygon-line-extractor/` | Extracts individual line images from Urdu book pages using polygon annotations (e.g. from VoTT). Supports OCR pipeline preprocessing. |
| `video-downloader/` | A REST API and CLI tool to download YouTube videos for offline media processing or transcription. |
| `selenium-e2e-tests/` | End-to-end Selenium testing suite simulating multi-user activity on Urdu transcription and video analysis platforms. |

---

## 🚀 Use Cases

- Automated Urdu PDF & image OCR
- Line-level annotation preprocessing
- YouTube-based Urdu video transcription workflows
- Test automation for Urdu language platforms

---

## 🏗 Project Structure

```bash
urdu-ocr-media-utils/
├── ocr-api/                         # Upload image/PDF and get Urdu OCR output
├── urdu-polygon-line-extractor/    # Extract polygon-annotated text lines
├── video-downloader/               # Download Urdu videos via link lists
├── selenium-e2e-tests/             # End-to-end UI automation scripts
└── README.md                       # Project overview
```

---

## ⚙️ Tech Stack

- **Languages & Frameworks**: Python, Django, FastAPI, Selenium, HTML/JS, Bash
- **Libraries**: OpenCV, Pillow, pytube, youtube_dl, Tesseract OCR
- **Environments**: Python 3.10+, VS Code, Linux

---

## 🔧 Setup Instructions

Each module is self-contained. Navigate to the folder and follow the local `README.md` to:

- Set up virtual environments
- Install dependencies (`requirements.txt`)
- Run the tools or APIs locally

---

## 📸 Previews (Examples)

- OCR Output: Urdu PDF → line-by-line text JSON
- Polygon Extraction: Annotated Urdu book page → cropped text lines
- Video Downloader: YouTube URL → local .mp4 file
- Selenium Test: Automated browser navigation + form input simulation

---

## 👨‍💻 Author

**Aroosh Ahmad**  
AI Engineer | Python Developer | Urdu NLP & CV Enthusiast

<p align="left">
  <a href="https://linkedin.com/in/arooshahmad-data">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://github.com/arooshahmad-data">
    <img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white" />
  </a>
  <a href="https://www.kaggle.com/arooshahmad">
    <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=flat&logo=kaggle&logoColor=white" />
  </a>
</p>

---

> ✨ This toolkit is actively maintained and evolving. Feel free to fork, contribute, or contact for collaboration!
