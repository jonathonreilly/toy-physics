# PR #230 Top Mass-Scan Response Harness Gate

**Status:** bounded-support / infrastructure only

**Runner:** `scripts/frontier_yt_pr230_top_mass_scan_response_harness_gate.py`

**Certificate:** `outputs/yt_pr230_top_mass_scan_response_harness_gate_2026-05-12.json`

## What Landed

The production harness now serializes
`top_mass_scan_response_analysis` for each ensemble.  The field is built from
the existing three-mass top correlator scan, so it adds no new solves:

- `row_schema_version = top_mass_scan_response_v1`
- per-configuration tau=1 effective energies by bare mass
- per-configuration endpoint slopes `dE/dm_bare` around the selected middle mass
- multi-tau effective-energy and slope rows for future covariance/window gates
- explicit `used_as_physical_yukawa_readout = false`
- explicit `physical_higgs_normalization = not_derived`

The existing selected-mass FH/LSZ optimization is preserved: scalar
source-response, scalar two-point LSZ, and source-Higgs cross rows remain
selected-mass-only, while the ordinary three-mass top scan is still computed.

## Smoke Validation

Command:

```bash
python3 scripts/yt_direct_lattice_correlator_production.py \
  --volumes 2x4 \
  --masses 0.45,0.75,1.05 \
  --therm 1 \
  --measurements 2 \
  --separation 1 \
  --engine numba \
  --scalar-source-shifts=-0.01,0.0,0.01 \
  --scalar-two-point-modes 0,0,0 \
  --scalar-two-point-noises 1 \
  --production-output-dir outputs/yt_pr230_top_mass_scan_response_harness_smoke_tmp \
  --output outputs/yt_pr230_top_mass_scan_response_harness_smoke_2026-05-12.json
```

Gate result:

```bash
python3 scripts/frontier_yt_pr230_top_mass_scan_response_harness_gate.py
# SUMMARY: PASS=14 FAIL=0
```

The gate verifies:

- `rng_seed_control.seed_control_version = numba_gauge_seed_v1`
- the three mass scan remains `[0.45, 0.75, 1.05]`
- `top_mass_scan_response_analysis` has per-configuration effective energies
  and slopes
- scalar source-response per-configuration rows still exist
- scalar two-point `C_ss_timeseries` rows still exist
- metadata says the rows are support only and not a physical readout

## Claim Boundary

These rows are `dE/dm_bare` support rows, not `dE/dh`.  They do not derive
`kappa_s`, canonical `O_H`, W/Z response identity, strict `g2`, matched W/Z
covariance, scalar LSZ residue, or top-Yukawa closure.

No retained or `proposed_retained` PR #230 closure is claimed.
