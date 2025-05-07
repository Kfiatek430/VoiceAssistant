from edge_tts import Communicate
from playsound3 import playsound
import os
import asyncio

class VoiceGenerator:
    counter = 0

    @staticmethod
    async def generate_and_play_audio(text):
        output_file = f"output{VoiceGenerator.counter}.mp3"
        VoiceGenerator.counter += 1

        communicate = Communicate(text, voice='pl-PL-ZofiaNeural')
        await communicate.save(output_file)
        playsound(output_file)
        os.remove(output_file)

    @staticmethod
    def speak_text(text):
        print(f"[-] {text}")
        asyncio.run(VoiceGenerator.generate_and_play_audio(text))

    @staticmethod
    def convert_number_to_text(number):
        number = str(number)
        return number.replace("-", "minus ").replace(".", " i ")