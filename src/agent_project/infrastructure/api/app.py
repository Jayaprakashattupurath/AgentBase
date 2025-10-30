from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ...core.agent import HealthAgent
from ...core.utils.validators import validate_vitals_payload


class VitalsEvent(BaseModel):
	heart_rate: float = Field(..., ge=0)
	spo2: float = Field(..., ge=0, le=100)
	temperature_c: float = Field(..., ge=25, le=45)
	fall_detected: bool = False
	meta: dict | None = None


app = FastAPI(title="Health Monitoring Agent API")
agent = HealthAgent()


@app.get("/health")
def health() -> dict:
	return {"status": "ok"}


@app.post("/v1/analyze")
def analyze(event: VitalsEvent) -> dict:
	try:
		validate_vitals_payload(event.model_dump())
	except ValueError as exc:
		raise HTTPException(status_code=400, detail=str(exc))
	return agent.analyze(event.model_dump())
