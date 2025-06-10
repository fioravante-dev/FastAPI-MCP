# Enterprise AI Agent with FastAPI and Docker

This project demonstrates how to build a robust, production-ready AI agent using a professional, layered architecture. The agent manages a user database through natural language commands, performing full CRUD (Create, Read, Update, Delete) operations.

This application serves as a powerful alternative to a simple collection of serverless functions, providing a structured, scalable, and maintainable backend powered by Model-Centric Programming (MCP).

---

## Features

- **Full CRUD Capabilities:** Add, read, update, and delete users via natural language.
- **Conversational Context:** Maintains conversation history for follow-up questions.
- **Layered Architecture:** Clean separation of concerns between API, services, agent logic, and data persistence.
- **Containerized Environment:** Managed by Docker Compose for consistent and reliable deployments.
- **Production-Ready:** Health checks, robust database connection handling, and scalable structure.

---

## Architecture

The application uses a layered (N-Tier) architecture for separation of concerns and maintainability:

- **Presentation Layer (`/api`):** Handles all HTTP requests and responses.
- **Service Layer (`/services`):** Orchestrates business logic, bridging API and backend systems.
- **Agent Layer (`/agents`):** Contains core AI logic, prompts, and tools.
- **Persistence Layer (`/persistence`):** Handles all database interactions.

```
text/mcp-fastapi-pro
├── .env
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
└── /app
    ├── /api
    ├── /agents
    ├── /core
    ├── /persistence
    ├── /schemas
    └── /services
```

---

## Technology Stack

- **Backend:** Python 3.11 with FastAPI
- **AI Framework:** LangChain
- **LLM Provider:** Groq API (Llama 3)
- **Database:** MySQL 8.0 (in a separate container)
- **Database Driver:** `mysql-connector-python`
- **Containerization:** Docker & Docker Compose
- **Configuration:** Pydantic Settings

---

## Setup and Installation

Follow these steps to get the application stack running locally.

### 1. Prerequisites

- **Docker:** Install Docker Desktop
- **Git:** To clone the repository

> You do **not** need Python or MySQL installed locally; Docker handles everything.

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd mcp-fastapi-pro
```

### 3. Configure Environment Variables (`.env` file)

Create a `.env` file in the project root and add the following, replacing the Groq API key placeholder:

```env
# --- Groq API Settings ---
# Get your key from https://console.groq.com/
GROQ_API_KEY="gsk_YourSecretGroqApiKeyHere"

# --- Database Connection Settings ---
DB_HOST=db
DB_PORT=3306
DB_NAME=agent_db
DB_USER=myuser
DB_PASSWORD=mypassword

# --- Database Admin Settings ---
DB_ROOT_PASSWORD=myrootpassword
```

### 4. Run the Application

With Docker Desktop running, execute:

```bash
docker-compose up --build
```

- `docker-compose up`: Starts all services defined in `docker-compose.yml`.
- `--build`: Forces Docker to build a fresh image for your API.

Wait for logs indicating successful database connection and Uvicorn running on `http://0.0.0.0:8000`.

---

## Usage and API Interaction

Interact with the agent via the `/api/v1/chat` endpoint.

- **Endpoint:** `POST /api/v1/chat`
- **Content-Type:** `application/json`

### Request Body Format

```json
{
  "user_input": "Your message to the agent goes here",
  "chat_history": [
    { "role": "human", "content": "A previous message from the user." },
    { "role": "ai", "content": "A previous response from the agent." }
  ]
}
```

- `user_input` (string): The new message.
- `chat_history` (list): Conversation memory. For the first message, send `[]`. For follow-ups, send the full history.

---

### Example `curl` Conversation

**1. Start the conversation:**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "user_input": "hello",
  "chat_history": []
}'
```

**2. Send a follow-up command:**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "user_input": "add a user named \"Lois Lane\" with email \"lois@dailyplanet.com\"",
  "chat_history": [
    {"role": "human", "content": "hello"},
    {"role": "ai", "content": "Hello! I am a database management assistant..."}
  ]
}'
```

---

## Interactive API Docs

FastAPI provides automatic, interactive documentation:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
