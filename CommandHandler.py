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
    isSilentMode = False

    def __init__(self):
        self.voice_generator = VoiceGenerator()
        self.weather_fetcher = WeatherFetcher()
        self.commands = {
            "otwórz przeglądarkę": Command(self.open_browser, 0),
            "wyszukaj": Command(self.search, 1),
            "szukaj wikipedia": Command(self.search_wiki, 1),
            "sprawdź pogodę": Command(self.check_weather, 1),
            "zamknij": Command(self.exit_program, 0),
            "komendy": Command(self.display_commands, 0),
            "powiedz": Command(self.voice_generator.speak_text, 1),
            "muzyka": Command(self.open_wmplayer, 0),
            "zegar": Command(self.set_alarm, 0),
            "włącz tryb cichy": Command(self.enable_silent_mode, 0),
            "wyłącz tryb cichy": Command(self.disable_silent_mode, 0)
        }

    def handle_command(self, text):
        command, parameters = self.parse_text(text)
        self.execute_command(command, *parameters)

    def parse_text(self, text):
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
        if command in self.commands:
            try:
                self.commands[command].command(*parameters)
            except TypeError:
                self.voice_generator.speak_text("Nieprawidłowa liczba parametrów")
        else:
            self.voice_generator.speak_text("Nie rozumiem tej komendy.")

    def open_browser(self):
        webbrowser.open("https://www.google.com")
        self.voice_generator.speak_text("Otwieram przeglądarkę")

    def search(self, query):
        parsed_query = urllib.parse.quote(query)
        webbrowser.open(f"https://www.google.com/search?q={parsed_query}")
        self.voice_generator.speak_text(f"Szukam: {query}")

    def search_wiki(self, query):
        polish_characters_pattern = r'[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]'

        if re.search(polish_characters_pattern, query):
            parsed_query = urllib.parse.quote_plus(query)
            webbrowser.open(f"https://www.google.com/search?q={parsed_query}%20wikipedia")
        else:
            parsed_query = query.replace(" ", "_")
            webbrowser.open(f"https://pl.wikipedia.org/wiki/{parsed_query}")

        self.voice_generator.speak_text(f"Szukam: {query} na Wikipedii")

    def check_weather(self, city):
        weather_data = self.weather_fetcher.get_weather(city)
        if weather_data:
            text_to_speak = f"Pogoda dla {city}: "
            for key, value in weather_data.items():
                text_to_speak += f"{key}: {value}, "
            self.voice_generator.speak_text(text_to_speak)
        else:
            self.voice_generator.speak_text(f"Nie znaleziono danych dla {city}.")

    def display_commands(self):
        text_to_speak = "Dostępne komendy to: "
        for command in self.commands.keys():
            text_to_speak += command + ", "

        self.voice_generator.speak_text(text_to_speak)

    def open_wmplayer(self):
        os.system("start wmplayer")
        self.voice_generator.speak_text("Otwieram Windows Media Player")

    def set_alarm(self):
        os.system("start ms-clock:")
        self.voice_generator.speak_text("Otwieram zegar")

    def enable_silent_mode(self):
        if not self.isSilentMode:
            self.set_silent_mode(1)
        else:
            self.voice_generator.speak_text("Tryb cichy jest już włączony")

    def disable_silent_mode(self):
        if self.isSilentMode:
            self.set_silent_mode(0)
        else:
            self.voice_generator.speak_text("Tryb cichy jest już wyłączony")

    def set_silent_mode(self, state):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_controller = cast(interface, POINTER(IAudioEndpointVolume))

        if state == 1:
            volume_controller.SetMute(1, None)
            self.isSilentMode = True
            self.voice_generator.speak_text("Włączam tryb cichy")
        else:
            volume_controller.SetMute(0, None)
            self.isSilentMode = False
            self.voice_generator.speak_text("Wyłączam tryb cichy")

    def exit_program(self):
        self.voice_generator.speak_text("Do zobaczenia!")
        exit()