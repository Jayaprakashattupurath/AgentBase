from agent_project.infrastructure.vector_database.memory import SimpleLongTermMemory

if __name__ == "__main__":
	mem = SimpleLongTermMemory(max_items=3)
	print("Before:", list(mem.all()))
	# Reset by re-instantiation in this simple stub
	mem = SimpleLongTermMemory(max_items=3)
	print("After:", list(mem.all()))
