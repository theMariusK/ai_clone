# Separation
import moviepy as mp
# Audio
import librosa
from pydub import AudioSegment
from io import BytesIO
import soundfile as sf
import numpy as np
# Video
import tempfile
import json
import os
import subprocess
from typing import Dict, Any
import cv2
import whisper
from deepface import DeepFace



def separate_video_audio(video_file, video_folder, audio_folder):
    """Separate the audio and video streams from the uploaded video file."""
    video = mp.VideoFileClip(video_file)
    audio = video.audio
    
    video_output = f"{video_folder}/{video_file.split('/')[-1].split('.')[0]}_video.mp4"
    audio_output = f"{audio_folder}/{video_file.split('/')[-1].split('.')[0]}_audio.mp3"

    video.write_videofile(video_output, audio=False)
    audio.write_audiofile(audio_output)

    return video_output, audio_output

def process_video(video_file_path):
    """Process the uploaded video file."""
    print("Processing video")
    
    video_processing_results = analyze_video(video_file_path)
    
    return video_processing_results

def process_audio(audio_file_path):
    # Preprocess audio
    # with open(audio_file_path, 'rb') as audio_file:
    #     audio_data = audio_file.read()
    prep_audio_wav = preprocess_audio(audio_file_path)
    
    # Extract mel spectogram from speech audio
    mel_spectogram = generate_mel_spectrogram(prep_audio_wav)
    mel_spectogram = mel_spectogram.tolist()
    
    # Save mel spectogram
    # TODO: save me spectogram in databse together with username associated to the speech audio. 
    # Username should be obtained somehow in the request of Flask
    return mel_spectogram



# Audio

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



# Video

def analyze_video(video_file_path: str) -> Dict[str, Any]:
    # Check if uploaded file is a video format
    if not video_file_path.endswith(('.mp4', '.m4v', '.mpeg', '.mov')):
        return {"error": "Invalid video format. Please upload an MP4 or a compatible video file."}

    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        with open(video_file_path, "rb") as file:
            tmp_video.write(file.read())
            tmp_video_path = tmp_video.name

    try:
        # Extract audio from the video using ffmpeg
        tmp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        # Using ffmpeg to extract audio: ensure ffmpeg is installed in the system
        subprocess.run(["ffmpeg", "-y", "-i", tmp_video_path, "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", tmp_audio_path], check=True)

        # Load video with OpenCV
        cap = cv2.VideoCapture(tmp_video_path)
        if not cap.isOpened():
            raise ValueError("Failed to open the video file.")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0

        # We will analyze one frame per second to speed up emotion detection
        frame_interval = int(fps) if fps > 0 else 1
        emotion_results = []

        # Iterate through video frames
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Process every 'frame_interval' frame (approximately once per second)
            if frame_idx % frame_interval == 0:
                # Convert BGR to RGB (DeepFace expects RGB)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Analyze emotions - using enforce_detection=False for speed and robustness
                analysis = DeepFace.analyze(img_path=rgb_frame, actions=['emotion'], enforce_detection=False)

                # If multiple faces, just take the first one
                if isinstance(analysis, list) and len(analysis) > 0:
                    analysis = analysis[0]

                emotions = analysis.get('emotion', {})
                if emotions:
                    # Top emotion
                    top_emotion = max(emotions, key=emotions.get)
                    timestamp_seconds = frame_idx / fps if fps > 0 else frame_idx
                    # Store the result with timestamp
                    emotion_results.append({
                        "time_start": timestamp_seconds,
                        "time_end": timestamp_seconds,  # For a single frame, start=end
                        "top_emotion": top_emotion,
                        "emotions": {k: float(v) for k, v in emotions.items()}
                    })

            frame_idx += 1

        cap.release()

        # Now run speech-to-text using whisper
        # Load a whisper model (you can choose "tiny", "base", "small", "medium", "large")
        model = whisper.load_model("base")
        transcription = model.transcribe(tmp_audio_path)

        # Whisper returns segments with start/end times in seconds
        text_segments = []
        for seg in transcription.get("segments", []):
            text_segments.append({
                "time_start": seg["start"],
                "time_end": seg["end"],
                "text": seg["text"].strip()
            })

        # Cleanup temp files
        if os.path.exists(tmp_video_path):
            os.remove(tmp_video_path)
        if os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)

        output = {
            "video_duration": duration,
            "emotions_over_time": emotion_results,
            "speech_segments": text_segments
        }

        # Save the output to a .json file
        with open('output.json', 'w') as json_file:
            json.dump(output, json_file)

        return output
    
    except Exception as e:
        # Cleanup temp files in case of error
        if os.path.exists(tmp_video_path):
            os.remove(tmp_video_path)
        # Audio might not exist if ffmpeg failed early
        if 'tmp_audio_path' in locals() and os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)

        return {"error": f"Video analysis failed: {str(e)}"}