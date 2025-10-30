# Health Monitoring Agent (AgentBase)

AgentBase is a production-ready scaffold for building an agentic Health Monitoring and Alerting system tailored to aged, weak, and special-care users (including people living with Alzheimer's). It provides a clean, extendable Python structure with FastAPI endpoints, core agent logic, tool abstractions, basic memory, and CI-ready ops files.

## What this project does
- Monitors vitals such as heart rate, SpO2, and body temperature
- Detects important events (e.g., falls) and generates actionable alerts
- Exposes a simple API to ingest measurements and retrieve agent assessments
- Provides a foundation for expanding into LLM-driven reasoning, richer memory, and caregiver workflows

## Highlights
- Clear package layout under `src/agent_project/` following application/core/infrastructure separation
- Minimal, readable agent loop with transparent rule-based thresholds you can tune
- FastAPI app ready to run locally or in Docker
- Lightweight long-term memory stub for experimentation
- Ready-to-use Makefile, tests, linting, and GitHub Actions CI

## Directory overview
```
agent-project/
  .github/workflows/ci.yml        # Lint and test on PRs
  data/                           # Datasets / artifacts (placeholder)
  notebooks/                      # Prompt/memory/tool exploration notebooks
  src/agent_project/
    application/                  # Use-case services
    core/                         # Agent, tools, prompts, utils
    infrastructure/               # API, monitoring, vector DB, LLM client stubs
  tools/                          # CLI entrypoints
  tests/                          # Unit tests
  Dockerfile, Makefile, pyproject.toml, config.py
```

## Core components
- `HealthAgent` (`src/agent_project/core/agent/agent.py`):
  - Accepts a vitals event and returns an assessment
  - Triggers alerts via `AlertDispatcher` when thresholds are exceeded or a fall is detected
- `Vitals rules` (`src/agent_project/core/tools/vitals.py`):
  - Simple, transparent thresholds for `heart_rate`, `spo2`, `temperature_c`
  - Built to be swapped for advanced analytics or ML
- `Alert dispatcher` (`src/agent_project/core/tools/alerts.py`):
  - Sends alerts to stdout and optional webhook (stubbed for easy extension to SMS/Email)
- `API` (`src/agent_project/infrastructure/api/app.py`):
  - `GET /health` healthcheck
  - `POST /v1/analyze` to analyze a vitals payload

## Example API payload
```json
{
  "heart_rate": 130,
  "spo2": 89,
  "temperature_c": 39.1,
  "fall_detected": false
}
```

## Extending the system
- Replace the vector memory stub with a real store (e.g., FAISS/pgvector)
- Add provider-specific alert channels (Twilio SMS, SendGrid Email, PagerDuty, Slack)
- Introduce rolling-window analytics, anomaly detection, or personalization per user
- Integrate LLM reasoning via `infrastructure/llm_clients` and `core/prompts`

## Getting started
See `bootstrap.md` for step-by-step setup, environment variables, running locally or via Docker, and testing.
