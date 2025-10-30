from typing import Dict, Any

REQUIRED_VITAL_KEYS = {"heart_rate", "spo2", "temperature_c"}


def validate_vitals_payload(payload: Dict[str, Any]) -> None:
	missing = [k for k in REQUIRED_VITAL_KEYS if k not in payload]
	if missing:
		raise ValueError(f"Missing vital fields: {', '.join(missing)}")
