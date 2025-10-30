from agent_project.core.agent import HealthAgent

if __name__ == "__main__":
	agent = HealthAgent()
	event = {"heart_rate": 130, "spo2": 89, "temperature_c": 39.1, "fall_detected": False}
	print(agent.analyze(event))
