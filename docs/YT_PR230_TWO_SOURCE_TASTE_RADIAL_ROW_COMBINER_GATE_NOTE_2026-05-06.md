# PR230 Two-Source Taste-Radial Row Combiner Gate

**Status:** bounded support / partial `C_sx/C_xx` row combiner gate.

**Runner:** `scripts/frontier_yt_pr230_two_source_taste_radial_row_combiner_gate.py`

**Certificate:** `outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json`

## Purpose

The two-source taste-radial manifest defines 63 L12_T24 production chunks for
the second-source `C_sx/C_xx` route.  This gate is the acceptance boundary
between completed chunk JSON and the future combined measurement-row file:

```text
outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json
```

It audits completed chunks for production metadata, `numba_gauge_seed_v1`
seed control, selected-mass-only source/FH/LSZ policy, and `C_sx/C_xx`
timeseries.  It deliberately refuses to write the combined measurement-row
file until all 63 manifest chunks are present and schema-clean.

## Current Result

Chunks001-004 are present and schema-clean.  The set is still partial:
`ready=4/63`, so no combined row packet is written.

Chunks005-006 are active under the row-wave supervisor's two-worker cap.  Live
status and logs are run-control state only.

## Claim Boundary

Partial chunks and this combiner certificate are support only.  They are not
combined L12 pole evidence, not canonical `O_H`, not scalar LSZ normalization,
not `kappa_s`, and not retained or proposed-retained `y_t` closure.

Even a future complete `C_sx/C_xx` row packet remains a second-source
taste-radial packet until canonical `O_H`/source-overlap authority or a
genuine physical-response bridge closes, with pole/FV/IR controls.

## Verification

```bash
python3 -m py_compile \
  scripts/frontier_yt_pr230_two_source_taste_radial_row_combiner_gate.py

python3 scripts/frontier_yt_pr230_two_source_taste_radial_row_combiner_gate.py
# SUMMARY: PASS=12 FAIL=0
```
