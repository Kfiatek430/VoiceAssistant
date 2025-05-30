from modules.voice_generator import VoiceGenerator
import requests

class WeatherFetcher:
    @staticmethod
    def get_weather(city):
        try:
            response = requests.get('https://danepubliczne.imgw.pl/api/data/meteo/')
            if response.status_code == 200:
                return_dictionary = {}
                meteo_data = response.json()
                for station in meteo_data:
                    if city.lower() in station["nazwa_stacji"].lower():
                        if station.get('temperatura_gruntu', None) is not None:
                            return_dictionary["Temperatura"] = VoiceGenerator.convert_number_to_text(station['temperatura_gruntu'] + " stopni Celsjusza")

                        if station.get('wiatr_srednia_predkosc', None) is not None:
                            return_dictionary["Wiatr"] = VoiceGenerator.convert_number_to_text(station['wiatr_srednia_predkosc'] + " metrów na sekundę")

                        if station.get('opad_10min', None) is not None:
                            return_dictionary["Opad"] = VoiceGenerator.convert_number_to_text(station['opad_10min'] + " milimetrów")

                return return_dictionary
            return None
        except requests.RequestException as e:
            print(f"Błąd pobierania danych pogodowych: {e}")
            return None