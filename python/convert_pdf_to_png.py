# Called from C++. Converts PDF files of scores into PNG files. Stores in temporary application storage. Returns a path to the png files

import sys
import fitz
import os

# Get arguments
pdf_path = sys.argv[1]
save_path = sys.argv[2]

def convert_pdf_to_png(pdf_path, save_path):
    # Create the save_path if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    pdf_document = fitz.open(pdf_path)
    png_paths = []
    num_pages = pdf_document.page_count
    print("Number of pages: ", num_pages)
    for page_number in range(num_pages):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        png_path = save_path + "/page" + str(page_number) + ".png"
        pix.save(png_path)
        png_paths.append(png_path)

convert_pdf_to_png(pdf_path, save_path)