# urdu-media-ai-utils
A collection of modular tools and scripts for processing Urdu media using AI, including OCR for scanned PDFs, polygon-based annotation utilities, YouTube video downloading, and end-to-end Selenium testing for Urdu language platforms. Designed for research automation and production-ready Urdu media workflows.

This repository contains code-only implementations of selected modules I developed as part of a broader Urdu media analysis system. 

This repository focuses on:

- 🧾 OCR and Annotation Utilities for Urdu scanned book pages

- 📹 YouTube Video Downloading for offline media processing

- 🧪 End-to-End Selenium Testing for verifying multi-user functionality

Each module is self-contained, with:

- Its own README file

- Clear setup and usage instructions

- Example configurations or scripts to help you run it independently

 🔍 These tools were developed primarily for OCR, Urdu News Processing, and automated testing workflows — and can serve as strong templates or foundations for similar projects involving annotation, media automation, and testing.

---

## Modules Included

###  `urdu-polygon-line-extractor`
Utility to extract individual line images from Urdu book page images annotated with polygons (from VoTT).  
Used in OCR pipeline of scanned Urdu books.  
📄 [See module README](./urdu-polygon-line-extractor/README.md)

---

###  `video-downloader`
A Django REST API and Python scripts to download videos from YouTube using a list of links.  
Useful when analyzing media content where users provide video URLs.  
📄 [See module README](./video-downloader/README.md)

---

###  `selenium-e2e-tests`
Selenium-based end-to-end testing module to simulate multi-user activity on various parts of the web system for Urdu OCR and Video Analysis  (login, transcription, summary, etc.).  
📄 [See module README](./selenium-e2e-tests/README.md)

---

## 🛠 Tech Stack

- **Python 3.10**
- **Django 4.2**
- **Selenium**
- **Pillow**, **pytube**, **youtube_dl**
- OCR, Computer Vision, NLP and Image Processing techniques used in related systems

---

##  Development Environment

For development and testing:
- Setup Python 3.10 virtual environment
- Use `requirements.txt` from each module
- Each module is standalone and includes its own README with setup instructions

---

##  Author

**Aroosh Ahmad**  
AI Engineer | Python Developer | Computer Vision & NLP Enthusiast  
[LinkedIn](https://www.linkedin.com/in/arooshahmad-data) | [Email](mailto:arooshahmad.data@gmail.com)



