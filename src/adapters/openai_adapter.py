from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Dict

from .base import Adapter


class OpenAIAdapter(Adapter):
    """Adapter for OpenAI Chat Completions API via stdlib HTTP."""

    def __init__(
        self,
        model_name: str,
        temperature: float = 0.0,
        base_url: str = "https://api.openai.com/v1",
        timeout_s: int = 120,
        api_key_env: str = "OPENAI_API_KEY",
    ) -> None:
        super().__init__(model_name=model_name, temperature=temperature)
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.api_key = os.environ.get(api_key_env)
        if not self.api_key:
            raise RuntimeError(
                f"Missing API key in environment variable '{api_key_env}' for model '{model_name}'"
            )

    def complete(self, prompt: str) -> Dict:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model_name,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": "Return only valid JSON matching requested fields.",
                },
                {"role": "user", "content": prompt},
            ],
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
            raise RuntimeError(f"OpenAI HTTP error for model '{self.model_name}': {msg}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"OpenAI request failed for model '{self.model_name}': {e}") from e

        try:
            content = raw["choices"][0]["message"]["content"]
        except Exception as e:
            raise ValueError(f"Unexpected OpenAI response shape: {raw}") from e

        if not content:
            raise ValueError(f"Empty response content for OpenAI model '{self.model_name}'")

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"OpenAI model '{self.model_name}' returned non-JSON content: {content[:200]}"
            ) from e
        return parsed
