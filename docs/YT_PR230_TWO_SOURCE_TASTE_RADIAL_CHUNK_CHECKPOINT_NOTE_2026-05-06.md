# PR230 Two-Source Taste-Radial Chunk Checkpoint Note

**Status:** bounded support / row-chunk schema checkpoint infrastructure.

## Purpose

`scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py`
audits one completed L12_T24 taste-radial `C_sx/C_xx` row chunk.  It is the
per-chunk gate to run as soon as a row worker writes its JSON.

The runner can also be called with `--allow-pending-active` for a still-running
chunk.  Pending mode is deliberately weaker: it records only active process
state and the absence of completed row JSON.  It is not evidence.

## Completed-Chunk Checks

For a completed chunk, the runner checks:

- production JSON and per-volume artifact are present;
- the per-volume artifact matches the certificate ensemble;
- production metadata uses `12x24`, seed `2026056000 + chunk`, 1000
  thermalization sweeps, 16 measurements, separation 20, and `numba`;
- `rng_seed_control.seed_control_version` is `numba_gauge_seed_v1`;
- the three-mass scan `[0.45, 0.75, 1.05]` is preserved;
- scalar FH/LSZ/source-Higgs analysis is selected-mass-only at `0.75`;
- source response has per-configuration slopes/effective energies;
- scalar LSZ rows carry `C_ss_timeseries` for the four production modes;
- taste-radial source rows carry `C_sx_timeseries` and `C_xx_timeseries`
  for the four production modes while preserving legacy `C_sH/C_HH` fields;
- source-Higgs metadata and action-certificate firewalls remain clean;
- the manifest row matches the chunk seed and output path;
- proposal firewalls remain off.

## Claim Boundary

A passing completed chunk is still only partial row support.  It is not
combined L12 evidence, not pole-residue evidence, not canonical `O_H`, not
`kappa_s`, and not retained or proposed-retained `y_t` closure.

Pending mode is even weaker: active workers, logs, empty directories, and
partial directories are run-control state only.

## Validation

```bash
python3 -m py_compile \
  scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py

python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py \
  --chunk-index 1 \
  --allow-pending-active \
  --output outputs/yt_pr230_two_source_taste_radial_chunk001_pending_checkpoint_2026-05-06.json

python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py \
  --chunk-index 1 \
  --output outputs/yt_pr230_two_source_taste_radial_chunk001_checkpoint_2026-05-06.json

python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py \
  --chunk-index 2 \
  --output outputs/yt_pr230_two_source_taste_radial_chunk002_checkpoint_2026-05-06.json
```

Expected pending summary while chunk001 is active and not yet complete:
`PASS=2 FAIL=0`.

Completed chunk001 and chunk002 now pass completed mode with `PASS=15 FAIL=0`
each.  The runner accepts the explicit metadata non-readout firewall for older
completed artifacts and the production harness now also writes the same
`used_as_physical_yukawa_readout: false` flag directly under future scalar
source-response and scalar-LSZ analysis objects.
