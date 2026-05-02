# Left-Handed Charge Matching on the Selected-Axis Surface

**Date:** 2026-04-14 (scope tightened 2026-05-02)
**Type:** positive_theorem (proposed; audit-lane to ratify)
**Claim scope:** the unique traceless abelian eigenvalue pattern
`(+1/3, −1)` on the `(2,3)` and `(2,1)` blocks of the LH-doublet sector,
on the graph-first selected-axis surface. SM hypercharge identification
via `Q = T_3 + Y/2` is **explicitly out of scope** (separate downstream
labelling step).
**Authority role:** canonical main-branch note for the left-handed
charge-matching row.
**Script:** `scripts/frontier_graph_first_su3_integration.py`

## Safe statement

On the graph-first selected-axis surface, the unique traceless abelian
direction in the gl(3) ⊕ gl(1) commutant has eigenvalue pattern
**`(+1/3, −1)`** on the `(2,3)` and `(2,1)` sub-decompositions of the
LH-doublet sector, where:

- `(2,3)` denotes the SU(2)-doublet × Sym²(C²) (3-dim) block;
- `(2,1)` denotes the SU(2)-doublet × Anti²(C²) (1-dim) block.

The eigenvalue ratio `1 : (−3)` is forced structurally by tracelessness
on the (6 + 2) state count of the LH-doublet sector
(`6 · α + 2 · β = 0` ⇒ `β = −3α`); the overall scale `α = +1/3` is fixed
by the convention that the lepton-doublet eigenvalue is `−1`.

This is the retained publication-safe statement.

## Canonical derivation stack

1. [GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md](./GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)
   fixes the selector uniquely up to graph automorphism.
2. [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](./GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
   shows that the selected axis produces the canonical weak fiber,
   residual `3 ⊕ 1` base split, and structural `SU(3)` closure.
3. On that same selected-axis surface, the unique traceless abelian
   direction has the left-handed eigenvalue pattern `+1/3` on the
   `(2,3)` (quark-doublet) block and `−1` on the `(2,1)` (lepton-doublet)
   block. **This is the load-bearing step (class A algebraic).**

## Out of scope: SM hypercharge identification

The identification of the eigenvalue pattern `(+1/3, −1)` with **Standard
Model hypercharge** `(Y_QL, Y_LL)` via the SM convention `Q = T_3 + Y/2`
is a **separate downstream labelling step**, **not** in this row's
load-bearing chain. Specifically:

- The eigenvalue pattern `(+1/3, −1)` is derived above on the
  graph-first surface from tracelessness — class (A) algebraic.
- The labelling of these eigenvalues as SM hypercharges `Y_QL = +1/3`,
  `Y_LL = −1` is the SM-convention identification; this is the
  `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24` /
  `HYPERCHARGE_IDENTIFICATION_NOTE.md` lane, not this row.
- Likewise, the SM electric-charge formula `Q = T_3 + Y/2` matching to
  observable charges `Q(u_L) = +2/3, Q(d_L) = −1/3, Q(ν_L) = 0,
  Q(e_L) = −1` is downstream.

## Boundary

The safe authority boundary is:

- selected-axis left-handed eigenvalue pattern `(+1/3, −1)` is retained;
- full anomaly-complete hypercharge closure is **not** claimed here
  (absorbed into `ONE_GENERATION_MATTER_CLOSURE_NOTE.md`);
- SM hypercharge identification is **not** claimed here (separate
  downstream labelling).

## Audit-lane disposition (proposed)

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Eigenvalue pattern (+1/3, -1) on (2,3) and (2,1) blocks of LH-doublet
  sector under graph-first commutant decomposition, with overall scale
  fixed by lepton-doublet = -1 convention. SM hypercharge identification
  out of scope (separate downstream labelling step).
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
```

If the audit lane reads the load-bearing step as the **class-(A)
algebraic eigenvalue derivation** in step 3 (rather than the SM
labelling step that's now explicitly out of scope), the row's
load-bearing class is (A) and `effective_status` should land **retained**
(positive_theorem + audited_clean + retained-grade deps:
`graph_first_selector_derivation_note` and
`graph_first_su3_integration_note`, both retained_bounded).

## Validation

- primary runner:
  [frontier_graph_first_su3_integration.py](./../scripts/frontier_graph_first_su3_integration.py)
- supporting selector runner:
  [frontier_graph_first_selector_derivation.py](./../scripts/frontier_graph_first_selector_derivation.py)
- narrow ratio sister theorem:
  [LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md](./LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md)
  (cycle 1 of retained-positive-rescope campaign, PR #292) — proves the
  ratio `1:(-3)` from minimal premises with no normalization-scale claim.
