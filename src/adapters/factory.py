from __future__ import annotations

from typing import Dict

from .mock_adapter import MockAdapter
from .ollama_adapter import OllamaAdapter


def make_adapter(model_cfg: Dict):
    provider = model_cfg["provider"].lower()
    model_name = model_cfg["name"]
    temperature = float(model_cfg.get("temperature", 0.0))

    if provider == "mock":
        return MockAdapter(model_name=model_name, temperature=temperature)

    if provider == "ollama":
        return OllamaAdapter(
            model_name=model_name,
            temperature=temperature,
            base_url=model_cfg.get("base_url", "http://127.0.0.1:11434"),
            timeout_s=int(model_cfg.get("timeout_s", 120)),
        )

    raise ValueError(
        f"Unsupported provider '{provider}'. Add an adapter in src/adapters and extend factory.py"
    )
