import os
from typing import Dict, Any


class AlertDispatcher:
	"""Dispatch alerts via simple channels (stdout/webhook placeholders)."""

	def __init__(self) -> None:
		self.webhook_url = os.getenv("ALERT_WEBHOOK_URL")

	def dispatch(self, alert: Dict[str, Any]) -> None:
		# In a real system, integrate email/SMS/webhook here
		print(f"[ALERT] {alert['type'].upper()}: {alert['message']}")
		if self.webhook_url:
			# Placeholder for outbound call
			# e.g., httpx.post(self.webhook_url, json=alert)
			pass
