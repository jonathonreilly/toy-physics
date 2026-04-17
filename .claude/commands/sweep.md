# /sweep — Parameter Sweep Generator

You are the Computational Physicist generating systematic parameter sweeps for this discrete event-network toy physics project.

## Preflight

1. Acquire the repo lock:
   ```bash
   python3 scripts/automation_lock.py status
   ```
   - If held by another owner, STOP.
   - If free, acquire:
   ```bash
   python3 scripts/automation_lock.py acquire --owner pstack-sweep --purpose "generating sweep scripts" --ttl-hours 1
   ```

2. Identify the base script and parameters:
   - Which script in `scripts/` is the starting point?
   - What parameters will be swept and over what ranges?
   - Read the experiment design from `.claude/science/experiments/` if one exists.

## Generation Process

### 1. Analyze Base Script
- Read the base script fully.
- Identify all tunable parameters (hardcoded values, argparse arguments, constants).
- Identify the output format (what gets printed/logged and where).
- Identify the runtime per execution (estimate or measure).

### 2. Design the Sweep
- Parameter grid:

| Parameter | Values | Count |
|-----------|--------|-------|
| ... | [list or range] | N |

- Total combinations: N1 x N2 x ...
- Estimated total runtime: combinations x per-run time.
- If > 2 hours total, warn the user and suggest reduction.

### 3. Generate Sweep Script
Create a single runner script at `scripts/sweep_{name}.py` that:
- Iterates over all parameter combinations
- For each combination:
  - Sets parameters
  - Runs the computation
  - Captures the result with parameter metadata
  - Writes to a structured log file at `logs/{sweep_name}_{timestamp}.txt`
- Handles failures gracefully (logs the failure, continues to next combination)
- Reports progress every 10% of combinations
- Includes a header comment documenting the parameter grid

### 4. Generate Collector Script
Create a companion script at `scripts/sweep_{name}_collect.py` that:
- Reads all output from the sweep log
- Aggregates results into a summary table
- Computes statistics per parameter value (mean, std, min, max)
- Identifies the parameter combination with the strongest/weakest effect
- Outputs a structured summary

### 5. Dry Run
- Run the sweep with just the FIRST parameter combination to verify it works.
- Check that the output format is parseable by the collector.
- Fix any issues before the full sweep.

## Output

- `scripts/sweep_{name}.py` — the runner
- `scripts/sweep_{name}_collect.py` — the collector
- Report to user: total combinations, estimated runtime, how to launch.

## Cleanup

Release the lock:
```bash
python3 scripts/automation_lock.py release --owner pstack-sweep
```

## Rules

- Always acquire lock. Always release.
- Never generate more than 1000 combinations without user approval.
- Always include a dry-run step before the full sweep.
- Every sweep script must handle failures without crashing.
- Every sweep must be reproducible (record random seeds if applicable).
- Prefer adapting existing scripts over writing from scratch.
- Name scripts descriptively: `sweep_delay_vs_persistence_2026-03-30.py`, not `sweep1.py`.
