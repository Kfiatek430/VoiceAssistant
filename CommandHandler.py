import webbrowser
import os
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

class CommandHandler:
    isSilentMode = False

    def __init__(self, voice_generator, weather_fetcher):
        self.voice_generator = voice_generator
        self.weather_fetcher = weather_fetcher
        self.commands = {
            "otwórz przeglądarkę": self.open_browser,
            "wyszukaj": self.search,
            "szukaj wikipedia": self.search_wiki,
            "sprawdź pogodę": self.check_weather,
            "zamknij": self.exit_program,
            "komendy": self.display_commands,
            "powiedz": self.voice_generator.play_text,
            "włącz muzykę": self.open_wmplayer,
            "zegar": self.set_alarm,
            "włącz tryb cichy": self.enable_silent_mode,
            "wyłącz tryb cichy": self.disable_silent_mode
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
                parameters = words[i:]
                break

        return command, parameters

    def execute_command(self, command, *parameters):
        if command in self.commands:
            try:
                self.commands[command](*parameters)
            except TypeError:
                self.voice_generator.play_text("Nieprawidłowa liczba parametrów")
        else:
            self.voice_generator.play_text("Nie rozumiem tej komendy.")

    def open_browser(self):
        webbrowser.open("https://www.google.com")
        self.voice_generator.play_text("Otwieram przeglądarkę")

    def search(self, query):
        webbrowser.open(f"https://www.google.com/search?q={query}")
        self.voice_generator.play_text(f"Szukam: {query}")

    def search_wiki(self, query):
        webbrowser.open(f"https://pl.wikipedia.org/wiki/{query}")
        self.voice_generator.play_text(f"Szukam: {query} na Wikipedii")

    def check_weather(self, city):
        weather_data = self.weather_fetcher.get_weather(city)
        if weather_data:
            text_to_speak = f"Pogoda dla {city}: "
            for key, value in weather_data.items():
                text_to_speak += f"{key}: {value}, "
            self.voice_generator.play_text(text_to_speak)
        else:
            self.voice_generator.play_text(f"Nie znaleziono danych dla {city}.")

    def display_commands(self):
        text_to_speak = "Dostępne komendy to: "
        for command in self.commands.keys():
            text_to_speak += command + ", "

        self.voice_generator.play_text(text_to_speak)

    def open_wmplayer(self):
        os.system("start wmplayer")
        self.voice_generator.play_text("Otwieram Windows Media Player")

    def set_alarm(self):
        os.system("start ms-clock:")
        self.voice_generator.play_text("Otwieram zegar")

    def enable_silent_mode(self):
        if not self.isSilentMode:
            self.set_silent_mode(1)
        else:
            self.voice_generator.play_text("Tryb cichy jest już włączony")

    def disable_silent_mode(self):
        if self.isSilentMode:
            self.set_silent_mode(0)
        else:
            self.voice_generator.play_text("Tryb cichy jest już wyłączony")

    def set_silent_mode(self, state):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_controller = cast(interface, POINTER(IAudioEndpointVolume))

        if state == 1:
            volume_controller.SetMute(1, None)
            self.isSilentMode = True
            self.voice_generator.play_text("Włączam tryb cichy")
        else:
            volume_controller.SetMute(0, None)
            self.isSilentMode = False
            self.voice_generator.play_text("Wyłączam tryb cichy")

    def exit_program(self):
        self.voice_generator.play_text("Do zobaczenia!")
        exit()