import os
import json
from groq import Groq
from dotenv import load_dotenv # 👈 Naya Import

# Load all environment variables from .env file
load_dotenv()
# ... baki aapka pura brain.py ka code bilkul same rahega ...
# System Environment Variable se key uthana (100% Secure & Professional)
# Make sure apne terminal me `export GROQ_API_KEY="your_key"` ya Windows me setx kiya ho.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    # Fallback backup agar env variables na load huye hon (Development convenience)

client = Groq(api_key=GROQ_API_KEY)
HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def ask_ai(user_prompt):
    # Identity fix: Pure system me name 'Nova' rakha hai ab
    system_instruction = (
        "You are Nova, an obedient, highly professional, and elite-level AI Corporate Assistant. "
        "The user is your Executive Boss (Ashirwad/Ashu). You must address him with absolute professional respect.\n\n"
        
        "CRITICAL RULES FOR LANGUAGE & LENGTH:\n"
        "1. RESPOND SHORTLY: Keep your responses extremely short, crisp, and directly to-the-point (STRICT MAXIMUM OF 1-2 SENTENCES). No explanations unless asked.\n"
        "2. DYNAMIC LANGUAGE SWITCHING:\n"
        "   - Read the user's prompt carefully to detect the language script and words.\n"
        "   - If the Boss inputs in English, you MUST reply strictly in formal corporate English.\n"
        "   - If the Boss inputs in Hinglish (Hindi text written in Latin alphabet/mix), you MUST reply strictly in smart, professional Hinglish.\n"
        "   - Never mix these rules. Match his language behavior dynamically.\n"
        "3. PERSONALITY BOUNDARIES: STRICTLY FORBID any romantic, girlfriend/boyfriend tones, or casual flirting. "
        "Do NOT write any emotional action markers, brackets, or expressions like *giggles*, *haha*, *smiles*, (hehe), or *blushes*. No emojis. "
        "Act strictly as a female professional employee using proper feminine Hindi grammar ('karti hoon', 'rahi hoon') ONLY when speaking in Hinglish."
    )

    history = load_history()
    messages = [{"role": "system", "content": system_instruction}]
    
    # Last 10 turns for context memory
    for msg in history[-10:]:
        messages.append(msg)
        
    messages.append({"role": "user", "content": user_prompt})

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.25, # Thoda aur stable short context responses ke liye
            max_tokens=100,
            top_p=1,
            stream=False
        )
        
        ai_reply = completion.choices[0].message.content
        
        history.append({"role": "user", "content": user_prompt})
        history.append({"role": "assistant", "content": ai_reply})
        save_history(history)
        
        return ai_reply
        
    except Exception as e:
        print(f"❌ [Brain Error]: {e}")
        return "System error, Boss. Please check the network configuration."