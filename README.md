# ByLand.ai

> How do you let yourself be moved?

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
Ensure the `app` package is on the PYTHON path by setting the app directory to `backend` and using the new modular planner app:
```bash
uv run uvicorn app.planner.main:app --reload --port 8000 --app-dir backend
```

### API Endpoints
- POST `/plan`: Plan a backpacking trip. Request body: `{ "origin": "<start>", "destination": "<end>", "days": <int> }`
- GET `/agents`: List available agents with their purpose
