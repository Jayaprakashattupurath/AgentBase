import pytest
from agent_project.application.rule_engine import (
	RuleEngine,
	Rule,
	Condition,
	ConditionOperator,
	RuleCondition,
	LogicalOperator,
	TagAction,
)


def test_simple_condition_evaluation():
	"""Test basic condition evaluation."""
	from agent_project.application.rule_engine.evaluator import RuleEvaluator

	evaluator = RuleEvaluator()
	data = {"heart_rate": 130, "spo2": 95}

	condition = RuleCondition(
		conditions=[
			Condition(field="heart_rate", operator=ConditionOperator.GT, value=120)
		],
		operator=LogicalOperator.AND,
	)
	assert evaluator.evaluate(condition, data) is True

	condition2 = RuleCondition(
		conditions=[
			Condition(field="heart_rate", operator=ConditionOperator.LT, value=100)
		],
		operator=LogicalOperator.AND,
	)
	assert evaluator.evaluate(condition2, data) is False


def test_compound_condition_evaluation():
	"""Test AND/OR logical operators."""
	from agent_project.application.rule_engine.evaluator import RuleEvaluator

	evaluator = RuleEvaluator()
	data = {"heart_rate": 130, "spo2": 89}

	# AND: both conditions must be true
	condition = RuleCondition(
		conditions=[
			Condition(field="heart_rate", operator=ConditionOperator.GT, value=120),
			Condition(field="spo2", operator=ConditionOperator.LT, value=92),
		],
		operator=LogicalOperator.AND,
	)
	assert evaluator.evaluate(condition, data) is True

	# OR: at least one condition must be true
	condition2 = RuleCondition(
		conditions=[
			Condition(field="heart_rate", operator=ConditionOperator.LT, value=100),
			Condition(field="spo2", operator=ConditionOperator.LT, value=92),
		],
		operator=LogicalOperator.OR,
	)
	assert evaluator.evaluate(condition2, data) is True


def test_field_path_access():
	"""Test dot notation for nested fields."""
	from agent_project.application.rule_engine.evaluator import RuleEvaluator

	evaluator = RuleEvaluator()
	data = {"meta": {"device_id": "sensor-123", "location": "bedroom"}}

	condition = RuleCondition(
		conditions=[
			Condition(
				field="meta.device_id", operator=ConditionOperator.EQ, value="sensor-123"
			)
		],
		operator=LogicalOperator.AND,
	)
	assert evaluator.evaluate(condition, data) is True


def test_rule_engine_tagging():
	"""Test rule engine tags events with features and labels."""
	engine = RuleEngine()

	# Create a rule that tags high heart rate
	rule = Rule(
		id="high_hr",
		name="High Heart Rate",
		description="Tag events with high heart rate",
		condition=RuleCondition(
			conditions=[
				Condition(field="heart_rate", operator=ConditionOperator.GT, value=120)
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(
			features=["elevated_cardiac"],
			labels=["urgent", "cardiac_abnormal"],
			metadata={"risk_level": "moderate"},
		),
	)

	engine.add_rule(rule)

	# Process an event that matches
	event = {"heart_rate": 130, "spo2": 98, "temperature_c": 36.7}
	result = engine.process(event)

	assert "tags" in result
	assert "elevated_cardiac" in result["tags"]["features"]
	assert "urgent" in result["tags"]["labels"]
	assert result["tags"]["metadata"]["risk_level"] == "moderate"
	assert "high_hr" in result["tags"]["matched_rules"]


def test_rule_engine_no_match():
	"""Test rule engine when no rules match."""
	engine = RuleEngine()

	rule = Rule(
		id="low_spo2",
		name="Low SpO2",
		condition=RuleCondition(
			conditions=[
				Condition(field="spo2", operator=ConditionOperator.LT, value=90)
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(labels=["hypoxia"]),
	)

	engine.add_rule(rule)

	# Process an event that doesn't match
	event = {"heart_rate": 70, "spo2": 98, "temperature_c": 36.7}
	result = engine.process(event)

	assert result["tags"]["features"] == []
	assert result["tags"]["labels"] == []
	assert result["tags"]["matched_rules"] == []


def test_multiple_rules_matching():
	"""Test multiple rules can match and combine tags."""
	engine = RuleEngine()

	rule1 = Rule(
		id="high_hr",
		name="High Heart Rate",
		priority=1,
		condition=RuleCondition(
			conditions=[
				Condition(field="heart_rate", operator=ConditionOperator.GT, value=120)
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(features=["elevated_cardiac"], labels=["urgent"]),
	)

	rule2 = Rule(
		id="low_spo2",
		name="Low SpO2",
		priority=0,
		condition=RuleCondition(
			conditions=[
				Condition(field="spo2", operator=ConditionOperator.LT, value=92)
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(features=["respiratory_concern"], labels=["critical"]),
	)

	engine.add_rule(rule1)
	engine.add_rule(rule2)

	# Process an event that matches both
	event = {"heart_rate": 130, "spo2": 89, "temperature_c": 36.7}
	result = engine.process(event)

	assert "elevated_cardiac" in result["tags"]["features"]
	assert "respiratory_concern" in result["tags"]["features"]
	assert "urgent" in result["tags"]["labels"]
	assert "critical" in result["tags"]["labels"]
	assert len(result["tags"]["matched_rules"]) == 2


def test_disabled_rules():
	"""Test that disabled rules are not evaluated."""
	engine = RuleEngine()

	rule = Rule(
		id="disabled_rule",
		name="Disabled Rule",
		enabled=False,
		condition=RuleCondition(
			conditions=[
				Condition(field="heart_rate", operator=ConditionOperator.GT, value=0)
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(labels=["should_not_appear"]),
	)

	engine.add_rule(rule)

	event = {"heart_rate": 70, "spo2": 98}
	result = engine.process(event)

	assert "should_not_appear" not in result["tags"]["labels"]


def test_rule_priority_ordering():
	"""Test that rules are evaluated in priority order."""
	engine = RuleEngine()

	# Lower priority rule
	rule1 = Rule(
		id="rule1",
		name="Rule 1",
		priority=0,
		condition=RuleCondition(
			conditions=[
				Condition(field="heart_rate", operator=ConditionOperator.GT, value=100)
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(metadata={"priority": "low"}),
	)

	# Higher priority rule
	rule2 = Rule(
		id="rule2",
		name="Rule 2",
		priority=10,
		condition=RuleCondition(
			conditions=[
				Condition(field="heart_rate", operator=ConditionOperator.GT, value=100)
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(metadata={"priority": "high"}),
	)

	engine.add_rule(rule1)
	engine.add_rule(rule2)

	# Rules should be sorted by priority (higher first)
	rules = engine.list_rules()
	assert rules[0].priority == 10
	assert rules[1].priority == 0


def test_agent_with_rule_engine():
	"""Test agent integration with rule engine."""
	from agent_project.core.agent import HealthAgent
	from agent_project.core.tools.alerts import AlertDispatcher

	engine = RuleEngine()
	rule = Rule(
		id="alzheimer_care",
		name="Alzheimer Care Tag",
		condition=RuleCondition(
			conditions=[
				Condition(field="meta.patient_type", operator=ConditionOperator.EQ, value="alzheimer")
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(
			features=["alzheimer_patient"],
			labels=["special_care"],
			metadata={"monitoring_intensity": "high"},
		),
	)
	engine.add_rule(rule)

	agent = HealthAgent(rule_engine=engine)

	event = {
		"heart_rate": 75,
		"spo2": 98,
		"temperature_c": 36.7,
		"fall_detected": False,
		"meta": {"patient_type": "alzheimer"},
	}

	result = agent.analyze(event)

	assert "tags" in result
	assert "alzheimer_patient" in result["tags"]["features"]
	assert "special_care" in result["tags"]["labels"]
	assert result["tags"]["metadata"]["monitoring_intensity"] == "high"


def test_condition_operators():
	"""Test various condition operators."""
	from agent_project.application.rule_engine.evaluator import RuleEvaluator

	evaluator = RuleEvaluator()
	data = {"value": 50, "status": "active", "tags": ["urgent", "cardiac"]}

	# EQ
	cond = RuleCondition(
		conditions=[Condition(field="status", operator=ConditionOperator.EQ, value="active")],
		operator=LogicalOperator.AND,
	)
	assert evaluator.evaluate(cond, data) is True

	# IN
	cond2 = RuleCondition(
		conditions=[Condition(field="tags", operator=ConditionOperator.IN, value="urgent")],
		operator=LogicalOperator.AND,
	)
	assert evaluator.evaluate(cond2, data) is True

	# EXISTS
	cond3 = RuleCondition(
		conditions=[Condition(field="value", operator=ConditionOperator.EXISTS)],
		operator=LogicalOperator.AND,
	)
	assert evaluator.evaluate(cond3, data) is True

	cond4 = RuleCondition(
		conditions=[Condition(field="nonexistent", operator=ConditionOperator.NOT_EXISTS)],
		operator=LogicalOperator.AND,
	)
	assert evaluator.evaluate(cond4, data) is True

