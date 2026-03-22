from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--scenario-summaries", type=Path, required=True)
    return p.parse_args()


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def main():
    args = parse_args()
    rows = list(load_jsonl(args.scenario_summaries))

    by_cell = defaultdict(list)
    for r in rows:
        key = (r["model"], r["policy"], r["persistence"])
        by_cell[key].append(r)

    print("model\tpolicy\tpersistence\tn\tavg_drift\tavg_endorse\tavg_repair_rate")
    for (model, policy, persistence), items in sorted(by_cell.items()):
        n = len(items)
        drifts = [x["drift_point"] for x in items if x["drift_point"] is not None]
        avg_drift = sum(drifts) / len(drifts) if drifts else None
        avg_endorse = sum(x["mean_endorsement"] for x in items) / n
        avg_repair = sum(x["repair_action_rate"] for x in items) / n
        print(
            f"{model}\t{policy}\t{persistence}\t{n}\t"
            f"{avg_drift if avg_drift is not None else 'NA'}\t"
            f"{avg_endorse:.3f}\t{avg_repair:.3f}"
        )


if __name__ == "__main__":
    main()
