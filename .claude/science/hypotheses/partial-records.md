# Hypothesis: Partial Record Formation Creates Gradual Decoherence

## Date
2026-03-30

## Statement
If records are formed probabilistically (with probability p per path crossing the barrier), visibility will decrease continuously from V_coherent (at p=0) to V_record=0 (at p=1), producing a decoherence curve V(p) that characterizes the model's transition between coherent and record-dominated regimes.

## Prediction
- At p=0: full coherent visibility (identical to record_created=False).
- At p=1: zero visibility (identical to record_created=True).
- The transition V(p) is monotonically decreasing.
- The functional form of V(p) is unknown and will be the main finding:
  - Linear: V(p) = V_0 * (1 - p) — trivial mixing
  - Quadratic: V(p) = V_0 * (1 - p)² — suppression requires both paths to be recorded
  - Threshold: V(p) ≈ V_0 for p < p_c, then drops sharply — phase transition in record formation
  - Other: something specific to this model's path-sum structure

## Falsification Criteria
- If V(p) is non-monotonic (increases at intermediate p), the model has an unexpected resonance.
- If V(p) = V_0 for all p < 1 and drops to 0 only at p=1 exactly, partial records have no effect and the mechanism is truly binary with no gradual transition.

## Null Hypothesis
The record mechanism is genuinely binary: ANY nonzero record probability p > 0 immediately destroys all interference (V drops to 0), with no intermediate regime.

## Proposed Experiments
1. Implement probabilistic record creation: at the barrier, each path creates a record with probability p (splitting into recorded and unrecorded sectors with appropriate amplitudes).
2. Sweep p from 0 to 1 in steps of 0.05 at the default geometry (width=16, slit_sep=8).
3. Measure V(y=0) and mean V across the screen at each p.
4. Repeat at 2-3 other geometries to check universality.
5. Fit V(p) to candidate functional forms.

## Status
PROPOSED
