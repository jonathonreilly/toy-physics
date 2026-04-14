# Left-Handed Charge Matching on the Selected-Axis Surface

**Date:** 2026-04-14
**Status:** retained corollary on the current paper surface
**Script:** `scripts/frontier_graph_first_su3_integration.py`
**Authority role:** canonical main-branch note for the left-handed charge-matching row

## Safe statement

On the graph-first selected-axis surface, the abelian factor gives the safe
left-handed Standard Model charge pattern

- `Q_L : (2,3)_{+1/3}`
- `L_L : (2,1)_{-1}`

This is the retained publication-safe corollary.

By itself, this note does **not** claim a full anomaly-complete
`U(1)_Y` derivation. The anomaly-complete branch belongs to the
full-framework one-generation closure.

## Canonical derivation stack

1. [GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md](./GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)
   fixes the selector uniquely up to graph automorphism.
2. [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](./GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
   shows that the selected axis produces the canonical weak fiber, residual
   `3 \oplus 1` base split, and structural `SU(3)` closure.
3. On that same selected-axis surface, the unique traceless abelian direction
   gives the left-handed eigenvalue pattern `+1/3` on the quark-doublet block
   and `-1` on the lepton-doublet block.
4. The charge formula `Q = T_3 + Y/2` then matches the left-handed doublet
   charges on the safe retained surface.

## Boundary

The safe authority boundary is:

- selected-axis left-handed charge matching is retained
- full anomaly-complete hypercharge closure is **not** claimed here

That stronger statement is absorbed into
[ONE_GENERATION_MATTER_CLOSURE_NOTE.md](./ONE_GENERATION_MATTER_CLOSURE_NOTE.md).

## Validation

- primary runner:
  [frontier_graph_first_su3_integration.py](./../scripts/frontier_graph_first_su3_integration.py)
- supporting selector runner:
  [frontier_graph_first_selector_derivation.py](./../scripts/frontier_graph_first_selector_derivation.py)
