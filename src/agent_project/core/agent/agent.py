from typing import Dict, Any, List

from ..tools.vitals import evaluate_vitals_against_thresholds
from ..tools.alerts import AlertDispatcher


class HealthAgent:
	"""Simple rule-and-tool driven agent for elderly-care health monitoring."""

	def __init__(self, alert_dispatcher: AlertDispatcher | None = None) -> None:
		self.alert_dispatcher = alert_dispatcher or AlertDispatcher()

	def analyze(self, vitals_event: Dict[str, Any]) -> Dict[str, Any]:
		"""Analyze incoming vitals and produce actions.

		Returns a decision dict with any alerts generated.
		"""
		assessment = evaluate_vitals_against_thresholds(vitals_event)
		alerts: List[Dict[str, Any]] = []
		if assessment.get("should_alert"):
			alert_payload = {
				"type": assessment["severity"],
				"message": assessment["message"],
				"data": vitals_event,
			}
			self.alert_dispatcher.dispatch(alert_payload)
			alerts.append(alert_payload)

		return {"assessment": assessment, "alerts": alerts}
