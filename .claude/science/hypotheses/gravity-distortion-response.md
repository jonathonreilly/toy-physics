# Hypothesis: Gravity-Like Bending Has a Quantitative Distortion-Response Curve

## Date
2026-03-30

## Statement
The magnitude of gravity-like path bending (deviation of the stationary-action path from the free path) increases monotonically with the number and proximity of persistent nodes that source the delay-field distortion, producing a quantitative "bending vs distortion strength" curve.

## Prediction
- With zero persistent nodes: free path is straight (no bending). Baseline.
- With increasing persistent-node count near the path: bending increases monotonically.
- With persistent nodes farther from the path: bending decreases (falls off with distance).
- The bending-vs-distance curve characterizes the model's "gravitational" falloff.
- The bending-vs-count curve characterizes whether effects are additive or nonlinear.

## Falsification Criteria
- If bending does NOT increase monotonically with persistent node count: hypothesis falsified — the gravity mechanism is non-monotonic or saturates.
- If bending does NOT fall off with distance: the delay-field distortion has no spatial locality, which would undermine the "gravity-like" interpretation.
- If the free path and distorted path are identical even with persistent nodes present: the gravity claim (Result #2) needs re-examination.

## Null Hypothesis
Path bending is insensitive to the arrangement of persistent nodes — it depends only on whether ANY persistent nodes exist, not on how many or where they are.

## Relevant Prior Work
- `compare_geodesics()` in `toy_event_physics.py` (line 3625) — compares free vs distorted paths.
- `derive_local_rule()` with persistent_nodes parameter — existing mechanism for delay-field distortion.
- `robustness_scenarios()` and `benchmark_packs()` — existing benchmark suite that tests bending, but with fixed configurations, no sweeps.
- No scripts or logs sweep distortion strength systematically.

## Proposed Experiments
1. Fix grid geometry (width=20, height=10). Sweep number of persistent nodes from 0 to 20, placed at (10, 0) and expanding outward.
2. Fix persistent node count at 5. Sweep their distance from the path center (distance 0 to 8).
3. Measure: path deflection (max |y_distorted - y_free|), action difference, and path topology.
4. Repeat at multiple source-target pairs to check universality.

## Status
PROPOSED
