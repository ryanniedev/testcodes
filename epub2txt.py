import os
from zipfile import ZipFile
from bs4 import BeautifulSoup
import re

def sanitize_filename(filename):
    # Remove invalid characters from the filename
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', '', filename)

    # Limit the filename length to 10 characters
    return sanitized[:10]

def extract_epub(epub_file, output_folder):
    with ZipFile(epub_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)

    html_files = []
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            if file.endswith('.html') or file.endswith('.xhtml'):
                html_files.append(os.path.join(root, file))

    for i, html_file in enumerate(html_files):
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            content = soup.get_text()

        # Get the first two lines of the content
        lines = content.strip().split('\n')
        first_two_lines = '\n'.join(lines[:2])

        # Generate a sanitized filename using the first two lines
        filename = sanitize_filename(first_two_lines) + '.txt'

        # Save the content to a text file
        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Extracted: {filename}")
        print(f"Output Path: {output_path}")

    print("Extraction completed.")

# Usage example
epub_file_path = r'C:\Users\RYAN\Documents\coding\silkroad.epub'
output_folder_path = r'C:\Users\RYAN\Documents\coding\extracted_text'

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

extract_epub(epub_file_path, output_folder_path)
