from typing import Protocol
from .schemas import SemanticSignals

class LLMProvider(Protocol):
    def interpret_response(
        self,
        conversation_context: dict,
        seller_response: str,
        objective_signals: dict,
    ) -> SemanticSignals:
        ...
