import os
import asyncio
import ebooklib
from ebooklib import epub
import edge_tts
from edge_tts import VoicesManager


async def txt_to_mp3(txt, mp3, announcer='Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)'):
    # Convert text to MP3 audio
    communicate = edge_tts.Communicate(txt, announcer)
    await communicate.save(mp3)


async def get_announcer(Gender="Female", Language="zh"):
    voices = await VoicesManager.create()
    voice = voices.find(Gender=Gender, Language=Language)
    print(voice)


if __name__ == "__main__":
    epub_file = r'C:\Users\RYAN\Documents\coding\silkroad.epub'
    output_folder = r'C:\Users\RYAN\Documents\coding\epub_text_files'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    loop = asyncio.get_event_loop()
    try:
        book = epub.read_epub(epub_file)
        chapters = []

        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                chapters.append(item.get_content())

        loop.run_until_complete(get_announcer(Gender="Female", Language="zh"))

        for i, chapter_text in enumerate(chapters):
            txt_file = os.path.join(output_folder, f'chapter_{i+1}.txt')
            mp3_file = os.path.join(output_folder, f'chapter_{i+1}.mp3')

            with open(txt_file, 'w', encoding='utf-8') as file:
                file.write(chapter_text)

            loop.run_until_complete(txt_to_mp3(chapter_text, mp3_file))

            print(f'Converted: {txt_file} -> {mp3_file}')
    finally:
        loop.close()
