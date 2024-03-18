import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_into_pages(pdf_path, output_folder):
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)

    for i in range(num_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        
        output_filename = os.path.join(output_folder, f"page_{i+1}.pdf")
        with open(output_filename, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"Saved: {output_filename}")

# Example usage
pdf_path = 'uploads/Hello.pdf'  # Path to your PDF file
output_folder = 'uploads/pages'  # Folder where individual pages will be saved

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

split_pdf_into_pages(pdf_path, output_folder)
