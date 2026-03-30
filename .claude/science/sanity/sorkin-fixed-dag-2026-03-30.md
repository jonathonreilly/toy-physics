# Sanity Check: Fixed-DAG Sorkin Test

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | CLEAN | Same path-sum, same nodes. Only change: amplitude mask instead of node removal. |
| Scale Reasonableness | CLEAN | I₃/P ratios at 10⁻¹⁶ = machine epsilon for float64. Exactly zero. |
| Symmetry Compliance | CLEAN | Symmetric configs give symmetric I₃ profiles. |
| Limit Behavior | CLEAN | Same result at all 4 slit configurations. Universal. |
| Numerical Artifacts | CLEAN | The 10⁻¹⁶ residual IS the expected floating-point rounding. Not a real signal. |
| Bug Likelihood | CLEAN | Fixed-DAG function produces nonzero P_ABC (interference works). Only I₃ is zero. The amplitude mask correctly blocks non-slit paths while preserving DAG. |

## Skeptical Reviewer's Best Objection
"Of course I₃ = 0 — you're using a linear path-sum with |sum|² probability. That's the Born rule by construction. You haven't learned anything about the model."

## Response
Partially correct — the Born rule IS built into |sum(amplitudes)|². But the test still had value:
1. It confirmed that the original I₃ ≠ 0 was DAG reconfiguration, not a surprise property of the path-sum.
2. It established that the model's interference is standard quantum-like, ruling out post-quantum behavior.
3. It identified DAG reconfiguration as a separate, distinctly-discrete phenomenon worth studying on its own.

## Verdict
**CLEAN**
