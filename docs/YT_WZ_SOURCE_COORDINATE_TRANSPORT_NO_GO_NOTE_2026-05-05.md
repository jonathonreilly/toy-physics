# PR #230 W/Z Source-Coordinate Transport No-Go

```yaml
actual_current_surface_status: exact negative boundary / WZ source-coordinate transport shortcut rejected
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_wz_source_coordinate_transport_no_go.py`
**Certificate:** `outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json`

## Purpose

This block tests the remaining W/Z derivation shortcut after the same-source
EW action and W/Z mass-fit path gates: can static electroweak mass algebra act
as W/Z row authority if the PR230 scalar source is simply transported to the
canonical Higgs radial coordinate?

It cannot.  Static `dM_W/dh = g_2/2` is not a same-source `dM_W/ds` row until
the source-to-Higgs Jacobian `dh/ds` is certified on the same surface.

## Counterfamily

The runner constructs a non-data algebraic family with:

- fixed top source response;
- fixed static electroweak W-mass dictionary;
- fixed same-source label;
- varying source-to-Higgs Jacobian;
- compensating orthogonal neutral top coupling.

Across that family the transported W source response and top/W response ratio
change.  Therefore static electroweak algebra plus the PR230 top response does
not determine W/Z response rows.

## Validation

```text
python3 scripts/frontier_yt_wz_source_coordinate_transport_no_go.py
# SUMMARY: PASS=20 FAIL=0
```

## Boundary

This is an exact negative boundary for the current W/Z shortcut.  It writes no
W/Z measurement rows, does not define a same-source EW action, does not set the
source-to-Higgs Jacobian by convention, and does not authorize a closure
proposal.

Next action: supply a real same-source EW action and source-transport
certificate, then W/Z correlator mass-fit rows; otherwise pursue measured
matched top/W rows, source-Higgs rows after canonical-Higgs identity, Schur
rows, or neutral-sector irreducibility.
