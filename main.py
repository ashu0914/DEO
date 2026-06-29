import time
import re
from core.speak import speak, stop_speaking, AUDIO_PLAYING
from core.voice import listen
from core.commands import execute
from core.brain import ask_ai

WAKE_WORDS = ["nova", "nove", "noova", "noa", "noba", "नोवा", "नवा", "नोve"]

# ⚡ SYSTEM KEYWORDS: Direct OS execution
SYSTEM_KEYWORDS = [
    "youtube", "spotify", "chrome", "google", "volume", "aawaz", "pause", 
    "play", "chalao", "gaana", "song", "gana", "screenshot", "lock pc", 
    "shutdown", "restart", "vs code", "vscode", "terminal", "cmd", 
    "calculator", "notepad", "time", "samay", "date", "tarikh", "weather", 
    "mausam", "close", "band karo"
]

def clean_wake_word(raw_text):
    """Wake word ko remove karne ka safe aur clean tareeka regular expressions se"""
    pattern = re.compile(r'\b(' + '|'.join(WAKE_WORDS) + r')\b', re.IGNORECASE)
    cleaned = pattern.sub("", raw_text)
    return cleaned.strip()

ddef main():
    print("🚀 [System]: Nova is starting up...")
    
    # 🕒 TIME LOGIC: Current hour nikalne ke liye
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        time_context = "Morning"
    elif 12 <= current_hour < 17:
        time_context = "Afternoon"
    elif 17 <= current_hour < 22:
        time_context = "Evening"
    else:
        time_context = "Night"

    # AI Brain ko current time zone bataya taaki greeting hamesha accurate ho
    prompt = (
        f"It is currently {time_context}. Greet Boss Ashu in strictly one short English sentence "
        f"appropriate for this time of day like a professional employee and ask how you can assist him."
    )
    
    startup_greeting = ask_ai(prompt)
    speak(startup_greeting)
    time.sleep(1.5) 

    print("🎧 [Mic Check]: Ready. Waiting for 'Nova'...")
    # ... baaki aapka niche ka poora loop bilkul same rahega ...

        # 🛑 INSTANT INTERRUPTION CONTROL
        if any(x in raw_lower for x in ["nova chup", "chup ho ja", "stop", "gaana roko", "pause"]):
            print("🛑 [System]: Interruption detected!")
            stop_speaking() 
            execute("pause") 
            continue

        wake_detected = any(word in raw_lower for word in WAKE_WORDS)

        if wake_detected:
            clean_command = clean_wake_word(raw_lower)
            print(f"✨ [Nova Active]: Command is -> '{clean_command}'")

            if not clean_command:
                # Sirf naam lene par quick professional acknowledgement
                reply = ask_ai("Boss just called your name. Respond in 3-4 words max in Hinglish, acknowledging you are listening.")
                speak(reply)
                execute("", ai_reply=reply)
            else:
                if any(x in clean_command for x in ["bye", "exit", "band ho"]):
                    speak("Ok Boss, system off kar rahi hoon. Take care.")
                    time.sleep(1.5)
                    break
                
                # ⚡ FAST TRACK BYPASS: Check if it's a direct system command
                if any(keyword in clean_command for keyword in SYSTEM_KEYWORDS):
                    print("⚙️ [Fast Track]: Executing system/app command directly...")
                    execute(clean_command)
                else:
                    # Normal baatein -> Goes to AI Brain
                    reply = ask_ai(clean_command)
                    speak(reply)
                    execute(clean_command, ai_reply=reply)
            
            time.sleep(1.5)

if __name__ == "__main__":
    main()