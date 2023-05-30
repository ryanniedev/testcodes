import os
from zipfile import ZipFile
from bs4 import BeautifulSoup
import re
import asyncio
import edge_tts
from pathlib import Path
from tkinter import Tk, filedialog

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

    extracted_files = []
    for i, html_file in enumerate(html_files):
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            content = soup.get_text()

        # Get the first two lines of the content
        lines = content.strip().split('\n')
        first_two_lines = '\n'.join(lines[:2])

        # Generate a sanitized filename using the first two lines
        filename = sanitize_filename(first_two_lines) + '.txt'

        # Save the content to a text file in the extracted folder on the user's desktop
        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)

        extracted_files.append(output_path)

        print(f"Extracted: {filename}")
        print(f"Output Path: {output_path}")

    print("Extraction completed.")

    return extracted_files

async def convert_to_mp3(input_files, output_folder, voice):
    converted_files = []

    for input_file in input_files:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        # Extract the base filename from the input text file
        base_filename = os.path.splitext(os.path.basename(input_file))[0]

        # Construct the output MP3 file path with the voice name as a suffix
        output_mp3_file = os.path.join(output_folder, f"{base_filename}_{voice}.mp3")

        communicate = edge_tts.Communicate(text, voice)

        try:
            # Perform the conversion
            await communicate.save(output_mp3_file)
            converted_files.append(output_mp3_file)
            print(f"Conversion completed for: {output_mp3_file}")
        except Exception as e:
            print(f"An error occurred during conversion: {e}")

    return converted_files

# User-defined paths
root = Tk()
root.withdraw()
epub_file_path = filedialog.askopenfilename(title="Select EPUB File", filetypes=(("EPUB Files", "*.epub"),))
output_folder_path = filedialog.askdirectory(title="Select Output Folder")

if not epub_file_path or not output_folder_path:
    print("EPUB file or output folder not selected. Exiting...")
    exit()

# Create the output folder on the user's desktop if it doesn't exist
output_folder_path = os.path.join(output_folder_path, 'extracted')
os.makedirs(output_folder_path, exist_ok=True)

# Extract EPUB to text files
extracted_files = extract_epub(epub_file_path, output_folder_path)

# Convert text files to MP3
voice = "zh-TW-HsiaoYuNeural"
converted_files = asyncio.run(convert_to_mp3(extracted_files, output_folder_path, voice))
