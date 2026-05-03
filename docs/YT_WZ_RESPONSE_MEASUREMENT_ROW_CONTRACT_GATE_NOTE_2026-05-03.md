# PR #230 W/Z Response Measurement-Row Contract Gate

**Status:** bounded-support / WZ response measurement-row contract gate  
**Runner:** `scripts/frontier_yt_wz_response_measurement_row_contract_gate.py`  
**Certificate:** `outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json`

## Purpose

The same-source W/Z physical-response route can bypass `kappa_s` only if the
repo supplies actual W/Z mass-response rows under the same scalar source used
for the top FH slope.  This block makes the future row contract executable
before any such rows exist.

The contract requires production source-shift rows with:

- negative, zero, and positive scalar-source shifts
- per-shift top energy fits from top correlators
- per-shift W or Z mass fits from W/Z correlators
- fitted `dE_top/ds` and `dM_W/ds` or `dM_Z/ds`
- covariance between the top and W/Z slopes
- retained `g2` provenance
- sector-overlap, canonical-Higgs identity, and retained-route gate
  certificates
- explicit false firewall flags for observed W/Z, observed top/y_t, observed
  `g2`, static-VEV selectors, `H_unit`, Ward authority, `alpha_LM`,
  plaquette/u0, `c2=1`, and `Z_match=1`

## Result

The positive in-memory witness passes the row contract.  The gate rejects
static EW algebra, aggregate slope-only rows without source-shift correlator
fits and identity certificates, and rows that use observed W/Z or observed
`g2` selectors.

The current measurement-row file
`outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json` is absent,
so the current W/Z measurement-row gate is not passed.  This is intentional:
the artifact is a schema/firewall gate only, not production evidence.

## Verification

```bash
python3 scripts/frontier_yt_wz_response_measurement_row_contract_gate.py
# SUMMARY: PASS=10 FAIL=0
```

## Claim Boundary

This block does not create W/Z data, infer `dM_W/ds`, set `kappa_s`,
`k_top/k_gauge`, `c2`, or `Z_match` to one, or authorize retained or
`proposed_retained` wording.  PR #230 still needs production same-source W/Z
measurement rows satisfying this contract, followed by the W/Z builder,
same-source W/Z gate, retained-route gate, and campaign status gate.
