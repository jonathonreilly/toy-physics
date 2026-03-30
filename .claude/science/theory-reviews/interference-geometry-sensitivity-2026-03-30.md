# Theory Review: Interference Pattern Geometry Sensitivity

## Date
2026-03-30

## Hypothesis Under Review
The interference fringe contrast depends quantitatively on network geometry (grid width, slit separation), revealing a continuous transition between coherent and record-dominated regimes.

## Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Axiom Compliance | COMPLIANT | Uses only events, links, delays, records, and the path-sum over the causal DAG. Grid geometry is a property of the network structure, not an imported concept. |
| Internal Consistency | CONSISTENT | The prediction that longer paths → sharper fringes follows from the existing `local_edge_properties()` phase accumulation mechanism. More edges traversed = more phase accumulated = larger phase difference between paths. No contradiction with confirmed results. |
| Limiting Behavior | WELL-BEHAVED | At width→0: no barrier possible, trivially no interference. At slit_separation→0: single slit, no two-path interference. At slit_separation→large: paths too divergent, detector coverage drops. All sensible. |
| Falsifiability | SHARP | Three distinct falsification criteria named with specific thresholds. The null hypothesis (geometry independence) is cleanly testable. |
| Minimality | MINIMAL | Uses existing simulator machinery with no new axioms. The only variation is network geometry parameters that already exist. |
| Emergent vs. Imposed | EMERGENT | The interference pattern itself emerges from the path-sum over the causal DAG. The record mechanism is part of the model's axioms (Axiom 9). Geometry dependence would be genuinely emergent from the network structure. |

## Overall Verdict
PROCEED

## Notes
- One subtle concern: the `two_slit_distribution()` function hardcodes `width=16`, `height=10`, `barrier_x=8`, `slit_ys={-4, 4}`. The experiment script will need to GENERALIZE this function to accept geometry parameters. This is a code modification, not an axiom change.
- The `phase_per_action=4.0` and `attenuation_power=1.0` in `RulePostulates` are fixed. Consider whether these should also be swept, or whether geometry alone is sufficient for the first experiment. Recommendation: geometry only for the first sweep, postulate sweep as follow-up.
- The prediction about "wider grids → sharper fringes" has a non-trivial interaction with attenuation: longer paths also attenuate more, which could REDUCE contrast by making one path dominate. This is an interesting tension that the experiment will resolve.

## Suggested Simplifications
None needed — the hypothesis is already minimal and well-scoped.
