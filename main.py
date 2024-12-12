import Bot
import VoiceGenerator
import WeatherFetcher
import CommandHandler
import speech_recognition as sr

if __name__ == "__main__":
    voice_generator = VoiceGenerator.VoiceGenerator()
    voice_recognizer = sr.Recognizer()
    weather_fetcher = WeatherFetcher.WeatherFetcher()
    command_handler = CommandHandler.CommandHandler(voice_generator, weather_fetcher)
    bot = Bot.Bot(command_handler, voice_recognizer)
