# ByLand.ai

ByLand.ai is a modular, production-ready platform for personalized hiker onboarding and trip planning, built with FastAPI (Python backend) and Chainlit (Python conversational frontend).

## Overview

- **Backend:**
  - Built with FastAPI, SQLAlchemy, and PostgreSQL for robust, persistent storage.
  - Modular architecture: separate packages for hiker profile onboarding (conversational, step-by-step) and trip planner logic.
  - Conversational onboarding flow powered by LangGraph and LangChain, with persistent state management in the database.
  - All user and profile data is stored using UUIDs for consistency and security.
  - Endpoints for onboarding, profile CRUD, and conversational chat.
  - Designed for extensibility: add authentication, admin analytics, and more as needed.

- **Frontend:**
  - Built with Chainlit for a modern, chat-based user experience.
  - Connects directly to the backend's onboarding/chat endpoints.
  - Simple, Pythonic codebase—no React or Vite required.
  - Easily customizable for branding, admin features, and analytics.

## Quick Start

1. **Backend:**
   - Install dependencies: `pip install -r requirements.txt`
   - Set up PostgreSQL (see Docker instructions in code comments or use your own instance)
   - Run the FastAPI server: `uvicorn backend.app.main:app --reload`

2. **Frontend:**
   - Go to `frontend/`
   - Install dependencies: `pip install -r requirements.txt`
   - Copy `.env.example` to `.env` and set your backend API URL
   - Start Chainlit: `chainlit run app.py`

## Features & Roadmap
- Conversational onboarding for hikers (LLM-powered, persistent)
- Hiker profile CRUD and management
- Admin/analytics endpoints (planned)
- Chainlit chat UI with extensible commands and customizations
- See `backend/app/hiker_profiles/routes.py` and `frontend/todo.md` for detailed TODOs and next steps

## Contributing
- See TODOs in code and `frontend/todo.md` for open tasks
- PRs and issues welcome!

---

*ByLand.ai is a work in progress. More features, docs, and polish coming soon!*

## Backend Setup

### Prerequisites
- Install [uv](https://github.com/astral-sh/uv) (e.g. via `pipx install uv` or `curl install.sh | sh`)

### Initialize & Sync Dependencies
1. Initialize the project (creates lockfile & venv):
   ```bash
   uv init
   ```
2. Sync dependencies from requirements.txt:
   ```bash
   uv pip sync requirements.txt
   ```

### Run the FastAPI server
```bash
uv run uvicorn app.main:app --reload --port 8000 --app-dir backend
```

### API Endpoints
- POST `/plan`: Plan a backpacking trip. Request body: `{ "origin": "<start>", "destination": "<end>", "days": <int> }`
- GET `/agents`: List available agents with their purpose
