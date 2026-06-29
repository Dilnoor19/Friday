# 🤖 Friday — AI Voice Assistant
### *The foundation of Orion v1*

> Friday is a modular Python-based voice assistant built for Windows.  
> It serves as the direct predecessor to **Orion v1** — a more powerful, fully modular AI assistant currently in development.

---

## 🚀 What's New in This Version

This is a significant upgrade over the original Friday codebase:

| Area | Before | Now |
|------|--------|-----|
| Mic handling | Basic, crash-prone | Retry logic, noise threshold, OSError catch |
| Error handling | Bare except everywhere | Per-function try/except with meaningful messages |
| Reminders | ❌ | ✅ Background thread, natural language parsing |
| System Info | ❌ | ✅ CPU, RAM, Disk, Battery via psutil |
| Calculator | ❌ | ✅ Math eval + 15+ unit conversions |
| Chat History | ❌ | ✅ Last 10 exchanges stored in memory |
| Code structure | Single flat script | Grouped, documented, clean sections |

---

## 🧠 Features

### 🎙️ Voice Recognition
- Listens with retry logic (2 attempts before giving up)
- Dynamic energy threshold — adapts to noisy environments
- Graceful mic-not-found error handling

### 💬 AI Chat (Gemini)
- Fallback for any unrecognised command
- Powered by Google Gemini API

### ⏰ Reminders
- `"Set reminder call mom in 10 minutes"`
- `"Remind me to drink water in 5 minutes"`
- `"List reminders"` — shows all pending ones
- Fires in a background thread, never blocks the assistant

### 📊 System Info
- `"System info"` / `"CPU usage"` / `"Battery"`
- Shows CPU %, RAM usage, Disk space, Battery level & charging status

### 🧮 Calculator & Unit Converter
- `"Calculate 25 times 4 plus 10"`
- `"Convert 100 km to miles"`
- `"Convert 37 celsius to fahrenheit"`
- Supports: length, weight, temperature, and data units

### 🗂️ Chat History
- `"Show history"` / `"Last commands"`
- Displays last 10 exchanges between you and Friday

### 🌐 Open Websites & Apps
- `"Open Netflix"` / `"Open VS Code"` / `"Open GitHub"`
- Easily extendable — just add entries to the dictionaries

### 🌤️ Weather
- `"Weather"` → fetches live Delhi weather via OpenWeatherMap API

### 📰 News
- `"News"` → reads top 5 Indian headlines via NewsAPI

### 🎵 Play Songs
- `"Play song"` → asks for song name, plays on YouTube

### 📸 Screenshot
- `"Take screenshot"` / `"Take SS"`

### 😂 Jokes
- `"Tell me a joke"` / `"Something funny"`

### 📅 Schedule & Time
- `"Schedule"` → reads your daily plan
- `"Time"` → tells current time

---

## 🛠️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/dilnoor19/friday-assistant.git
cd friday-assistant
```

### 2. Install dependencies
```bash
pip install pyttsx3 SpeechRecognition pyautogui pyjokes wikipedia pywhatkit requests psutil pyaudio
```

> ⚠️ If `pyaudio` fails on Windows:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 3. Add your API keys
Open `friday_upgraded.py` and replace the placeholders at the top:
```python
GEMINI_API_KEY  = "your_gemini_api_key"
GEMINI_URL      = "your_gemini_endpoint_url"
WEATHER_API_KEY = "your_openweathermap_api_key"
NEWS_API_KEY    = "your_newsapi_key"
```

### 4. Update app shortcuts
In `open_apps()`, update the `.lnk` paths to match your own desktop shortcuts.

### 5. Run
```bash
python friday_upgraded.py
```

---

## 📁 Project Structure

```
friday-assistant/
│
├── friday_upgraded.py   # Main assistant file
├── screenshot.png       # Saved here when you say "take screenshot"
└── README.md            # This file
```

---

## 🗣️ Example Commands

```
"Open Netflix"
"What's the weather?"
"Set reminder drink water in 20 minutes"
"List reminders"
"System info"
"Calculate 150 divided by 6"
"Convert 5 kg to pounds"
"Show history"
"Tell me a joke"
"Play song Dil Chahta Hai"
"News"
"Take screenshot"
"Exit"
```

---

## 🔮 Orion v1 — What's Coming Next

Friday is the foundation. **Orion v1** is the evolution.

Planned upgrades in Orion:

- 🧩 **Fully modular architecture** — each feature in its own Python module
- 🧠 **Persistent memory** — remembers user preferences across sessions (JSON/SQLite)
- 🖥️ **GUI dashboard** — live status, command history, reminders panel (Tkinter or PyQt)
- 🔌 **Plugin system** — drop in new skills without touching core code
- 🌐 **Offline fallback** — works without internet using local LLM (Ollama)
- 📱 **Multi-device support** — control from phone via local network
- 🎯 **Wake word detection** — always-on listening with "Hey Orion"

> Friday was the experiment. Orion is the product.

---

## 👨‍💻 Author

**Dilnoor** — BCA Student, Python Developer  
GitHub: [github.com/dilnoor19](https://github.com/dilnoor19)

---

## 📄 License

MIT License — free to use, modify, and build on.
