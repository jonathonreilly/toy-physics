# Analysis: Fixed-DAG Sorkin Test

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-interference-sorkin-fixed-dag.txt`

## Key Finding: I₃ = 0 to machine precision. Born rule holds.

With the causal DAG held FIXED (all barrier nodes present, amplitude zeroed at closed slits instead of removing nodes), the Sorkin parameter is:

| Config | max |I₃|/|P_ABC| |
|--------|-------------------|
| Symmetric (-4, 0, +4) | 4.73 × 10⁻¹⁶ |
| Close (-2, 0, +2) | 6.44 × 10⁻¹⁶ |
| Wide (-6, 0, +6) | 2.56 × 10⁻¹⁶ |
| Asymmetric (-4, +1, +6) | 4.22 × 10⁻¹⁶ |

All ratios are at machine epsilon (~10⁻¹⁶). I₃ = 0 exactly.

## Comparison with original (topology-changing) test

| Config | Original I₃/P | Fixed-DAG I₃/P | Ratio |
|--------|---------------|----------------|-------|
| Symmetric | 1.67 × 10⁶ | 4.73 × 10⁻¹⁶ | 10²² drop |
| Close | 9.19 × 10¹ | 6.44 × 10⁻¹⁶ | 10¹⁷ drop |
| Wide | 4.61 × 10⁹ | 2.56 × 10⁻¹⁶ | 10²⁵ drop |
| Asymmetric | 4.21 × 10⁹ | 4.22 × 10⁻¹⁶ | 10²⁵ drop |

The original I₃ was entirely DAG reconfiguration. Zero genuine higher-order interference.

## What this means

1. **The model's path-sum obeys the Born rule.** All interference reduces to pairwise amplitude combination. There is no third-order or higher-order interference.

2. **The original I₃ ≠ 0 was a topological artifact.** Blocking barrier nodes changes the causal DAG globally, creating nonlinear coupling between slit configurations. This is real but is a property of how the discrete network reconfigures, not a property of the interference mechanism.

3. **The model's interference is standard quantum-like.** Amplitudes add linearly, probabilities are |sum|², and the inclusion-exclusion identity holds exactly. This is the expected behavior for any path-sum model with linear amplitude propagation.

## Hypothesis Verdict
The original Sorkin test was **AMBIGUOUS** (I₃ ≠ 0 but mechanism unclear). The fixed-DAG refinement resolves it: **BORN RULE CONFIRMED**. The model has standard pairwise interference only.

## Significance
This is a clean, quantitative result that constrains the model: its interference is quantum-like (Born rule, pairwise only), not post-quantum (no higher-order terms). The DAG reconfiguration effect is separately interesting as a discrete-network phenomenon, but it's not interference in the physics sense.
