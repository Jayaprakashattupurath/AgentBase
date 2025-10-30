from ...core.prompts.templates import SYSTEM_PROMPT
from ...infrastructure.llm_clients.openai_client import OpenAIClient


class ConversationService:
	def __init__(self) -> None:
		self.client = OpenAIClient()

	def ask(self, user_message: str) -> str:
		messages = [
			{"role": "system", "content": SYSTEM_PROMPT},
			{"role": "user", "content": user_message},
		]
		return self.client.chat(messages)
