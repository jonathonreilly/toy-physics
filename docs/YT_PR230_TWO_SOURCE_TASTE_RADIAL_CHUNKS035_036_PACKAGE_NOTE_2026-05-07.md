# PR230 Two-Source Taste-Radial Chunks035-036 Package

**Status:** bounded-support / chunks001-036 packaged; no closure

**Checkpoint certificates:**
`outputs/yt_pr230_two_source_taste_radial_chunk035_checkpoint_2026-05-06.json`,
`outputs/yt_pr230_two_source_taste_radial_chunk036_checkpoint_2026-05-06.json`

## Result

Chunks035-036 now pass completed-mode checkpoints and are included in the
two-source taste-radial row package.  The row combiner reports `ready=36/63`
with `combined_rows_written=false`.

Both chunks preserve the production surface:

- fixed seeds `2026056035` and `2026056036`;
- selected-mass-only scalar FH/LSZ at `m=0.75`;
- three-mass top correlator scan preserved;
- `numba_gauge_seed_v1`;
- normal-equation cache metadata present;
- explicit non-readout source-Higgs/taste-radial metadata.

## Route Diagnostics

The refresh does not close the scalar or source-Higgs routes.

- Raw `C_ss` still fails the strict scalar-LSZ first-shell Stieltjes
  nonincrease check: shell-minus-zero is positive with
  `z=143.92652720800947`.
- The Schur split remains bounded support only.  `C_s|x` fails
  (`z=134.33514802069274`), while `C_x|s` survives only the necessary
  first-shell check (`z=-494.595619807674`).
- Complete monotonicity remains unavailable because the packet still has only
  the zero shell and first shell, not a higher-shell or analytic threshold
  certificate.
- The primitive-transfer and orthogonal-top exclusion gates still reject
  finite `C_sx/C_xx` rows as physical transfer or top-coupling tomography.

## Run-Control Boundary

Chunk037 is active under the row-wave supervisor.  Its logs, live status,
partial directories, active process, and pending checkpoint are run-control
only and are not counted as evidence in this checkpoint.

## Verification

```bash
python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py --chunk-index 35 --output outputs/yt_pr230_two_source_taste_radial_chunk035_checkpoint_2026-05-06.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py --chunk-index 36 --output outputs/yt_pr230_two_source_taste_radial_chunk036_checkpoint_2026-05-06.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_package_audit.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_row_combiner_gate.py
# SUMMARY: PASS=13 FAIL=0, ready=36/63, combined_rows_written=false
```

Aggregate gates remain open/support-only after refresh:

```bash
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=92 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=339 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=152 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=306 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=61 FAIL=0
```

## Non-Claim

This package is finite `C_ss/C_sx/C_xx` row support only.  It is not canonical
`O_H`, not canonical `C_sH/C_HH`, not physical `kappa_s`, not strict
scalar-LSZ/FV authority, not W/Z response evidence, and not retained or
`proposed_retained` top-Yukawa closure.
