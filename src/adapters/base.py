from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class Adapter(ABC):
    def __init__(self, model_name: str, temperature: float = 0.0) -> None:
        self.model_name = model_name
        self.temperature = temperature

    @abstractmethod
    def complete(self, prompt: str) -> Dict:
        """Return parsed dict with required schema keys."""
        raise NotImplementedError
