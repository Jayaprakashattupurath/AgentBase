from agent_project.application.evaluation_service.service import EvaluationService

if __name__ == "__main__":
	svc = EvaluationService()
	sample = {"heart_rate": 70, "spo2": 98, "temperature_c": 36.7, "fall_detected": False}
	print(svc.evaluate_sample(sample))
