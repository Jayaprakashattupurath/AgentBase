from typing import Dict, List, Optional
from .models import Rule


class RuleStorage:
	"""Simple in-memory rule storage. Replace with database in production."""

	def __init__(self) -> None:
		self._rules: Dict[str, Rule] = {}

	def add(self, rule: Rule) -> None:
		"""Add or update a rule."""
		self._rules[rule.id] = rule

	def get(self, rule_id: str) -> Optional[Rule]:
		"""Get a rule by ID."""
		return self._rules.get(rule_id)

	def get_all(self, enabled_only: bool = False) -> List[Rule]:
		"""Get all rules, optionally filtering by enabled status."""
		rules = list(self._rules.values())
		if enabled_only:
			rules = [r for r in rules if r.enabled]
		# Sort by priority (higher first), then by ID
		rules.sort(key=lambda r: (-r.priority, r.id))
		return rules

	def delete(self, rule_id: str) -> bool:
		"""Delete a rule. Returns True if rule existed."""
		if rule_id in self._rules:
			del self._rules[rule_id]
			return True
		return False

	def exists(self, rule_id: str) -> bool:
		"""Check if a rule exists."""
		return rule_id in self._rules

