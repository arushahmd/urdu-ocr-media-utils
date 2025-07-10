import os
import csv

def classify_files(combined_text_file, threshold, output_good_bad_file, output_summary_file):
    good_files = []
    bad_files = []
    book_stats = {}

    # Open the combined text file for reading
    with open(combined_text_file, "r", encoding="utf-8") as infile:
        # Iterate over each line in the combined file
        for line in infile:
            if ": " in line:
                # Extract the file name and content
                file_name, content = line.split(": ", 1)
                
                # Check if content length is above or below the threshold
                if len(content.strip()) > threshold:
                    good_files.append(file_name)
                else:
                    bad_files.append(file_name)

                # Extract book name from the file name (assuming file names are like 'bookname_<whatever>.txt')
                book_name = file_name.split('_')[0]

                # Update the book's stats
                if book_name not in book_stats:
                    book_stats[book_name] = {"good": 0, "bad": 0}
                
                if len(content.strip()) > threshold:
                    book_stats[book_name]["good"] += 1
                else:
                    book_stats[book_name]["bad"] += 1

    # Write the file names of good and bad files to a CSV
    with open(output_good_bad_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Name", "Status"])  # Header

        for file in good_files:
            writer.writerow([file, "Good"])
        for file in bad_files:
            writer.writerow([file, "Bad"])

    # Write the book stats summary to another CSV
    with open(output_summary_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Book Name", "Good Files", "Bad Files"])  # Header

        for book_name, stats in book_stats.items():
            writer.writerow([book_name, stats["good"], stats["bad"]])

    print(f"Classification completed. Good and bad files listed in {output_good_bad_file}, summary in {output_summary_file}.")


# Example usage
combined_text_file = "/media/cle-nb-183/New Volume/CLE/2. Testing Data/3. analysis/1. New Technique Analysis/5. categorized data/2. ip/other lang/combined_text.txt"  # The input file containing filenames and content
threshold =9   # Example threshold for content length

# Output CSV file paths
stats_path = "/media/cle-nb-183/New Volume/CLE/2. Testing Data/3. analysis/1. New Technique Analysis/3. Stats/2. ip/good bad status"
output_good_bad_file = os.path.join(stats_path,"misc.csv") # colored_good_bad_files
output_summary_file = os.path.join(stats_path,"other_lang_book_summary.csv")

classify_files(combined_text_file, threshold, output_good_bad_file, output_summary_file)
