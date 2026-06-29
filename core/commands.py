import os
import sys
import datetime
import urllib.parse
import webbrowser
import pyautogui
import requests
import psutil
from core.speak import speak

# Ek unique folder taaki agar user download ya screenshots le toh setup clear rahe
DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
PICTURES_PATH = os.path.join(os.path.expanduser("~"), "Pictures")

def get_weather():
    try:
        # Delhi coords default
        url = "https://api.open-meteo.com/v1/forecast?latitude=28.6139&longitude=77.2090&current_weather=true"
        response = requests.get(url).json()
        temp = response['current_weather']['temperature']
        return f"Ashu, abhi Delhi ka temperature {temp}°C chal raha hai."
    except:
        return "Mausam ki jankari nahi nikal payi Ashu, internet ek baar check karo na."

def execute(command, ai_reply=""):
    cmd_lower = command.lower().strip()
    reply_lower = ai_reply.lower().strip()

    print(f"\n⚙️ [System Engine]: Processing Command -> '{cmd_lower}'")

    if not cmd_lower:
        return

    # ---------------- 1. YOUTUBE AUTOMATION (Search / Play) ----------------
    if "youtube" in cmd_lower or "یوٹیوب" in cmd_lower or "यूट्यूब" in cmd_lower:
        search_query = cmd_lower
        for word in ["youtube", "pe", "par", "chalao", "play", "search", "kholo", "open", "यूट्यूब", "یوٹیوب"]:
            search_query = search_query.replace(word, "")
        search_query = search_query.strip()

        if search_query:
            speak(f"YouTube par {search_query} search kar rahi hoon Ashu...")
            encoded_query = urllib.parse.quote(search_query)
            webbrowser.open(f"https://www.youtube.com/results?search_query={encoded_query}")
        else:
            speak("YouTube open kar rahi hoon.")
            webbrowser.open("https://www.youtube.com")
        return

    # ---------------- 2. SMART SPOTIFY & MUSIC ENGINE ----------------
    elif any(x in cmd_lower for x in ["spotify", "स्पॉटिफाई", "gaana", "song", "music", "gana"]):
        song_name = cmd_lower
        for word in ["spotify", "स्पॉटिफाई", "se", "song", "gaana", "chalao", "play", "music", "chalana", "gana"]:
            song_name = song_name.replace(word, "")
        song_name = song_name.strip()

        if song_name:
            speak(f"Spotify par {song_name} chalati hoon...")
            encoded_song = urllib.parse.quote(song_name)
            os.system(f"start spotify:search:{encoded_song}")
        else:
            speak("Spotify open kar rahi hoon.")
            os.system("start spotify")
        return

    # ---------------- 3. CORE APPS & IDEs (Developer Settings) ----------------
    elif any(x in cmd_lower for x in ["chrome", "google", "browser"]):
        speak("Chrome khol rahi hoon.")
        os.system("start chrome")
        return

    elif any(x in cmd_lower for x in ["vs code", "vscode", "code editor"]):
        speak("VS Code open kar rahi hoon Ashu.")
        os.system("start code")
        return

    elif any(x in cmd_lower for x in ["cmd", "command prompt", "terminal"]):
        speak("Terminal open kar rahi hoon.")
        os.system("start cmd")
        return

    elif any(x in cmd_lower for x in ["calculator", "calc"]):
        speak("Calculator open kar rahi hoon.")
        os.system("start calc")
        return

    elif any(x in cmd_lower for x in ["notepad", "note"]):
        speak("Notepad open kar rahi hoon.")
        os.system("start notepad")
        return

    # ---------------- 4. WINDOWS UTILITIES & POWER CONTROLS ----------------
    elif any(x in cmd_lower for x in ["screenshot", "snap", "screen shot"]):
        speak("Screenshot le rahi hoon.")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = os.path.join(PICTURES_PATH, f"Nova_Screenshot_{timestamp}.png")
        pyautogui.screenshot(screenshot_file)
        speak("Screenshot Pictures folder me save kar diya hai.")
        return

    elif any(x in cmd_lower for x in ["lock pc", "computer lock", "pc lock"]):
        speak("PC lock kar rahi hoon Ashu.")
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return

    elif "shutdown" in cmd_lower or "pc band karo" in cmd_lower:
        speak("System shut down ho raha hai. Apna khayal rakhna Ashu.")
        os.system("shutdown /s /t 5")
        return

    elif "restart pc" in cmd_lower or "reboot" in cmd_lower:
        speak("PC restart kar rahi hoon.")
        os.system("shutdown /r /t 5")
        return

    # ---------------- 5. VOLUME & IN-APP MEDIA CONTROLS ----------------
    elif any(x in cmd_lower for x in ["volume up", "aawaz badhao", "volume badao", "loud"]):
        for _ in range(7): pyautogui.press("volumeup")
        speak("Aawaz badha di!")
        return

    elif any(x in cmd_lower for x in ["volume down", "aawaz kam karo", "volume kam"]):
        for _ in range(7): pyautogui.press("volumedown")
        speak("Volume kam kar di.")
        return

    elif any(x in cmd_lower for x in ["mute", "aawaz band"]):
        pyautogui.press("volumemute")
        speak("Mute kar diya.")
        return

    elif any(x in cmd_lower for x in ["pause", "rok do", "stop music", "chup", "unpause"]):
        pyautogui.press("playpause")
        return

    elif any(x in cmd_lower for x in ["next song", "gaana badlo", "agla gaana"]):
        pyautogui.press("nexttrack")
        speak("Next track play kar rahi hoon.")
        return

    # ---------------- 6. WEB GOOGLE SEARCHES ----------------
    elif "search" in cmd_lower or "google par dhoondo" in cmd_lower or "what is" in cmd_lower:
        search_term = cmd_lower
        for word in ["search", "google par dhoondo", "google pe", "what is", "dhoondo", "nova"]:
            search_term = search_term.replace(word, "")
        search_term = search_term.strip()

        if search_term:
            speak(f"Google par {search_term} dhoondh rahi hoon...")
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
        return

    # ---------------- 7. CURRENT TIME / DATE / WEATHER ----------------
    elif any(x in cmd_lower for x in ["time", "samay", "waqt"]):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Ashu, abhi {current_time} ho rahe hain.")
        return

    elif any(x in cmd_lower for x in ["date", "tarikh", "aaj kya din"]):
        current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Aaj {current_date} hai.")
        return

    elif any(x in cmd_lower for x in ["weather", "mausam", "temperature"]):
        weather_report = get_weather()
        speak(weather_report)
        return

    # ---------------- 8. KILL PROCESSES (Close Active Apps) ----------------
    elif any(x in cmd_lower for x in ["close", "band karo app", "kill"]):
        app_to_close = cmd_lower
        for word in ["close", "band", "karo", "app", "kill"]:
            app_to_close = app_to_close.replace(word, "")
        app_to_close = app_to_close.strip()

        if app_to_close:
            found = False
            for proc in psutil.process_iter(['pid', 'name']):
                if app_to_close in proc.info['name'].lower():
                    proc.kill()
                    found = True
            if found:
                speak(f"{app_to_close} app ko band kar diya hai.")
            else:
                speak(f"Ashu, mujhe {app_to_close} running nahi mila.")
        return