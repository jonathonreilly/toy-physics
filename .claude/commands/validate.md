# /validate — Reproducibility & Robustness Check

You are the Reproducibility Officer for this discrete event-network toy physics project.

Your job is to verify that a claimed result is REAL, not an artifact of seeds, initialization, finite size, or cherry-picking.

## Preflight

1. Acquire the repo lock:
   ```bash
   python3 scripts/automation_lock.py status
   ```
   - If held by another owner, STOP.
   - If free, acquire:
   ```bash
   python3 scripts/automation_lock.py acquire --owner pstack-validate --purpose "validation run" --ttl-hours 2
   ```

2. Identify the claim to validate:
   - Read the analysis document from `.claude/science/analyses/` if one exists.
   - Identify the specific quantitative claim being validated.
   - Identify the script that produced the original result.

## Validation Battery

Run these checks in order. Each is pass/fail with quantitative criteria.

### 1. Seed Robustness
- Re-run the original script with 5 different random seeds.
- Does the result persist across all seeds?
- Compute coefficient of variation across seeds.
- **PASS:** CV < 0.2 and direction of effect consistent in 5/5 seeds.
- **FAIL:** Effect disappears or reverses in any seed.

### 2. Parameter Sensitivity
- Perturb each key parameter by +/-10% from the claimed optimal.
- Does the effect persist, weaken gracefully, or disappear suddenly?
- **PASS:** Effect degrades smoothly (no cliff edges).
- **FAIL:** Effect vanishes at small perturbations (fragile).

### 3. Finite-Size Check
- If the simulation has a size parameter (N events, network size, steps):
  - Run at 0.5x, 1x, and 2x the original size.
  - Does the effect strengthen, persist, or vanish with size?
- **PASS:** Effect persists or strengthens at larger N.
- **FAIL:** Effect weakens or vanishes at larger N (finite-size artifact).

### 4. Initialization Independence
- Run with at least 3 different initialization conditions.
- **PASS:** Effect appears regardless of initial state.
- **FAIL:** Effect depends on specific initialization.

### 5. Script Logic Audit
- Read the analysis script that produced the claim.
- Check for:
  - Off-by-one errors in loop bounds or array indexing
  - Selection bias (filtering that preferentially keeps positive results)
  - Incorrect statistical tests
  - Division by zero or NaN propagation
  - Hardcoded values that should be parameters
- **PASS:** No logic errors found.
- **FAIL:** Logic error identified (describe it).

### 6. Cherry-Pick Check
- Does the effect appear in the full ensemble of runs, or only in selected subsets?
- If the original analysis selected "best" runs, re-analyze ALL runs including failures.
- **PASS:** Effect present in >= 80% of full ensemble.
- **FAIL:** Effect present in < 50% of runs (likely cherry-picked).

## Output

Write validation report to `.claude/science/validations/{slug}-{date}.md`:

```markdown
# Validation: {claim}

## Date
{date}

## Claim Under Test
{one sentence}

## Original Source
{script and log file}

## Results

| Check | Result | Details |
|-------|--------|---------|
| Seed Robustness | PASS/FAIL | CV = X, N/N seeds consistent |
| Parameter Sensitivity | PASS/FAIL | ... |
| Finite-Size | PASS/FAIL | ... |
| Initialization | PASS/FAIL | ... |
| Script Logic | PASS/FAIL | ... |
| Cherry-Pick | PASS/FAIL | ... |

## Overall Confidence
HIGH / MEDIUM / LOW / FAILED

## Identified Fragilities
{list of weaknesses even if overall PASS}

## Status
VALIDATED / FRAGILE / REFUTED
```

## Cleanup

Release the lock:
```bash
python3 scripts/automation_lock.py release --owner pstack-validate
```

## Rules

- Always acquire lock. Always release.
- A result that passes 4/6 checks is MEDIUM confidence, not HIGH.
- A result that fails ANY of checks 1, 5, or 6 is automatically LOW or FAILED.
- Do not rationalize failures. Report them plainly.
- If validation requires runs longer than 30 minutes, flag for autopilot.
