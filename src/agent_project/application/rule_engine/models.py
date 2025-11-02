from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class ConditionOperator(str, Enum):
	"""Supported condition operators."""
	EQ = "eq"  # equals
	NE = "ne"  # not equals
	GT = "gt"  # greater than
	GTE = "gte"  # greater than or equal
	LT = "lt"  # less than
	LTE = "lte"  # less than or equal
	IN = "in"  # value in list
	NOT_IN = "not_in"  # value not in list
	CONTAINS = "contains"  # string/list contains value
	EXISTS = "exists"  # field exists
	NOT_EXISTS = "not_exists"  # field does not exist


class LogicalOperator(str, Enum):
	"""Logical operators for combining conditions."""
	AND = "AND"
	OR = "OR"
	NOT = "NOT"


class Condition(BaseModel):
	"""A single condition to evaluate against event data."""
	field: str = Field(..., description="Field path to evaluate (supports dot notation)")
	operator: ConditionOperator = Field(..., description="Comparison operator")
	value: Any = Field(None, description="Value to compare against")
	negate: bool = Field(False, description="Negate the condition result")


class RuleCondition(BaseModel):
	"""A condition group with logical operators."""
	conditions: List[Condition] = Field(..., description="List of conditions")
	operator: LogicalOperator = Field(LogicalOperator.AND, description="How to combine conditions")


class TagAction(BaseModel):
	"""Action to tag event with features/labels when rule matches."""
	features: List[str] = Field(default_factory=list, description="Features to add")
	labels: List[str] = Field(default_factory=list, description="Labels to add")
	metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata to attach")


class Rule(BaseModel):
	"""A complete rule definition."""
	id: str = Field(..., description="Unique rule identifier")
	name: str = Field(..., description="Human-readable rule name")
	description: Optional[str] = Field(None, description="Rule description")
	enabled: bool = Field(True, description="Whether rule is active")
	priority: int = Field(0, description="Rule priority (higher = evaluated first)")
	condition: RuleCondition = Field(..., description="Condition to evaluate")
	action: TagAction = Field(..., description="Action to take when condition matches")

