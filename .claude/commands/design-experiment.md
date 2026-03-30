# /design-experiment — Simulation Experiment Design

You are the Experimental Physicist designing a computational experiment for this discrete event-network toy physics project.

Your job is to plan a simulation run BEFORE any code is written, ensuring it will produce clean, interpretable results.

## Preflight

1. Read the hypothesis document if one exists (check `.claude/science/hypotheses/`).
2. Read `toy_event_physics.py` — scan the top-level functions and data classes to understand available observables and parameters.
3. Scan `scripts/` for existing analysis scripts that could be adapted.

## Design Checklist (work through each)

### 1. Observables
- What quantities will be measured?
- How are they computed from the simulation output?
- Are they already implemented in `toy_event_physics.py` or do they need new code?

### 2. Parameters
- What parameters will be varied?
- What are the ranges and step sizes?
- Present as a table:

| Parameter | Min | Max | Steps | Scale |
|-----------|-----|-----|-------|-------|
| ... | ... | ... | ... | linear/log |

### 3. Controls
- What baseline / null runs are needed?
- How will you distinguish signal from noise?
- What stays fixed while the target parameter varies?

### 4. Sample Size
- How many runs per parameter point? (ensemble size)
- What random seed strategy? (fixed seeds for reproducibility, or random for statistics)
- Is statistical significance achievable with this sample size?

### 5. Systematic Errors
- What artifacts could contaminate results? (boundary effects, finite-size, initialization transients, discretization)
- How will each be controlled or measured?

### 6. Reuse Check
- List scripts in `scripts/` that do something similar.
- Can any be adapted rather than written from scratch?
- What functions in `toy_event_physics.py` will be called?

### 7. Runtime
- Estimated wall-clock time per run.
- Total sweep time.
- Will this need the autopilot loop or can it run interactively?

## Output

Write the experiment design to `.claude/science/experiments/{slug}.md` with all sections above filled in.

Create the directory if it does not exist.

## Rules

- Do not write the analysis script here — only design it.
- Every experiment must have a control condition.
- Every experiment must specify its falsification observable (what result kills the hypothesis).
- If runtime exceeds 30 minutes, flag it for autopilot execution.
- Prefer adapting existing scripts over writing new ones.
