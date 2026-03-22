#!/usr/bin/env bash
set -euo pipefail

# Optional: pull free local models once
# ollama pull llama3.2:3b
# ollama pull phi3:mini
# ollama pull gemma2:2b

python -m src.run_eval \
  --model-preset free_local \
  --policies configs/policies.json \
  --scenarios data/scenarios.jsonl \
  --output outputs
