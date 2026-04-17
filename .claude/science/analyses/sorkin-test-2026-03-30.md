# Analysis: Sorkin Inclusion-Exclusion Test

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-interference-sorkin-test.txt`
- Script: `scripts/interference_sorkin_test.py`

## Key Finding: I₃ ≠ 0 — but the interpretation is subtle

The Sorkin parameter I₃ = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C is nonzero at every tested configuration and every screen position. The ratio |I₃|/|P_ABC| ranges from O(1) to O(10⁹).

| Config | max |I₃|/|P_ABC| |
|--------|-------------------|
| Symmetric (-4, 0, +4) | 1.67 × 10⁶ |
| Close (-2, 0, +2) | 9.19 × 10¹ |
| Wide (-6, 0, +6) | 4.61 × 10⁹ |
| Asymmetric (-4, +1, +6) | 4.21 × 10⁹ |

## Critical Interpretation: This is NOT a Born rule violation

The Sorkin test assumes that opening a new slit ADDS paths to the network without changing existing ones. In a continuum model, this is correct — an additional aperture adds new propagation channels.

But on the discrete grid, blocking/unblocking barrier nodes changes the **entire causal DAG**. When slit C is opened:
- New nodes become available at the barrier
- Arrival times change globally (because the Dijkstra-like propagation has new routes)
- The causal DAG edges change (an edge exists only if arrival_time(B) > arrival_time(A))
- Paths that existed with slits AB may have different timing with slits ABC

This means P_ABC is not a simple superposition of P_AB + (contribution from C). The network topology itself changes, creating a nonlinear coupling between slit configurations that has nothing to do with Born rule violation.

## What I₃ ≠ 0 actually tells us

I₃ ≠ 0 measures the **DAG reconfiguration effect**: how much the causal structure changes when the barrier topology changes. This is a genuinely discrete-network phenomenon:
- On a continuous manifold: I₃ = 0 (paths add linearly)
- On a discrete network with arrival-time-dependent causal DAG: I₃ ≠ 0 (topology changes nonlinearly)

The massive I₃ values (especially for wide and asymmetric configurations) reflect cases where opening a distant slit changes arrival times enough to reconfigure the DAG significantly.

## How to distinguish DAG reconfiguration from genuine higher-order interference

To test for actual Born rule deviation (not just DAG reconfiguration), one would need:
1. A fixed DAG that doesn't change with slit configuration (e.g., keep all barrier nodes but set amplitude transmission to 0 or 1)
2. Or: compare I₃ on a grid large enough that opening distant slits has negligible effect on the local DAG near other slits

## Hypothesis Verdict
**AMBIGUOUS** — I₃ ≠ 0 is confirmed, but the primary mechanism is DAG reconfiguration (topology change), not Born rule violation. The experiment needs refinement to separate the two effects.

## Significance
This is still an important finding: the model's discrete causal structure creates nonlinear coupling between slit configurations that has no continuum analogue. Whether this should be called "higher-order interference" or "topological nonlinearity" is a definitional question. Either way, it's a distinctly discrete-network effect.
