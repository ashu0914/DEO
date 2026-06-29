import os
import time
import threading
import pygame
import asyncio
import edge_tts
import re
import datetime # 👈 Time check karne ke liye add kiya
from core.audio_fx import enhance_voice 

AUDIO_PLAYING = False
SHOULD_STOP = False
VOICE_NAME = "hi-IN-SwaraNeural" 

async def generate_audio(text, output_file):
    try:
        communicate = edge_tts.Communicate(text, VOICE_NAME)
        await communicate.save(output_file)
        return True
    except Exception as e:
        print(f"\n[Edge-TTS Internal Error]: {e}")
        return False

def _play_worker(text):
    global AUDIO_PLAYING, SHOULD_STOP
    AUDIO_PLAYING = True
    SHOULD_STOP = False
    
    raw_temp_file = "raw_voice.wav"
    venom_output_file = "deo_voice.wav"
    
    print(f"\n[DEO]: {text}") 
    
    # 🔊 TEXT CLEANING
    text_fixed = text.lower()
    text_fixed = re.sub(r'\*.*?\*', '', text_fixed)
    text_fixed = re.sub(r'\(.*?\)', '', text_fixed)
    
    text_fixed = text_fixed.replace(" fir ", " phir ").replace(" fir,", " phir ").replace(" fir.", " phir ")
    text_fixed = text_fixed.replace("firise", "phir se").replace("fir se", "phir se")
    text_fixed = text_fixed.replace("maza", "maajja").replace("maze lene", "maajje lene").replace("maze", "maajje")
    
    text_fixed = ' '.join(text_fixed.split())
    
    # 1. Pehle normal voice generate karo
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    success = loop.run_until_complete(generate_audio(text_fixed, raw_temp_file))
    loop.close()
    
    if not success or not os.path.exists(raw_temp_file):
        print("[Audio Error]: Normal voice generate nahi ho payi!")
        AUDIO_PLAYING = False
        return

    # 2. ⚡ APPLY VENOM EFFECT (With FFmpeg Smart Bypass)
    # Agar FFmpeg error (WinError 2) aayega, toh system crash nahi hoga, raw file direct chalegi!
    file_to_play = venom_output_file
    try:
        enhance_voice(raw_temp_file, venom_output_file)
        if not os.path.exists(venom_output_file) or os.path.getsize(venom_output_file) == 0:
            file_to_play = raw_temp_file
    except FileNotFoundError:
        print("⚠️ [System Alert]: FFmpeg missing hai, Boss. Normal voice me play kar rahi hoon.")
        file_to_play = raw_temp_file
    except Exception as e:
        print(f"⚠️ [Audio FX Error]: {e}. Falling back to normal voice.")
        file_to_play = raw_temp_file

    # 3. Final audio wave play karo
    try:
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load(file_to_play)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            if SHOULD_STOP:
                pygame.mixer.music.stop()
                break
            time.sleep(0.05)
            
        pygame.mixer.music.unload()
        pygame.mixer.quit()
    except Exception as e:
        print(f"\n[Pygame Mixer Error]: {e}")
        
    # Temporary files clean up safely
    try:
        time.sleep(0.2)
        if os.path.exists(raw_temp_file): os.remove(raw_temp_file)
        if os.path.exists(venom_output_file): os.remove(venom_output_file)
    except:
        pass
        
    AUDIO_PLAYING = False

def speak(text):
    t = threading.Thread(target=_play_worker, args=(text,))
    t.daemon = True
    t.start()

def stop_speaking():
    global SHOULD_STOP          
    if AUDIO_PLAYING:
        SHOULD_STOP = True
        print("\n🛑 [Nova Chup ho gayi]")