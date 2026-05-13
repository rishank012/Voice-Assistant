# 🤖 Friday - Interactive AI Voice Assistant

Friday is a personalized, multithreaded voice assistant built entirely in Python. It features a custom Tkinter-based Graphical User Interface (GUI) with animated GIF themes and uses real-time speech recognition to execute a variety of system and web commands. 

To ensure the GUI remains highly responsive during voice processing and text-to-speech outputs, the project utilizes Python's `threading` and `queue` modules.

## ✨ Features

* **Wake Word Detection:** Friday continuously listens in the background and activates upon hearing the magic word ("Friday").
* **Dynamic GUI:** A custom, fullscreen Tkinter interface with 8 interchangeable animated themes (GIFs).
* **High-Quality Voice Output:** Uses `edge-tts` for natural, high-fidelity voice responses.
* **Smart Dictation:** Can take spoken notes and automatically write them to a structured `.txt` file.
* **System Automation:** Opens local applications (VS Code, Notepad, Discord, File Manager, WhatsApp) and plays local music.
* **Web Integration:** Performs YouTube searches, Google searches, and fetches answers dynamically using `pywhatkit` and `webbrowser`.
* **Multithreaded Architecture:** Prevents the application from freezing by separating the listening loop from the main GUI loop.

## 🛠️ Tech Stack & Libraries

This project relies on several Python libraries for audio processing, web scraping, and GUI generation. 

* `tkinter` & `Pillow` (GUI and image rendering)
* `SpeechRecognition` (Audio input and STT)
* `edge-tts` & `pyttsx3` (Text-to-Speech engines)
* `pygame` & `playsound` (Audio playback)
* `pywhatkit`, `wikipedia`, `pyjokes` (Web queries and entertainment)
* `pyautogui` (Keyboard automation)

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/rishank012/Voice-Assistant.git](https://github.com/rishank012/Voice-Assistant.git)
   cd Voice-Assistant
   ```

2. **Install the required dependencies:**
   ```bash
   pip install Pillow SpeechRecognition playsound pygame pyttsx3 wikipedia pywhatkit pyjokes pyautogui edge-tts
   ```

3. **Install PyAudio:**
   *If you are on Windows, you can usually install it directly:*
   ```bash
   pip install pyaudio
   ```
   *If you encounter errors, you may need to install the appropriate `.whl` file for your Python version.*

4. **Directory Structure Requirements:**
   Friday relies on specific audio and visual files to function correctly. Ensure your local directory has the following folders populated with your media:
   * `Themes/` (Contains your `1.gif` through `8.gif` files)
   * `audios/` (Contains categorized `.mp3` files for responses like `greetings/`, `wish/`, etc.)

## ⚠️ Important Developer Note

**Local Paths:** Some functions in this script (like opening VS Code, Discord, or specific music folders) currently use hardcoded local directories (e.g., `C:\Users\risha\...`). 
* If you are cloning this repository to run on your own machine, please update these directory paths in the `start_listening()` function to match your system's configuration.

## 🤝 Usage

Run the main Python file to launch the assistant:
```bash
python Friday.py
```
* **To activate:** Say "Friday".
* **To exit:** Say "Close", "Exit", or "Hata", or use the `File > Exit` dropdown in the GUI.
