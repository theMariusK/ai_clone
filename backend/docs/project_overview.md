# Project Overview

## Architecture

The backend architecture consists of a Flask application that serves as an API Gateway for two main services:
- **Data Processing Service**: Handles video and audio processing tasks.
- **Streaming Service**: Manages the streaming of video content.

Both services communicate through HTTP requests, and MongoDB is used for data storage, including video, audio files, and metadata in JSON format.

## Data Flow

1. The client sends requests to the API Gateway.
2. The API Gateway routes these requests to the appropriate service based on the endpoint.
3. The services process the requests, interact with the database as needed, and send responses back through the API Gateway to the client.

## Technologies Used
- **Flask**: For building the web application and RESTful APIs.
- **MongoDB**: For database management and storage of video and audio files.
- **Docker**: For containerization and deployment of the backend services.

This overview provides a high-level understanding of the project's architecture and data flow.
