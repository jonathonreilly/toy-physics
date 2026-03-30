# Sanity Check: Partial Records

## Date
2026-03-30

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | CLEAN | Probabilistic record creation splits amplitude into coherent + recorded sectors. Standard quantum-like amplitude splitting rule. |
| Scale Reasonableness | CLEAN | V ranges smoothly from V_0 to 0 as p goes 0→1. |
| Symmetry Compliance | CLEAN | V(+y) = V(-y) maintained at all p values. |
| Limit Behavior | CLEAN | p=0 reproduces coherent case exactly. p=1 reproduces full-record case exactly. |
| Numerical Artifacts | CLEAN | Linear relationship holds to floating-point precision. No rounding or discretization effects. |
| Bug Likelihood | CLEAN | p=0 and p=1 reproduce the binary cases from the original two_slit_distribution(). The intermediate behavior follows mathematically from the amplitude splitting. |

## Skeptical Reviewer's Best Objection
"V = V_0(1-p) is mathematically guaranteed by your amplitude splitting rule √p / √(1-p). You've confirmed a tautology, not discovered physics."

## Response
The reviewer is correct. The linear decoherence is a mathematical consequence of the amplitude splitting, not an emergent property of the model's dynamics. The experiment successfully tests the partial-record MECHANISM (it works, decoherence is gradual, not binary) but the resulting law is the trivial one. A more interesting partial-record mechanism would involve records that affect the continuation landscape or delay structure, not just sector labeling.

## Verdict
**CLEAN** — but the result is mathematically trivial. The mechanism works as designed; the law V = V_0(1-p) is the expected outcome of amplitude splitting, not a new finding.
