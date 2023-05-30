#!/usr/bin/env python3

"""
Example of using edge_tts to convert a text file to an MP3 file.
"""

import asyncio
import edge_tts

input_text_file = r'C:\Users\RYAN\Documents\coding\extracted_text\Chatpers\第一章丝绸之路的诞生.txt'
output_mp3_file = r'C:\Users\RYAN\Documents\coding\extracted_text\Chatpers\第一章丝绸之路的诞生.mp3'
voice = "zh-CN-XiaoxiaoNeural"

async def main():
    with open(input_text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_mp3_file)

    print("Conversion completed.")

if __name__ == "__main__":
    asyncio.run(main())
