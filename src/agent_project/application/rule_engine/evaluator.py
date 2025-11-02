from typing import Dict, Any, Optional
from .models import Condition, ConditionOperator, RuleCondition, LogicalOperator


class RuleEvaluator:
	"""Evaluates rule conditions against event data."""

	@staticmethod
	def _get_field_value(data: Dict[str, Any], field_path: str) -> Any:
		"""Extract field value using dot notation (e.g., 'meta.device_id')."""
		keys = field_path.split(".")
		value = data
		for key in keys:
			if isinstance(value, dict):
				value = value.get(key)
			else:
				return None
		return value

	@staticmethod
	def _evaluate_condition(condition: Condition, data: Dict[str, Any]) -> bool:
		"""Evaluate a single condition against event data."""
		field_value = RuleEvaluator._get_field_value(data, condition.field)

		# Handle EXISTS and NOT_EXISTS operators
		if condition.operator == ConditionOperator.EXISTS:
			result = field_value is not None
		elif condition.operator == ConditionOperator.NOT_EXISTS:
			result = field_value is None
		else:
			if field_value is None:
				return False

			# Compare field value with condition value
			operator = condition.operator
			compare_value = condition.value

			if operator == ConditionOperator.EQ:
				result = field_value == compare_value
			elif operator == ConditionOperator.NE:
				result = field_value != compare_value
			elif operator == ConditionOperator.GT:
				result = field_value > compare_value
			elif operator == ConditionOperator.GTE:
				result = field_value >= compare_value
			elif operator == ConditionOperator.LT:
				result = field_value < compare_value
			elif operator == ConditionOperator.LTE:
				result = field_value <= compare_value
			elif operator == ConditionOperator.IN:
				if not isinstance(compare_value, list):
					return False
				result = field_value in compare_value
			elif operator == ConditionOperator.NOT_IN:
				if not isinstance(compare_value, list):
					return False
				result = field_value not in compare_value
			elif operator == ConditionOperator.CONTAINS:
				if isinstance(field_value, (str, list)):
					result = compare_value in field_value
				else:
					return False
			else:
				return False

		# Apply negation if requested
		if condition.negate:
			result = not result

		return result

	@staticmethod
	def evaluate(condition: RuleCondition, data: Dict[str, Any]) -> bool:
		"""Evaluate a rule condition group against event data."""
		if not condition.conditions:
			return True

		if condition.operator == LogicalOperator.AND:
			return all(
				RuleEvaluator._evaluate_condition(cond, data) for cond in condition.conditions
			)
		elif condition.operator == LogicalOperator.OR:
			return any(
				RuleEvaluator._evaluate_condition(cond, data) for cond in condition.conditions
			)
		elif condition.operator == LogicalOperator.NOT:
			if len(condition.conditions) != 1:
				raise ValueError("NOT operator requires exactly one condition")
			return not RuleEvaluator._evaluate_condition(condition.conditions[0], data)
		else:
			raise ValueError(f"Unknown logical operator: {condition.operator}")

