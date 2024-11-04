# Backend for Video and Audio Processing Application

This is the backend service for a video and audio processing application built using Flask and Docker. The backend consists of a Data Processing Service and a Streaming Service, both accessible via an API Gateway.

## Project Structure

backend/
├── app.py
├── services/
│ ├── data_processing_service.py
│ ├── streaming_service.py
│ └── init.py
├── api_gateway/
│ ├── gateway.py
│ └── config.py
├── database/
│ ├── mongo_connection.py
│ ├── data_model.py
│ └── gridfs_storage.py
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

2. **Build and run the services:**:
docker-compose up --build

3. **Access the application:**:
The backend API will be accessible at http://localhost:5000.


## Usage
The backend provides endpoints for processing videos and audio files and storing metadata in JSON format. You can define routes in app.py and configure them in the api_gateway/gateway.py file.

## Development Workflow
For a smooth development experience, you can use volumes to sync your local code changes with the Docker container:

1. Ensure Docker is running.
2. Modify your code locally.
3. Changes will reflect immediately in the running container.

To stop the services, run:
docker-compose down


## Deployment
For deploying changes to production:

1. Pull the latest code.
2. Rebuild and restart the services:
docker-compose up --build -d

## Documentation
For detailed architecture and usage instructions, refer to the project_overview.md.

## Acknowledgements
Flask - A lightweight WSGI web application framework.
MongoDB - A document database for storing video and audio files.
