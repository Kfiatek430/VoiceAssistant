import platform
import pyautogui
from modules.voice_generator import VoiceGenerator
from modules.weather_fetcher import WeatherFetcher
from modules.command import Command
import webbrowser
import os
import urllib.parse
import re

class CommandHandler:
    def __init__(self):
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
        if command != "":
            try:
                self.commands[command].command(*parameters)
            except TypeError:
                VoiceGenerator.speak_text("Nieprawidłowa liczba parametrów")
        else:
            VoiceGenerator.speak_text("Nie rozumiem tej komendy.")

    @staticmethod
    def open_browser():
        webbrowser.open("https://www.google.com")
        VoiceGenerator.speak_text("Otwieram przeglądarkę")

    @staticmethod
    def search(query):
        parsed_query = urllib.parse.quote(query)
        webbrowser.open(f"https://www.google.com/search?q={parsed_query}")
        VoiceGenerator.speak_text(f"Szukam: {query}")

    @staticmethod
    def search_wiki(query):
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
        weather_data = WeatherFetcher.get_weather(city)
        if weather_data:
            text_to_speak = f"Pogoda dla {city}: "
            for key, value in weather_data.items():
                text_to_speak += f"{key}: {value}, "
            VoiceGenerator.speak_text(text_to_speak)
        else:
            VoiceGenerator.speak_text(f"Nie znaleziono danych dla {city}.")

    def display_commands(self):
        text_to_speak = "Dostępne komendy to: "
        for command in self.commands.keys():
            text_to_speak += command + ", "
        VoiceGenerator.speak_text(text_to_speak)

    @staticmethod
    def open_wmplayer():
        os.system("start wmplayer")
        VoiceGenerator.speak_text("Otwieram Windows Media Player")

    @staticmethod
    def open_clock():
        os.system("start ms-clock:")
        VoiceGenerator.speak_text("Otwieram zegar")

    def enable_silent_mode(self):
        if not self.isSilentMode:
            self.set_silent_mode(1)
        else:
            VoiceGenerator.speak_text("Tryb cichy jest już włączony")

    def disable_silent_mode(self):
        if self.isSilentMode:
            self.set_silent_mode(0)
        else:
            VoiceGenerator.speak_text("Tryb cichy jest już wyłączony")

    def set_silent_mode(self, state):
        current_os = platform.system()

        if current_os == "Windows":
            if state == 1 and not self.isSilentMode:
                pyautogui.press("volumemute")
                self.isSilentMode = True
                VoiceGenerator.speak_text("Włączam tryb cichy")
            elif state == 0 and self.isSilentMode:
                pyautogui.press("volumemute")
                self.isSilentMode = False
                VoiceGenerator.speak_text("Wyłączam tryb cichy")
            else:
                VoiceGenerator.speak_text("Tryb cichy już jest ustawiony")
        elif current_os == "Linux":
            if state == 1:
                os.system("amixer set Master mute")
                self.isSilentMode = True
                VoiceGenerator.speak_text("Włączam tryb cichy")
            else:
                os.system("amixer set Master unmute")
                self.isSilentMode = False
                VoiceGenerator.speak_text("Wyłączam tryb cichy")
        elif current_os == "Darwin":  # macOS
            if state == 1:
                os.system("osascript -e 'set volume with output muted'")
                self.isSilentMode = True
                VoiceGenerator.speak_text("Włączam tryb cichy")
            else:
                os.system("osascript -e 'set volume without output muted'")
                self.isSilentMode = False
                VoiceGenerator.speak_text("Wyłączam tryb cichy")
        else:
            VoiceGenerator.speak_text("System operacyjny nie jest obsługiwany przez funkcję zmiany głośności.")

    @staticmethod
    def exit_program():
        VoiceGenerator.speak_text("Do zobaczenia!")
        exit()