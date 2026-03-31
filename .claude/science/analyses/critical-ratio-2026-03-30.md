# Analysis: Critical Ratio Fine Sweep

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-interference-critical-ratio-sweep.txt`
- Script: `scripts/interference_critical_ratio_sweep.py`

## Data Summary
- 19 widths (4-40 step 2) x 12 slit_halves (1-12) = ~216 geometry points
- V measured at y=1,2,3,5 for each

## Key Findings

### Finding 1: The threshold IS sharp, IS y-dependent, and is perfectly resolved

For slit_half=4 (slit_sep=8), tracing V from zero to nonzero:

| y | Last zero width | First nonzero width | R_threshold | V at jump |
|---|----------------|--------------------| ------------|-----------|
| 1 | 8 | 10 | 1.25 | 0.875 |
| 2 | 10 | 12 | 1.50 | 0.246 |
| 3 | 12 | 14 | 1.75 | 0.071 |
| 5 | 16 | 18 | 2.25 | 0.004 |

The transition is DISCONTINUOUS: V jumps from exactly 0 to a finite value (0.004 to 0.875 depending on y). There are no gradual-onset values between 0 and 0.004.

### Finding 2: The threshold ratio increases with off-center distance

R_c(y) is monotonically increasing: positions farther from center require larger width/slit_sep to achieve two-slit reachability. This makes geometric sense — paths to farther-off-center positions require wider grids to "bend around" far enough to reach both slits.

The relationship is approximately linear: R_c ≈ 0.25 * y + 1.0 (for slit_half=4).

### Finding 3: The jump size decreases with off-center distance

V at the threshold drops from 0.875 (y=1) to 0.004 (y=5). Positions farther from center have weaker second-slit contribution even when it first becomes available, because the newly reachable path is longer and more attenuated.

### Finding 4: The slit-height boundary is at slit_half = height - 1

For slit_half ≥ 10 (height=10), V=0 at all widths tested. This is because the slit is at the grid edge (y=±10) and the grid extends only to y=±10, so the far slit can never be reached through a path that stays within the grid bounds.

### Finding 5: Post-threshold growth is monotonic and saturating

After the jump, V increases monotonically with width and appears to asymptote toward 1.0 for y=1 (already 0.996 at w=40) but much more slowly for y=5 (only 0.304 at w=40). The saturation rate decreases with off-center distance.

## Hypothesis Verdict
**SUPPORTED with refinement.** The sharp threshold exists and is y-dependent (R_c increases with |y|). The transition is discontinuous (step function). The original hypothesis predicted either a universal R_c or a y-dependent one — the data confirms the y-dependent version, consistent with the slit-reachability mechanism.

## Significance
The threshold is a topological property: it marks the point where the discrete grid's causal DAG first admits paths through both slits to a given screen position. This is intrinsically discrete — no continuum analogue exists.
