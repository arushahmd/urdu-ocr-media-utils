# 📄 PDF Pipeline Utils  

## 📌 Overview  
**PDF Pipeline Utils** is a set of utilities designed to perform **OCR on PDF documents** through a structured multi-step process:  
1. **Convert PDF to individual pages**  
2. **Extract lines from each page**  
3. **Perform OCR** on the extracted line images  

## 🛠 Key Functionalities  
- 📄 **PDF to Pages:** Converts each PDF into individual image pages.  
- 🔍 **Page to Lines:** Segments each page into separate lines.  
- 🖥 **OCR Processing:** Runs OCR on the extracted line images to obtain text.

---

# Setting Up the Environment

## Option 1: Using PyCharm

### Create a New Conda Environment

1. Open PyCharm and navigate to `File` > `Settings` (or `Preferences` on macOS) > `Project` > `Project Interpreter`.
2. Click the gear icon and select `Add`.
3. Choose `Conda Environment` and follow the prompts to create a new environment.

## Option 2: Using Command Line

1. Run the following to create conda environment 
    ```bash
    conda create --name myenv python=3.8
2. Activate the environment
   ```bash
   conda activate myenv

### Install the Required Packages

In the terminal inside PyCharm, run:

```bash
pip install -r requirements.txt
