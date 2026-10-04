from __future__ import annotations

import argparse
import json
from pathlib import Path
from datasets import load_dataset


def infer_columns(columns: list[str]) -> tuple[str, str]:
    lower = {c.lower(): c for c in columns}

    src_candidates = ["english", "en", "source_en", "source", "instruction", "input"]
    tgt_candidates = ["myanmar", "burmese", "my", "mm", "target_my", "target", "output", "response"]

    src = next((lower[x] for x in src_candidates if x in lower), None)
    tgt = next((lower[x] for x in tgt_candidates if x in lower), None)

    if not src or not tgt:
        raise RuntimeError(
            f"Could not infer English/Burmese columns from: {columns}. "
            "Inspect the dataset and update infer_columns()."
        )
    return src, tgt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="cpe-kmutt-nlp/my-mm-med-synth")
    ap.add_argument("--split", default="train")
    ap.add_argument("--output", required=True)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    ds = load_dataset(args.dataset, split=args.split)
    src_col, tgt_col = infer_columns(ds.column_names)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    n = len(ds) if args.limit <= 0 else min(args.limit, len(ds))
    written = 0
    with out.open("w", encoding="utf-8") as f:
        for i in range(n):
            row = ds[i]
            item = {
                "id": str(i),
                "source_en": str(row[src_col]).strip(),
                "reference_my": str(row[tgt_col]).strip(),
                "domain": "medical",
            }
            if item["source_en"] and item["reference_my"]:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                written += 1

    print(f"Wrote {written} rows to {out}")


if __name__ == "__main__":
    main()
