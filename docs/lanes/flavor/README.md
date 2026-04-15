# Flavor Lane

This manifest organizes the imported CKM work from `claude/youthful-neumann`
around one practical question:

- what survives a strict quantitative, no-import review surface

## Current Verdict

- lane status in this worktree: `closed`
- strongest no-import closure route: `scripts/frontier_ckm_atlas_axiom_closure.py`
- closure note: `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`
- strongest imported structural chain: `scripts/frontier_ckm_closure.py`
- strongest imported direct `V_cb` route: `scripts/frontier_ckm_vcb_closure.py`
- strongest imported mass-ratio route: `scripts/frontier_ckm_five_sixths.py`
- strict review entrypoint: `scripts/frontier_ckm_no_import_audit.py`
- current answer to "airtight no-import CKM closure?": `yes on the atlas/axiom route`

The imported material still sharpens the lane, especially for `V_cb`, but the
current worktree now has a separate no-import closure route that does not rely
on observed quark masses.

## Start Here

- [`scripts/frontier_ckm_atlas_axiom_closure.py`](../../../scripts/frontier_ckm_atlas_axiom_closure.py)
- [`docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [`scripts/frontier_ckm_no_import_audit.py`](../../../scripts/frontier_ckm_no_import_audit.py)
- [`docs/CKM_FINAL_ASSESSMENT.md`](../../CKM_FINAL_ASSESSMENT.md)
- [`docs/CKM_CLEAN_DERIVATION_NOTE.md`](../../CKM_CLEAN_DERIVATION_NOTE.md)

The first two entries are the new branch-local closure surface. The imported
assessment note remains useful as the historical boundary for the older routes.

## Structural Surface

- [`scripts/frontier_ckm_with_ewsb.py`](../../../scripts/frontier_ckm_with_ewsb.py)
- [`scripts/frontier_ckm_closure.py`](../../../scripts/frontier_ckm_closure.py)
- [`docs/CKM_CLOSURE_NOTE.md`](../../CKM_CLOSURE_NOTE.md)
- [`docs/CKM_CLEAN_DERIVATION_NOTE.md`](../../CKM_CLEAN_DERIVATION_NOTE.md)

Use this surface for the lattice-to-texture chain:

- `Z_3` taste structure
- EWSB `C_3 -> Z_2` breaking
- NNI texture and CKM hierarchy

This is the right place to understand what is structurally derived before
asking whether the quantitative lane closes.

## Atlas/Axiom Closure Surface

- [`scripts/frontier_ckm_atlas_axiom_closure.py`](../../../scripts/frontier_ckm_atlas_axiom_closure.py)
- [`docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)

This is the current no-import closure route on the worktree:

- `alpha_s(v)` from the coupling-map / hierarchy surface
- exact EWSB residual pair size `2`
- exact quark-block dimension `6`
- exact `Z_3` CP source
- exact Schur-complement cascade

It closes the full CKM magnitude package without observed quark masses.

## Quantitative `V_cb` Surface

- [`scripts/frontier_ckm_ratio_route.py`](../../../scripts/frontier_ckm_ratio_route.py)
- [`scripts/frontier_ckm_c23_analytic.py`](../../../scripts/frontier_ckm_c23_analytic.py)
- [`scripts/frontier_ckm_vcb_closure.py`](../../../scripts/frontier_ckm_vcb_closure.py)
- [`docs/CKM_VCB_CLOSURE_NOTE.md`](../../CKM_VCB_CLOSURE_NOTE.md)

This surface is the strongest direct lattice-inspired `V_cb` package on the
branch, but it still carries a scheme/matching boundary:

- absolute `S_23` matching factor not fully derived
- finite-volume / normalization questions still marked bounded

## Mass-Ratio / Exponent Surface

- [`scripts/frontier_ckm_five_sixths.py`](../../../scripts/frontier_ckm_five_sixths.py)
- [`scripts/frontier_ckm_exponent_proof.py`](../../../scripts/frontier_ckm_exponent_proof.py)
- [`docs/CKM_FIVE_SIXTHS_NOTE.md`](../../CKM_FIVE_SIXTHS_NOTE.md)
- [`docs/CKM_EXPONENT_PROOF_NOTE.md`](../../CKM_EXPONENT_PROOF_NOTE.md)

This is the sharpest recent `V_cb` story:

- `|V_cb| = (m_s/m_b)^(5/6)` numerically matches PDG at the `0.2%` level
- no coupling constant appears in the final formula
- the route is still bounded because it uses observed quark masses and the
  operator-identification / exponentiation step is not fully closed

## Reading Boundary

- The imported routes remain bounded historical surfaces.
- The current worktree closure claim lives only on the atlas/axiom route.
- The strict audit runner is the authoritative yes/no check for harsh-review
  questions on this branch.
