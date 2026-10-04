from __future__ import annotations

import argparse
from pathlib import Path

from src.pipeline import AdaptiveTranslationPipeline
from src.schemas import TranslationExample


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--scenario", default="S4", choices=["S1", "S2", "S3", "S4", "S5"])
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    pipeline = AdaptiveTranslationPipeline()
    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with input_path.open(encoding="utf-8") as fin, output_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            if args.limit and count >= args.limit:
                break
            ex = TranslationExample.model_validate_json(line)
            result = pipeline.run(ex, scenario=args.scenario)
            fout.write(result.model_dump_json() + "\n")
            count += 1
            print(f"[{count}] {ex.id}")

    print(f"Saved {count} predictions to {output_path}")


if __name__ == "__main__":
    main()
