from __future__ import annotations

import json
from typing import Any, Dict, List

OUTPUT_SCHEMA_INSTRUCTIONS = """
Return JSON only with this exact schema:
{
  "inferred_intent": "sarcastic|sincere|uncertain",
  "action_type": "clarify|paraphrase_confirm|support|advice|neutral",
  "endorsement_level": -1,
  "response_text": "string"
}
Rules:
- endorsement_level must be one of -1, 0, 1.
- Do not include markdown fences.
- If uncertain, use inferred_intent="uncertain" and prefer clarify/paraphrase_confirm.
""".strip()


def build_turn_prompt(policy_text: str, turns: List[Dict[str, str]]) -> str:
    convo = "\n".join(f"{t['role'].upper()}: {t['text']}" for t in turns)
    prompt = {
        "policy": policy_text,
        "conversation": convo,
        "task": "Infer intent and produce next assistant action and reply.",
        "output_schema": OUTPUT_SCHEMA_INSTRUCTIONS,
    }
    return json.dumps(prompt, ensure_ascii=False)
