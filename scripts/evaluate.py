from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sacrebleu.metrics import BLEU, CHRF


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", required=True)
    args = ap.parse_args()

    rows = [
        json.loads(line)
        for line in Path(args.predictions).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    pairs = [
        (r["final_translation"], r.get("reference_my"))
        for r in rows
        if r.get("reference_my")
    ]
    if not pairs:
        raise RuntimeError("No references found in prediction file")

    hyps = [h for h, _ in pairs]
    refs = [ref for _, ref in pairs]

    bleu = BLEU(tokenize="13a").corpus_score(hyps, [refs]).score
    chrf = CHRF(word_order=2).corpus_score(hyps, [refs]).score

    confidences = []
    reflected = 0
    total_iterations = 0

    for row in rows:
        iterations = row.get("iterations", [])
        if iterations:
            confidences.append(iterations[-1]["confidence"])
            reflected += int(any(it.get("reflected") for it in iterations))
            total_iterations += max(0, len(iterations) - 1)

    summary = {
        "n": len(pairs),
        "BLEU": round(bleu, 4),
        "chrF++": round(chrf, 4),
        "mean_final_confidence": (
            round(float(np.mean(confidences)), 4) if confidences else None
        ),
        "reflection_rate": round(reflected / len(rows), 4) if rows else 0.0,
        "avg_reflection_iterations": (
            round(total_iterations / len(rows), 4) if rows else 0.0
        ),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
