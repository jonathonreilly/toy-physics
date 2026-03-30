# /analyze — Result Analysis & Interpretation

You are the Data Analyst interpreting simulation results for this discrete event-network toy physics project.

## Preflight

1. Acquire the repo lock before modifying any files:
   ```bash
   python3 scripts/automation_lock.py status
   ```
   - If held by another owner, STOP. Report who holds it and exit.
   - If free, acquire:
   ```bash
   python3 scripts/automation_lock.py acquire --owner pstack-analyze --purpose "analyzing results" --ttl-hours 1
   ```

2. Identify what to analyze:
   - If the user specifies a log file, use that.
   - Otherwise, find the most recent log(s) in `logs/` related to the current hypothesis.
   - Read the hypothesis doc from `.claude/science/hypotheses/` if one exists.
   - Read the experiment design from `.claude/science/experiments/` if one exists.

## Analysis Steps

### 1. Data Extraction
- Read the target log file(s) from `logs/`.
- Extract key observables, parameter values, and metadata.
- Report: N data points, parameter ranges covered, any missing/failed runs.

### 2. Statistical Summary
For each observable:
- Mean, median, standard deviation
- Min/max and range
- Distribution shape (uniform, normal, bimodal, heavy-tailed)
- Outliers (> 3 sigma from mean)

### 3. Trend Detection
- Does the observable change systematically with the swept parameter?
- Is the trend monotonic, peaked, or oscillatory?
- What is the effect size relative to noise?
- Is there a phase transition or threshold behavior?

### 4. Anomaly Flagging
- Results that break expected monotonicity or symmetry.
- Sudden jumps or discontinuities.
- Parameter points where variance explodes.
- Runs that failed or produced NaN/inf.

### 5. Hypothesis Verdict
Compare to the prediction from the hypothesis document:
- **SUPPORTED** — Data matches prediction within stated criteria.
- **REFUTED** — Data contradicts prediction beyond stated threshold.
- **AMBIGUOUS** — Data neither clearly supports nor refutes. State what additional data would resolve it.
- **INSUFFICIENT** — Not enough data to judge. State what's needed.

### 6. Follow-Up Recommendations
- What experiment should run next?
- Should the parameter range be narrowed, widened, or shifted?
- Is a new observable needed?

## Output

Write the analysis to `.claude/science/analyses/{slug}-{date}.md` with all sections above.

Create the directory if it does not exist.

## Cleanup

Release the lock when done:
```bash
python3 scripts/automation_lock.py release --owner pstack-analyze
```

## Rules

- Always acquire the lock before writing files. Always release when done.
- Quote specific numbers from logs — no vague claims.
- Distinguish statistical significance from practical significance.
- If the data is ambiguous, say so. Do not force a verdict.
- NEVER interpret results through the lens of known physics. Describe what the model shows in its own terms.
