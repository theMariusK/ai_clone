from fastapi import FastAPI, File, UploadFile, HTTPException
from deepface import DeepFace
import uvicorn
import json
import cv2
import numpy as np
import tempfile
import os
import subprocess
from typing import Dict, Any, List
import torch
import whisper

app = FastAPI()

@app.post("/analyze-video/")
async def analyze_video(file: UploadFile = File(...)) -> Dict[str, Any]:
    # Check if uploaded file is a video format
    if not file.filename.endswith(('.mp4', '.m4v', '.mpeg', '.mov')):
        raise HTTPException(status_code=400, detail="Invalid video format. Please upload an MP4 or a compatible video file.")


    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        tmp_video.write(await file.read())
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

        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")

# To run the server: uvicorn try:app --reload
# POST to /analyze-video/ with a video file (e.g. MP4) to get the analysis.
# Example using curl (if in current directory):
# curl -X POST "http://127.0.0.1:8000/analyze-video/" -F "file=@test_video.mp4"
# Example using curl if video is in a different directory:
# curl -X POST "http://127.0.0.1:8000/analyze-video/" -F "file=@/path/to/your/test_video.mp4"