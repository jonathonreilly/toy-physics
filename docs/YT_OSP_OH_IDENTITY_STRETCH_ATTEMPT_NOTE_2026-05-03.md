# O_sp / O_H Identity Stretch Attempt

**Date:** 2026-05-03
**Status:** exact negative boundary / `O_sp`-to-`O_H` identity not derived on current surface
**Runner:** `scripts/frontier_yt_osp_oh_identity_stretch_attempt.py`
**Certificate:** `outputs/yt_osp_oh_identity_stretch_attempt_2026-05-03.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support if a future C_sH/C_HH Gram-purity row, W/Z response row, or rank-one neutral-scalar theorem closes the overlap
proposal_allowed: false
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Target

After deriving the Legendre/LSZ source-pole operator

```text
O_sp(q) = sqrt(dGamma_ss/dx | pole) O_s(q),
```

the remaining PR230 closure target is:

```text
O_sp = O_H
```

up to a sign convention, where `O_H` is the canonical Higgs radial operator
whose VEV supplies `v`.

## Minimal Premise Set

The stretch attempt allows only:

- the Cl(3)/Z3 substrate and the uniform additive scalar source `s`;
- the newly derived `O_sp` Legendre/LSZ source-pole normalization;
- existing canonical Higgs / `v` surfaces after `H` is supplied;
- exact taste-scalar isotropy support;
- existing one-Higgs gauge-monomial selection support.

It forbids `H_unit` matrix-element readout, `yt_ward_identity`, observed
targets, `alpha_LM`, plaquette, `u0`, and unproved unit settings such as
`kappa_s = 1`, `cos(theta) = 1`, `c2 = 1`, or `Z_match = 1`.

## Result

The identity is not derived on the current surface.  A positive counterfamily
remains:

```text
O_sp = cos(theta) O_H + sin(theta) O_chi.
```

Across that family, the runner holds `Res(C_sp,sp)=1` and the same-source top
readout fixed while varying the canonical-Higgs component and a finite
orthogonal neutral top coupling.  The family is not excluded by source-only
data, taste isotropy, static EW Higgs algebra, one-Higgs monomial selection,
D17/H_unit carrier support, or current neutral-scalar rank gates.

Verification:

```bash
python3 scripts/frontier_yt_osp_oh_identity_stretch_attempt.py
# SUMMARY: PASS=21 FAIL=0
```

## Stuck Fan-Out

The stretch attempt checks five independent frames:

- `v` order-parameter identity: blocked by the gauge-VEV/source-overlap no-go;
- taste-scalar isotropy: exact support, but it does not select the PR230
  source axis;
- one-Higgs gauge selection: selects allowed monomials after canonical `H` is
  supplied, but does not prove source-pole purity;
- neutral-scalar rank-one theorem: not derived on the current surface;
- observable overlap measurement: open, because `C_sH/C_HH` or W/Z response
  rows are absent.

## Next Positive Route

Stop trying source-only or static-Higgs shortcuts.  The next positive route
must add one independent non-source row or theorem:

- source-Higgs `C_sH/C_HH` pole residues with Gram purity;
- same-source W/Z response with sector-overlap identity;
- a dynamical rank-one neutral-scalar theorem excluding `O_chi`.

## Non-Claims

- This note does not claim retained or `proposed_retained` top-Yukawa closure.
- This note does not define `O_H` by fiat.
- This note does not identify `O_sp` with `O_H`.
- This note does not set `kappa_s = 1` or `cos(theta) = 1`.
- This note does not use `H_unit`, `yt_ward_identity`, observed targets,
  `alpha_LM`, plaquette, `u0`, `c2 = 1`, or `Z_match = 1`.
