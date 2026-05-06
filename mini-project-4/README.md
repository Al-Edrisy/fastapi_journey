# Real-Time Polling Application

This project is a real-time polling system built using FastAPI and WebSockets. It allows multiple users to connect simultaneously, create polls, and cast votes that update instantly across all connected clients without requiring a page refresh.

## Project Structure

The project is contained within the `mini-project-4` directory and consists of the following components:

- Backend: A FastAPI application (`app/main.py`) that manages REST API endpoints and WebSocket connections.
- Frontend: A clean, interactive user interface (`app/index.html`) using vanilla JavaScript, HTML, and CSS to interact with both the REST API and the WebSocket server.
- Containerization: A `Dockerfile` and `docker-compose.yml` for easy deployment.
- Documentation: Detailed explanations of design choices can be found in `DECISIONS.md`.

## Features

- REST API for poll management (Create, List, View, Delete).
- Fallback REST endpoint for voting.
- Persistent WebSocket connection manager handling multiple active connections per poll.
- Real-time broadcasting of vote updates to all clients connected to a specific poll.
- In-memory state storage for fast retrieval during active sessions.
- Dynamic frontend visualization that smoothly animates vote percentages.

## How to Run Locally

You can run this application either natively using Python or through Docker.

### Using Python

1. Navigate to the project directory:
   cd mini-project-4

2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

3. Install the required dependencies:
   pip install -r requirements.txt

4. Start the Uvicorn server:
   uvicorn app.main:app --reload

5. Open your web browser and navigate to `http://localhost:8000/`.

### Using Docker

1. Navigate to the project directory:
   cd mini-project-4

2. Build and start the container using Docker Compose:
   docker-compose up --build

3. Access the application at `http://localhost:8000/`.

## API Endpoints

- POST /polls : Creates a new poll.
- GET /polls : Lists all available polls.
- GET /polls/{id} : Retrieves the details of a specific poll.
- POST /polls/{id}/vote : Submits a vote via REST.
- DELETE /polls/{id} : Deletes a poll.
- GET / : Serves the user interface.

## WebSocket Connection

- ws://localhost:8000/ws/polls/{poll_id} : Establishes a persistent connection to receive real-time vote updates and submit votes.
