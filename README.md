# trail-angel

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
uv run uvicorn backend.app.main:app --reload --port 8000
```

### API Endpoints
- POST `/plan`: Plan a backpacking trip. Request body: `{ "origin": "<start>", "destination": "<end>", "days": <int> }`
- GET `/agents`: List available agents with their purpose
