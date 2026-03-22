from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Dict

from .base import Adapter


class OllamaAdapter(Adapter):
    """Adapter for local Ollama models (free, local inference)."""

    def __init__(
        self,
        model_name: str,
        temperature: float = 0.0,
        base_url: str = "http://127.0.0.1:11434",
        timeout_s: int = 120,
    ) -> None:
        super().__init__(model_name=model_name, temperature=temperature)
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s

    def complete(self, prompt: str) -> Dict:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": self.temperature},
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            raise RuntimeError(f"Ollama request failed for model '{self.model_name}': {e}") from e

        text = raw.get("response", "").strip()
        if not text:
            raise ValueError(f"Empty response from Ollama model '{self.model_name}'")

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Ollama model '{self.model_name}' returned non-JSON output: {text[:200]}"
            ) from e
        return parsed
