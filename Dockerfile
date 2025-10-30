FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY pyproject.toml /app/
RUN pip install --no-cache-dir pipx && pipx install poetry && pipx ensurepath
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false
COPY . /app
RUN poetry install --no-interaction --no-ansi
EXPOSE 8000
CMD ["uvicorn", "agent_project.infrastructure.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
