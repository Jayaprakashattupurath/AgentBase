from ...core.tools.vitals import evaluate_vitals_against_thresholds


class EvaluationService:
	def evaluate_sample(self, sample: dict) -> dict:
		return evaluate_vitals_against_thresholds(sample)
