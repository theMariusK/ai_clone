# backend/Dockerfile
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg
RUN apt update && apt install -y ffmpeg

# Install OpenGL Dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Install GTK Dependencies
RUN apt-get update && apt-get install -y libglib2.0-0

# Copy the rest of the application code
COPY . .

# Expose the Flask app's port
EXPOSE 5000

ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]