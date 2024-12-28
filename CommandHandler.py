"""
CommandHandler module.

This module provides the CommandHandler class for handling commands and executing corresponding actions.

Classes:
    CommandHandler: A class to handle and execute commands.
"""

from VoiceGenerator import VoiceGenerator
from WeatherFetcher import WeatherFetcher
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from Command import Command
import webbrowser
import os
import urllib.parse
import re

class CommandHandler:
    """
    Handles and executes commands.

    This class is responsible for interpreting commands and executing the corresponding actions.

    Attributes:
        isSilentMode (bool): Indicates whether silent mode is enabled.
        commands (dict): A dictionary mapping command strings to Command objects.

    Methods:
        handle_command(text):
            Handles the given command.
        parse_text(text):
            Parses the given text to identify the command and its parameters.
        execute_command(command, *parameters):
            Executes the given command with the provided parameters.
        open_browser():
            Opens the default web browser to the Google homepage.
        search(query):
            Searches for the given query using Google.
        search_wiki(query):
            Searches Wikipedia for the given query.
        check_weather(city):
            Checks the weather for a given city.
        display_commands():
            Displays the available commands.
        open_wmplayer():
            Opens Windows Media Player.
        open_clock():
            Opens the Windows Clock application.
        enable_silent_mode():
            Enables silent mode.
        disable_silent_mode():
            Disables silent mode.
        set_silent_mode(state):
            Sets the silent mode state.
        exit_program():
            Exits the program.
    """

    def __init__(self):
        """
        Initializes an instance of the CommandHandler class.

        Sets the `isSilentMode` attribute to False and the `commands` attribute to a dictionary
        mapping command strings to Command objects.
        """

        self.isSilentMode = False

        self.commands = {
            "otwórz przeglądarkę": Command(self.open_browser, 0),
            "wyszukaj": Command(self.search, 1),
            "szukaj wikipedia": Command(self.search_wiki, 1),
            "sprawdź pogodę": Command(self.check_weather, 1),
            "zamknij": Command(self.exit_program, 0),
            "komendy": Command(self.display_commands, 0),
            "powiedz": Command(VoiceGenerator.speak_text, 1),
            "muzyka": Command(self.open_wmplayer, 0),
            "zegar": Command(self.open_clock, 0),
            "włącz tryb cichy": Command(self.enable_silent_mode, 0),
            "wyłącz tryb cichy": Command(self.disable_silent_mode, 0)
        }

    def handle_command(self, text):
        """
        Handles the given command.

        This method parses the input text to identify the command and its parameters,
        then executes the corresponding command.

        Args:
            text (str): The input text containing the command and its parameters.
        """

        command, parameters = self.parse_text(text)
        self.execute_command(command, *parameters)

    def parse_text(self, text):
        """
        Parses a given text input to identify a command and its associated parameters.

        This method processes the input `text` to extract the first valid command and its parameters.
        The function stops at the first command that matches the beginning of the input text.

        Args:
            text (str): The input text to be parsed.

        Returns:
            tuple: A tuple containing the identified command (str) and a list of parameters (list).
        """

        words = text.split(" ")
        command = ""
        parameters = []

        for i in range(1, len(words) + 1):
            potential_command = " ".join(words[:i])
            if potential_command in self.commands:
                command = potential_command
                if self.commands[command].param_count == 1:
                    if i < len(words):
                        parameters = [" ".join(words[i:])]
                break

        return command, parameters

    def execute_command(self, command, *parameters):
        """
        Executes the given command with the provided parameters.

        This method looks up the command in the `commands` dictionary and executes it with the given parameters.
        If the command is not found or the number of parameters is incorrect, it provides appropriate feedback.

        Args:
            command (str): The command to be executed.
            *parameters: The parameters to be passed to the command.

        Raises:
            TypeError: If the number of parameters is incorrect.
        """

        if command != "":
            try:
                self.commands[command].command(*parameters)
            except TypeError:
                VoiceGenerator.speak_text("Nieprawidłowa liczba parametrów")
        else:
            VoiceGenerator.speak_text("Nie rozumiem tej komendy.")

    @staticmethod
    def open_browser():
        """
        Opens the default web browser to the Google homepage.

        This method uses the `webbrowser` module to open the default web browser
        and navigate to "https://www.google.com".
        """

        webbrowser.open("https://www.google.com")
        VoiceGenerator.speak_text("Otwieram przeglądarkę")

    @staticmethod
    def search(query):
        """
        Searches for the given query using Google.

        This method constructs a URL to search for the query on Google and opens it in the default web browser.

        Args:
            query (str): The search query.
        """

        parsed_query = urllib.parse.quote(query)
        webbrowser.open(f"https://www.google.com/search?q={parsed_query}")
        VoiceGenerator.speak_text(f"Szukam: {query}")

    @staticmethod
    def search_wiki(query):
        """
        Searches Wikipedia for the given query.

        This method constructs a URL to search for the query on Wikipedia. If the query contains Polish characters,
        it performs a Google search for the query followed by "wikipedia". Otherwise, it directly constructs a Wikipedia
        URL for the query.

        Args:
            query (str): The search query.
        """

        polish_characters_pattern = r'[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]'

        if re.search(polish_characters_pattern, query):
            parsed_query = urllib.parse.quote(query)
            webbrowser.open(f"https://www.google.com/search?q={parsed_query}%20wikipedia")
        else:
            parsed_query = query.replace(" ", "_")
            webbrowser.open(f"https://pl.wikipedia.org/wiki/{parsed_query}")

        VoiceGenerator.speak_text(f"Szukam {query} na Wikipedii")

    @staticmethod
    def check_weather(city):
        """
        Checks the weather for a given city.

        This method fetches the weather data for the specified city using the `WeatherFetcher` class.
        If no weather data is found, it informs the user.

        Args:
            city (str): The name of the city to check the weather for.
        """

        weather_data = WeatherFetcher.get_weather(city)
        if weather_data:
            text_to_speak = f"Pogoda dla {city}: "
            for key, value in weather_data.items():
                text_to_speak += f"{key}: {value}, "
            VoiceGenerator.speak_text(text_to_speak)
        else:
            VoiceGenerator.speak_text(f"Nie znaleziono danych dla {city}.")

    def display_commands(self):
        """
        Displays the available commands.
        """

        text_to_speak = "Dostępne komendy to: "
        for command in self.commands.keys():
            text_to_speak += command + ", "

        VoiceGenerator.speak_text(text_to_speak)

    @staticmethod
    def open_wmplayer():
        """
        Opens Windows Media Player.

        This method uses the `os.system` function to start Windows Media Player.
        """

        os.system("start wmplayer")
        VoiceGenerator.speak_text("Otwieram Windows Media Player")

    @staticmethod
    def open_clock():
        """
        Opens the Windows Clock application.

        This method uses the `os.system` function to open the Windows Clock application
        """

        os.system("start ms-clock:")
        VoiceGenerator.speak_text("Otwieram zegar")

    def enable_silent_mode(self):
        """
        Enables silent mode.

        This method mutes the system volume if silent mode is not currently enabled.
        If silent mode is already enabled, it informs the user.
        """

        if not self.isSilentMode:
            self.set_silent_mode(1)
        else:
            VoiceGenerator.speak_text("Tryb cichy jest już włączony")

    def disable_silent_mode(self):
        """
        Disables silent mode.

        This method unmutes the system volume if silent mode is currently enabled.
        If silent mode is already disabled, it informs the user.
        """

        if self.isSilentMode:
            self.set_silent_mode(0)
        else:
            VoiceGenerator.speak_text("Tryb cichy jest już wyłączony")

    def set_silent_mode(self, state):
        """
        Sets the silent mode state.

        This method mutes or unmutes the system volume based on the provided state.
        It uses the pycaw library to control the system audio endpoint volume.

        Args:
            state (int): The state to set the silent mode to.
            1 to enable silent mode (mute), 0 to disable silent mode (unmute).

        Raises:
            Exception: If there is an error accessing the audio endpoint volume.
        """

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_controller = cast(interface, POINTER(IAudioEndpointVolume))

        if state == 1:
            volume_controller.SetMute(1, None)
            self.isSilentMode = True
            VoiceGenerator.speak_text("Włączam tryb cichy")
        else:
            volume_controller.SetMute(0, None)
            self.isSilentMode = False
            VoiceGenerator.speak_text("Wyłączam tryb cichy")

    @staticmethod
    def exit_program():
        """
        Exits the program.
        """

        VoiceGenerator.speak_text("Do zobaczenia!")
        exit()