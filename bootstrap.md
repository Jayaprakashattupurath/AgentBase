# Bootstrap Guide

Follow these steps to configure, run, and test the Health Monitoring Agent.

## 1) Prerequisites
- Python 3.9–3.12
- Recommended: [Poetry](https://python-poetry.org/) for dependency management
- Optional: Docker (for containerized run)

## 2) Install dependencies
Using Poetry:

```bash
poetry install
```

If you prefer plain pip, you can inspect `pyproject.toml` and install packages manually.

## 3) Configure environment
Copy and edit the environment template:

```bash
cp .env.example .env
```

Set values as needed:
- `ENVIRONMENT` — `development` | `staging` | `production`
- `ALERT_WEBHOOK_URL` — optional URL to receive JSON alerts
- `OPENAI_API_KEY` — optional; only needed when you swap in a real LLM client

## 4) Run the API
Start the FastAPI server (Uvicorn):

```bash
poetry run uvicorn agent_project.infrastructure.api.app:app --reload --port 8000
```

Or with Make:

```bash
make run
```

Health check:

```bash
curl http://localhost:8000/health
```

Analyze vitals:

```bash
curl -X POST http://localhost:8000/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 130,
    "spo2": 89,
    "temperature_c": 39.1,
    "fall_detected": false
  }'
```

## 5) CLI entrypoints
- Quick agent run:

```bash
poetry run python tools/run_agent.py
```

- Evaluate a sample:

```bash
poetry run python tools/evaluate_agent.py
```

- Generate a synthetic dataset:

```bash
poetry run python tools/generate_evaluation_dataset.py
```

## 6) Testing and linting
Run tests and lint checks:

```bash
make test
make lint
```

## 7) Docker
Build and run locally:

```bash
docker build -t health-agent .
docker run -p 8000:8000 --env-file .env health-agent
```

## 8) Where to customize
- Threshold rules: `src/agent_project/core/tools/vitals.py`
- Alert destinations: `src/agent_project/core/tools/alerts.py`
- API schemas/endpoints: `src/agent_project/infrastructure/api/app.py`
- Memory adapter: `src/agent_project/infrastructure/vector_database/memory.py`
- LLM integration: `src/agent_project/infrastructure/llm_clients/`

## 9) Next steps
- Add real alert providers (SMS/Email/Slack/PagerDuty)
- Implement rolling-window analytics and anomaly detection
- Store historical data in a proper DB and add caregiver dashboards
