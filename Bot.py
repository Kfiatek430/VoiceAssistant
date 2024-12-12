import speech_recognition as sr

class Bot:
    def __init__(self, command_handler, voice_recognizer):
        self.command_handler = command_handler
        self.voice_recognizer = voice_recognizer

        while True:
            print("Czekam na komendę...")
            self.listen_and_execute()

    def listen_and_execute(self):
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