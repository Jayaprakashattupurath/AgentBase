class AddNewToolService:
	def add(self, name: str, spec: dict) -> dict:
		return {"status": "added", "tool": name, "spec": spec}
