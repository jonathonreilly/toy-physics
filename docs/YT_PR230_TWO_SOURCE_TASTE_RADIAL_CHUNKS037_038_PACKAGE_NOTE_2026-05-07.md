# PR230 Two-Source Taste-Radial Chunks037-038 Package

**Status:** bounded-support / chunks001-038 packaged; no closure

**Checkpoint certificates:**
`outputs/yt_pr230_two_source_taste_radial_chunk037_checkpoint_2026-05-06.json`,
`outputs/yt_pr230_two_source_taste_radial_chunk038_checkpoint_2026-05-06.json`

## Result

Chunks037-038 now pass completed-mode checkpoints and are included in the
two-source taste-radial row package.  The row combiner reports `ready=38/63`
with `combined_rows_written=false`.

Both chunks preserve the production surface:

- fixed seeds `2026056037` and `2026056038`;
- selected-mass-only scalar FH/LSZ and two-source rows at `m=0.75`;
- three-mass top correlator scan preserved;
- `numba_gauge_seed_v1`;
- normal-equation cache metadata present;
- explicit non-readout source-Higgs/taste-radial metadata.

The row-wave launcher then filled the second worker slot without collision:
chunks039-040 are active run-control only and are not counted as evidence.

## Route Diagnostics

The refresh improves finite-row statistics but does not close the scalar or
source-Higgs routes.

- Raw `C_ss` still fails the strict scalar-LSZ first-shell Stieltjes
  nonincrease check: shell-minus-zero is positive with
  `z=151.05795820785409`.
- The Schur split remains bounded support only.  `C_s|x` fails
  (`z=129.56013352763375`), while `C_x|s` survives only the necessary
  first-shell check (`z=-457.34516684060026`).
- The refreshed `C_x|s` one-pole interpolation gives
  `C(0)=0.28083305484735893`,
  `C(0.267949192431123)=0.2695387018970143`,
  `m^2=6.394583011507037`, and `R=1.7958102815965453`; positive two-pole
  endpoint counterfamilies still match the same endpoints, so this is not
  pole-residue authority.
- Complete monotonicity remains unavailable because the packet still has only
  the zero shell and first shell, not a higher-shell or analytic threshold
  certificate.
- The primitive-transfer and orthogonal-top exclusion gates still reject
  finite `C_sx/C_xx` rows as physical transfer or top-coupling tomography.

## Verification

```bash
python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py --chunk-index 37 --output outputs/yt_pr230_two_source_taste_radial_chunk037_checkpoint_2026-05-06.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py --chunk-index 38 --output outputs/yt_pr230_two_source_taste_radial_chunk038_checkpoint_2026-05-06.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_package_audit.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_row_combiner_gate.py
# SUMMARY: PASS=13 FAIL=0, ready=38/63, combined_rows_written=false

python3 scripts/frontier_yt_pr230_strict_scalar_lsz_moment_fv_authority_gate.py
# SUMMARY: PASS=13 FAIL=0

python3 scripts/frontier_yt_pr230_schur_complement_stieltjes_repair_gate.py
# SUMMARY: PASS=22 FAIL=0

python3 scripts/frontier_yt_pr230_schur_complement_complete_monotonicity_gate.py
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_schur_x_given_source_one_pole_scout.py
# SUMMARY: PASS=13 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate.py
# SUMMARY: PASS=13 FAIL=0

python3 scripts/frontier_yt_pr230_orthogonal_top_coupling_exclusion_candidate_gate.py
# SUMMARY: PASS=12 FAIL=0
```

Aggregate gates remain open/support-only after refresh:

```bash
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=93 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=341 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=154 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=308 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=63 FAIL=0
```

## Non-Claim

This package is finite `C_ss/C_sx/C_xx` row support only.  It is not canonical
`O_H`, not canonical `C_sH/C_HH`, not physical `kappa_s`, not strict
scalar-LSZ/FV authority, not W/Z response evidence, and not retained or
`proposed_retained` top-Yukawa closure.
