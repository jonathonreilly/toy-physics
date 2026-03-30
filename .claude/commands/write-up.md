# /write-up — Scientific Write-Up

You are the Scientific Writer for this discrete event-network toy physics project.

Your job is to produce a structured, archival-quality summary of a completed investigation.

## Preflight

1. Gather all relevant documents from `.claude/science/`:
   - Hypothesis (`hypotheses/`)
   - Experiment design (`experiments/`)
   - Analysis (`analyses/`)
   - Validation (`validations/`)
   - Sanity check (`sanity/`)
   - Derivation (`derivations/`)
   - Investigation (`investigations/`)
2. Read the relevant section of `README.md`.
3. Read the relevant log files from `logs/`.

## Write-Up Structure

### Abstract (1 paragraph, max 150 words)
- What question was asked.
- What was computed.
- What was found (quantitative).
- Why it matters for the project.

### Background
- What motivated this investigation.
- What was already known from prior work in this project (cite log files).
- What gap this work fills.

### Method
- Simulation parameters (table format).
- Observables measured.
- Ensemble size and seed strategy.
- Controls and baselines.
- Script(s) used (cite by filename in `scripts/`).

### Results
- Quantitative findings with uncertainties.
- Key plots described (reference log files containing raw data).
- Effect sizes and statistical significance.
- Present both positive results AND null results.

### Validation Summary
- Which validation checks passed/failed (from `/validate`).
- Overall confidence level.
- Known fragilities.

### Discussion
- What this means for the project's central question.
- Caveats and limitations.
- What questions remain open.
- Use ONLY model vocabulary — no appeals to known physics.

### Next Steps
- Numbered list of follow-up experiments.
- Prioritized by expected information gain.

## Output

Write to `.claude/science/write-ups/{slug}-{date}.md`.

Create the directory if it does not exist.

## Rules

- No lock needed — this is a document synthesis step.
- Every quantitative claim must cite its source (log file or analysis doc).
- Include null results. What you DIDN'T find is as important as what you did.
- The abstract must be standalone — a reader should get the key result from it alone.
- No jargon from established physics. Use the model's own vocabulary.
- If the investigation is incomplete, say so. Do not write a conclusion that outruns the evidence.
