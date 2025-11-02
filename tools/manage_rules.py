"""
CLI tool to demonstrate rule engine usage.
"""
import json
from agent_project.application.rule_engine import (
	RuleEngine,
	Rule,
	Condition,
	ConditionOperator,
	RuleCondition,
	LogicalOperator,
	TagAction,
)
from agent_project.core.agent import HealthAgent


def main():
	# Create rule engine and add sample rules
	engine = RuleEngine()

	# Rule 1: Tag Alzheimer's patients
	alzheimer_rule = Rule(
		id="alzheimer_patient_tag",
		name="Alzheimer Patient Identification",
		description="Tag events from Alzheimer's patients with special care labels",
		priority=10,
		condition=RuleCondition(
			conditions=[
				Condition(
					field="meta.patient_type",
					operator=ConditionOperator.EQ,
					value="alzheimer",
				)
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(
			features=["alzheimer_patient", "cognitive_care"],
			labels=["special_care", "high_priority"],
			metadata={"care_level": "intensive", "monitoring": "continuous"},
		),
	)

	# Rule 2: Tag elderly with mobility issues
	elderly_mobility_rule = Rule(
		id="elderly_mobility",
		name="Elderly Mobility Concern",
		description="Tag events with mobility-related features",
		priority=5,
		condition=RuleCondition(
			conditions=[
				Condition(
					field="meta.age",
					operator=ConditionOperator.GTE,
					value=75,
				),
				Condition(
					field="meta.mobility_assistance",
					operator=ConditionOperator.EQ,
					value=True,
				),
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(
			features=["elderly", "mobility_concern"],
			labels=["fall_risk"],
			metadata={"assistance_required": True},
		),
	)

	# Rule 3: Tag critical vitals
	critical_vitals_rule = Rule(
		id="critical_vitals",
		name="Critical Vitals Alert",
		description="Tag when multiple vitals are in critical range",
		priority=15,
		condition=RuleCondition(
			conditions=[
				Condition(
					field="heart_rate",
					operator=ConditionOperator.GT,
					value=120,
				),
				Condition(
					field="spo2",
					operator=ConditionOperator.LT,
					value=92,
				),
			],
			operator=LogicalOperator.AND,
		),
		action=TagAction(
			features=["cardiac_distress", "respiratory_distress"],
			labels=["critical", "emergency"],
			metadata={"severity": "critical", "immediate_action": True},
		),
	)

	engine.add_rule(alzheimer_rule)
	engine.add_rule(elderly_mobility_rule)
	engine.add_rule(critical_vitals_rule)

	# Create agent with rule engine
	agent = HealthAgent(rule_engine=engine)

	# Test event 1: Alzheimer's patient
	print("=" * 60)
	print("Test Event 1: Alzheimer's Patient")
	print("=" * 60)
	event1 = {
		"heart_rate": 75,
		"spo2": 98,
		"temperature_c": 36.7,
		"fall_detected": False,
		"meta": {"patient_type": "alzheimer", "age": 80},
	}
	result1 = agent.analyze(event1)
	print(json.dumps(result1, indent=2))

	# Test event 2: Elderly with mobility issues
	print("\n" + "=" * 60)
	print("Test Event 2: Elderly with Mobility Assistance")
	print("=" * 60)
	event2 = {
		"heart_rate": 82,
		"spo2": 96,
		"temperature_c": 37.0,
		"fall_detected": False,
		"meta": {"age": 78, "mobility_assistance": True},
	}
	result2 = agent.analyze(event2)
	print(json.dumps(result2, indent=2))

	# Test event 3: Critical vitals
	print("\n" + "=" * 60)
	print("Test Event 3: Critical Vitals")
	print("=" * 60)
	event3 = {
		"heart_rate": 135,
		"spo2": 88,
		"temperature_c": 38.5,
		"fall_detected": False,
		"meta": {},
	}
	result3 = agent.analyze(event3)
	print(json.dumps(result3, indent=2))

	# List all rules
	print("\n" + "=" * 60)
	print("All Rules in Engine:")
	print("=" * 60)
	for rule in engine.list_rules():
		print(f"\n{rule.name} (ID: {rule.id})")
		print(f"  Priority: {rule.priority}")
		print(f"  Enabled: {rule.enabled}")
		print(f"  Description: {rule.description}")


if __name__ == "__main__":
	main()

