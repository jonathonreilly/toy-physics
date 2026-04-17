# Sanity Check: Topological Decoherence

## Date
2026-03-30

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | CLEAN | Uses DAG modification via arrival-time shortcuts. Within model primitives. |
| Scale Reasonableness | CLEAN | Amplitudes drop 100× (10¹⁰→10⁸) with shortcuts, consistent with edge pruning reducing available paths. |
| Symmetry Compliance | CLEAN | Symmetric shortcuts preserve V(y=0)=1. Asymmetric shortcuts break it (V→0.729). Both correct. |
| Limit Behavior | CLEAN | p=0 reproduces normal case. p=1 gives full shortcut case. Smooth interpolation between. |
| Numerical Artifacts | CLEAN | Amplitude magnitudes are well above precision floor. |
| Bug Likelihood | CLEAN | Per-slit decomposition confirms the mechanism: shortcuts equalize amplitude balance. |

## Root Cause of V-Increase (Resolved)

The V-increase is NOT an error. The shortcuts speed up arrival times, causing the DAG to PRUNE 81 edges while adding only 39. This pruning removes redundant paths that were diluting the interference pattern. The remaining paths have more balanced per-slit amplitudes (ratio goes from 0.165 to 0.502), which mathematically increases fringe visibility.

This is analogous to spatial filtering in optics: removing some paths can SHARPEN the interference pattern if the removed paths were contributing incoherently or with poor amplitude balance.

## Skeptical Reviewer's Best Objection
"Your 'topological decoherence' is just mixing two different interference patterns incoherently. The recorded DAG has its own coherent pattern (with higher V). Mixing it with the normal pattern produces V between the two values. There's nothing 'decoherent' about this — it's just classical averaging of two quantum-like systems."

## Response
Correct — at the current level, this IS incoherent mixing of two coherent path-sums. The non-trivial part is that the two DAGs produce DIFFERENT visibility profiles (the topology change matters), and the resulting V(p) is not the trivial V₀(1-p). Whether this constitutes "decoherence" in a deeper sense depends on whether the model can be extended so the two DAG branches interact (interfere with each other across topology changes), which is an open question.

## Verdict
**CLEAN** — the V-increase is explained by amplitude rebalancing from DAG pruning. The result is genuine but the "decoherence" interpretation has the caveat noted above.
