# PR #230 W/Z Correlator Mass-Fit Path Gate

```yaml
actual_current_surface_status: exact negative boundary / WZ correlator mass-fit path absent on PR230 surface
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_wz_correlator_mass_fit_path_gate.py`  
**Certificate:** `outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json`

## Purpose

The W/Z fallback route can bypass scalar-source normalization only with a real
same-source W/Z mass response.  Static electroweak algebra gives
`M_W = g_2 v / 2` after canonical `H` is already supplied; it is not a measured
`dM_W/ds`.

This gate closes the second W/Z implementation work unit at the current PR230
surface: do we have a W/Z two-point correlator mass-fit path under source
shifts?

## Result

No.  The current QCD/top production harness has a W/Z absent guard and no W/Z
correlator CLI/path.  The gate defines the future mass-fit row contract and
verifies that a positive in-memory witness with per-shift W correlators,
effective-mass plateaus, fit windows, jackknife/bootstrap errors, and
negative/zero/positive source shifts would pass.  It rejects static EW algebra,
aggregate slope-only rows, mismatched source coordinates, and observed-W/Z
selectors.

No W/Z mass-fit rows or response rows are written.

## Validation

```text
python3 scripts/frontier_yt_wz_correlator_mass_fit_path_gate.py
# SUMMARY: PASS=16 FAIL=0
```

## Boundary

This is an exact negative boundary for the current W/Z mass-fit work unit, not
physics closure.  It does not use `H_unit`, `yt_ward_identity`, observed
targets, `alpha_LM`, plaquette, or `u0`, and it does not authorize retained or
`proposed_retained` wording.

Next action: implement a genuine same-source EW action plus W/Z two-point
correlator mass-fit harness, or pivot to source-Higgs `C_sH/C_HH` pole rows,
Schur A/B/C rows, neutral-sector irreducibility, or FH/LSZ production evidence.
