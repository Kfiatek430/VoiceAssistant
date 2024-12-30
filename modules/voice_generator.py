"""
voice_generator module.

This module provides the VoiceGenerator class for generating and playing audio from text using the edge_tts library.

Classes:
    VoiceGenerator: A class to generate and play audio from text.

Usage example:
    VoiceGenerator.speak_text("Witaj świecie!")
"""

from edge_tts import Communicate
from playsound3 import playsound
import os
import asyncio

class VoiceGenerator:
    """
    A class to generate and play audio from text using the edge_tts library.

    Attributes:
        counter (int): A counter that increments with each speech file generation, ensuring unique file names for conflict-free deletion.

    Methods:
        generate_and_play_audio(text): Generates and plays audio for the given text.
        speak_text(text): Converts the given text to speech and plays the audio.
        convert_number_to_text(number): Converts a number to its textual representation.
    """

    counter = 0

    @staticmethod
    async def generate_and_play_audio(text):
        """
        Generates and plays audio for the given text.

        This method creates an audio file from the provided text using the edge_tts library,
        plays the audio file, and then removes it.

        Args:
            text (str): The text to be converted to speech.

        Raises:
            Exception: If there is an error during audio generation, playback, or file removal.
        """

        output_file = f"output{VoiceGenerator.counter}.mp3"
        VoiceGenerator.counter += 1

        communicate = Communicate(text, voice='pl-PL-ZofiaNeural')
        await communicate.save(output_file)
        playsound(output_file)
        os.remove(output_file)

    @staticmethod
    def speak_text(text):
        """
        Converts the given text to speech and plays the audio.

        This method prints the text to the console and then uses the `generate_and_play_audio`
        method to convert the text to speech and play the resulting audio file.

        Args:
            text (str): The text to be converted to speech.
        """

        print(f"[-] {text}")
        asyncio.run(VoiceGenerator.generate_and_play_audio(text))

    @staticmethod
    def convert_number_to_text(number):
        """
        Converts a number to its textual representation.

        This method takes a number, converts it to a string, and replaces
        certain characters to create a more readable textual representation.

        Args:
            number (int or float): The number to be converted.

        Returns:
            str: The textual representation of the number.
        """

        number = str(number)
        return number.replace("-", "minus ").replace(".", " i ")