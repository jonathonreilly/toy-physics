# PR #230 Non-Chunk Route-Family Import Audit

**Status:** open / non-chunk route-family import audit selects
scalar-LSZ polynomial-contact no-go block
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

All five retain load-bearing open imports.  The only family with a current
non-chunk executable route is scalar-LSZ/contact-model control, because the
current finite-shell polefit8x8 certificates already expose a concrete
contact-repair shortcut to test.  The selected block is therefore the
polynomial-contact repair no-go.

2026-05-05 update: the W/Z family now also carries the
source-coordinate transport no-go at
`outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json`.  Static
W-mass algebra is not row authority unless the source-to-Higgs Jacobian is
certified on the same surface.

## Boundary

This audit does not authorize retained or proposed-retained PR230 closure.  It
does not package or rerun chunk MC, define `y_t_bare`, or use `H_unit`, Ward
authority, `alpha_LM`, plaquette/u0, observed targets, bare-coupling algebra,
or unit shortcuts.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_nonchunk_route_family_import_audit.py
python3 scripts/frontier_yt_pr230_nonchunk_route_family_import_audit.py
# SUMMARY: PASS=9 FAIL=0
```
