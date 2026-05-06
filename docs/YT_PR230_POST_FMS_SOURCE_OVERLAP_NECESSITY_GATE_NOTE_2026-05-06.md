# PR230 Post-FMS Source-Overlap Necessity Gate

**Date:** 2026-05-06
**Status:** exact negative boundary / post-FMS source-overlap not derivable
from current PR230 source-only or `C_sx/C_xx` rows
**Claim type:** no_go
**Runner:** `scripts/frontier_yt_pr230_post_fms_source_overlap_necessity_gate.py`
**Certificate:** `outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json`

```yaml
actual_current_surface_status: exact negative boundary / post-FMS source-overlap not derivable from current PR230 source-only or C_sx/C_xx rows
conditional_surface_status: exact-support if future PR230 artifacts supply canonical O_H plus C_ss/C_sH/C_HH pole rows with Gram/FV/IR checks, or a same-source physical-response bypass
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
```

## Question

After the FMS composite theorem, the future operator target is sharp:

```text
O_H = Phi^dagger Phi - <Phi^dagger Phi>
    = v h + h^2/2 + pi^2/2 .
```

This gate asks whether current PR230 source-pole data, source-only LSZ rows,
or the completed taste-radial `C_sx/C_xx` chunks determine the remaining
source-overlap row `C_sH`.

## Result

They do not.  The current surface still needs a real same-surface
source-overlap row or theorem.

The runner constructs a fixed-residue counterfamily:

```text
Res C_ss = 18
Res C_HH = 18
Res C_sH = rho sqrt(Res C_ss Res C_HH)
rho in {1, 0.75, 0.5, 0.25, 0, -0.25}
```

All members keep the source residue and FMS `C_HH` residue fixed while changing
the source-Higgs overlap and Gram determinant.  Therefore the FMS composite
definition and current source-only rows do not infer `Res C_sH`.

The runner also constructs an orthogonal-top-coupling counterfamily: the same
measured source response can be held fixed while changing the canonical `y_t`
if an orthogonal neutral scalar coupling is allowed.  This restates why a
source-overlap or physical-response bridge is load-bearing.

## Completed Chunk Boundary

Chunks001-004 contain bounded `C_sx/C_xx` taste-radial rows.  Their metadata
explicitly records that `C_sx/C_xx` aliases are second-source taste-radial
rows, not canonical-Higgs `C_sH/C_HH` pole rows unless a separate canonical
`O_H` bridge passes.  They also have zero pole-residue rows.  Active chunks and
launcher status remain run-control only.

## Positive Contract

The route reopens with one of:

- same-surface canonical `O_H` certificate;
- same-ensemble `C_ss/C_sH/C_HH` pole rows with `C_HH` from the certified
  `O_H`;
- Gram purity `Res(C_sH)^2 = Res(C_ss) Res(C_HH)` with uncertainty control;
- FV/IR/isolated-pole and scalar-LSZ authority;
- a physical-response bypass such as matched top/W/Z rows with strict
  `g2`, covariance, and `delta_perp`.

## Non-Claims

This note does not claim retained or `proposed_retained` PR230 closure.  It
does not treat the FMS expansion as source-overlap authority, does not treat
`C_sx/C_xx` taste-radial rows as canonical `C_sH/C_HH` pole rows, does not set
`kappa_s`, `c2`, or `Z_match` to one, and does not use `H_unit`,
`yt_ward_identity`, observed targets, `alpha_LM`, plaquette, or `u0`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_post_fms_source_overlap_necessity_gate.py
# SUMMARY: PASS=14 FAIL=0
```
