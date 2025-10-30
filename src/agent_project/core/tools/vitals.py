from typing import Dict, Any

VITAL_THRESHOLDS = {
	"heart_rate": {"low": 45, "high": 120},
	"spo2": {"low": 92, "high": 100},
	"temperature_c": {"low": 35.5, "high": 38.0},
}


def evaluate_vitals_against_thresholds(vitals: Dict[str, Any]) -> Dict[str, Any]:
	"""Return a simple assessment and severity for the provided vitals.

	Rules are intentionally simple and transparent to start; they can be
	replaced with learned policies later.
	"""
	issues: list[str] = []
	severity = "info"

	# Fall detection is always a high priority alert
	if bool(vitals.get("fall_detected")):
		issues.append("Fall detected")
		severity = "critical"

	for key, bounds in VITAL_THRESHOLDS.items():
		value = vitals.get(key)
		if value is None:
			continue
		if value < bounds["low"]:
			issues.append(f"{key} low: {value}")
			severity = "high" if severity != "critical" else severity
		elif value > bounds["high"]:
			issues.append(f"{key} high: {value}")
			severity = "high" if severity != "critical" else severity

	should_alert = len(issues) > 0
	message = ", ".join(issues) if issues else "Vitals within expected ranges"
	return {"should_alert": should_alert, "severity": severity, "message": message}
