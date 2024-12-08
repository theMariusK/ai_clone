import moviepy as mp
import librosa
from pydub import AudioSegment
from io import BytesIO
import soundfile as sf
import numpy as np

def separate_video_audio(video_file, video_folder, audio_folder):
    """Separate the audio and video streams from the uploaded video file."""
    video = mp.VideoFileClip(video_file)
    audio = video.audio
    
    video_output = f"{video_folder}/{video_file.split('/')[-1].split('.')[0]}_video.mp4"
    audio_output = f"{audio_folder}/{video_file.split('/')[-1].split('.')[0]}_audio.mp3"

    video.write_videofile(video_output, audio=False)
    audio.write_audiofile(audio_output)

    return video_output, audio_output

def process_video(video_file):
    """Process the uploaded video file."""
    print("Processing video")
    # Implement video processing logic (e.g., transcoding, encoding)
    pass

def process_audio(audio_file):
    # Preprocess audio
    prep_audio_wav = preprocess_audio(audio_file)
    
    # Extract mel spectogram from speech audio
    mel_spectogram = generate_mel_spectrogram(prep_audio_wav)
    
    # Save mel spectogram
    # TODO: save me spectogram in databse together with username associated to the speech audio. 
    # Username should be obtained somehow in the request of Flask
    pass

def preprocess_audio(mp3_file, target_dbfs=-20.0, top_db=20, target_sample_rate=22050, target_channels=1):
    """
    Preprocess an MP3 file: convert to WAV, remove silence, and normalize volume.

    Args:
        mp3_file (BytesIO): MP3 file in memory.
        target_dbfs (float): Target volume level in dBFS (default: -20.0).
        top_db (int): Threshold in dB to consider as silence (default: 20).
        target_sample_rate (int): Desired sample rate (default: 22050 Hz).
        target_channels (int): Desired number of channels (default: 1, mono).

    Returns:
        BytesIO: Preprocessed WAV file in memory.
    """
    try:
        wav_file = convert_mp3_to_wav(mp3_file)

        wav_file = remove_silence(wav_file, top_db=top_db)

        wav_file = normalize_audio(wav_file, target_dbfs=target_dbfs)

        return wav_file

    except Exception as e:
        raise RuntimeError(f"Error en el preprocesamiento: {str(e)}")

def convert_mp3_to_wav(mp3_file):
    try:
        audio = AudioSegment.from_file(mp3_file, format="mp3")
        audio = audio.set_frame_rate(22050).set_channels(1) # Modify Hz and chanel settings (mono chanel)

        wav_file = BytesIO() # Output file

        audio.export(wav_file, format="wav")
        wav_file.seek(0)

        return wav_file

    except Exception as e:
        raise RuntimeError(f"Error converting MP3 to WAV: {str(e)}")

def remove_silence(wav_file, top_db=20):
    try:
        # Make cursor point to the begining of the file
        wav_file.seek(0)
        y, sr = librosa.load(wav_file, sr=None)

        # Trim silences
        y_trimmed, _ = librosa.effects.trim(y, top_db=top_db)

        processed_wav = BytesIO()
        sf.write(processed_wav, y_trimmed, sr, format='WAV')

        # Reset cursor
        processed_wav.seek(0)

        return processed_wav

    except Exception as e:
        raise RuntimeError(f"Error removing silences: {str(e)}")
    
def normalize_audio(wav_file, target_dbfs=-20.0):
    try:
        wav_file.seek(0)
        audio = AudioSegment.from_file(wav_file, format="wav")

        change_in_db = target_dbfs - audio.dBFS
        normalized_audio = audio.apply_gain(change_in_db)

        processed_wav = BytesIO()
        normalized_audio.export(processed_wav, format="wav")

        processed_wav.seek(0)

        return processed_wav

    except Exception as e:
        raise RuntimeError(f"Error al normalizar audio: {str(e)}")
    
def generate_mel_spectrogram(wav_file, n_mels=80, hop_length=256, win_length=1024, sr=22050):
    """
    Generate Mel Spectrogram from WAV file.
    
    Args:
        wav_file (BytesIO): WAV audio file in memory.
        n_mels (int): Number of Mel bands (default: 80).
        hop_length (int): Number of samples between successive frames (default: 256).
        win_length (int): Length of each window (default: 1024).
        sr (int): Sample rate (default: 22050 Hz).
        
    Returns:
        np.ndarray: Mel Spectrogram (log scale).
    """
    wav_file.seek(0)
    y, sr = librosa.load(wav_file, sr=sr)

    # Generate Mel spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_mels=n_mels,
        hop_length=hop_length,
        win_length=win_length,
        fmax=sr // 2
    )

    # Convert the Mel spectrogram to a logarithmic scale (log scale)
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
    
    return log_mel_spectrogram