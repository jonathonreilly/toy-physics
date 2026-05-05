# PR230 W/Z Harness Smoke-Schema Gate Note

**Status:** bounded support / W/Z harness smoke schema path.

This block adds a default-off W/Z mass-response smoke path to
`scripts/yt_direct_lattice_correlator_production.py` and certifies it with
`scripts/frontier_yt_pr230_wz_harness_smoke_schema_gate.py`.

The smoke path is deliberately not a physics readout.  It emits synthetic
positive W or Z correlators only when `--wz-mass-response-smoke` and
`--wz-source-shifts` are passed.  It preserves the production harness schema,
the selected-mass-only scalar FH/LSZ policy, numba seed control, scalar target
time series, and LSZ `C_ss_timeseries` rows while adding contract-shaped W/Z
mass-fit rows for downstream schema validation.

## Certified Surface

The gate runs a tiny numba smoke command with:

```bash
python3 scripts/yt_direct_lattice_correlator_production.py \
  --volumes 2x4 \
  --masses 0.45,0.75,1.05 \
  --therm 0 \
  --measurements 2 \
  --separation 0 \
  --overrelax 0 \
  --engine numba \
  --production-targets \
  --scalar-source-shifts=-0.01,0.0,0.01 \
  --scalar-two-point-modes "0,0,0;1,0,0;0,1,0;0,0,1" \
  --scalar-two-point-noises 2 \
  --wz-mass-response-smoke \
  --wz-source-shifts=-0.01,0.0,0.01 \
  --wz-boson-channel W \
  --production-output-dir outputs/yt_pr230_wz_harness_smoke_schema_tmp \
  --seed 2026050501 \
  --output outputs/yt_pr230_wz_harness_smoke_schema_smoke_2026-05-05.json
```

The certificate checks:

- `metadata.wz_mass_response.enabled == true`;
- `implementation_status == smoke_schema_enabled_not_ew_production`;
- `production_wz_rows_written == false`;
- `rng_seed_control.seed_control_version == numba_gauge_seed_v1`;
- scalar FH `per_configuration_effective_energies` and
  `per_configuration_slopes` are still present;
- LSZ mode rows still carry `C_ss_timeseries`;
- W/Z rows cover negative, zero, and positive source shifts;
- W/Z mass fits are marked `from_correlator == true` but
  `correlator_source == synthetic_scout_contract_not_EW_field`;
- electroweak coupling, same-source identity, canonical-Higgs identity, and
  retained-route certificates remain absent/false;
- all firewall flags remain false.

## Claim Boundary

The smoke path is infrastructure only.  It does not define a same-source EW
action, does not measure production W/Z correlators, does not provide
top/W-Z covariance, does not certify the source-coordinate identity, and does
not derive the canonical-Higgs/source overlap.

Therefore it cannot be used as retained or proposed-retained top-Yukawa
closure evidence.  The exact next physics action remains a genuine same-source
EW action plus production W/Z correlator mass-fit rows, or an independent
canonical-Higgs/source-overlap closure route.

## Verification

```bash
python3 -m py_compile \
  scripts/yt_direct_lattice_correlator_production.py \
  scripts/frontier_yt_pr230_wz_harness_smoke_schema_gate.py

python3 scripts/frontier_yt_pr230_wz_harness_smoke_schema_gate.py
# SUMMARY: PASS=22 FAIL=0
```

Certificate:

- `outputs/yt_pr230_wz_harness_smoke_schema_gate_2026-05-05.json`
