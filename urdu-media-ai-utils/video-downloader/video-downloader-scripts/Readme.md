# **YouTube Video Downloader**

## **Project Overview**
This project automates the downloading of YouTube videos from a list of links provided in a text file. It utilizes the **pytube** and **youtube-dl** libraries to fetch and save videos in `.mp4` format. The project also supports login authentication for private or restricted videos.

---

## **Directory Structure**

### **1. Configuration File**
#### `config.py` – Configuration Settings  
This file contains key parameters for video downloading:
- **`links_file`**: Path to the text file containing YouTube video links.
- **`output_dir`**: Directory where downloaded videos will be saved.
- **`username`** *(optional)*: Username for login authentication (if required).
- **`password`** *(optional)*: Password for login authentication (if required).

### **2. Video Downloader Script**
#### `download.py` – Video Downloading Script  
This script reads YouTube links from the specified text file and downloads them as `.mp4` files.
- Supports batch downloading.
- Handles login authentication if credentials are provided.
- Saves videos in the specified output directory.

---

## **Usage Instructions**

### **1. Install Dependencies**
Ensure you have the required libraries installed:
```bash
pip install pytube youtube-dl
```

### **2. Configure Settings**
Update `config.py` with the appropriate file paths and credentials (if needed).

### **3. Run the Downloader**
Execute the script to start downloading videos:
```bash
python download.py
```

---

## **Additional Features**
- Supports both **pytube** and **youtube-dl** for enhanced compatibility.
- Downloads videos in **high quality** `.mp4` format.
- Provides **batch processing** for multiple video links.
- Includes **authentication support** for private videos.

For further improvements or custom requirements, modify `download.py` as needed.

---

## **License**
This project is released under [Insert License Here].

