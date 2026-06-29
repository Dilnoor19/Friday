import datetime
import time
import threading
import psutil
import pyautogui
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import requests
import pyjokes
import wikipedia
import pywhatkit as kit

# ─────────────────────────────────────────────
#  CONFIG  —  replace with your actual keys
# ─────────────────────────────────────────────
GEMINI_API_KEY = "put your own api key"
GEMINI_URL     = "put your gemini url"
WEATHER_API_KEY = "put your own api key"
NEWS_API_KEY    = "put your own api key"

# ─────────────────────────────────────────────
#  CHAT HISTORY  (last 10 exchanges)
# ─────────────────────────────────────────────
chat_history = []   # [ {"role": "user"/"friday", "text": "..."} ]

def add_to_history(role: str, text: str):
    chat_history.append({"role": role, "text": text})
    if len(chat_history) > 20:          # keep last 10 pairs
        chat_history.pop(0)

def show_history():
    if not chat_history:
        speak("No chat history yet, boss.")
        return
    speak(f"Here are your last {len(chat_history)//2 or 1} exchanges.")
    for entry in chat_history[-10:]:
        label = "You" if entry["role"] == "user" else "Friday"
        print(f"  [{label}]: {entry['text']}")

# ─────────────────────────────────────────────
#  REMINDERS
# ─────────────────────────────────────────────
reminders = []   # [ {"time": datetime, "message": str, "fired": bool} ]

def add_reminder(message: str, minutes: int):
    fire_at = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    reminders.append({"time": fire_at, "message": message, "fired": False})
    speak(f"Reminder set: '{message}' in {minutes} minute{'s' if minutes != 1 else ''}.")

def check_reminders():
    """Background thread — fires reminders on time."""
    while True:
        now = datetime.datetime.now()
        for r in reminders:
            if not r["fired"] and now >= r["time"]:
                speak(f"⏰ Reminder: {r['message']}")
                r["fired"] = True
        time.sleep(15)

threading.Thread(target=check_reminders, daemon=True).start()

def parse_reminder_command(command: str):
    """
    Accepts commands like:
      'set reminder call mom in 10 minutes'
      'remind me to drink water in 5 minutes'
    """
    try:
        # extract minutes
        words = command.split()
        minutes = None
        for i, w in enumerate(words):
            if w.isdigit():
                minutes = int(w)
                break
        if minutes is None:
            speak("Please tell me how many minutes for the reminder.")
            return

        # extract message — everything before 'in N minute'
        if "remind me to" in command:
            msg_raw = command.split("remind me to")[1]
        elif "set reminder" in command:
            msg_raw = command.split("set reminder")[1]
        else:
            msg_raw = command

        # strip the trailing 'in N minutes' part
        for kw in [f"in {minutes} minutes", f"in {minutes} minute"]:
            msg_raw = msg_raw.replace(kw, "").strip()

        message = msg_raw.strip() or "your reminder"
        add_reminder(message, minutes)
    except Exception as e:
        speak("Sorry, I couldn't parse that reminder.")
        print(f"[Reminder parse error] {e}")

def list_reminders():
    pending = [r for r in reminders if not r["fired"]]
    if not pending:
        speak("You have no pending reminders.")
        return
    speak(f"You have {len(pending)} pending reminder{'s' if len(pending) > 1 else ''}.")
    for r in pending:
        time_str = r["time"].strftime("%I:%M %p")
        print(f"  • {r['message']} at {time_str}")
        speak(f"{r['message']} at {time_str}")

# ─────────────────────────────────────────────
#  SYSTEM INFO
# ─────────────────────────────────────────────
def get_system_info():
    cpu    = psutil.cpu_percent(interval=1)
    ram    = psutil.virtual_memory()
    disk   = psutil.disk_usage('/')
    battery = psutil.sensors_battery()

    ram_used  = round(ram.used  / (1024**3), 1)
    ram_total = round(ram.total / (1024**3), 1)
    disk_used  = round(disk.used  / (1024**3), 1)
    disk_total = round(disk.total / (1024**3), 1)

    info = (
        f"CPU usage is {cpu}%. "
        f"RAM: {ram_used} GB used out of {ram_total} GB ({ram.percent}%). "
        f"Disk: {disk_used} GB used out of {disk_total} GB."
    )
    if battery:
        charge = round(battery.percent)
        plugged = "plugged in" if battery.power_plugged else "on battery"
        info += f" Battery is at {charge}%, {plugged}."

    print(f"\n📊 System Info:\n  CPU     : {cpu}%\n  RAM     : {ram_used}/{ram_total} GB\n  Disk    : {disk_used}/{disk_total} GB")
    if battery:
        print(f"  Battery : {charge}% ({'🔌' if battery.power_plugged else '🔋'})")
    speak(info)

# ─────────────────────────────────────────────
#  CALCULATOR / UNIT CONVERTER
# ─────────────────────────────────────────────
def safe_calculate(expression: str) -> str:
    """Evaluate a simple math expression safely."""
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return None
    try:
        result = eval(expression)   # safe — only digits & operators allowed
        return str(result)
    except Exception:
        return None

UNIT_CONVERSIONS = {
    # length
    "km to miles":      lambda v: v * 0.621371,
    "miles to km":      lambda v: v * 1.60934,
    "meters to feet":   lambda v: v * 3.28084,
    "feet to meters":   lambda v: v / 3.28084,
    "cm to inches":     lambda v: v / 2.54,
    "inches to cm":     lambda v: v * 2.54,
    # weight
    "kg to pounds":     lambda v: v * 2.20462,
    "pounds to kg":     lambda v: v / 2.20462,
    "grams to ounces":  lambda v: v * 0.035274,
    "ounces to grams":  lambda v: v / 0.035274,
    # temperature
    "celsius to fahrenheit": lambda v: (v * 9/5) + 32,
    "fahrenheit to celsius": lambda v: (v - 32) * 5/9,
    # data
    "mb to gb":         lambda v: v / 1024,
    "gb to mb":         lambda v: v * 1024,
    "gb to tb":         lambda v: v / 1024,
    "tb to gb":         lambda v: v * 1024,
}

def handle_calculator(command: str):
    """
    Routes to either unit converter or math evaluator.
    Examples:
      'calculate 25 * 4 + 10'
      'convert 100 km to miles'
    """
    command = command.lower()

    # ── unit conversion ──────────────────────
    if "convert" in command:
        for key, fn in UNIT_CONVERSIONS.items():
            if key in command:
                parts = command.replace("convert", "").strip().split()
                try:
                    value = float(parts[0])
                    result = round(fn(value), 4)
                    speak(f"{value} {key.split(' to ')[0]} is {result} {key.split(' to ')[1]}.")
                    print(f"  🔁 {value} {key} = {result}")
                    return
                except (ValueError, IndexError):
                    speak("Please say the value before the unit, like: convert 100 km to miles.")
                    return
        speak("Sorry, I don't know that conversion yet.")
        return

    # ── math calculation ─────────────────────
    expr = command.replace("calculate", "").replace("what is", "").replace("?", "").strip()
    # replace spoken words with symbols
    expr = (expr
            .replace("plus", "+").replace("minus", "-")
            .replace("multiplied by", "*").replace("times", "*")
            .replace("divided by", "/").replace("x", "*"))
    result = safe_calculate(expr)
    if result:
        speak(f"The answer is {result}.")
        print(f"  🧮 {expr} = {result}")
    else:
        speak("Sorry, I couldn't calculate that.")

# ─────────────────────────────────────────────
#  TTS ENGINE
# ─────────────────────────────────────────────
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", engine.getProperty("rate") - 50)
engine.setProperty("volume", min(engine.getProperty("volume") + 0.25, 1.0))

def speak(text: str):
    print(f"🤖 Friday: {text}")
    engine.say(text)
    engine.runAndWait()

# ─────────────────────────────────────────────
#  LISTEN  (improved)
# ─────────────────────────────────────────────
def listen(retries: int = 2) -> str:
    """
    Listens for a voice command with retry logic and better noise handling.
    Returns the recognised text (lowercase) or "" on failure.
    """
    r = sr.Recognizer()
    r.energy_threshold = 300          # more sensitive than default 4000
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8

    for attempt in range(1, retries + 1):
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.6)
                print(f"🎙️  Listening... (attempt {attempt}/{retries})")
                audio = r.listen(source, timeout=6, phrase_time_limit=12)

            text = r.recognize_google(audio, language="en-in").lower()
            print(f"   Heard: {text}")
            return text

        except sr.WaitTimeoutError:
            print("   [Timeout — no speech detected]")
        except sr.UnknownValueError:
            print("   [Could not understand audio]")
        except sr.RequestError as e:
            speak("Network error reaching speech service.")
            print(f"   [RequestError] {e}")
            return ""
        except OSError as e:
            speak("Microphone not found. Please check your mic and try again.")
            print(f"   [OSError] {e}")
            return ""

    speak("I couldn't catch that. Please try again.")
    return ""

# ─────────────────────────────────────────────
#  MISC HELPERS  (unchanged logic, tidied up)
# ─────────────────────────────────────────────
def fun():
    speak(pyjokes.get_joke())

def take_screenshot():
    pyautogui.screenshot().save("screenshot.png")
    speak("Screenshot taken and saved.")

def cal_day() -> str:
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    return days[datetime.datetime.today().weekday()]

def wishme():
    hour = int(datetime.datetime.now().hour)
    t    = time.strftime("%I:%M %p")
    day  = cal_day()
    if hour < 12:
        speak(f"Good morning, boss! It's {day} and the time is {t}.")
    elif hour < 17:
        speak(f"Good afternoon, boss! It's {day} and the time is {t}.")
    else:
        speak(f"Good evening, boss! It's {day} and the time is {t}.")

def show_time():
    t = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {t}.")
    print(f"🕐 {t}")

def search_wikipedia(query: str):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("That topic is ambiguous. Can you be more specific?")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find a Wikipedia page for that.")
    except Exception as e:
        speak("Sorry, Wikipedia search failed.")
        print(f"[Wikipedia error] {e}")

def schedule():
    day = cal_day().lower()
    plans = {
        "monday":    "Work 9–5, workout after 6 PM, then personal projects 8–10 PM.",
        "tuesday":   "Work 9–5, workout after 6 PM, then skill-building 8–10 PM.",
        "wednesday": "Work 9–5, workout after 6 PM, then reading or studying 8–10 PM.",
        "thursday":  "Work 9–5, workout after 6 PM, then project review 8–10 PM.",
        "friday":    "Work 9–5, relax after 6 PM, light learning or hobby 8–10 PM.",
        "saturday":  "Free day! 3 hours of learning or passion project, workout at 7 PM.",
        "sunday":    "Rest day. Reflect on the week and plan the next one.",
    }
    speak(plans.get(day, "No schedule found for today."))

def open_website(command: str) -> bool:
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
        "paper trading": "https://in.tradingview.com/",
        "github":        "https://github.com/",
        "stackoverflow": "https://stackoverflow.com/",
        "leetcode":      "https://leetcode.com/",
    }
    for name, url in websites.items():
        if f"open {name}" in command:
            try:
                webbrowser.open(url)
                speak(f"Opening {name}.")
            except Exception as e:
                speak(f"Couldn't open {name}.")
                print(f"[Website error] {e}")
            return True
    return False

def open_apps(command: str) -> bool:
    apps = {
        "instagram":       "C:/Users/dilno/OneDrive/Desktop/Instagram.lnk",
        "brave":           "C:/Users/dilno/OneDrive/Desktop/Brave.lnk",
        "spotify":         "C:/Users/dilno/OneDrive/Desktop/Spotify.lnk",
        "whatsapp":        "C:/Users/dilno/OneDrive/Desktop/WhatsApp.lnk",
        "youtube":         "C:/Users/dilno/OneDrive/Desktop/YouTube.lnk",
        "vs code":         "C:/Users/dilno/OneDrive/Desktop/Visual Studio Code.lnk",
        "store":           "C:/Users/dilno/OneDrive/Desktop/Microsoft Store.lnk",
        "chrome":          "C:/Users/Public/Desktop/Google Chrome.lnk",
        "microsoft edge":  "C:/Users/Public/Desktop/Microsoft Edge.lnk",
        "copilot":         "C:/Users/dilno/OneDrive/Desktop/Copilot.lnk",
        "chatgpt":         "C:/Users/dilno/OneDrive/Desktop/ChatGPT.lnk",
        "github desktop":  "C:/Users/dilno/OneDrive/Desktop/GitHub.lnk",
        "camera":          "C:/Users/dilno/OneDrive/Desktop/Camera.lnk",
        "linkedin":        "C:/Users/dilno/OneDrive/Desktop/LinkedIn.lnk",
    }
    for name, path in apps.items():
        if f"open {name}" in command:
            try:
                os.startfile(path)
                speak(f"Opening {name}.")
            except Exception as e:
                speak(f"Couldn't open {name}. Make sure the shortcut path is correct.")
                print(f"[App error] {e}")
            return True
    return False

def get_weather(city: str = "Delhi"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        data = requests.get(url, timeout=5).json()
        if data.get("cod") != 200:
            speak("Sorry, I couldn't fetch the weather. Check your API key or city name.")
            return
        desc  = data["weather"][0]["description"]
        temp  = data["main"]["temp"]
        hum   = data["main"]["humidity"]
        wind  = data["wind"]["speed"]
        speak(f"Weather in {city}: {desc}. Temperature {temp}°C, humidity {hum}%, wind {wind} m/s.")
    except requests.exceptions.Timeout:
        speak("Weather request timed out. Check your internet.")
    except Exception as e:
        speak("Couldn't retrieve weather details.")
        print(f"[Weather error] {e}")

def play_song():
    speak("What song would you like to play?")
    song = listen()
    if song:
        kit.playonyt(song)
        speak(f"Playing {song} on YouTube.")
    else:
        speak("Couldn't catch the song name.")

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    try:
        data  = requests.get(url, timeout=5).json()
        items = data.get("articles", [])[:5]
        if not items:
            speak("No news found right now.")
            return
        speak("Here are today's top 5 headlines.")
        for i, a in enumerate(items, 1):
            print(f"  {i}. {a['title']}")
            speak(a["title"])
    except Exception as e:
        speak("Couldn't fetch news.")
        print(f"[News error] {e}")

def chat_with_gemini(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    data    = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        resp = requests.post(GEMINI_URL, headers=headers, json=data, timeout=10)
        if resp.status_code == 200:
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        return f"Gemini error {resp.status_code}."
    except requests.exceptions.Timeout:
        return "Gemini request timed out."
    except Exception as e:
        return f"Gemini error: {e}"

# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────
def command_prompt():
    wishme()
    speak("Friday is online and ready, boss.")

    while True:
        command = listen()
        if not command:
            continue

        add_to_history("user", command)

        # ── OPEN website / app ────────────────
        if "open " in command:
            if not open_website(command):
                if not open_apps(command):
                    speak("Couldn't find that website or application.")

        # ── REMINDERS ────────────────────────
        elif any(kw in command for kw in ["set reminder", "remind me"]):
            parse_reminder_command(command)

        elif "list reminder" in command or "show reminder" in command:
            list_reminders()

        # ── SYSTEM INFO ──────────────────────
        elif any(kw in command for kw in ["system info", "cpu usage", "ram usage", "battery", "disk space"]):
            get_system_info()

        # ── CALCULATOR / CONVERTER ───────────
        elif any(kw in command for kw in ["calculate", "what is", "convert"]):
            handle_calculator(command)

        # ── CHAT HISTORY ─────────────────────
        elif any(kw in command for kw in ["chat history", "show history", "last commands"]):
            show_history()

        # ── MISC ─────────────────────────────
        elif "something funny" in command or "tell me a joke" in command:
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

        elif "play song" in command or "play music" in command:
            play_song()

        elif "screenshot" in command or "take ss" in command:
            take_screenshot()

        elif "news" in command:
            get_news()

        elif "wikipedia" in command:
            query = command.replace("wikipedia", "").strip()
            search_wikipedia(query) if query else speak("What should I search on Wikipedia?")

        elif "exit" in command or "stop" in command or "shutdown" in command:
            speak("Goodbye, boss. Friday going offline.")
            break

        # ── FALLBACK → Gemini ─────────────────
        else:
            response = chat_with_gemini(command)
            add_to_history("friday", response)
            speak(response)


if __name__ == "__main__":
    command_prompt()
