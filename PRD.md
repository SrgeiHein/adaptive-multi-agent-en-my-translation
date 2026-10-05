# PRD — Adaptive Multi-Agent Machine Translation for English–Burmese Translation Using Confidence-Guided Reflection

## 1. Document Purpose

This Product Requirements Document (PRD) defines the research, system, experimental, and implementation requirements for the thesis project:

> **Adaptive Multi-Agent Machine Translation for English–Burmese Translation Using Confidence-Guided Reflection**

The project is not intended to be only a translation application. It is a **research framework and benchmark-oriented experimental system** for studying whether a coordinated set of language-model agents can improve English-to-Burmese machine translation quality, reliability, and efficiency through **critique, confidence estimation, selective reflection, and revision**.

The framework is inspired by the controlled evaluation philosophy used by projects such as SEA-TauBench: instead of evaluating one final system only, we define multiple controlled scenarios and progressively add capabilities. This makes it possible to measure exactly which components improve translation quality and which components add unnecessary cost or instability.

---

# 2. Thesis Motivation

English–Burmese machine translation remains challenging because Burmese is comparatively low-resource, has fewer high-quality publicly available parallel corpora than major languages, and presents linguistic and orthographic challenges for modern language models.

A conventional translation pipeline generally follows:

```
English input
   ↓
Translation model
   ↓
Burmese output
```

The major weakness of this approach is that the model usually produces one answer and stops. If the output contains:

- mistranslation,
- omission,
- hallucinated information,
- incorrect terminology,
- unnatural Burmese,
- incorrect numerical information,
- medical terminology errors,
- entity corruption,
- or semantic inconsistency,

there is no explicit mechanism to detect and repair the problem.

Modern large language models can perform multiple roles. Instead of asking one model to translate once, the thesis investigates a **multi-agent workflow** where different logical agents perform different responsibilities.

The proposed process is:

```
Translate
   ↓
Critique
   ↓
Estimate confidence
   ↓
Decide whether revision is needed
   ↓
Reflect and revise when needed
   ↓
Re-evaluate
   ↓
Return final translation
```

The central research idea is that reflection should **not** always happen. Easy translations should be accepted without unnecessary extra calls, while difficult or low-confidence translations should receive additional reasoning and revision.

This is why the system is called **adaptive** and **confidence-guided**.

---

# 3. Research Problem

The main research problem is:

> Can an adaptive multi-agent framework improve English-to-Burmese translation quality and reliability compared with a conventional single-pass translation approach while avoiding unnecessary reflection on already-good translations?

The project studies three connected problems.

## 3.1 Translation Quality

Can critique and reflection improve:

- semantic adequacy,
- fluency,
- terminology,
- source-target consistency,
- preservation of entities, numbers, and units?

## 3.2 Confidence Reliability

Can the system estimate whether its own translation is likely to be correct?

A useful confidence mechanism should satisfy:

```
high predicted confidence → usually high actual translation quality
low predicted confidence  → higher probability that reflection is useful
```

## 3.3 Efficiency

Unconditional reflection may improve some outputs, but it also increases:

- LLM calls,
- latency,
- token usage,
- monetary cost,
- and the possibility of over-editing a translation that was already correct.

The thesis therefore studies whether **selective reflection** can improve the quality-efficiency trade-off.

---

# 4. Research Objectives

The project has the following primary objectives.

1. Build a modular English-to-Burmese multi-agent translation framework.

2. Implement separate logical roles for:
   - Translator Agent
   - Critic Agent
   - Confidence Evaluation
   - Reflection Agent
   - optional Judge Agent

3. Design a confidence-guided decision mechanism that determines whether a translation should be accepted or revised.

4. Compare the proposed framework with simpler baselines.

5. Evaluate translation quality using automatic and, where possible, human evaluation.

6. Measure whether confidence scores correlate with real translation quality.

7. Measure efficiency using reflection rate, number of iterations, latency, and token usage.

8. Evaluate robustness by repeating selected experiments multiple times.

9. Support both domain-specific and general-domain English–Burmese datasets.

10. Produce a reproducible benchmark structure that can be extended to additional models and datasets.

---

# 5. Research Questions

The main research questions are:

### RQ1
Does a multi-agent translation framework improve English-to-Burmese translation quality compared with single-pass translation?

### RQ2
Does critic-guided reflection improve adequacy and fluency?

### RQ3
Can confidence-guided reflection identify translations that benefit from additional revision?

### RQ4
Does confidence-guided reflection achieve better or comparable translation quality than unconditional reflection while using fewer agent interactions?

### RQ5
Do confidence scores correlate with automatic and human translation-quality measurements?

### RQ6
How stable is the system across repeated runs?

### RQ7
Does the benefit of reflection differ between general-domain and specialized-domain translation?

---

# 6. Hypotheses

### H1 — Multi-Agent Improvement

```
Multi-Agent Translation Quality > Single-Pass Translation Quality
```

The full multi-agent system is expected to achieve higher average translation quality than a translator-only baseline.

### H2 — Reflection Improvement

Critic-guided reflection is expected to improve translations that contain identifiable semantic or linguistic problems.

### H3 — Confidence Utility

Lower-confidence translations are expected to benefit more from reflection than higher-confidence translations.

### H4 — Adaptive Efficiency

Confidence-guided reflection is expected to require fewer revision calls than unconditional reflection while maintaining or improving translation quality.

### H5 — Confidence Calibration

Predicted confidence should positively correlate with reference-based and/or human quality scores.

---

# 7. High-Level System Architecture

The core architecture is:

```
                         ┌─────────────────────┐
                         │   English Source    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Translator Agent   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         Initial Burmese Output
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Critic Agent     │
                         │                     │
                         │ • Adequacy          │
                         │ • Fluency           │
                         │ • Consistency       │
                         │ • Terminology       │
                         │ • Error analysis    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Confidence Scoring  │
                         └──────────┬──────────┘
                                    │
                               C >= threshold?
                              /               \
                            yes                no
                             │                  │
                             ▼                  ▼
                          Accept        ┌─────────────────┐
                                        │ Reflection Agent│
                                        └────────┬────────┘
                                                 │
                                                 ▼
                                         Revised Translation
                                                 │
                                                 ▼
                                           Re-evaluate
                                                 │
                                                 ▼
                                       Stop or reflect again
                                                 │
                                                 ▼
                                        Final Translation
```

For the most advanced scenario, a Judge Agent may choose the best candidate from the original and revised translations.

---

# 8. Agent Responsibilities

## 8.1 Translator Agent

### Purpose

Generate the initial Burmese translation.

### Input

- English source sentence
- optional domain instruction

### Output

- Burmese translation candidate

### Requirements

The Translator Agent should:

- preserve the meaning of the source,
- preserve numbers and dates,
- preserve units,
- preserve named entities,
- preserve drug names and medical terminology where appropriate,
- avoid adding unsupported information,
- produce fluent Burmese.

The Translator Agent must not see the reference translation during inference.

---

## 8.2 Critic Agent

### Purpose

Analyze the quality of the current translation.

### Input

- English source
- Burmese candidate

### Output

Structured quality feedback.

### Core evaluation dimensions

1. **Adequacy**
   - Is the source meaning preserved?

2. **Fluency**
   - Is the Burmese natural and grammatically acceptable?

3. **Consistency**
   - Is every important source concept represented appropriately?

4. **Terminology**
   - Are important domain-specific terms correct?

5. **Error-Free Score**
   - Overall absence of severe translation defects.

### Error taxonomy

The Critic should identify problems such as:

- mistranslation,
- omission,
- unsupported addition,
- hallucination,
- number error,
- date error,
- unit error,
- entity error,
- terminology error,
- grammar problem,
- word-order problem,
- unnatural expression,
- ambiguity,
- semantic contradiction.

The Critic should return structured JSON whenever possible so experiments can be analyzed programmatically.

---

## 8.3 Confidence Estimator

### Purpose

Convert the critic's multidimensional assessment into a single reliability score.

The initial implementation uses:

```
C =
0.35 × Adequacy
+ 0.20 × Fluency
+ 0.25 × Consistency
+ 0.10 × Terminology
+ 0.10 × Error-Free
```

where:

```
0 <= C <= 1
```

### Initial threshold

```
τ = 0.80
```

This value is an experimental starting point and **must not be treated as theoretically optimal**.

The final threshold should be selected using development/validation data.

### Decision rule

```
if C >= τ:
    accept translation
else:
    trigger reflection
```

---

## 8.4 Reflection Agent

### Purpose

Improve a translation using critic feedback.

### Input

- source English,
- current Burmese candidate,
- critic feedback,
- optional confidence breakdown.

### Output

- revised Burmese translation.

### Design rule

The Reflection Agent should **repair identified errors without unnecessarily rewriting correct parts**.

This is important because reflection can sometimes make an already-good translation worse.

---

## 8.5 Judge Agent

### Purpose

Select the best translation candidate when multiple versions exist.

### Candidate set

For example:

```
T0 = initial translation
T1 = first revision
T2 = second revision
```

The Judge returns:

```
T* = best candidate
```

The Judge is optional and belongs to the most advanced benchmark scenario.

---

# 9. Adaptive Reflection Loop

The proposed algorithm is:

```python
translation = translator(source)

for iteration in range(MAX_REFLECTIONS):

    critique = critic(source, translation)

    confidence = score(critique)

    if confidence >= threshold:
        break

    translation = reflector(
        source,
        translation,
        critique
    )

return translation
```

Recommended initial value:

```
MAX_REFLECTIONS = 2
```

Possible thesis experiments may compare:

- 1 reflection maximum,
- 2 reflections maximum,
- 3 reflections maximum.

The system must always have a stopping condition.

---

# 10. Benchmark Scenarios

To make the thesis scientifically interpretable, the project uses controlled scenarios.

| Scenario | Translator | Critic | Reflection | Confidence Gate | Judge |
|---|---:|---:|---:|---:|---:|
| S1 | ✓ |  |  |  |  |
| S2 | ✓ | ✓ |  |  |  |
| S3 | ✓ | ✓ | ✓ always |  |  |
| S4 | ✓ | ✓ | ✓ selective | ✓ |  |
| S5 | ✓ | ✓ | ✓ selective | ✓ | ✓ |

## S1 — Single-Pass Baseline

```
Translator → Output
```

Purpose:

- establish the simplest baseline,
- measure raw model translation ability.

## S2 — Critic-Assisted Analysis

```
Translator → Critic → Output
```

The critic scores the translation, but no correction is made.

Purpose:

- evaluate confidence and criticism independently from reflection.

## S3 — Unconditional Reflection

```
Translator → Critic → Reflection → Output
```

Every translation is reflected on, regardless of confidence.

Purpose:

- test whether reflection itself helps,
- create a comparison against adaptive reflection.

## S4 — Confidence-Guided Reflection

```
Translator
   ↓
Critic
   ↓
Confidence
   ↓
high → accept
low  → reflect
```

This is the primary proposed method.

## S5 — Full Adaptive Multi-Agent

```
Translator
→ Critic
→ Confidence
→ Selective Reflection
→ Candidate Set
→ Judge
→ Final Output
```

This represents the complete framework.

---

# 11. Dataset Strategy

## 11.1 Primary Initial Dataset

The first dataset integrated into the project is:

`cpe-kmutt-nlp/my-mm-med-synth`

This dataset is intended to support English–Burmese / Myanmar medical-domain experiments.

### Why use it?

It provides a specialized domain where translation mistakes can expose weaknesses in:

- terminology,
- numerical preservation,
- treatment descriptions,
- medical expressions,
- entity handling.

### Important limitation

The dataset is synthetic.

The thesis must clearly document:

- that it is synthetic,
- how it was generated if documented by the dataset authors,
- its license,
- possible generation bias,
- possible model contamination,
- possible unnatural phrasing.

Synthetic evaluation alone is not enough to claim general English–Burmese translation quality.

---

## 11.2 Recommended External General-Domain Dataset

A human-authored English–Burmese corpus such as ALT/WAT should be added for external evaluation when feasible.

This allows the thesis to compare:

```
Medical / specialized domain
vs.
General / news domain
```

The modular architecture should allow datasets to be added without changing the agent logic.

---

# 12. Dataset Splitting

The project must maintain strict separation between:

- training / few-shot examples,
- development / validation,
- final test set.

Recommended structure:

```
data/
├── raw/
├── processed/
│   ├── train.jsonl
│   ├── dev.jsonl
│   └── test.jsonl
```

### Train

Used only if:

- fine-tuning,
- prompt example selection,
- model adaptation,
- terminology extraction.

### Development

Used for:

- prompt tuning,
- confidence threshold tuning,
- weight selection,
- maximum-reflection tuning,
- model configuration choices.

### Test

Used only for final evaluation.

The final test set must never be used for:

- prompt engineering,
- threshold selection,
- model selection,
- few-shot demonstration examples,
- manual iterative debugging.

This prevents evaluation leakage.

---

# 13. Data Schema

Recommended normalized JSONL format:

```json
{
  "id": "example_00001",
  "source_en": "The patient should discontinue the medication.",
  "reference_my": "...",
  "domain": "medical"
}
```

Optional future fields:

```json
{
  "source_dataset": "my-mm-med-synth",
  "split": "test",
  "difficulty": "medium",
  "entities": [],
  "terminology": [],
  "metadata": {}
}
```

---

# 14. Experimental Design

Each model should be tested under the same scenarios and dataset split.

Example experimental matrix:

| Model | S1 | S2 | S3 | S4 | S5 |
|---|---:|---:|---:|---:|---:|
| Model A | ✓ | ✓ | ✓ | ✓ | ✓ |
| Model B | ✓ | ✓ | ✓ | ✓ | ✓ |
| Model C | ✓ | ✓ | ✓ | ✓ | ✓ |

The same:

- source sentences,
- prompts,
- thresholds,
- maximum iteration counts,
- evaluation metrics,

should be used wherever possible.

This allows fair comparison.

---

# 15. Evaluation Metrics

No single metric is sufficient.

## 15.1 BLEU

Purpose:

- traditional MT comparison,
- n-gram overlap with the reference.

Strength:

- widely reported.

Limitation:

- weak sensitivity to valid paraphrases,
- can undervalue semantically correct alternate Burmese translations.

---

## 15.2 chrF / chrF++

Purpose:

- character-level overlap.

This is useful for morphologically and orthographically variable languages.

chrF++ includes word-order information in addition to character n-grams.

---

## 15.3 COMET

Recommended if available.

Purpose:

- semantic quality estimation using learned representations.

Should not completely replace BLEU/chrF.

---

## 15.4 Human Evaluation

A subset of approximately 100–200 examples can be manually evaluated if qualified Burmese speakers are available.

Suggested scales:

| Dimension | Range |
|---|---:|
| Adequacy | 1–5 |
| Fluency | 1–5 |
| Grammar | 1–5 |
| Terminology | 1–5 |
| Overall meaning preservation | 1–5 |

Human evaluation should use anonymized system outputs when possible.

---

# 16. Confidence Evaluation

Because confidence-guided reflection is central to the thesis, confidence must be evaluated independently.

For each test item record:

- predicted confidence,
- BLEU/chrF/COMET score,
- whether reflection occurred,
- quality before reflection,
- quality after reflection,
- human score if available.

Useful analyses include:

### Confidence-quality correlation

```
corr(confidence, actual_quality)
```

### Confidence buckets

| Confidence | Count | Avg chrF++ | Avg Human Score |
|---|---:|---:|---:|
| 0.00–0.49 | ... | ... | ... |
| 0.50–0.69 | ... | ... | ... |
| 0.70–0.79 | ... | ... | ... |
| 0.80–0.89 | ... | ... | ... |
| 0.90–1.00 | ... | ... | ... |

### Reflection benefit by confidence

Measure:

```
quality_gain = quality_after - quality_before
```

Then test whether low-confidence sentences receive larger gains.

---

# 17. Reflection Evaluation

Reflection must be analyzed separately from final translation quality.

Record:

- initial translation,
- initial confidence,
- critic errors,
- revised translation,
- revised confidence,
- number of reflection iterations.

Important measurements:

### Reflection Rate

```
number of reflected examples / total examples
```

### Average Reflection Iterations

```
total reflection calls / total examples
```

### Improvement Rate

```
examples improved after reflection / reflected examples
```

### Degradation Rate

```
examples made worse after reflection / reflected examples
```

The degradation rate is important because reflection is not automatically beneficial.

---

# 18. Efficiency Metrics

The thesis should evaluate quality together with computational cost.

Track:

- total LLM calls,
- translator calls,
- critic calls,
- reflector calls,
- judge calls,
- average latency per sentence,
- input tokens,
- output tokens,
- approximate API cost,
- reflection rate.

The intended advantage of S4 is:

```
higher or similar quality
with
fewer reflection calls than S3
```

---

# 19. Robustness Evaluation

LLM outputs can vary across runs.

For selected experiments, run the same scenario multiple times.

Example:

```
Run 1
Run 2
Run 3
```

Measure:

- variation in BLEU/chrF,
- translation consistency,
- confidence variance,
- reflection-decision variance,
- failure frequency.

This addresses whether the method is consistently reliable or only occasionally successful.

---

# 20. Ablation Studies

Ablation is required to prove which component contributes to the final result.

Recommended comparisons:

### A1
Translator only.

### A2
Translator + critic.

### A3
Translator + unconditional reflection.

### A4
Translator + confidence-guided reflection.

### A5
Full system + judge.

Additional possible ablations:

- remove fluency from confidence,
- remove terminology score,
- equal weighting vs weighted confidence,
- different thresholds,
- different maximum reflection counts.

---

# 21. Threshold Experiments

The confidence threshold should be treated as a tunable parameter.

Candidate values:

```
0.60
0.70
0.75
0.80
0.85
0.90
```

For every threshold measure:

- translation quality,
- reflection rate,
- latency,
- token usage,
- improvement rate.

The final threshold should be chosen on validation data based on the quality-efficiency trade-off.

---

# 22. Confidence Weight Experiments

Current weights:

| Component | Weight |
|---|---:|
| Adequacy | 0.35 |
| Fluency | 0.20 |
| Consistency | 0.25 |
| Terminology | 0.10 |
| Error-free | 0.10 |

These are initial design values, not final scientific conclusions.

Possible experiments:

- equal weights,
- adequacy-heavy,
- terminology-heavy for medical domain,
- weights optimized on validation data.

---

# 23. Functional Requirements

## FR-1 Dataset Loading

The system must load English–Burmese dataset examples from normalized JSONL.

## FR-2 Dataset Preparation

The system should support converting Hugging Face datasets into the common schema.

## FR-3 Translation

The system must generate Burmese output from English input.

## FR-4 Critique

The system must generate structured translation-quality feedback.

## FR-5 Confidence Calculation

The system must convert critic dimensions into a reproducible confidence score.

## FR-6 Threshold Decision

The system must decide whether reflection is required.

## FR-7 Reflection

The system must revise low-confidence outputs.

## FR-8 Iterative Re-evaluation

After reflection, the system must re-run quality evaluation.

## FR-9 Stopping Condition

The system must stop when:

- confidence reaches the threshold, or
- maximum reflection iterations are reached.

## FR-10 Scenario Selection

Users must be able to select S1–S5.

## FR-11 Logging

Every experiment should log:

- source,
- reference,
- output,
- confidence,
- critique,
- iteration number,
- reflection status.

## FR-12 Evaluation

The system must calculate BLEU and chrF++.

## FR-13 Extensibility

The design should allow future addition of:

- COMET,
- additional datasets,
- additional LLM providers,
- alternative confidence mechanisms,
- alternative judges.

---

# 24. Non-Functional Requirements

## NFR-1 Reproducibility

All important experiment parameters must be configurable and documented.

## NFR-2 Modularity

Agents should be logically separated.

## NFR-3 Provider Independence

The system should support OpenAI-compatible model APIs rather than hard-code one model.

## NFR-4 Data Safety

API keys and credentials must never be committed to Git.

## NFR-5 Traceability

Every final result should preserve the sequence of agent decisions that produced it.

## NFR-6 Robustness

Malformed model JSON should eventually be handled with validation/retry logic.

## NFR-7 Scalability

Dataset processing should support running subsets during development and full datasets for final experiments.

---

# 25. Current Repository Structure

```
adaptive-multi-agent-en-my-translation/
│
├── README.md
├── PRD.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── agents.py
│   ├── config.py
│   ├── llm.py
│   ├── pipeline.py
│   └── schemas.py
│
├── scripts/
│   ├── prepare_dataset.py
│   ├── run_benchmark.py
│   └── evaluate.py
│
├── docs/
│   └── methodology.md
│
├── tests/
│   └── test_confidence.py
│
├── data/
│   ├── raw/
│   └── processed/
│
└── results/
```

---

# 26. Configuration

Environment configuration currently includes:

```
LLM_PROVIDER
LLM_API_BASE
LLM_API_KEY
LLM_MODEL
CONFIDENCE_THRESHOLD
MAX_REFLECTIONS
TEMPERATURE
```

Recommended future settings:

```
RANDOM_SEED
DATASET_NAME
DATASET_SPLIT
MAX_EXAMPLES
OUTPUT_DIR
REPEAT_RUNS
SAVE_INTERMEDIATE
ENABLE_JUDGE
```

---

# 27. Experiment Output Format

Each prediction should preserve a complete trace.

Example:

```json
{
  "id": "123",
  "source_en": "...",
  "reference_my": "...",
  "final_translation": "...",
  "scenario": "S4",
  "iterations": [
    {
      "iteration": 0,
      "translation": "...",
      "confidence": 0.67,
      "reflected": false,
      "critique": {
        "adequacy": 0.62,
        "fluency": 0.85,
        "consistency": 0.66,
        "terminology": 0.50,
        "error_free": 0.55,
        "errors": ["medical terminology error"]
      }
    },
    {
      "iteration": 1,
      "translation": "...",
      "confidence": 0.88,
      "reflected": true,
      "critique": {}
    }
  ]
}
```

This enables detailed post-hoc analysis.

---

# 28. Main Thesis Contribution

The contribution should not be described simply as:

> We used several agents to translate English into Burmese.

A stronger contribution is:

> We propose and evaluate an adaptive multi-agent English–Burmese machine translation framework that selectively invokes reflection using an explicit confidence mechanism, and we analyze translation quality, calibration, computational efficiency, and robustness under controlled benchmark scenarios.

Potential contributions are:

1. A modular English–Burmese multi-agent MT framework.

2. A confidence-guided reflection strategy.

3. A controlled S1–S5 benchmark design.

4. Analysis of reflection benefit vs cost.

5. Confidence calibration analysis for low-resource MT.

6. Domain comparison between medical and general-domain translation.

7. Reproducible code and evaluation structure.

---

# 29. Relationship to SEA-TauBench

The project is inspired by SEA-TauBench's **controlled benchmark design philosophy**, not by copying its exact task.

SEA-TauBench progressively changes experimental conditions to understand where system capability changes.

This thesis applies a similar controlled logic to translation:

```
S1: translation only
S2: + critique
S3: + unconditional reflection
S4: + confidence-guided selective reflection
S5: + full multi-agent selection
```

This lets the thesis answer:

> Which additional capability actually produces measurable improvement?

rather than reporting only one final score.

---

# 30. Risks

## Risk 1 — Synthetic Dataset Bias

The medical dataset may not represent natural English–Burmese translation.

### Mitigation

Add a human-authored external evaluation set.

---

## Risk 2 — LLM Self-Evaluation Bias

The same model may be overconfident when judging its own output.

### Mitigation

Compare:

- same-model critic,
- separate critic model,
- automatic metrics,
- human evaluation.

---

## Risk 3 — Reflection Degradation

Reflection can make good translations worse.

### Mitigation

Measure degradation rate and optionally use a Judge Agent.

---

## Risk 4 — Confidence Is Not True Probability

The confidence score is a heuristic unless calibrated.

### Mitigation

Evaluate correlation and calibration explicitly.

---

## Risk 5 — Dataset Leakage

LLMs may have seen public datasets during pretraining.

### Mitigation

Discuss this limitation and include newly sampled or manually reviewed evaluation items where feasible.

---

## Risk 6 — API Cost

Multi-agent systems can require many calls.

### Mitigation

Use subset experiments first and emphasize selective reflection.

---

## Risk 7 — Burmese Evaluation Difficulty

Reference-based metrics can penalize correct alternative translations.

### Mitigation

Use multiple metrics and human evaluation.

---

# 31. Ethical Considerations

Because the initial dataset is medical-domain:

- the system must not be presented as a clinical translation service,
- experimental outputs should not be used for medical decisions,
- translation errors must be acknowledged,
- evaluation data should avoid exposing personal medical information.

The thesis should clearly state that the work is for machine translation research.

---

# 32. Success Criteria

The project will be considered successful if:

1. S1–S5 can run reproducibly.

2. The framework can process a complete held-out test set.

3. Every scenario produces evaluation outputs.

4. Reflection decisions are logged.

5. Confidence scores are analyzable.

6. At least one proposed scenario is statistically or practically better than S1 in a meaningful quality metric.

7. The thesis reports efficiency alongside quality.

8. The thesis analyzes cases where reflection helps and where it hurts.

9. Experiments are reproducible from documented commands.

---

# 33. Minimum Viable Thesis Experiment

The minimum experiment required for a complete thesis is:

### Dataset

One English–Burmese held-out test set.

### Model

At least one capable LLM.

### Scenarios

- S1
- S3
- S4

### Metrics

- BLEU
- chrF++
- reflection rate
- average number of reflection iterations
- final confidence

### Analysis

- S1 vs S3
- S3 vs S4
- before/after reflection
- confidence vs quality

This is the minimum scientifically meaningful version.

---

# 34. Strong Thesis Experiment

A stronger final experiment includes:

### Datasets

- medical synthetic dataset,
- ALT/WAT or another human-authored English–Burmese set.

### Models

2–4 different models.

### Scenarios

S1–S5.

### Metrics

- BLEU
- chrF++
- COMET
- human evaluation
- confidence correlation
- calibration error
- reflection rate
- improvement/degradation rate
- latency
- token cost
- robustness.

### Repeated runs

At least three repeated runs for selected configurations.

---

# 35. Suggested Thesis Chapter Mapping

## Chapter 1 — Introduction

- background,
- English–Burmese MT problem,
- motivation,
- objectives,
- research questions,
- contributions.

## Chapter 2 — Literature Review

- machine translation,
- low-resource MT,
- English–Burmese MT,
- LLM translation,
- multi-agent systems,
- self-reflection,
- confidence estimation,
- translation evaluation,
- benchmark design.

## Chapter 3 — Proposed Methodology

- dataset,
- preprocessing,
- agent architecture,
- confidence function,
- adaptive reflection,
- benchmark scenarios,
- experimental setup.

## Chapter 4 — Experiments and Results

- baseline results,
- S1–S5 comparison,
- threshold experiments,
- reflection analysis,
- confidence analysis,
- domain comparison,
- efficiency results.

## Chapter 5 — Discussion

- why reflection helps,
- when it fails,
- calibration,
- domain differences,
- limitations.

## Chapter 6 — Conclusion and Future Work

- findings,
- contribution,
- limitations,
- future research.

---

# 36. Planned Development Milestones

## Milestone 1 — Core Framework

- translator,
- critic,
- confidence score,
- reflector,
- scenario runner.

Status: initial implementation exists.

## Milestone 2 — Dataset Validation

- confirm actual dataset fields,
- define deterministic train/dev/test split,
- dataset statistics,
- preprocessing validation.

## Milestone 3 — Baseline Experiments

- run S1,
- run S2,
- record baseline quality.

## Milestone 4 — Reflection Experiments

- run S3,
- inspect improvement and degradation examples.

## Milestone 5 — Adaptive Experiments

- tune confidence threshold on dev set,
- run S4.

## Milestone 6 — Full Multi-Agent

- run S5,
- evaluate Judge Agent.

## Milestone 7 — Metrics and Analysis

- BLEU,
- chrF++,
- COMET if available,
- confidence analysis,
- efficiency analysis.

## Milestone 8 — Human Evaluation

- sample outputs,
- create evaluation form,
- collect ratings.

## Milestone 9 — Thesis Results

- tables,
- figures,
- statistical analysis,
- case studies.

---

# 37. Future Extensions

Potential future work includes:

- learned confidence estimator,
- token-level uncertainty,
- ensemble critics,
- bilingual terminology database,
- retrieval-augmented medical translation,
- error-aware prompting,
- back-translation validation,
- Burmese spell/grammar checking,
- source difficulty classifier,
- automatic model routing,
- multilingual expansion,
- human-in-the-loop review.

---

# 38. Final Thesis Framing

The thesis should be framed around the following central idea:

```
               Translate
                   ↓
                Critique
                   ↓
          Estimate Confidence
                   ↓
          ┌────────┴────────┐
          │                 │
     High confidence   Low confidence
          │                 │
        Accept           Reflect
                            ↓
                          Revise
                            ↓
                       Re-evaluate
```

The main novelty is not simply using more agents.

The key idea is:

> **Use additional reasoning only when the system has evidence that the current translation may be unreliable.**

This makes the framework both a translation-quality method and an efficiency-aware decision system.

---

# 39. One-Sentence Project Definition

> **A controlled benchmark and adaptive multi-agent inference framework that improves English–Burmese machine translation by detecting low-confidence translations, reflecting on identified errors, and selectively revising outputs while measuring quality, calibration, robustness, and computational cost.**

---

# 40. Project Status

Current repository:

`SrgeiHein/adaptive-multi-agent-en-my-translation`

Current implemented components:

- project structure,
- Hugging Face dataset preparation script,
- Translator Agent,
- Critic Agent,
- Reflection Agent,
- Judge Agent,
- confidence scoring,
- S1–S5 pipeline,
- BLEU evaluation,
- chrF++ evaluation,
- basic unit tests,
- methodology document.

Next priorities:

1. verify the exact schema of `cpe-kmutt-nlp/my-mm-med-synth`,
2. implement deterministic train/dev/test splitting,
3. add experiment metadata and token/latency logging,
4. run a small end-to-end S1–S4 pilot,
5. inspect Burmese outputs manually,
6. tune confidence threshold on the dev set,
7. add ALT/WAT external evaluation if available,
8. generate final thesis tables and plots.
