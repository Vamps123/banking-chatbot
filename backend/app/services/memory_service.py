from collections import deque
from typing import Deque

class MemoryService:
    def __init__(self, max_turns: int = 6):
        self.sessions: dict[str, Deque[str]] = {}
        self.max_turns = max_turns

    def add_message(self, session_id: str, role: str, text: str) -> None:
        conversation = self.sessions.setdefault(session_id, deque(maxlen=self.max_turns * 2))
        conversation.append(f"{role}: {text}")

    def get_context(self, session_id: str) -> str:
        conversation = self.sessions.get(session_id, deque())
        return "\n".join(conversation)

memory_service = MemoryService()
