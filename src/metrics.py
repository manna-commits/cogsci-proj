from __future__ import annotations

from typing import Dict, List, Optional


def drift_point(turn_rows: List[Dict]) -> Optional[int]:
    """Earliest turn index where inferred intent is sincere."""
    for row in sorted(turn_rows, key=lambda r: r["turn_idx"]):
        if row.get("inferred_intent") == "sincere":
            return int(row["turn_idx"])
    return None


def mean_endorsement(turn_rows: List[Dict]) -> float:
    vals = [int(r.get("endorsement_level", 0)) for r in turn_rows]
    return sum(vals) / len(vals) if vals else 0.0


def repair_action_rate(turn_rows: List[Dict]) -> float:
    if not turn_rows:
        return 0.0
    repair = sum(
        1
        for r in turn_rows
        if r.get("action_type") in {"clarify", "paraphrase_confirm"}
    )
    return repair / len(turn_rows)
