import datetime
import time
import pyautogui
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import requests
import json
import pyjokes
import wikipedia
import pywhatkit as kit

# ─────────────────────────────────────────────
#  CONFIG  —  replace with your actual keys
# ─────────────────────────────────────────────
API_KEY = "put your own api key"
URL     = "put your gemini url"

# ─────────────────────────────────────────────
#  GEMINI CHATBOT
# ─────────────────────────────────────────────
def chat_with_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError:
            return "Error: Unexpected response format."
    return f"Error {response.status_code}: {response.text}"

# ─────────────────────────────────────────────
#  TTS ENGINE
# ─────────────────────────────────────────────
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)
volume = engine.getProperty('volume')
engine.setProperty('volume', volume + 0.25)

def speak(text):
    print(f"🤖 Friday: {text}")
    engine.say(text)
    engine.runAndWait()

# ─────────────────────────────────────────────
#  LISTEN
# ─────────────────────────────────────────────
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("🎙️ Listening...")
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
    try:
        return r.recognize_google(audio, language='en-in').lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def fun():
    speak(pyjokes.get_joke())

def take_screenshot():
    pyautogui.screenshot().save("screenshot.png")
    speak("Screenshot taken.")

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {
        1: "Monday", 2: "Tuesday", 3: "Wednesday",
        4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"
    }
    return day_dict.get(day, "unknown")

def wishme():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()
    if hour >= 0 and hour <= 12 and 'AM' in t:
        speak(f"Good morning sir, it's {day} and the time is {t}.")
    elif hour >= 12 and hour <= 16 and 'PM' in t:
        speak(f"Good afternoon sir, it's {day} and the time is {t}.")
    else:
        speak(f"Good evening sir, it's {day} and the time is {t}.")

def show_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")
    speak(f"Current time: {current_time}")

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except Exception:
        speak("Sorry, I couldn't find anything on Wikipedia.")

def schedule():
    day = cal_day().lower()
    week = {
        "monday":    "Hey boss, today you have work from 9am to 5pm. After 6pm, do a little workout. Then, from 8pm to 10pm, work on personal projects or learn something new.",
        "tuesday":   "Hey boss, today you have work from 9am to 5pm. After 6pm, do a little workout. Then, from 8pm to 10pm, focus on improving a skill or working on a side project.",
        "wednesday": "Hey boss, today you have work from 9am to 5pm. After 6pm, do a little workout. Then, from 8pm to 10pm, read a book, work on a project, or study something useful.",
        "thursday":  "Hey boss, today you have work from 9am to 5pm. After 6pm, do a little workout. Then, from 8pm to 10pm, review your progress on your projects and plan for the next steps.",
        "friday":    "Hey boss, today you have work from 9am to 5pm. After 6pm, relax a little. Then, from 8pm to 10pm, either socialize, watch something educational, or practice a hobby.",
        "saturday":  "Hey boss, today is a free day! Spend at least 3 hours learning something new or working on a passion project. Do a workout at 7pm. After dinner, unwind, watch something informative, or read.",
        "sunday":    "Boss, today is a rest day. No workout, but make sure to eat well and reflect on the past week. Spend some time planning and preparing for the upcoming week."
    }
    if day in week:
        speak(week[day])

def open_website(query):
    websites = {
        "anime":         "https://hianime.to/",
        "discord":       "https://discord.com/",
        "type test":     "https://www.typingtest.com/",
        "jiocinema":     "https://www.jiocinema.com/",
        "snapchat":      "https://web.snapchat.com/",
        "w3":            "https://www.w3schools.com/",
        "fiverr":        "https://www.fiverr.com/",
        "aifinder":      "https://theresanaiforthat.com/",
        "mxplayer":      "https://www.mxplayer.in/",
        "netflix":       "https://www.netflix.com/in/",
        "c compiler":    "https://www.programiz.com/c-programming/online-compiler/",
        "paper trading": "https://in.tradingview.com/chart/Ovn2F72s/?symbol=BITSTAMP%3ABTCUSD",
    }
    query = query.lower()
    for name, url in websites.items():
        if f"open {name}" in query:
            try:
                webbrowser.open(url)
                speak(f"Opening {name}.")
            except Exception as e:
                speak(f"Sorry, I couldn't open {name}.")
                print(f"[Error] {e}")
            return True
    return False

def open_apps(query):
    apps = {
        "instagram":      "C:/Users/dilno/OneDrive/Desktop/Instagram.lnk",
        "brave":          "C:/Users/dilno/OneDrive/Desktop/Brave.lnk",
        "spotify":        "C:/Users/dilno/OneDrive/Desktop/Spotify.lnk",
        "whatsapp":       "C:/Users/dilno/OneDrive/Desktop/WhatsApp.lnk",
        "youtube":        "C:/Users/dilno/OneDrive/Desktop/YouTube.lnk",
        "vs code":        "C:/Users/dilno/OneDrive/Desktop/Visual Studio Code.lnk",
        "store":          "C:/Users/dilno/OneDrive/Desktop/Microsoft Store.lnk",
        "chrome":         "C:/Users/Public/Desktop/Google Chrome.lnk",
        "microsoft edge": "C:/Users/Public/Desktop/Microsoft Edge.lnk",
        "copilot":        "C:/Users/dilno/OneDrive/Desktop/Copilot.lnk",
        "chatgpt":        "C:/Users/dilno/OneDrive/Desktop/ChatGPT.lnk",
        "github":         "C:/Users/dilno/OneDrive/Desktop/GitHub.lnk",
        "camera":         "C:/Users/dilno/OneDrive/Desktop/Camera.lnk",
        "linkedin":       "C:/Users/dilno/OneDrive/Desktop/LinkedIn.lnk",
    }
    query = query.lower()
    for name, path in apps.items():
        if f"open {name}" in query:
            try:
                os.startfile(path)
                speak(f"Opening {name}.")
            except Exception as e:
                speak(f"Sorry, I couldn't open {name}.")
                print(f"[Error] {e}")
            return True
    return False

def get_weather(city="Delhi"):
    WEATHER_API_KEY = "put your own api key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        data = requests.get(url).json()
        if data["cod"] != 200:
            speak("Sorry, I couldn't fetch the weather.")
            return
        desc  = data["weather"][0]["description"]
        temp  = data["main"]["temp"]
        hum   = data["main"]["humidity"]
        wind  = data["wind"]["speed"]
        speak(f"The weather in {city} is {desc}. Temperature {temp}°C, humidity {hum}%, wind {wind} m/s.")
    except Exception as e:
        speak("I couldn't retrieve the weather details.")
        print(f"[Error] {e}")

def play_song():
    speak("What song would you like to play?")
    song_name = listen()
    if song_name:
        kit.playonyt(song_name)
        speak(f"Playing {song_name} on YouTube.")
    else:
        speak("I couldn't understand the song name.")

def get_news():
    NEWS_API_KEY = "put your own api key"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    try:
        data     = requests.get(url).json()
        articles = data.get("articles", [])[:5]
        for article in articles:
            speak(article["title"])
    except Exception as e:
        speak("Couldn't fetch news.")
        print(f"[Error] {e}")

# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────
def command_prompt():
    wishme()
    speak("Friday is online.")
    while True:
        command = listen()
        if not command:
            continue
        command = command.lower()

        if "open " in command:
            if not open_website(command):
                if not open_apps(command):
                    speak("Website or application not found.")
        elif "something funny" in command or "joke" in command:
            fun()
        elif "time" in command:
            show_time()
        elif "schedule" in command:
            schedule()
        elif "volume up" in command or "increase volume" in command:
            pyautogui.press("volumeup")
            speak("Volume increased.")
        elif "volume down" in command or "decrease volume" in command:
            pyautogui.press("volumedown")
            speak("Volume decreased.")
        elif "mute" in command:
            pyautogui.press("volumemute")
            speak("Muted.")
        elif "weather" in command:
            get_weather()
        elif "play song" in command:
            play_song()
        elif "take ss" in command or "screenshot" in command:
            take_screenshot()
        elif "news" in command:
            get_news()
        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        else:
            response = chat_with_gemini(command)
            speak(response)

if __name__ == "__main__":
    command_prompt()
