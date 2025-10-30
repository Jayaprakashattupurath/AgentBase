run:
	uvicorn agent_project.infrastructure.api.app:app --reload --port 8000

test:
	pytest -q

lint:
	ruff check .
