from agent_project.infrastructure.vector_database.memory import SimpleLongTermMemory

if __name__ == "__main__":
	mem = SimpleLongTermMemory(max_items=10)
	for i in range(5):
		mem.add({"event_id": i, "note": "Routine check"})
	print(list(mem.all()))
