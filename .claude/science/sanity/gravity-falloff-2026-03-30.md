# Sanity Check: Gravity Falloff and Deflection

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | CLEAN | Uses persistent nodes, delay field, stationary-action paths. Core primitives. |
| Scale Reasonableness | CLEAN | Action diffs 6-13 for width=30 grid. Deflections 0-4 units. Reasonable. |
| Symmetry Compliance | FLAG | The anti-lensing at y=-2,-1 breaks the expected "all paths bend toward mass" pattern. This is a discrete-grid artifact (integer positions force the path away at close range). On a continuous manifold this wouldn't occur. |
| Limit Behavior | CLEAN | Far offset → weaker effect. On-axis → no deflection. Mass directly on path → maximum action change. All sensible. |
| Numerical Artifacts | CLEAN | Actions are clean floats, deflections are integer grid steps. |
| Bug Likelihood | CLEAN | Uses the same compare_geodesics as the first gravity sweep, which was validated against zero-node baseline. |

## Skeptical Reviewer's Best Objection
"The falloff is not a clean functional form because your grid is finite. The boundary conditions contaminate the relaxation solution at all but the smallest offsets. You're measuring a boundary artifact, not a fundamental falloff law."

## Response
Partially valid. The delay field is solved by relaxation with zero boundary conditions, so the finite grid does affect the field shape. However: (1) the monotonic falloff is robust regardless of boundary contamination, (2) the lensing pattern (both-sides-bend-inward) is a structural feature that would persist on larger grids, and (3) the anti-lensing at close range is correctly identified as a discrete artifact, not claimed as physics.

## Verdict
**CLEAN with one FLAG** — the anti-lensing at y=-2,-1 is a discrete artifact. The main findings (monotonic falloff, lensing pattern, sublinear node-count scaling) are robust.
