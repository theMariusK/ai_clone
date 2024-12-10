import pyttsx3
from io import BytesIO
import os

def text_to_speech(prompt) -> BytesIO:
    # Initialize pyttsx3 engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Selecting a female voice
    engine.setProperty('rate', 150)  # Adjust the speech rate if needed
    text_to_speak = f"<pitch middle='10'>{prompt}</pitch>"
    byte_array = BytesIO()
    
    # Use a temporary file for synthesis
    temp_file = "temp_audio.wav"
    try:
        engine.save_to_file(text_to_speak, temp_file)
        engine.runAndWait()

        # Read the WAV file back into BytesIO
        with open(temp_file, "rb") as f:
            byte_array.write(f.read())

    finally:
        # Delete the temporary file after reading
        if os.path.exists(temp_file):
            os.remove(temp_file)

    # Reset buffer position to the start
    byte_array.seek(0)

    return byte_array
