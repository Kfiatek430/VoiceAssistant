"""
bot module.

This module contains the `Bot` class, which represents a voice-controlled bot. The bot listens for voice commands,
interprets them, and executes the corresponding actions using a command handler and a voice recognizer.

Classes:
    Bot: A class to represent a voice-controlled bot.

Usage Example:
    from command_handler import CommandHandler
    import speech_recognition as sr

    if __name__ == "__main__":
        voice_recognizer = sr.Recognizer()
        command_handler = CommandHandler()
        bot = Bot(command_handler, voice_recognizer)
"""

import speech_recognition as sr

class Bot:
    """
    A class to represent a voice-controlled bot.

    This bot listens for voice commands, interprets them, and executes the corresponding actions using a command handler and a voice recognizer.

    Attributes:
        command_handler (CommandHandler): The handler for executing commands.
        voice_recognizer (sr.Recognizer): The recognizer for interpreting voice commands.

    Methods:
        listen_and_execute():
            Listens for a voice command and executes the corresponding action.
    """

    def __init__(self, command_handler, voice_recognizer):
        """
        Initializes the Bot with a command handler and a voice recognizer.

        Args:
            command_handler (CommandHandler): The handler for executing commands.
            voice_recognizer (sr.Recognizer): The recognizer for interpreting voice commands.
        """

        self.command_handler = command_handler
        self.voice_recognizer = voice_recognizer

        while True:
            print("Czekam na komendę...")
            self.listen_and_execute()

    def listen_and_execute(self):
        """
        Listens for a voice command and executes the corresponding action.

        This method uses the speech_recognition library to capture audio from the
        microphone, recognize the spoken command, and pass it to the command handler
        for execution. If the speech is not recognized or there is an API error, it
        handles the exceptions and provides appropriate feedback.

        Raises:
            speech_recognition.UnknownValueError: If the speech is unintelligible.
            speech_recognition.RequestError: If there is an unhandled error with the speech recognition API.
        """

        with sr.Microphone() as source:
            print("Słucham...")
            audio = self.voice_recognizer.listen(source)

        try:
            text = self.voice_recognizer.recognize_google(audio, language="pl-PL").lower()
            print(f"Rozpoznano: {text}")
            self.command_handler.handle_command(text)
        except sr.UnknownValueError:
            print("Nie zrozumiałem, powtórz proszę.")
        except sr.RequestError as e:
            print(f"Błąd API rozpoznawania mowy: {e}")