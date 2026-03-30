# Sanity Check: Slit Reachability

## Date
2026-03-30

## Target
The finding that V=0 is caused by single-slit reachability in all 6 tested cases, and V>0 requires both slits contributing in all 4 tested cases.

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | CLEAN | Uses only the causal DAG path structure. Per-slit decomposition is a direct measurement, not an interpretation. |
| Scale Reasonableness | CLEAN | Single-slit amplitudes range from 8.6e2 to 3.5e12, consistent with grid-size-dependent path counts. |
| Symmetry Compliance | CLEAN | For y>0 in symmetric setups, the closer slit (y=+4 or +6) contributes, as expected. |
| Limit Behavior | CLEAN | At w=8 (minimal grid past barrier), only the nearest slit path fits. At w=24 (large grid), both slits easily reach y=5. |
| Numerical Artifacts | CLEAN | The absent slit contributes EXACTLY zero, not a tiny residual. This is topological (no path exists), not numerical. |
| Bug Likelihood | CLEAN | The per-slit tracking is a simple sector label applied at the barrier crossing. Same mechanism as the record sector labeling, which is well-tested. |

## Skeptical Reviewer's Best Objection
"You tested 10 cases. How do you know there isn't a geometry where V=0 with both slits contributing (perfect cancellation at all phases)?"

## Response
For two-slit interference, perfect cancellation at ALL phases simultaneously is mathematically impossible when both slits contribute non-degenerate amplitudes with the phase shift applied to only one slit. A phase sweep rotates one amplitude relative to the other; if both are nonzero, they cannot cancel at every rotation angle. The only way to get V=0 at all phases is for one amplitude to be exactly zero.

## Verdict
**CLEAN**
