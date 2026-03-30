# Analysis: Gravity-Like Distortion Response

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-gravity-distortion-response-sweep.txt`
- Script: `scripts/gravity_distortion_response_sweep.py`

## Key Findings

### 1. Path bending onset requires ≥2 persistent nodes
0-1 persistent nodes produce zero deflection at all targets. At 2+ nodes, paths to off-center targets immediately deflect. The onset is sharp (0 → finite). This suggests a minimum "mass" threshold for the delay-field distortion to alter the stationary-action path.

### 2. Action difference grows monotonically with node count
For target y=0 (straight path): action_diff goes from -5.08 (n=2) to -8.51 (n=5) and continues decreasing. The persistent nodes reduce the action along the path — they make the continuation landscape "easier" to traverse near them, consistent with a gravitational potential well.

### 3. Gravitational potential falls off with distance
With 5 nodes, sweeping their y-offset from 0 to 9 (distance from path):
- offset=0: action_diff = -8.51
- offset=5: action_diff = -6.90
- offset=9: action_diff = -4.09

The falloff is monotonic. Between offset 0 and 9, the effect drops by ~52%. This is the model's gravitational potential falloff — the first quantitative measurement.

### 4. x-position effect is symmetric with peak at center
Persistent nodes at x=10 (center of 0-20 grid) have maximum effect (action_diff = -7.38). Moving them toward either edge (x=2 or x=18) reduces the effect symmetrically to -5.29. The curve is bell-shaped — nodes along the middle of the path have the most influence.

### 5. Path deflection is asymmetric around the "mass"
For target y=5 (above the persistent nodes at y=4): the path is pulled up early and stays near y=5. Max deflection = 3.0.
For target y=-5 (below): the path stays at y=0 until late, then drops. Max deflection = 2.0.
Paths toward the mass deflect more than paths away — directionally asymmetric bending.

### 6. The source-to-center path never deflects
For target y=0 with persistent nodes at y>0: the stationary-action path stays at y=0 (zero deflection) even though the action changes substantially. The mass doesn't bend a path that passes directly below it — only off-axis paths bend. This is consistent with a gravitational-lensing-like picture where head-on paths feel the potential but don't deflect.

## Hypothesis Verdict
**SUPPORTED** — bending increases monotonically with persistent node count (above the 2-node threshold) and the potential falls off monotonically with distance. The null hypothesis (bending depends only on presence/absence of nodes) is falsified.

## Significance
This is the first quantitative distortion-response curve for the model's gravity-like mechanism. The key structural features — monotonic count dependence, distance falloff, x-symmetry, asymmetric bending, and the 2-node onset threshold — are all newly measured.
