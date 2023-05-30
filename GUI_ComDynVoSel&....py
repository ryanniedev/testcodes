import os
from zipfile import ZipFile
from bs4 import BeautifulSoup
import re
import asyncio
import edge_tts
from tkinter import Tk, filedialog, ttk
from tkinter import messagebox as mbox

def sanitize_filename(filename):
    # Remove invalid characters from the filename
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', '', filename)

    # Limit the filename length to 10 characters
    return sanitized[:10]

def extract_epub(epub_file, output_folder, progress_bar):
    with ZipFile(epub_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)

    html_files = []
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            if file.endswith('.html') or file.endswith('.xhtml'):
                html_files.append(os.path.join(root, file))

    extracted_files = []
    total_files = len(html_files)

    for i, html_file in enumerate(html_files):
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            content = soup.get_text()

        # Get the first two lines of the content
        lines = content.strip().split('\n')
        first_two_lines = '\n'.join(lines[:2])

        # Generate a sanitized filename using the first two lines
        filename = sanitize_filename(first_two_lines) + '.txt'

        # Save the content to a text file in the extracted folder
        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)

        extracted_files.append(output_path)
        progress = (i + 1) / total_files * 100
        progress_bar['value'] = progress
        progress_bar.update()

    mbox.showinfo("Information", "Extraction completed.")
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
        except Exception as e:
            print(f"An error occurred during conversion: {e}")

    return converted_files

def select_epub_file():
    root = Tk()
    root.withdraw()
    epub_file_path = filedialog.askopenfilename(title="Select EPUB File", filetypes=(("EPUB Files", "*.epub"),))
    return epub_file_path

def select_output_folder():
    root = Tk()
    root.withdraw()
    output_folder_path = filedialog.askdirectory(title="Select Output Folder")
    return output_folder_path

def select_voice():
    voices = edge_tts.VoicesManager()
    voice_options = voices.voices
    voice_names = [voice["Name"].replace("Microsoft Server Speech Text to Speech ", "") for voice in voice_options]

    root = Tk()
    root.withdraw()
    selected_voice = mbox.askinteger("Select Voice", "Available voices:\n" + "\n".join([f"{index+1}. {name}" for index, name in enumerate(voice_names)]))

    if selected_voice is not None and 1 <= selected_voice <= len(voice_options):
        return voice_options[selected_voice-1]
    else:
        return None

def process_epub():
    epub_file_path = select_epub_file()
    if not epub_file_path:
        mbox.showerror("Error", "EPUB file not selected.")
        return

    output_folder_path = select_output_folder()
    if not output_folder_path:
        mbox.showerror("Error", "Output folder not selected.")
        return

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder_path, exist_ok=True)

    # Initialize the progress bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=20)

    # Extract EPUB to text files
    extracted_files = extract_epub(epub_file_path, output_folder_path, progress_bar)

    # Select voice
    selected_voice = select_voice()
    if not selected_voice:
        mbox.showerror("Error", "Voice not selected.")
        return

    voice = selected_voice["Name"]

    # Convert text files to MP3
    converted_files = asyncio.run(convert_to_mp3(extracted_files, output_folder_path, voice))

    mbox.showinfo("Information", "Conversion completed.")

if __name__ == "__main__":
    root = Tk()
    root.title("EPUB Extractor & Converter")
    root.geometry("400x200")

    def select_epub():
        epub_file_path = select_epub_file()
        if epub_file_path:
            mbox.showinfo("Information", "EPUB file selected.")
        else:
            mbox.showerror("Error", "No EPUB file selected.")

    def select_output():
        output_folder_path = select_output_folder()
        if output_folder_path:
            mbox.showinfo("Information", "Output folder selected.")
        else:
            mbox.showerror("Error", "No output folder selected.")

    def select_voice():
        selected_voice = select_voice()
        if selected_voice:
            mbox.showinfo("Information", "Voice selected.")
        else:
            mbox.showerror("Error", "No voice selected.")

    def start_conversion():
        mbox.showinfo("Information", "Conversion started.")

    select_epub_button = ttk.Button(root, text="Select EPUB", command=select_epub)
    select_epub_button.pack(pady=10)

    select_output_button = ttk.Button(root, text="Select Output", command=select_output)
    select_output_button.pack(pady=10)

    select_voice_button = ttk.Button(root, text="Select Voice", command=select_voice)
    select_voice_button.pack(pady=10)

    start_button = ttk.Button(root, text="Start Conversion", command=start_conversion)
    start_button.pack(pady=10)

    root.mainloop()
