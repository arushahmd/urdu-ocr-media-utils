import os

def combine_text_files(folder_path, output_file):
    # Get all text files from the folder
    text_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    # Sort the text files alphabetically
    text_files.sort()

    # Open the output file in write mode
    with open(output_file, "w", encoding="utf-8") as outfile:
        # Iterate through the sorted text files
        for filename in text_files:
            # Build full file path
            file_path = os.path.join(folder_path, filename)
                
            # Open each text file and read its content
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                
            # Write the filename and its content to the output file
            outfile.write(f"{filename}: {content},\n")

    print(f"All text files have been combined and sorted into {output_file}")

# Example usage
folder_path = "/media/cle-nb-183/New Volume/CLE/2. Testing Data/3. analysis/1. New Technique Analysis/5. categorized data/2. ip/colored"  # Replace with your folder path
output_path = os.path.join(folder_path, "combined_text.txt")
combine_text_files(folder_path, output_path)

