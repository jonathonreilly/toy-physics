# PR230 Radial-Spurion Sector-Overlap Theorem

**Status:** exact-support / conditional theorem; current additive-source shortcut blocked
**Date:** 2026-05-06
**Runner:** `scripts/frontier_yt_pr230_radial_spurion_sector_overlap_theorem.py`
**Certificate:** `outputs/yt_pr230_radial_spurion_sector_overlap_theorem_2026-05-06.json`

## Verdict

The clean same-source physical-response route has a sharp positive condition:
if the PR230 scalar source is adopted as a single canonical-Higgs radial
spurion, so top, W, and Z masses all depend on the same branch `v(s)`, and no
independent additive top bare-mass source is present, then the sector-overlap
factor cancels exactly.

The top/W response formula becomes

```text
m_t(s) = y_t v(s) / sqrt(2)
M_W(s) = g2 v(s) / 2
y_t = g2 (dm_t/ds) / (sqrt(2) dM_W/ds)
```

and the top/Z formula is the analogous expression with
`sqrt(g2^2 + gY^2)` and `dM_Z/ds`.  The unknown `dv/ds` is common and cancels.

This is not current PR230 closure.  The current FH/LSZ source is an additive
top bare-mass shift, the same-source EW/Higgs ansatz is not adopted as actual
action authority, canonical `O_H` is absent, and W/Z mass-fit rows are absent.

## Boundary

The theorem also blocks a tempting shortcut.  If the same source coordinate
contains an independent additive top term, then

```text
dm_t/ds = y_t (dv/ds) / sqrt(2) + a_top
```

while `dM_W/ds = g2 (dv/ds)/2`.  The response ratio then changes with
`a_top`.  Therefore a shared source label does not derive
`k_top = k_gauge`; either the action must be radial-spurion-clean, or the
independent additive top component must be measured and subtracted by an
additional row theorem.

## What This Retires

This block retires one ambiguity in the action-first route:

- a radial-spurion action contract would supply the sector-overlap algebra;
- an additive top mass source plus Higgs composite source does not.

So the clean future contract is stricter than the previous same-source ansatz:
the accepted action must make the source a single canonical-Higgs radial
spurion for all top/W/Z mass responses, not merely reuse the same scalar
coordinate name.

## Claim Firewall

This note does not:

- claim retained or proposed-retained `y_t` closure;
- identify the current additive top mass source with a canonical radial
  spurion;
- set `kappa_s`, `c2`, `Z_match`, `k_top/k_gauge`, or `g2` to one;
- use `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`, plaquette,
  or `u0`;
- write accepted EW-action, canonical-`O_H`, W/Z row, or source-Higgs row
  certificates.

## Next Action

Tighten the action-first route around a no-independent-top-source
radial-spurion action contract.  Then either implement same-source W/Z
mass-fit rows under that source, or produce certified `O_H/C_sH/C_HH` pole rows
with Gram/FV/IR authority.
