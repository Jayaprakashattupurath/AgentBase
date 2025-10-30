from collections import deque
from typing import Deque, Dict, Any, Iterable


class SimpleLongTermMemory:
	"""A tiny append-only memory buffer acting as a vector DB placeholder."""

	def __init__(self, max_items: int = 1000) -> None:
		self._items: Deque[Dict[str, Any]] = deque(maxlen=max_items)

	def add(self, item: Dict[str, Any]) -> None:
		self._items.append(item)

	def all(self) -> Iterable[Dict[str, Any]]:
		return list(self._items)
