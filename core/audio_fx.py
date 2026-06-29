from pydub import AudioSegment

def enhance_voice(input_file, output_file):
    try:
        # WAV file direct read hogi bina ffmpeg warning ke
        sound = AudioSegment.from_file(input_file, format="wav")
        
        # Slow down and lower pitch for raw Venom effect
        slowed = sound - 6
        slowed = slowed.low_pass_filter(3000)
        
        # Strict WAV export constraint
        slowed.export(output_file, format="wav")
        return True
    except Exception as e:
        print(f"❌ [Audio FX Engine Error]: {e}")
        return False