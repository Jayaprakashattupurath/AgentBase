from typing import Dict, Any, List
from .models import Rule, TagAction
from .evaluator import RuleEvaluator
from .storage import RuleStorage


class RuleEngine:
	"""Rule engine service that evaluates rules and tags events with features/labels."""

	def __init__(self, storage: RuleStorage | None = None) -> None:
		self.storage = storage or RuleStorage()
		self.evaluator = RuleEvaluator()

	def process(self, event: Dict[str, Any]) -> Dict[str, Any]:
		"""Process an event through all enabled rules and return tagged event.

		Returns the event with additional 'tags' field containing:
		- features: List of feature strings
		- labels: List of label strings
		- metadata: Dict of custom metadata
		- matched_rules: List of rule IDs that matched
		"""
		tags = {
			"features": [],
			"labels": [],
			"metadata": {},
			"matched_rules": [],
		}

		# Evaluate all enabled rules in priority order
		rules = self.storage.get_all(enabled_only=True)
		for rule in rules:
			if self.evaluator.evaluate(rule.condition, event):
				# Rule matched - apply tagging action
				if rule.action.features:
					tags["features"].extend(rule.action.features)
				if rule.action.labels:
					tags["labels"].extend(rule.action.labels)
				if rule.action.metadata:
					tags["metadata"].update(rule.action.metadata)
				tags["matched_rules"].append(rule.id)

		# Deduplicate lists
		tags["features"] = list(dict.fromkeys(tags["features"]))
		tags["labels"] = list(dict.fromkeys(tags["labels"]))

		# Add tags to event (create copy to avoid mutation)
		tagged_event = event.copy()
		tagged_event["tags"] = tags

		return tagged_event

	def add_rule(self, rule: Rule) -> None:
		"""Add a new rule to the engine."""
		self.storage.add(rule)

	def get_rule(self, rule_id: str) -> Rule | None:
		"""Get a rule by ID."""
		return self.storage.get(rule_id)

	def list_rules(self, enabled_only: bool = False) -> List[Rule]:
		"""List all rules."""
		return self.storage.get_all(enabled_only=enabled_only)

	def delete_rule(self, rule_id: str) -> bool:
		"""Delete a rule."""
		return self.storage.delete(rule_id)

