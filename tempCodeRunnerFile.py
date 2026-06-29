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

def main():
    print("🚀 [System]: Nova is starting up...")
    
    # 💼 BOSS FIX: Professional 1-line startup greeting
    startup_greeting = ask_ai("Greet Boss Ashu in strictly one short english sentence like a professional employee and say what can i do for you.")
    speak(startup_greeting)
    time.sleep(1.5) 

    print("🎧 [Mic Check]: Ready. Waiting for 'Nova'...")

    while True:
        raw_activation = listen()

        if not raw_activation:
            continue
            
        raw_lower = raw_activation.lower().strip()
        print(f"🎤 [Mic Heard]: '{raw_lower}'")

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