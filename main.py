"""
Main module.

This module initializes and starts the voice assistant application.
"""

from Bot import Bot
from CommandHandler import CommandHandler
import speech_recognition as sr

if __name__ == "__main__":
    voice_recognizer = sr.Recognizer()
    command_handler = CommandHandler()
    bot = Bot(command_handler, voice_recognizer)
