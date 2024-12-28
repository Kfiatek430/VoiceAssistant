"""
WeatherFetcher module.

This module provides the WeatherFetcher class for fetching weather data from the IMGW public API.

Classes:
    WeatherFetcher: A class to fetch weather data for a given city.

Usage example:
    weather_fetcher = WeatherFetcher()
    weather_data = weather_fetcher.get_weather("Kraków")
"""

from VoiceGenerator import VoiceGenerator
import requests

class WeatherFetcher:
    """
    A class to fetch weather data from the IMGW public API.

    Methods:
        get_weather(city): Fetches the weather data for a given city.
    """

    @staticmethod
    def get_weather(city):
        """
        Fetches the weather data for a given city.

        This method retrieves weather data from the IMGW public API and returns
        a dictionary with weather information for the specified city.

        Args:
            city (str): The name of the city to fetch the weather for.

        Raises:
            requests.RequestException: If an error occurs while fetching the data.

        Returns:
            dict: A dictionary containing weather information such as temperature, wind speed, and precipitation if data is found.
            None: If no data is found or an error occurs.
        """

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