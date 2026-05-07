# PR #230 Source-Higgs Time-Kernel GEVP Contract

Date: 2026-05-07

Status: bounded-support / source-Higgs time-kernel GEVP contract; smoke rows
are not physics closure.

This block adds the first postprocessor contract for the new
`source_higgs_time_kernel_analysis` rows.  The runner consumes the numba smoke
artifact and verifies that the zero-mode `C_ij(t)` rows can be parsed into a
formal two-operator GEVP diagnostic using `C(1)` against `C(0)`.

## What It Checks

The gate reads:

```text
outputs/yt_pr230_source_higgs_time_kernel_harness_smoke_numba_2026-05-07.json
```

It checks:

- `source_higgs_time_kernel_v1` is present,
- `C_matrix_by_t` contains finite zero-mode `C_ij(0)` and `C_ij(1)` rows,
- `rng_seed_control.seed_control_version = numba_gauge_seed_v1`,
- a formal 2x2 GEVP diagnostic can be computed,
- the smoke remains support-only,
- the taste-radial `x` row is not relabeled as canonical `O_H`,
- the formal GEVP is not treated as pole, `kappa_s`, or `y_t` authority.

Runner:

```text
python3 scripts/frontier_yt_pr230_source_higgs_time_kernel_gevp_contract.py
# SUMMARY: PASS=12 FAIL=0
```

Certificate:

```text
outputs/yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json
```

## Claim Boundary

The current diagnostic is reduced smoke with one configuration, two time lags,
and the taste-radial second-source certificate.  It has
`canonical_higgs_operator_identity_passed = false`, no production statistics,
no reflection-positive canonical operator identity, no pole plateau, no
FV/IR/threshold authority, and no source-overlap normalization.

It is therefore not a physical pole extraction and not a top-Yukawa closure.

The production-grade route remains:

1. Supply a certified canonical `O_H` or physical neutral/W/Z identity.
2. Run production same-surface `C_ss(t)/C_sH(t)/C_HH(t)` rows, or authorized
   `C_ss(t)/C_sx(t)/C_xx(t)` rows if `x` is certified physical.
3. Apply OS/GEVP pole extraction with multitime, multiconfiguration,
   FV/IR/threshold, covariance, and source-overlap normalization authority.
4. Pass the retained-route and campaign closure gates before any retained or
   proposed-retained wording.
