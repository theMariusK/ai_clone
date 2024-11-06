from fastapi import FastAPI, File, UploadFile, HTTPException
from fer import FER
import cv2
import numpy as np
from typing import Dict

app = FastAPI()
emotion_detector = FER(mtcnn=True)

@app.post("/detect-emotion/")
async def detect_emotion(file: UploadFile = File(...)) -> Dict[str, float]:
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Please upload a JPEG or PNG image.")

    image_data = await file.read()
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    emotions = emotion_detector.detect_emotions(img)

    if emotions:
        top_emotion = emotions[0]['emotions']
        first_emotion = max(top_emotion, key = top_emotion.get)
        print(first_emotion)

        return top_emotion
    else:
        raise HTTPException(status_code=404, detail="No face detected in the image.")

# To run the server: `uvicorn app:app --reload`
# To test: you need to do a POST request to the server with image included, example: curl -X POST "http://127.0.0.1:8000/detect-emotion/" -F "file=@angry.jpeg"
