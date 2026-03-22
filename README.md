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

## Your exact request (GPT + free, max 4)

Run this one command:

```bash
bash scripts/run_mixed_4_models.sh
```

This uses `mixed_4` preset (exactly 4 models):
1. `gpt-4o-mini` (OpenAI)
2. `gpt-4.1-mini` (OpenAI)
3. `llama3.2:3b` (Ollama, free local)
4. `phi3:mini` (Ollama, free local)

If a model is unavailable (missing `OPENAI_API_KEY`, Ollama not running, model not pulled), the runner skips it and continues. Skip reasons are written to `skipped_models.jsonl`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
```

For GPT models:

```bash
export OPENAI_API_KEY="your_key_here"
```

For free local models (optional but recommended):

```bash
ollama pull llama3.2:3b
ollama pull phi3:mini
```

## Alternative runs

Only free local models:

```bash
bash scripts/run_free_models.sh
```

Custom model list from file:

```bash
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
