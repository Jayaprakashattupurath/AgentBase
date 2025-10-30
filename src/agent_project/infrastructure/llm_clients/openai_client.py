import os
from typing import List


class OpenAIClient:
	"""Stub for future LLM usage; avoids hard dependency at bootstrap."""

	def __init__(self) -> None:
		self.api_key = os.getenv("OPENAI_API_KEY")

	def chat(self, messages: List[dict]) -> str:
		_ = messages
		return "LLM response unavailable in stub mode"
