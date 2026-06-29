import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    # Dynamic ambient noise setup taaki background ka shor mic ko disturb na kare
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300  
    
    with sr.Microphone() as source:
        print("\n🎤 [Mic Status]: Listening silently...")
        r.adjust_for_ambient_noise(source, duration=0.8)
        try:
            # 3 second tak agar kuch nahi bola toh timeout ho jayega aur loop dubara chalega
            audio = r.listen(source, timeout=4, phrase_time_limit=5)
            print("⚡ [Mic Status]: Audio captured! Recognizing...")
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            print(f"❌ [Mic Error]: {e}")
            return ""

    try:
        # Hindi aur English dono mix pehchanne ke liye 'hi-IN' default rakha hai
        text = r.recognize_google(audio, language="hi-IN")
        if text.strip():
            return text
    except sr.UnknownValueError:
        # Iska matlab mic ne sound suna par samajh nahi paya kya bola
        print("❓ [Mic Status]: Kuch sunai diya par samajh nahi aaya...")
        return ""
    except sr.RequestError as e:
        print(f"❌ [Google API Error]: Internet issue hai shayad -> {e}")
        return ""
        
    return ""