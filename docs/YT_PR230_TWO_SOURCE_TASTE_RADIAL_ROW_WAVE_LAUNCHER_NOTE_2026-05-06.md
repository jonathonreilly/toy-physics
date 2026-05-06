# PR230 Two-Source Taste-Radial Row Wave Launcher Note

**Status:** bounded support / run-control infrastructure only.

## Purpose

`scripts/frontier_yt_pr230_two_source_taste_radial_row_wave_launcher.py`
turns the no-resume row-production manifest into a guarded bounded-wave
launcher.  It exists to keep the `C_sx/C_xx` replacement row campaign from
colliding with active jobs or overwriting completed outputs.

The launcher does not create physics evidence by itself.  A manifest row,
active process, log file, empty production directory, partial production
directory, or launcher certificate is not a measured `C_sx/C_xx` row.

## Guardrails

The runner checks:

- the manifest exists and is support-only;
- the manifest forbids `--resume`;
- the expected 63 chunk commands are present;
- launch commands are production-targeted no-resume row commands;
- no duplicate active chunk workers or unknown row workers are present;
- stale partial output directories block new launches;
- completed chunk outputs are excluded from launch;
- the local concurrency cap is positive and at most three workers;
- no launch occurs unless `--launch` is passed.

The default cap is two workers on this machine.  That is intentionally below
the manifest recommendation of at most three because the active row workers
use near-full CPU.  Future runs may pass `--max-concurrent 3` if resources
allow.

## Claim Boundary

The launcher preserves the PR #230 claim firewall:

- no retained or proposed-retained `y_t` closure;
- no conversion of `C_sx/C_xx` into canonical-Higgs `C_sH/C_HH`;
- no `kappa_s = 1`, `c2 = 1`, or `Z_match = 1`;
- no use of `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`,
  plaquette, or `u0`;
- no use of reduced, partial, or active jobs as production evidence.

The exact next evidence step is completed chunk JSON, followed by row schema
gates, combined pole/FV/IR diagnostics, and a separate canonical-source or
physical-response authority certificate.

## Validation

```bash
python3 -m py_compile \
  scripts/frontier_yt_pr230_two_source_taste_radial_row_wave_launcher.py

python3 scripts/frontier_yt_pr230_two_source_taste_radial_row_wave_launcher.py \
  --max-concurrent 2 \
  --output outputs/yt_pr230_two_source_taste_radial_row_wave_launcher_2026-05-06.json
```

Expected summary: `PASS=12 FAIL=0`.
