# PR #230 Source-Higgs Time-Kernel Production Manifest

Date: 2026-05-07

Status: bounded-support / source-Higgs time-kernel production manifest; no
physics closure.

Runner:
`scripts/frontier_yt_pr230_source_higgs_time_kernel_production_manifest.py`

Certificate:
`outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json`

## Purpose

The source-Higgs time-kernel harness and GEVP contract make same-surface
`C_ss(t)/C_sH(t)/C_HH(t)` rows executable once a canonical `O_H` or equivalent
physical neutral identity exists.  This block turns that route into an exact
future production manifest without launching jobs or counting rows as physics
evidence.

The manifest defines `63` non-colliding `L=12, T=24` chunk commands under:

```text
outputs/yt_pr230_source_higgs_time_kernel_rows/
outputs/yt_direct_lattice_correlator_production_source_higgs_time_kernel_rows/
```

The commands keep the current production settings:

```text
--masses 0.45,0.75,1.05
--therm 1000
--measurements 16
--separation 20
--scalar-source-shifts=-0.01,0.0,0.01
--scalar-two-point-modes 0,0,0;1,0,0;0,1,0;0,0,1
--source-higgs-cross-modes 0,0,0;1,0,0;0,1,0;0,0,1
--source-higgs-time-kernel-modes 0,0,0;1,0,0;0,1,0;0,0,1
--source-higgs-time-kernel-noises 16
--source-higgs-time-kernel-max-tau 4
--source-higgs-time-kernel-origin-count 4
```

Seeds are fixed at `2026058001..2026058063`.  The manifest emits commands
without `--resume`, so later replacement rows cannot silently reuse stale
artifacts.

## Current Boundary

The manifest is not a row packet, pole extraction, or source-overlap
normalization.  It records launch blockers:

- the current operator certificate is taste-radial support, not canonical
  `O_H`;
- no physical neutral/WZ identity currently substitutes for canonical `O_H`;
- active static taste-radial workers may own the two-worker cap;
- no production time-kernel rows, FV/IR/threshold authority, covariance gate,
  or overlap normalization exists.

The artifact explicitly keeps:

- `proposal_allowed = false`,
- `closure_launch_authorized_now = false`,
- `support_launch_authorized_now = false`,
- `operator_certificate_is_canonical_oh = false`.

It does not set `kappa_s`, `c2`, or `Z_match` to one and does not use
`H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`, plaquette/u0, or
value recognition as proof authority.

## Validation

```bash
python3 scripts/frontier_yt_pr230_source_higgs_time_kernel_production_manifest.py
# SUMMARY: PASS=16 FAIL=0
```

The manifest is infrastructure support only.  PR #230 remains open/draft with
no retained or proposed-retained top-Yukawa closure.
