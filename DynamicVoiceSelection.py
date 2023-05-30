#!/usr/bin/env python3

"""
Example of dynamic voice selection using VoicesManager.
"""

import asyncio
import random

import edge_tts
from edge_tts import VoicesManager


async def select_voice(voices):
    print("Available voices:")
    voice_options = voices.voices
    for index, voice in enumerate(voice_options):
        voice_name = voice["Name"].replace("Microsoft Server Speech Text to Speech ", "")
        print(f"{index + 1}. {voice_name}")

    while True:
        try:
            choice = int(input("Select a voice (enter the corresponding number): "))
            if 1 <= choice <= len(voice_options):
                return voice_options[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


async def _main() -> None:
    voices = await VoicesManager.create()
    voice = await select_voice(voices)

    communicate = edge_tts.Communicate(TEXT, voice["Name"])
    await communicate.save(OUTPUT_FILE)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_main())
    finally:
        loop.close()
