# Sanity Check: Asymmetric Interference

## Date
2026-03-30

## Target
The finding that asymmetric slit placement breaks the V(y=0)=1 symmetry protection and produces genuine asymmetric interference patterns.

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | CLEAN | Uses same path-sum with arbitrary source and slit positions. No new axioms. |
| Scale Reasonableness | CLEAN | V values range 0 to ~1.0, P(y) distributions normalize to 1.0. |
| Symmetry Compliance | CLEAN | Asymmetric inputs correctly produce asymmetric outputs. Symmetric baseline correctly reproduces prior results. |
| Limit Behavior | CLEAN | Strong asymmetry (+1, +8) almost eliminates interference (V≈0 except near slit_y=8) — sensible because the two slits are so far apart that paths rarely overlap. |
| Numerical Artifacts | CLEAN | No precision issues. V=0.000 at y=0 for strongly asymmetric case is genuine — confirmed by the reachability mechanism. |
| Bug Likelihood | CLEAN | The asymmetric function generalizes the parameterized function with an explicit source parameter and slit labeling. Baseline validation matches the symmetric case. |

## Skeptical Reviewer's Best Objection
"Your 'upper' slit labeling for the phase shift is arbitrary in the asymmetric case. How do you know the phase shift is applied correctly when slits aren't symmetric?"

## Response
The phase shift is applied to whichever slit has the larger y-coordinate (`upper_y = max(slit_ys)`). This is a labeling choice, not a physical constraint. Swapping which slit gets the phase shift would produce a reflected V(y) profile but the same contrast values. The key finding — that V(y=0) < 1 with asymmetry — is independent of this labeling.

## Verdict
**CLEAN**
