# PR #230 FH/LSZ Selected-Mass Normal-Cache Speedup

**Status:** bounded-support / FH-LSZ performance infrastructure support  
**Runner:** `scripts/frontier_yt_fh_lsz_selected_mass_normal_cache_speedup_certificate.py`  
**Certificate:** `outputs/yt_fh_lsz_selected_mass_normal_cache_speedup_certificate_2026-05-03.json`

## Optimization

The production harness still performs the three-mass top-correlator scan, but
scalar source-response and same-source scalar two-point LSZ target
measurements are now intentionally computed only at the selected middle mass
parameter, currently `0.75` for the PR #230 replacement chunks.  Non-selected
masses keep their top correlators and mass-fit rows, but they no longer pay
for scalar source shifts or stochastic scalar two-point solves.

The harness also caches the normal-equation system per saved gauge
configuration and mass/source-shift value.  For each needed value it builds
`D`, `D^dagger`, and `D^dagger D` once, then reuses that normal operator for
point-source and stochastic RHS solves while preserving CG info and residual
reporting.

The output schema adds explicit metadata:

- `fh_lsz_measurement_policy.policy = selected_mass_only_for_scalar_fh_lsz`
- `metadata.run_control.fh_lsz_selected_mass_only = true`
- `metadata.run_control.normal_equation_cache_enabled = true`
- non-selected masses skipped for scalar FH/LSZ are listed
- physical-Higgs normalization remains `not_derived`
- `used_as_physical_yukawa_readout` remains false

## Speedup Model

For the replacement-chunk schema with three masses, three scalar source shifts
`[-0.01, 0, +0.01]`, four scalar two-point modes, and sixteen noise vectors,
the old per-configuration model was:

```text
base scan solves:              9
source-shift solves:          18
scalar two-point solves:     384
total RHS solves:            411
normal-equation builds:      411
```

The optimized model is:

```text
base scan solves:              9
selected source-shift solves:  6
selected scalar two-point:   128
total RHS solves:            143
normal-equation builds:        5
```

This gives an estimated `2.87x` RHS-solve reduction and `82.2x`
normal-build reduction for the scalar FH/LSZ replacement workload.  The
certificate is a performance model plus source/metadata audit, not production
physics evidence.

## Validation

```text
python3 scripts/frontier_yt_fh_lsz_selected_mass_normal_cache_speedup_certificate.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_fh_lsz_target_timeseries_harness_certificate.py
# SUMMARY: PASS=12 FAIL=0
```

The optimized smoke artifact preserves the target schema required by the
replacement campaign:

```text
scalar_source_response_analysis.per_configuration_effective_energies: present
scalar_source_response_analysis.per_configuration_slopes: present
scalar_two_point_lsz_analysis.mode_rows[*].C_ss_timeseries: present
rng_seed_control.seed_control_version: numba_gauge_seed_v1
```

The replacement queue runner now emits full fixed-seed rerun commands without
`--resume`; prior ready chunks can predate target-timeseries serialization, so
the queued replacements must rebuild their chunk artifacts rather than append
to old targetless outputs.

After the optimization landed, chunks005-010 were rerun with the optimized
selected-mass-only/normal-cache harness at concurrency 3, with no `--resume`
and distinct production output directories. Chunk004 had already completed as
a pre-optimization replacement and was not rerun. Generic target-timeseries
checkpoints for chunks004-010 now pass (`PASS=14 FAIL=0` each), and the
current replacement queue is empty for ready chunks001-012.

## Claim Boundary

This optimization does not certify target ESS, response stability, full
L12/L16/L24 production, scalar-pole derivative/model-class/FV/IR control, or
canonical-Higgs identity.  It does not derive or set `kappa_s`, and it
authorizes no retained or `proposed_retained` wording.  Source-only FH/LSZ
target time series remain instrumentation until a same-surface
canonical-Higgs/source-overlap or W/Z response route closes.
