from agent_project.core.agent import HealthAgent


def test_alert_trigger_on_fall():
	agent = HealthAgent()
	res = agent.analyze({
		"heart_rate": 70,
		"spo2": 98,
		"temperature_c": 36.7,
		"fall_detected": True,
	})
	assert res["assessment"]["should_alert"] is True
	assert res["assessment"]["severity"] == "critical"
