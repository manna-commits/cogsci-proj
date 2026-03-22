# Sarcasm Drift Evaluation Harness

This repository contains a complete, automated pipeline for evaluating how different LLMs interpret persistent sarcasm across multi-turn dialogs.

## What this includes

- A **full scenario dataset** with **24 base situations × 2 persistence variants** (`low` and `high`) for a total of **48 scenarios**.
- Each scenario is **10 turns** (5 user + 5 assistant turns).
- A run harness that evaluates:
  - multiple models,
  - multiple policies (`baseline_silent_adaptation`, `repair_first`),
  - all scenarios,
  - all turns in each scenario.
- Structured output parsing + validation.
- Automatic metrics:
  - drift point,
  - mean endorsement,
  - repair action rate.

## Simple run (your request)

If you want one command with multiple **free** models (local via Ollama), run:

```bash
bash scripts/run_free_models.sh
```

That command uses preset `free_local` with:
- `mock-balanced` (always available),
- `llama3.2:3b` (Ollama),
- `phi3:mini` (Ollama),
- `gemma2:2b` (Ollama).

If Ollama is not installed or some models are missing, the runner will skip failing models and continue, writing `skipped_models.jsonl`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate

# Option A: use preset free local models
python -m src.run_eval \
  --model-preset free_local \
  --policies configs/policies.json \
  --scenarios data/scenarios.jsonl \
  --output outputs

# Option B: use explicit model file
python -m src.run_eval \
  --models configs/models.json \
  --policies configs/policies.json \
  --scenarios data/scenarios.jsonl \
  --output outputs
```

## Data format

`data/scenarios.jsonl` rows:

- `scenario_id`: unique ID (e.g., `coffee_spill_01_high`)
- `base_scenario_id`: base scenario id shared by low/high variants
- `domain`: event category
- `persistence`: `low` or `high`
- `turns`: list of 10 turns (`user` and `assistant` alternating)

## Output format

The model is instructed to return strict JSON:

```json
{
  "inferred_intent": "sarcastic|sincere|uncertain",
  "action_type": "clarify|paraphrase_confirm|support|advice|neutral",
  "endorsement_level": -1,
  "response_text": "..."
}
```

## Research alignment

This setup directly supports your project goals:

- compare **human vs model drift points**,
- estimate policy effect of **repair-first**,
- quantify inappropriate endorsement under sustained sarcasm.
