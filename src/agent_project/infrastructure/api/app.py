from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

from ...core.agent import HealthAgent
from ...core.utils.validators import validate_vitals_payload
from ...application.rule_engine import RuleEngine, Rule


class VitalsEvent(BaseModel):
	heart_rate: float = Field(..., ge=0)
	spo2: float = Field(..., ge=0, le=100)
	temperature_c: float = Field(..., ge=25, le=45)
	fall_detected: bool = False
	meta: dict | None = None


app = FastAPI(title="Health Monitoring Agent API")

# Initialize rule engine and agent
rule_engine = RuleEngine()
agent = HealthAgent(rule_engine=rule_engine)


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


# Rule Engine API endpoints
@app.post("/v1/rules", status_code=status.HTTP_201_CREATED)
def create_rule(rule: Rule) -> dict:
	"""Create a new rule."""
	try:
		rule_engine.add_rule(rule)
		return {"status": "created", "rule_id": rule.id, "rule": rule.model_dump()}
	except Exception as exc:
		raise HTTPException(status_code=400, detail=str(exc))


@app.get("/v1/rules", response_model=List[Rule])
def list_rules(enabled_only: bool = False) -> List[Rule]:
	"""List all rules."""
	return rule_engine.list_rules(enabled_only=enabled_only)


@app.get("/v1/rules/{rule_id}", response_model=Rule)
def get_rule(rule_id: str) -> Rule:
	"""Get a specific rule by ID."""
	rule = rule_engine.get_rule(rule_id)
	if not rule:
		raise HTTPException(status_code=404, detail=f"Rule {rule_id} not found")
	return rule


@app.delete("/v1/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(rule_id: str) -> None:
	"""Delete a rule by ID."""
	if not rule_engine.delete_rule(rule_id):
		raise HTTPException(status_code=404, detail=f"Rule {rule_id} not found")
