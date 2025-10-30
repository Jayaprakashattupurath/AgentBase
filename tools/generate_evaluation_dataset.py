import json

if __name__ == "__main__":
	dataset = [
		{"heart_rate": 65, "spo2": 98, "temperature_c": 36.6, "fall_detected": False},
		{"heart_rate": 125, "spo2": 90, "temperature_c": 38.5, "fall_detected": False},
		{"heart_rate": 55, "spo2": 88, "temperature_c": 37.0, "fall_detected": True},
	]
	print(json.dumps(dataset, indent=2))
