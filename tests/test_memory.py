from agent_project.infrastructure.vector_database.memory import SimpleLongTermMemory


def test_memory_retains_max_items():
	mem = SimpleLongTermMemory(max_items=2)
	mem.add({"id": 1})
	mem.add({"id": 2})
	mem.add({"id": 3})
	items = list(mem.all())
	assert len(items) == 2
