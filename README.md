# Adaptive Multi-Agent English–Burmese Translation

A thesis-oriented benchmark and inference framework for **English → Burmese machine translation using confidence-guided reflection**, inspired by the controlled evaluation philosophy of SEA-TauBench.

## Research idea

The project compares progressively stronger translation settings:

- **S1 — Single-pass:** translator only
- **S2 — Critic-assisted:** translator + critic
- **S3 — Unconditional reflection:** every output is revised
- **S4 — Confidence-guided reflection:** only low-confidence outputs are revised
- **S5 — Full adaptive multi-agent:** translator + critic + confidence estimator + selective reflection + optional judge

The initial dataset target is:

`cpe-kmutt-nlp/my-mm-med-synth`

The framework is modular so ALT/WAT English–Burmese data can be added later for general-domain evaluation.

## Pipeline

```
English source
   ↓
Translator Agent
   ↓
Initial Burmese translation
   ↓
Critic Agent
   ↓
Confidence Estimator
   ↓
confidence < threshold?
   ├── no  → accept
   └── yes → Reflection Agent → revised translation
                              ↓
                         re-evaluate
                              ↓
                        final translation
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set your model provider/API key in `.env`.

Prepare a sample:

```bash
python scripts/prepare_dataset.py --output data/processed/sample.jsonl --limit 100
```

Run one benchmark scenario:

```bash
python scripts/run_benchmark.py \
  --input data/processed/sample.jsonl \
  --scenario S4 \
  --output results/s4_predictions.jsonl
```

Evaluate:

```bash
python scripts/evaluate.py --predictions results/s4_predictions.jsonl
```

## Benchmark scenarios

| Scenario | Translator | Critic | Reflection | Confidence gate | Judge |
|---|---:|---:|---:|---:|---:|
| S1 | ✓ |  |  |  |  |
| S2 | ✓ | ✓ |  |  |  |
| S3 | ✓ | ✓ | ✓ always |  |  |
| S4 | ✓ | ✓ | ✓ selective | ✓ |  |
| S5 | ✓ | ✓ | ✓ selective | ✓ | ✓ |

## Repository structure

```
src/
  agents.py
  config.py
  llm.py
  pipeline.py
  schemas.py
scripts/
  prepare_dataset.py
  run_benchmark.py
  evaluate.py
tests/
  test_confidence.py
docs/
  methodology.md
data/
  raw/.gitkeep
  processed/.gitkeep
results/.gitkeep
```

## Confidence model

The default confidence score is:

`C = 0.35 adequacy + 0.20 fluency + 0.25 consistency + 0.10 terminology + 0.10 error_free`

All component scores are normalized to `[0,1]`.

## Thesis evaluation plan

Report both quality and efficiency:

- BLEU
- chrF / chrF++
- COMET (optional)
- confidence-quality correlation
- reflection rate
- average reflection iterations
- latency / token cost
- repeated-run robustness

## Notes

- Keep test data isolated from prompt tuning and threshold tuning.
- Because the medical dataset is synthetic, report that clearly as a limitation.
- Add a human-authored external test set (for example ALT/WAT) when possible.
