# PR #230 Non-Chunk Route-Family Import Audit

**Status:** open / non-chunk route-family import audit records Schur
compressed-denominator row-bootstrap no-go
**Runner:** `scripts/frontier_yt_pr230_nonchunk_route_family_import_audit.py`
**Certificate:** `outputs/yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json`

## Claim

The non-chunk route-family exercise compares five live positive families:

- same-surface canonical `O_H` plus source-Higgs `C_sH/C_HH`;
- same-source W/Z response with matched top/W rows, source-coordinate
  transport, non-observed `g_2`, and strict `delta_perp`;
- scalar-LSZ finite-shell/contact/model-class control;
- same-surface Schur `A/B/C` scalar-denominator rows;
- neutral-sector primitive-cone/rank-one irreducibility.

All five retain load-bearing open imports.  The scalar-LSZ/contact-model
shortcut exposed by the finite-shell polefit8x8 certificates was already
closed by the polynomial-contact repair no-go.  After the canonical `O_H`
stretch, W/Z source-coordinate transport, neutral primitive-cone, and
Goldstone-equivalence shortcuts closed negatively, the refreshed cycle-7 audit
selects the Schur family and records the compressed-denominator row-bootstrap
boundary.

2026-05-05 update: the W/Z family now also carries the
source-coordinate transport no-go at
`outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json`.  Static
W-mass algebra is not row authority unless the source-to-Higgs Jacobian is
certified on the same surface.

2026-05-05 cycle-5 update: the selected route is now
`neutral_scalar_rank_one`, and the cycle closes its source-only shortcut at
`outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json`.
Current source/neutral premises do not force a primitive neutral transfer
cone; a same-surface primitive-cone certificate remains required.

2026-05-05 cycle-6 update: the selected route is now
`same_source_wz_response`, and the cycle closes the Goldstone-equivalence
source-identity shortcut at
`outputs/yt_wz_goldstone_equivalence_source_identity_no_go_2026-05-05.json`.
Longitudinal-equivalence bookkeeping can be support after a canonical Higgs
direction is certified, but it does not identify the PR230 source coordinate.

2026-05-05 cycle-7 update: the selected route is now
`schur_scalar_denominator_rows`, and the cycle closes the shortcut at
`outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json`.
The compressed scalar denominator and its pole derivative do not reconstruct
the same-surface Schur `A/B/C` rows; genuine kernel rows remain required.

## Boundary

This audit does not authorize retained or proposed-retained PR230 closure.  It
does not package or rerun chunk MC, define a bare top-Yukawa readout, or use
prohibited operator/readout, target-value, coupling-normalization, or unit
shortcuts.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_nonchunk_route_family_import_audit.py
python3 scripts/frontier_yt_pr230_nonchunk_route_family_import_audit.py
# SUMMARY: PASS=9 FAIL=0
```
