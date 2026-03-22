from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

from src.adapters.factory import make_adapter
from src.metrics import drift_point, mean_endorsement, repair_action_rate
from src.prompts import build_turn_prompt

REQUIRED_KEYS = {"inferred_intent", "action_type", "endorsement_level", "response_text"}
VALID_INTENTS = {"sarcastic", "sincere", "uncertain"}
VALID_ACTIONS = {"clarify", "paraphrase_confirm", "support", "advice", "neutral"}
VALID_ENDORSE = {-1, 0, 1}


def free_local_models() -> List[Dict]:
    return [
        {"name": "mock-balanced", "provider": "mock", "temperature": 0.0},
        {"name": "llama3.2:3b", "provider": "ollama", "temperature": 0.1},
        {"name": "phi3:mini", "provider": "ollama", "temperature": 0.1},
    ]


def mixed_four_models() -> List[Dict]:
    """At most 4 models: 2 GPT + 2 free local."""
    return [
        {"name": "gpt-4o-mini", "provider": "openai", "temperature": 0.1},
        {"name": "gpt-4.1-mini", "provider": "openai", "temperature": 0.1},
        {"name": "llama3.2:3b", "provider": "ollama", "temperature": 0.1},
        {"name": "phi3:mini", "provider": "ollama", "temperature": 0.1},
    ]


def load_jsonl(path: Path) -> Iterable[Dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def validate_output(d: Dict) -> Dict:
    missing = REQUIRED_KEYS - d.keys()
    if missing:
        raise ValueError(f"Missing keys: {sorted(missing)}")
    if d["inferred_intent"] not in VALID_INTENTS:
        raise ValueError(f"Invalid inferred_intent: {d['inferred_intent']}")
    if d["action_type"] not in VALID_ACTIONS:
        raise ValueError(f"Invalid action_type: {d['action_type']}")
    if int(d["endorsement_level"]) not in VALID_ENDORSE:
        raise ValueError(f"Invalid endorsement_level: {d['endorsement_level']}")
    d["endorsement_level"] = int(d["endorsement_level"])
    d["response_text"] = str(d["response_text"])
    return d


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--models", type=Path, default=None)
    p.add_argument("--model-preset", choices=["free_local", "mixed_4"], default="mixed_4")
    p.add_argument("--policies", type=Path, required=True)
    p.add_argument("--scenarios", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("outputs"))
    p.add_argument("--max-scenarios", type=int, default=None)
    p.add_argument("--fail-fast", action="store_true", help="Stop on first model error")
    return p.parse_args()


def load_models(args: argparse.Namespace) -> List[Dict]:
    if args.models is not None:
        with args.models.open("r", encoding="utf-8") as f:
            model_cfg = json.load(f)
        return model_cfg["models"]

    if args.model_preset == "free_local":
        return free_local_models()
    if args.model_preset == "mixed_4":
        return mixed_four_models()

    raise ValueError(f"Unknown model preset: {args.model_preset}")


def main() -> None:
    args = parse_args()

    models = load_models(args)
    with args.policies.open("r", encoding="utf-8") as f:
        policy_cfg = json.load(f)

    policies: Dict[str, str] = policy_cfg["policies"]
    scenarios = list(load_jsonl(args.scenarios))

    if args.max_scenarios is not None:
        scenarios = scenarios[: args.max_scenarios]

    run_dir = args.output / datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    turn_path = run_dir / "all_turn_outputs.jsonl"
    scen_path = run_dir / "scenario_summaries.jsonl"
    skip_path = run_dir / "skipped_models.jsonl"

    grouped_turns = defaultdict(list)
    skipped_models: Dict[str, str] = {}

    with turn_path.open("w", encoding="utf-8") as turn_file:
        for model in models:
            model_key = f"{model['provider']}::{model['name']}"
            if model_key in skipped_models:
                continue

            try:
                adapter = make_adapter(model)
            except Exception as e:
                if args.fail_fast:
                    raise
                skipped_models[model_key] = f"adapter_init_error: {e}"
                continue

            for scenario in scenarios:
                for policy_name, policy_text in policies.items():
                    turns = scenario["turns"]
                    for turn_idx in range(1, len(turns) + 1):
                        partial = turns[:turn_idx]
                        prompt = build_turn_prompt(policy_text=policy_text, turns=partial)
                        try:
                            out = validate_output(adapter.complete(prompt))
                        except Exception as e:
                            if args.fail_fast:
                                raise
                            skipped_models[model_key] = f"runtime_error: {e}"
                            break

                        row = {
                            "scenario_id": scenario["scenario_id"],
                            "base_scenario_id": scenario["base_scenario_id"],
                            "domain": scenario["domain"],
                            "persistence": scenario["persistence"],
                            "model": model["name"],
                            "provider": model["provider"],
                            "policy": policy_name,
                            "turn_idx": turn_idx,
                            **out,
                        }
                        turn_file.write(json.dumps(row, ensure_ascii=False) + "\n")
                        grouped_turns[(
                            scenario["scenario_id"],
                            model["name"],
                            policy_name,
                            model["provider"],
                        )].append(row)

                    if model_key in skipped_models:
                        break
                if model_key in skipped_models:
                    break

    with scen_path.open("w", encoding="utf-8") as scen_file:
        for (scenario_id, model_name, policy_name, provider), rows in grouped_turns.items():
            first = rows[0]
            summary = {
                "scenario_id": scenario_id,
                "base_scenario_id": first["base_scenario_id"],
                "domain": first["domain"],
                "persistence": first["persistence"],
                "model": model_name,
                "provider": provider,
                "policy": policy_name,
                "drift_point": drift_point(rows),
                "mean_endorsement": mean_endorsement(rows),
                "repair_action_rate": repair_action_rate(rows),
                "n_turns": len(rows),
            }
            scen_file.write(json.dumps(summary, ensure_ascii=False) + "\n")

    with skip_path.open("w", encoding="utf-8") as f:
        for model_key, reason in skipped_models.items():
            f.write(json.dumps({"model": model_key, "reason": reason}, ensure_ascii=False) + "\n")

    print(f"Wrote turn-level outputs: {turn_path}")
    print(f"Wrote scenario summaries: {scen_path}")
    if skipped_models:
        print(f"Wrote skipped model report: {skip_path}")


if __name__ == "__main__":
    main()
