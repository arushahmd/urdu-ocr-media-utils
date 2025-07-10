# YouTube Video Downloader  

## Project Overview

This repository provides two ways to download YouTube videos using pytube and youtube_dl:

- A Django REST API in ```video-downloader-api/```

- Standalone scripts in ```video-downloader-scripts/```
- 
It supports public and private videos (via login), 
with fallback from ```youtube_dl``` to ```pytube``` on failure.

## Django API (video-downloader-api/)

This is a Django-based service that downloads YouTube videos from links provided in .txt files. 
It supports public and private videos using authentication if needed, and uses either ```youtube_dl``` or ```pytube```.

- If ```youtube_dl``` fails, it falls back to ```pytube```.

###  How it works  

1. Upload a ```.txt``` file with YouTube links.
2. The system downloads each video and saves it to temp_files/output/..  

##### API Endpoint    

```
 "http://127.0.0.0:<your-port>/api/download-videos/"
```
      
**Input:** ```.txt``` file (one YouTube link per line)

**Output:** Paths of downloaded videos + status per link


## Standalone Scripts (video-downloader-scripts/)

Run via terminal:

```
python download_videos.py
# or
python test_download.py
```

#### Script Config

Edit at top of the script:

```
links_file = "video_links.txt" # file containing video links
output_folder = "downloads" # folder to download videos to
``` 
Optional:

```
youtube_username = ""  # Only needed for restricted videos
youtube_password = ""  # Only needed for restricted videos
```

## Folder Structure

```
video-downloader/
├── video-downloader-api/             # Contains the Django API logic
│   ├── videodownloader/              # Django app with API logic
│   ├── manage.py
│   ├── settings.py, urls.py, etc.
│   ├── video-urls/                   # Text files with YouTube links (API use)
│   ├── temp_files/                   # Holds downloaded videos for API
│   │   └── output/
│
├── video-downloader-scripts/         # Standalone Python scripts
│   ├── download_videos.py
│   ├── test_download.py
│   ├── downloads/                    # Folder for script-based downloads
│
├── requirements.txt                  # Dependencies for both API and scripts
├── README.md                         # Project documentation
└── .gitignore
```

## Environment
- ```Python version```: 3.10

- ```Django version```: 4.2.2 or lower (higher versions may cause compatibility issues)

- ```Recommended environments```: ocr_tf1, ocr-3.6


## Requirements

   The ```requirements.txt``` file contains all the necessary requirements to run this project.

```
Django~=4.2
pytube~=15.0.0
youtube_dl~=2021.12.17
djangorestframework~=3.14.0
```
