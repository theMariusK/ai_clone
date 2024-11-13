# backend/Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Flask app's port
EXPOSE 5000

ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]