import PyPDF2

def extract_pages(input_pdf, output_pdf, start_page, end_page):
    try:
        # Open the original PDF file
        with open(input_pdf, 'rb') as infile:
            reader = PyPDF2.PdfReader(infile)

            # Check how many pages the input PDF has
            total_pages = len(reader.pages)
            print(f"Total pages in input PDF: {total_pages}")

            # Validate the requested page range
            if start_page < 1 or end_page > total_pages:
                print(f"Invalid page range. The input PDF only has {total_pages} pages.")
                return

            # Create a PDF writer object to write the extracted pages
            writer = PyPDF2.PdfWriter()

            # Loop through the pages from start_page to end_page (inclusive)
            for page_num in range(start_page - 1, end_page):
                writer.add_page(reader.pages[page_num])
                print(f"Adding page {page_num + 1} to the output PDF.")  # Debug message

            # Write the extracted pages to the output PDF
            with open(output_pdf, 'wb') as outfile:
                writer.write(outfile)
            print(f"Extracted pages {start_page}-{end_page} to {output_pdf}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_pdf = '/home/cle-nb-183/Downloads/4 THE ANTI TERRORISM ACT, 1997.pdf'  # Path to your input PDF
output_pdf = '/home/cle-nb-183/Documents/Short_4_THE_ANTI_TERRORISM_ACT_1997.pdf'  # Path for the output PDF
start_page = 4  # Starting page (1-indexed)
end_page = 6    # Ending page

extract_pages(input_pdf, output_pdf, start_page, end_page)

