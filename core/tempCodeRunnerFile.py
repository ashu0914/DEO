from pydub import AudioSegment

def enhance_voice(input_file, output_file):
    sound = AudioSegment.from_file(input_file)

    # Venom feel: slow + deep
    slowed = sound - 6
    slowed = slowed.low_pass_filter(3000)

    slowed.export(output_file, format="mp3")