# Polygon-Based Line Extraction from Urdu Book Scans

This script is part of an **Urdu OCR** project and is used during the **annotation and 
data preparation** phase. It extracts polygon-annotated regions (typically Urdu text lines) 
from scanned book page images, based on annotations created using 
[VoTT](https://github.com/microsoft/VoTT) by Microsoft.

## Use Case
Some Urdu lines overlap or smudge (e.g., ```kaaf ki dandi interfering with yay above it```), 

- so polygon-shaped annotations were used to mark precise line regions instead or rectangular annotations.

## Folder Structure
```
    polygon-extraction-utility/
    ├── data-books/
    │   ├── B150/
    │   │   ├── Annotated/   # VoTT JSON annotation files
    │   │   ├── Image/       # Book page images
    │   │   └── Text/        # Text data (if any)
    ├── output/              # Extracted line images
    ├── extract_polygon_area_from_image.py
    ├── requirements.txt
    └── README.md
```

## How to Run
You need to provide three arguments in the script (```extract_polygon_area_from_image.py```):

```
    annotation_file = 'data-books/B150/Annotated/annotation.json'
    images_folder = 'data-books/B150/Image'
    output_folder = 'output'
```

Then run the script:

```commandline
    python extract_polygon_area_from_image.py
```

## Requirements
 The requirements are in ```requirements.txt```
``````
# Python Version
python_version >=3.10,<3.11

# Required Libraries
Pillow~=10.0.0