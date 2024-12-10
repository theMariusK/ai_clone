# Backend for Video and Audio Processing Application

This is the backend service for a video and audio processing application built using Flask and Docker. The backend consists of a Data Processing Module and a Replication Module, both accessible via defined routes in `app.py`.

## Project Structure

backend/
├── app.py
├── internal_modules/
│ ├── data_processing_module.py
│ ├── replication_module.py
│ └── init.py
├── database/
│ ├── mongo_connection.py
│ ├── data_model.py
│ └── storage.py
├── Dockerfile
├── docker-compose.yml
├── .env
├── docs/
│ └── project_overview.md
├── requirements.txt
└── README.md

## Prerequisites

- **Docker**: Ensure Docker is installed on your machine. You can download it from [Docker's official website](https://www.docker.com/get-started).
- **Docker Compose**: Docker Compose is included with Docker Desktop.

## Getting Started

Follow these steps to set up and run the backend service:

1. **Clone the repository**:
   ```bash
   git clone [<repository-url>](https://github.com/theMariusK/ai_clone.git)
   cd backend
   ```

2. **Build and run the services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   The backend API will be accessible at [localhost](http://localhost:5000).

## Usage
The backend provides endpoints for processing videos and audio files and storing metadata in JSON format. You can define routes in `app.py` and configure them in the `internal_modules/init.py` file.

Additionally, this backend communicates with a `text_generation` service which generates responses. It also hosts WebSockets for the `client_service`, which connects to these WebSockets and awaits events with text responses from the `text_generation` AI model service.

## Development Workflow
For a smooth development experience, you can use volumes to sync your local code changes with the Docker container:

1. Ensure Docker is running.
2. Modify your code locally.
3. Changes will reflect immediately in the running container.

To stop the services, run:
```bash
docker-compose down
```
or press `Ctrl + C` in the terminal.

## Deployment
For deploying changes to production:

1. Pull the latest code.
2. Rebuild and restart the services:
   ```bash
   docker-compose up --build -d
   ```

## Documentation
For detailed architecture and usage instructions, refer to the project_overview.md.

## Acknowledgements
- Flask - A lightweight WSGI web application framework.
- MongoDB - A document database for storing video and audio files.
- FFmpeg - A complete, cross-platform solution to record, convert and stream audio and video.
- MoviePy - A Python library for video editing.
- Docker - A platform for developing, shipping, and running applications.
- DeepFace - A lightweight face recognition and facial attribute analysis framework for Python.