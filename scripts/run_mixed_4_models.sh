#!/usr/bin/env bash
set -euo pipefail

# Requires OPENAI_API_KEY for GPT models.
# Optional local free models:
# ollama pull llama3.2:3b
# ollama pull phi3:mini

python -m src.run_eval \
  --model-preset mixed_4 \
  --policies configs/policies.json \
  --scenarios data/scenarios.jsonl \
  --output outputs
