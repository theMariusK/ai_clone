# Project Overview

## Architecture

The backend architecture consists of a Flask application that handles three main components:
- **Data Processing Module**: Handles video and audio processing tasks.
- **Replication Module**: Manages the replication of video content.
- **Text Generation Service**: Generates responses for client requests.

The backend communicates with the text_generation service to generate responses and hosts web sockets for the client_service, which connects to these websockets and awaits events with text responses from the text_generation AI model service. The app routes are defined in `app.py`.

## Data Flow

1. The client connects to the backend via web sockets.
2. The backend routes these requests to the appropriate module based on the endpoint.
3. The modules process the requests, interact with the database as needed, and send responses back through the backend to the client.

## Technologies Used
- **Flask**: For building the web application and RESTful APIs.
- **MongoDB**: For database management and storage of video and audio files.
- **Docker**: For containerization and deployment of the backend services.
- **ffmpeg**: For audio and video separation and processing.
- **DeepFace**: For facial recognition and analysis.
- **MoviePy**: For video editing and processing.

This overview provides a high-level understanding of the project's architecture and data flow.
## Client Interaction

There are two types of clients: mobile devices and desktop devices (client services).

### Mobile Devices
- **Data Submission**: Mobile devices can send data for processing, which will be used for later AI model training.
- **Question Submission**: Mobile devices can also send questions to the trained model.

### Desktop Devices (Client Services)
- **Response Handling**: Questions sent from mobile devices to the trained model are answered by the Text Generation Service.
- **WebSocket Communication**: The responses are sent to the client service on desktop devices, which listen for WebSocket events.
- **Audio Conversion**: The received responses are converted to audio and played on the desktop client.

This interaction ensures seamless communication between mobile and desktop clients, leveraging the Text Generation Service for efficient response handling.
