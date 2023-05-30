#!/usr/bin/env python3

"""
Example of using edge_tts to convert a text file to an MP3 file.
"""

import asyncio
import edge_tts

input_text_file = r'/Users/ryan/Desktop/path/to/output/folder/Section002.txt'
output_mp3_file = r'/Users/ryan/Desktop/path/to/output/folder/Section002.txt.mp3'
voice = "zh-CN-XiaoyiNeural"

async def main():
    with open(input_text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_mp3_file)

    print("Conversion completed.")

if __name__ == "__main__":
    asyncio.run(main())
