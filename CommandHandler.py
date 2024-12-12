import webbrowser

class CommandHandler:
    def __init__(self, voice_generator, weather_fetcher):
        self.voice_generator = voice_generator
        self.weather_fetcher = weather_fetcher
        self.commands = {
            "otwórz przeglądarkę": self.open_browser,
            "wyszukaj": self.search,
            "szukaj wikipedia": self.search_wiki,
            "sprawdź pogodę": self.check_weather,
            "zamknij": self.exit_program,
            "komendy": self.display_commands
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

    def exit_program(self):
        self.voice_generator.play_text("Do zobaczenia!")
        exit()