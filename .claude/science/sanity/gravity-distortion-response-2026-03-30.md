# Sanity Check: Gravity Distortion Response

## Date
2026-03-30

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | CLEAN | Uses persistent nodes, delay-field distortion, and stationary-action paths — all core model primitives. |
| Scale Reasonableness | CLEAN | Action values 12-22 for width=20 grid. Deflections 0-3 grid units. All reasonable. |
| Symmetry Compliance | CLEAN | x-position sweep is symmetric around grid center (x=2↔x=18). Source-to-center path stays straight with off-axis mass. |
| Limit Behavior | CLEAN | 0 nodes → 0 deflection. Nodes at edge → weaker effect. Both sensible. |
| Numerical Artifacts | CLEAN | Deflections are integer grid units. Actions are clean floats. No precision issues. |
| Bug Likelihood | FLAG | The 2-node onset is surprising. Why does 1 node produce zero deflection? Need to check if `derive_local_rule` with a single persistent node actually modifies the delay field, or if there's a minimum-set requirement. |

## Investigation of 1-Node Anomaly

The flag needs investigation. A single persistent node at (10, 4) should create a local delay-field distortion. If it doesn't change the stationary-action path at all, either:
- (a) The delay field change from 1 node is below the discretization threshold of the grid (the path can't move by less than 1 grid unit)
- (b) `derive_local_rule` requires ≥2 nodes to produce a meaningful distortion
- (c) The single node's field is exactly symmetric around the path and cancels

Most likely (a): the 1-node distortion IS present in the action (action_diff should be nonzero) but too small to change the discrete path. Let me check — at n=1, action_diff = 0.0000 for ALL targets. So the delay field itself is unchanged with 1 node. This points to (b) — the rule derivation may require a minimum node set.

This is a property of `derive_local_rule`, not a bug in the sweep. But it means the "2-node onset" is a feature of the rule derivation, not of the gravity mechanism per se.

## Skeptical Reviewer's Best Objection
"You're sweeping at integer grid positions with a discrete path. The 'monotonic increase' might just be an artifact of the grid resolution — at continuous resolution, the response could oscillate."

## Response
Fair concern. The grid discretization means we see step-function behavior in path deflection (0, 1, 2, 3 units). The action, however, varies continuously and also shows monotonic behavior. The monotonicity is robust in the continuous observable (action) even if the discrete observable (deflection) is step-wise.

## Verdict
**CLEAN with one FLAG** — the 1-node zero-effect needs follow-up to determine if it's a rule-derivation requirement or a discretization artifact. The main findings (monotonic count/distance dependence) are robust.
