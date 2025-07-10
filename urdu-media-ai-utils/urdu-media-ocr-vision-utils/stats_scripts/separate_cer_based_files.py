import os
import pandas as pd
import shutil


def organize_files(excel_folder, images_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all files in the Excel folder
    for file_name in os.listdir(excel_folder):
        print(f"\n###############################\n"
              f"Reading File : {file_name}"
              f"\n###############################\n")
        file_path = os.path.join(excel_folder, file_name)

        # Only process if it's an Excel or CSV file
        if file_name.endswith('.xlsx') or file_name.endswith('.csv'):
            # Load the data from Excel or CSV
            if file_name.endswith('.xlsx'):
                df = pd.read_excel(file_path, engine='openpyxl')
            else:
                df = pd.read_csv(file_path)

            # Remove NaN values
            df = df.iloc[:, :5]
            df = df.dropna()

            # Normalize the 'CER' column to handle both numeric and string formats
            def normalize_cer(value):
                if isinstance(value, str) and '%' in value:
                    # Remove the '%' and convert to float
                    return float(value.replace('%', ''))
                elif isinstance(value, float) and value <= 1:
                    # Convert decimal to percentage
                    return value * 100
                return float(value)


            # Ensure 'CER' column is treated as strings, then remove '%' and convert to float
            # df['CER'] = df['CER'].astype(str).str.replace('%', '').astype(float)
            df['CER'] = df['CER'].apply(normalize_cer)
            print(f"Processed CER values from {file_name}: {df['CER'].unique()}")  # Debug output

            # Remove file extension from file name to use for folder naming
            base_file_name = os.path.splitext(file_name)[0]

            # Create a main folder for this Excel file in the output directory
            main_output_folder = os.path.join(output_folder, base_file_name)
            os.makedirs(main_output_folder, exist_ok=True)

            # Define the CER ranges and respective folder names
            cer_ranges = {
                '0-20': (0, 20),
                '21-40': (21, 40),
                '41-60': (41, 60),
                '61-100': (61, 100)
            }

            # Process each CER range
            for folder_name, (min_cer, max_cer) in cer_ranges.items():
                range_folder = os.path.join(main_output_folder, folder_name)

                # Filter the rows based on CER percentage range
                filtered_df = df[(df['CER'] >= min_cer) & (df['CER'] <= max_cer)]

                print(f"Filtered {folder_name} range: {filtered_df}")  # Debug output

                # Check if there are any files to process for this range
                if not filtered_df.empty:
                    os.makedirs(range_folder, exist_ok=True)

                    # Loop through each row in the filtered DataFrame
                    for _, row in filtered_df.iterrows():
                        filename = str(row['Filename'])  # Ensure filename is treated as a string

                        # Ensure actual_text and predicted_text are strings
                        actual_text = str(row['Actual'])  # Column for actual text
                        predicted_text = str(row['Prediction'])  # Column for predicted text

                        # Save actual text to a .txt file with a new name
                        actual_txt_name = os.path.join(range_folder, f"{filename}_actual.txt")
                        with open(actual_txt_name, 'w', encoding='utf-8') as f:
                            f.write(actual_text)

                        # Save predicted text to a .txt file with a new name
                        predicted_txt_name = os.path.join(range_folder, f"{filename}_predicted.txt")
                        with open(predicted_txt_name, 'w', encoding='utf-8') as f:
                            f.write(predicted_text)

                        # Construct the image file path by replacing the .txt extension with .jpg
                        image_name = filename.rsplit('.', 1)[0] + '.jpg'  # Replace .txt with .jpg
                        image_path = os.path.join(images_folder, image_name)
                        if os.path.isfile(image_path):
                            shutil.copy(image_path, range_folder)

    print("Files organized successfully.")


# Example usage
organize_files(
    excel_folder='/media/cle-nb-183/New Volume/CLE/2. Testing Data/4.CER_LER_stats/wp',
    images_folder='/media/cle-nb-183/New Volume/CLE/2. Testing Data/3. analysis/1. New Technique Analysis/1. lines/1. wp',
    # output_folder='/media/cle-nb-183/New Volume/CLE/2. Testing Data/4.CER_LER_stats/3.categorized based on cer/1.wp'
    output_folder='/media/cle-nb-183/New Volume/CLE/2. Testing Data/4.CER_LER_stats/3.categorized based on cer/1.wp'
)
