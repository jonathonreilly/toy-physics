# PR #230 Source-Higgs Time-Kernel Harness Extension

Date: 2026-05-07

Status: support-only infrastructure; open physics closure.

This block adds a default-off `source_higgs_time_kernel_analysis` path to
`scripts/yt_direct_lattice_correlator_production.py`.  The path keeps the
three-mass top correlator scan, but emits same-surface scalar Euclidean-time
matrix rows only at the selected FH/LSZ mass parameter, currently the middle
mass `0.75`.

The emitted rows are

- `C_ss(t)`,
- `C_sH(t)`,
- `C_Hs(t)`,
- `C_HH(t)`,

with taste-radial aliases `C_sx(t)`, `C_xs(t)`, and `C_xx(t)` when the supplied
operator certificate is the current taste-radial second-source certificate.
Each mode row carries `tau_rows` and `C_matrix_by_t` so a later OS/GEVP
postprocessor can consume an actual time-lag matrix instead of an equal-time
configuration covariance row.

## Engineering Change

The new CLI controls are:

```text
--source-higgs-time-kernel-modes
--source-higgs-time-kernel-noises
--source-higgs-time-kernel-max-tau
--source-higgs-time-kernel-origin-count
```

The path is disabled unless modes, positive noise count, and a
`--source-higgs-operator-certificate` are all present.  It reuses the existing
normal-equation cache for the selected mass on each configuration, preserving
the `D^\dagger D` reuse pattern and CG residual reporting.

## Validation

Smoke artifact:

```text
outputs/yt_pr230_source_higgs_time_kernel_harness_smoke_numba_2026-05-07.json
```

Gate:

```text
python3 scripts/frontier_yt_pr230_source_higgs_time_kernel_harness_extension_gate.py
```

Gate certificate:

```text
outputs/yt_pr230_source_higgs_time_kernel_harness_extension_gate_2026-05-07.json
```

The gate checks that the numba smoke retains
`rng_seed_control.seed_control_version = numba_gauge_seed_v1`, preserves the
three-mass scan, marks the time-kernel measurement as selected-mass-only, emits
`source_higgs_time_kernel_v1` rows with `C_matrix_by_t`, and keeps
`used_as_physical_yukawa_readout = false`.

Regression checks:

```text
python3 scripts/frontier_yt_fh_lsz_target_timeseries_harness_certificate.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_fh_lsz_multitau_target_timeseries_harness_certificate.py
# SUMMARY: PASS=14 FAIL=0
```

## Claim Boundary

This is not a retained or proposed-retained physics closure.  The current
operator certificate is taste-radial and explicitly has
`canonical_higgs_operator_identity_passed = false`.  These rows therefore do
not derive `kappa_s`, do not identify a canonical Higgs operator, and do not
authorize a physical `y_t` readout.

The next clean closure-relevant artifact is a production same-surface
time-kernel dataset paired with either a certified canonical `O_H` identity or
a physical neutral-transfer/W/Z response identity, followed by OS/GEVP pole
extraction, finite-volume/IR/threshold control, and source-overlap
normalization.
