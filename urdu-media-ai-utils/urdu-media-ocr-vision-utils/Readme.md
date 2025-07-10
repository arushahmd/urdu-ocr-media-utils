# urdu-media-ocr-vision-utils
This repository provides a comprehensive collection of utilities and scripts for 
**OCR processing, object detection, annotation conversion, dataset preparation, 
and statistics generation** specifically tailored for ```Urdu-language news media 
datasets```. 

It is structured to support modular development, allowing users to 
work with ```PDF processing, image generation, annotation formats, and model inference```.

## Project Structure

```
  urdu-media-ocr-vision-utils/
  │
  ├── 1. pdf-image-processing/            # Scripts for converting PDFs to page and line images
  │
  ├── 2. media-dataset-tools/            # Scripts to create datasets based on criteria such as news ticker positions
  │
  ├── 3. annotation-conversion-utils/    # Conversion scripts and helpers for annotations (XML, JSON, YOLO)
  │
  ├── 4. inference-scripts/              # Model inference and result analysis scripts
  │
  ├── 5. stats-scripts/                  # Scripts to compute text and layout statistics on Urdu datasets
  │
  ├── 6. statistics/                     # CSV files with precomputed statistics on different dataset variants
  │
  ├── utils/                             # General-purpose helper functions and configuration scripts
  │
  ├── .git/, .idea/, __pycache__/        # Version control and IDE-related directories
  │
  ├── config.py                          # Configuration for running the scripts
  ├── config.yaml                        # Optional YAML-based configuration
  ├── Readme.md                          # Project documentation
  ├── sss.py                             # Temporary or experimental script
  └── __init__.py                        # Marks the module as importable
```

## Key Features

**PDF to Image Conversion**  
Convert Urdu news PDFs into page-level and line-level images.

**Dataset Creation Utilities**  
Generate datasets from images based on positional metadata like ticker placement (top, middle, bottom) or balanced sampling.

**Annotation Format Conversion**  
Convert between XML, JSON (VoTT), and YOLO formats. Also includes annotation utilities for parsing and inspection.

**Corrupted Data Handling**  
Identify and remove problematic or incomplete data entries automatically.

**Connected Components & Layout Statistics**  
Scripts for computing page layout structure using connected components, text density, and other layout metrics.

**Inference Scripts**  
Run inference on datasets and optionally generate evaluation metrics such as accuracy, IoU, and confidence levels.

**Precomputed Statistics**  
Includes CSV summaries of channel-wise distributions, text statistics, and other key indicators.

## Setup Instructions
Ensure Python 3.9+ is installed. Create a virtual environment and install dependencies.

```
  python -m venv venv
  source venv/bin/activate  # on Windows: venv\Scripts\activate
  pip install -r requirements.txt  # if provided
```

## Usage
Each directory contains independently runnable scripts. Below are some examples:

```

  # Convert PDF to images and lines
  python 1. pdf-image-processing/pdf_to_pages_and_lines.py
  
  # Create dataset based on strip position
  python 2. media-dataset-tools/dataset_based_on_strip_position.py
  
  # Convert XML annotations to YOLO
  python annotation-conversion-utils/xml_to_yolo.py
  
  # Run model inference with statistics
  python inference-scripts/inference_with_stats.py

```

## Contributions
This repository is actively maintained and open to collaboration. 
If you find bugs or would like to suggest enhancements, please create 
an issue or submit a pull request.

