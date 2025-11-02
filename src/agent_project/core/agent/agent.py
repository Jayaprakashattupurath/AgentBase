from typing import Dict, Any, List

from ..tools.vitals import evaluate_vitals_against_thresholds
from ..tools.alerts import AlertDispatcher


class HealthAgent:
	"""Simple rule-and-tool driven agent for elderly-care health monitoring."""

	def __init__(
		self,
		alert_dispatcher: AlertDispatcher | None = None,
		rule_engine=None,  # RuleEngine type, avoiding circular import
	) -> None:
		self.alert_dispatcher = alert_dispatcher or AlertDispatcher()
		self.rule_engine = rule_engine

	def analyze(self, vitals_event: Dict[str, Any]) -> Dict[str, Any]:
		"""Analyze incoming vitals and produce actions.

		Processes event through rule engine to tag with features/labels,
		then evaluates vitals and generates alerts if needed.

		Returns a decision dict with assessment, alerts, and tags.
		"""
		# Apply rule engine to tag event with features/labels
		if self.rule_engine:
			tagged_event = self.rule_engine.process(vitals_event)
			tags = tagged_event.get("tags", {})
		else:
			tagged_event = vitals_event
			tags = {}

		# Evaluate vitals (can use tags in future enhancements)
		assessment = evaluate_vitals_against_thresholds(tagged_event)
		alerts: List[Dict[str, Any]] = []
		if assessment.get("should_alert"):
			alert_payload = {
				"type": assessment["severity"],
				"message": assessment["message"],
				"data": tagged_event,
			}
			self.alert_dispatcher.dispatch(alert_payload)
			alerts.append(alert_payload)

		return {
			"assessment": assessment,
			"alerts": alerts,
			"tags": tags,
		}
