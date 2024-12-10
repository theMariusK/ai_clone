from io import BytesIO
import sounddevice as sd
import soundfile as sf
import numpy

def play_audio(audio: BytesIO, output_device=23):
    
    # Read the synthesized speech data
    data, samplerate = sf.read(audio)

    # Set the output device if specified
    if output_device is not None:
        sd.default.device = output_device

    # Play the synthesized speech using sounddevice
    sd.play(data, samplerate)
    sd.wait()