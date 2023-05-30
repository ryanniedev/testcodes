#!/usr/bin/env python3

"""
Example of using edge_tts to convert a text file to an MP3 file.
"""

import os
import asyncio
import edge_tts

input_text_file = r'/Users/ryan/Desktop/path/to/output/folder/Section009.txt'
output_folder = r'/Users/ryan/Desktop/path/to/output/folder'
voice = "zh-TW-HsiaoYuNeural"

async def main():
    with open(input_text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Extract the base filename from the input text file
    base_filename = os.path.splitext(os.path.basename(input_text_file))[0]

    # Construct the output MP3 file path with the voice name as a suffix
    output_mp3_file = os.path.join(output_folder, f"{base_filename}_{voice}.mp3")

    communicate = edge_tts.Communicate(text, voice)

    try:
        # Perform the conversion
        await communicate.save(output_mp3_file)
        print("Conversion completed.")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

if __name__ == "__main__":
    asyncio.run(main())
