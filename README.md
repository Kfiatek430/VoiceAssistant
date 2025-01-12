# VoiceAssistant

VoiceAssistant is a Python-based application that allows users to execute various commands using voice input. It integrates with multiple modules to provide functionalities like web browsing, weather information and system control.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kfiatek430/VoiceAssistant.git
   ```

2. Navigate to the project directory:
   ```bash
   cd VoiceAssistant
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Execute commands using voice input. Example phrases:
   - "sprawdź pogodę Kraków"
   - "otwórz przeglądarkę"
   - "wyszukaj Python"

## Available Commands

The following table lists all available commands in the application along with their descriptions:

| **Command**                  | **Parameters** | **Description**                                                      |
|------------------------------|----------------|----------------------------------------------------------------------|
| `otwórz przeglądarkę`        | None           | Opens the default web browser.                                       |
| `wyszukaj`                   | `<query>`      | Performs a Google search for the specified query.                    |
| `szukaj wikipedia`           | `<query>`      | Searches Wikipedia for the specified query.                          |
| `sprawdź pogodę`             | `<city>`       | Fetches and announces the weather for the specified city.            |
| `zamknij`                    | None           | Terminates the application.                                          |
| `komendy`                    | None           | Lists all available commands.                                        |
| `powiedz`                    | `<text>`       | Converts the given text to speech and plays it.                      |
| `muzyka`                     | None           | Opens Windows Media Player.                                          |
| `zegar`                      | None           | Opens the system clock application.                                  |
| `włącz tryb cichy`           | None           | Mutes the system volume.                                             |
| `wyłącz tryb cichy`          | None           | Unmutes the system volume.                                           |

### Notes:
- Commands with `<parameters>` require user input for additional information (e.g., search query or city name).
- You can extend functionality by modifying the `self.commands` dictionary in the `CommandHandler` module.

## Documentation

Additional details are available in the [Wiki](https://github.com/Kfiatek430/VoiceAssistant/wiki). Explore the documentation for module descriptions, code examples and advanced usage.

## License

This project is licensed under the [MIT License](LICENSE.md).

## Acknowledgments

- Speech recognition functionality provided by the [speech_recognition](https://github.com/Uberi/speech_recognition) library.
- Powered by the [edge_tts](https://github.com/rany2/edge-tts) library for text-to-speech conversion.
- Weather data provided by the IMGW public API.
