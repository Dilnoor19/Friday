# 🤖 Friday — AI Voice Assistant

> A Python-based voice assistant for Windows, built to automate daily tasks through voice commands.  
> **Succeeded by [Orion v1](https://github.com/dilnoor19/orion-v1)** — a more powerful evolution of this project.

---

## 💡 About

Friday is a personal AI voice assistant that understands natural speech and responds with voice output. It was built as a hands-on Python project to explore speech recognition, TTS, API integration, and automation — and later became the foundation for **Orion v1**.

---

## ✨ Features

- 🎙️ **Voice recognition** — listens and responds using Google Speech API
- 💬 **AI chat** — powered by Google Gemini for open-ended conversations
- 🌤️ **Live weather** — fetches real-time weather via OpenWeatherMap
- 📰 **News updates** — reads top 5 Indian headlines via NewsAPI
- 🎵 **Play songs** — plays any song on YouTube by voice
- 🌐 **Open websites** — Netflix, Discord, GitHub, and more
- 🖥️ **Open apps** — VS Code, Spotify, WhatsApp, Chrome, and more
- 📅 **Daily schedule** — reads your personalised weekly plan
- 📸 **Screenshot** — saves a screenshot instantly
- 😂 **Jokes** — tells random programming jokes
- 🔊 **Volume control** — increase, decrease, or mute by voice
- 🕐 **Time & date** — tells current time and day

---

## 🛠️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/dilnoor19/friday.git
cd friday
```

### 2. Install dependencies
```bash
pip install pyttsx3 SpeechRecognition pyautogui pyjokes wikipedia pywhatkit requests pyaudio
```

> ⚠️ If `pyaudio` fails on Windows:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 3. Add your API keys
Open `main.py` and replace the placeholders:
```python
API_KEY         = "your_gemini_api_key"
URL             = "your_gemini_endpoint_url"
WEATHER_API_KEY = "your_openweathermap_api_key"
NEWS_API_KEY    = "your_newsapi_key"
```

### 4. Update app shortcuts
In `open_apps()`, update the `.lnk` paths to match shortcuts on your own desktop.

### 5. Run
```bash
python main.py
```

---

## 🗣️ Example Commands

```
"Open Netflix"
"What's the weather?"
"Tell me a joke"
"Play song Kesariya"
"News"
"Take screenshot"
"Schedule"
"Time"
"Exit"
```

---

## 📁 Project Structure

```
friday/
├── main.py        # Core assistant
├── screenshot.png # Saved when you say "take screenshot"
└── README.md
```

---

## 🔮 What's Next

This project has been succeeded by **[Orion v1](https://github.com/dilnoor19/orion-v1)** — a fully upgraded version with:
- Better mic handling & retry logic
- Reminders, system info, calculator & unit converter
- Chat history memory
- And more coming in Orion v2...

---

## 👨‍💻 Author

**Dilnoor** — BCA Student, Python Developer  
GitHub: [github.com/dilnoor19](https://github.com/dilnoor19)

---

## 📄 License

MIT License
