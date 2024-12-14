import os
from edge_tts import Communicate
from playsound3 import playsound
import asyncio

class VoiceGenerator:
    counter = 0

    def __init__(self):
        pass

    @staticmethod
    async def create_and_play_text(text):
        output_file = f"output{VoiceGenerator.counter}.mp3"
        VoiceGenerator.counter += 1

        communicate = Communicate(text, voice='pl-PL-ZofiaNeural')
        await communicate.save(output_file)
        playsound(output_file)
        os.remove(output_file)

    def play_text(self, text):
        print(f"[-] {text}")
        asyncio.run(self.create_and_play_text(text))


    @staticmethod
    def number_to_text(number):
        number = str(number)
        return number.replace("-", "minus ").replace(".", " i ")