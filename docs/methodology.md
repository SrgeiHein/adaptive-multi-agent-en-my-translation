# Methodology

## Benchmark scenarios

| Scenario | Translator | Critic | Reflection | Confidence gating | Judge |
|---|---:|---:|---:|---:|---:|
| S1 | ✓ |  |  |  |  |
| S2 | ✓ | ✓ |  |  |  |
| S3 | ✓ | ✓ | ✓ always |  |  |
| S4 | ✓ | ✓ | ✓ selective | ✓ |  |
| S5 | ✓ | ✓ | ✓ selective | ✓ | ✓ |

## Main research questions

1. Does multi-agent reflection improve English–Burmese translation quality over single-pass translation?
2. Does confidence-guided reflection outperform unconditional reflection in quality-efficiency trade-off?
3. Is predicted confidence correlated with actual translation quality?
4. Are improvements consistent across general and medical domains?
5. How stable are results across repeated stochastic runs?

## Confidence

The current implementation uses:

`C = 0.35A + 0.20F + 0.25S + 0.10T + 0.10E`

where:

- A = adequacy
- F = fluency
- S = source-target consistency
- T = terminology
- E = error-free score

The threshold should be tuned on validation data only.

## Evaluation

Primary automatic metrics:

- BLEU
- chrF++

Recommended extensions:

- COMET
- human adequacy/fluency ratings
- confidence-quality correlation
- expected calibration error
- reflection rate
- average number of reflection iterations
- latency
- token usage / cost
- repeated-run variance

## Dataset protocol

The initial dataset is `cpe-kmutt-nlp/my-mm-med-synth`.

Because it is synthetic medical data:

- document its generation origin and license,
- prevent train/test contamination,
- use a fixed held-out test split,
- and preferably include a human-authored external English–Burmese test set such as ALT/WAT.
