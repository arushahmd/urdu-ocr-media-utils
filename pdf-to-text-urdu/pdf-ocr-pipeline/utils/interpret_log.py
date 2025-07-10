import re
import pandas as pd
import os

# Define the log file path
log_file_path = "logs/ocr_log_20241126_112152/OCR_Log_20241126_112152(new_technique).txt"
output_csv_path = "logs/ocr_log_20241126_112152/log.csv"  # Change file extension to .csv

# Print the log file being processed
print(f"Reading log file from: {log_file_path}")

# Pattern to extract memory details and file name
pattern = r"before reading image: ([\d.]+ GB).*?after reading image: ([\d.]+ GB).*?before prediction: ([\d.]+ GB).*?after prediction: ([\d.]+ GB).*?after clearing session: ([\d.]+ GB).*?Processing (.+?) took"

# Prepare structured data (to be written to CSV)
data = []

# Open the log file and process line by line
with open(log_file_path, 'r') as file:
    for line in file:
        # Skip initial lines that are not useful
        if "Memory usage" not in line and "Processing" not in line:
            continue

        # Check if the current line matches the regex pattern
        match = re.search(pattern, line)

        if match:
            # If a match is found, extract the relevant information and append it to the data
            row = {
                "File Name": match.group(6),
                "Memory Usage Before Reading Image (Current)": match.group(1),
                "Memory Usage After Reading Image (Current)": match.group(2),
                "Memory Usage Before Prediction (Current)": match.group(3),
                "Memory Usage After Prediction (Current)": match.group(4),
                "Memory Usage After Clearing Session (Current)": match.group(5),
            }
            data.append(row)

            # Optionally, print the row for debugging purposes
            print(f"Match found: {row}")

# Print the number of matches found
print(f"Total matches found: {len(data)}")

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data)

# Check if any data was found before exporting
if not df.empty:
    # Ensure the directory for the output file exists
    output_dir = os.path.dirname(output_csv_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Export to CSV
    print(f"Exporting data to CSV: {output_csv_path}")
    df.to_csv(output_csv_path, index=False)  # Save as CSV instead of Excel
    print(f"Log data has been successfully converted to CSV: {output_csv_path}")
else:
    print("No matches found. No data was written to the CSV file.")
