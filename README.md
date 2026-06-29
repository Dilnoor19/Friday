# 🤖 Friday — AI Voice Assistant

> **This project has evolved.** Friday is the v1 predecessor to [Orion](https://github.com/dilnoor19/orion), a more powerful modular AI assistant. This repo is kept for reference and learning purposes.

Friday is a Python-based desktop voice assistant powered by Google Gemini AI. It listens to your voice, understands commands, and performs a wide range of tasks — from opening apps and playing music to fetching weather, news, and cracking jokes.

---

## ✨ Features

| Category | What it does |
|---|---|
| 🧠 AI Chat | Answers anything via Google Gemini API |
| 🎙️ Voice Input | Listens and recognizes speech using Google Speech Recognition |
| 🔊 Voice Output | Speaks responses using `pyttsx3` (offline TTS) |
| 🌐 Open Websites | Opens YouTube, Netflix, Discord, W3Schools, and more |
| 💻 Launch Apps | Launches VS Code, Spotify, WhatsApp, Instagram, etc. |
| 🌤️ Weather | Fetches live weather for any city via OpenWeatherMap |
| 📰 News | Reads out top 5 headlines from India via NewsAPI |
| 🎵 Play Music | Plays any song on YouTube via `pywhatkit` |
| 😂 Jokes | Tells random programmer jokes via `pyjokes` |
| 📸 Screenshot | Takes and saves a screenshot |
| 📅 Schedule | Reads out your daily schedule |
| 🕐 Time | Tells the current time |
| 🔊 Volume | Controls system volume (up/down/mute) |
| 📖 Wikipedia | Searches and reads Wikipedia summaries |

---

## 🛠️ Tech Stack

- **Python 3.x**
- `pyttsx3` — Text-to-Speech (offline, SAPI5)
- `speech_recognition` — Microphone input via Google Speech API
- `requests` — HTTP calls to Gemini, Weather, and News APIs
- `pywhatkit` — YouTube music playback
- `wikipedia` — Wikipedia search
- `pyjokes` — Random programmer jokes
- `pyautogui` — Screenshots and volume control
- `webbrowser` — Opening websites in browser
- `os` — Launching desktop apps

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/dilnoor19/friday-assistant.git
cd friday-assistant
```

### 2. Install dependencies

```bash
pip install pyttsx3 SpeechRecognition requests pywhatkit wikipedia pyjokes pyautogui
```

> **Note:** `pyaudio` is required for microphone access. Install it separately:
> ```bash
> pip install pyaudio
> ```
> If it fails on Windows, try:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 3. Add your API keys

Open `friday.py` and replace the placeholders at the top of the file:

```python
API_KEY = "your_gemini_api_key"
URL     = "your_gemini_endpoint_url"

WEATHER_API_KEY = "your_openweathermap_api_key"
NEWS_API_KEY    = "your_newsapi_key"
```

| API | Where to get it |
|---|---|
| Gemini | [Google AI Studio](https://aistudio.google.com/) |
| OpenWeatherMap | [openweathermap.org/api](https://openweathermap.org/api) |
| NewsAPI | [newsapi.org](https://newsapi.org/) |

### 4. Update app shortcut paths (Windows only)

In the `open_apps()` function, update the `.lnk` paths to match your own Desktop shortcuts:

```python
"vs code": "C:/Users/YOUR_USERNAME/OneDrive/Desktop/Visual Studio Code.lnk",
```

### 5. Run

```bash
python friday.py
```

---

## 🗣️ Voice Commands

```
"What is machine learning?"        → Asks Gemini AI
"Open YouTube"                     → Opens YouTube in browser
"Open VS Code"                     → Launches VS Code
"Play song"                        → Asks for song name, plays on YouTube
"What's the weather?"              → Reads Delhi weather
"Tell me the news"                 → Reads top 5 Indian headlines
"Tell me a joke"                   → Random programming joke
"Take screenshot"                  → Saves screenshot.png
"What's my schedule?"              → Reads today's daily plan
"What time is it?"                 → Tells current time
"Volume up / Volume down / Mute"   → Controls system volume
"Exit" / "Stop"                    → Shuts Friday down
```

---

## 📁 Project Structure

```
friday-assistant/
│
├── friday.py          # Main assistant script
├── screenshot.png     # Auto-saved here on screenshot command
└── README.md
```

---

## 🔮 What Changed in Orion v1 (Successor)

Friday was the foundation. [Orion](https://github.com/dilnoor19/orion) builds on everything here and adds:

- [x] Conversation history (last 10 exchanges remembered)
- [x] Reminder system with background thread timer
- [x] System info — CPU, RAM, battery, disk usage
- [x] Calculator and unit converter (km, kg, °C, GB, etc.)
- [x] Retry logic on failed mic input
- [x] Cleaner error handling across all modules
- [x] More websites (GitHub, LeetCode, Stack Overflow)

---

## 👨‍💻 Author

**Dilnoor** — BCA Student, Python Developer  
GitHub: [@dilnoor19](https://github.com/dilnoor19)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
