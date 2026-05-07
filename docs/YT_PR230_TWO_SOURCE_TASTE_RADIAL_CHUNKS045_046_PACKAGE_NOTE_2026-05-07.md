# PR230 Two-Source Taste-Radial Chunks045-046 Package

**Status:** bounded-support / chunks001-046 packaged; no closure

**Checkpoint certificates:**
`outputs/yt_pr230_two_source_taste_radial_chunk045_checkpoint_2026-05-06.json`,
`outputs/yt_pr230_two_source_taste_radial_chunk046_checkpoint_2026-05-06.json`

## Result

Chunks045-046 now pass completed-mode checkpoints and are included in the
two-source taste-radial row package.  The row combiner reports `ready=46/63`
with `combined_rows_written=false`.

Both chunks preserve the production surface:

- fixed seeds `2026056045` and `2026056046`;
- selected-mass-only scalar FH/LSZ and two-source rows at `m=0.75`;
- three-mass top correlator scan preserved;
- `numba_gauge_seed_v1`;
- normal-equation cache metadata present;
- explicit non-readout source-Higgs/taste-radial metadata.

Chunks047-048 are active under the row-wave supervisor's two-worker cap.
They are run-control state only and are not counted as evidence.

## Route Diagnostics

The refresh improves finite-row statistics but does not close the scalar or
source-Higgs routes.

- Raw `C_ss` still fails the strict scalar-LSZ first-shell Stieltjes
  nonincrease check: shell-minus-zero is positive with
  `z=170.33620497910093`.
- The Schur split remains bounded support only.  `C_s|x` fails
  (`z=155.053312483403`), while `C_x|s` survives only the necessary
  first-shell check (`z=-513.0902824488198` in the repair gate).
- The refreshed `C_x|s` one-pole interpolation gives
  `C(0)=0.28083041491298866`,
  `C(0.267949192431123)=0.26953424344658744`,
  `m^2=6.393447822464358`, and `R=1.7954746047072094`; positive two-pole
  endpoint counterfamilies still match the same endpoints, so this is not
  pole-residue authority.
- Complete monotonicity remains unavailable because the packet still has only
  the zero shell and first shell, not a higher-shell or analytic threshold
  certificate.
- The primitive-transfer and orthogonal-top exclusion gates still reject
  finite `C_sx/C_xx` rows as physical transfer or top-coupling tomography.

## Verification

```bash
python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py --chunk-index 45 --output outputs/yt_pr230_two_source_taste_radial_chunk045_checkpoint_2026-05-06.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_checkpoint.py --chunk-index 46 --output outputs/yt_pr230_two_source_taste_radial_chunk046_checkpoint_2026-05-06.json
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_chunk_package_audit.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_row_combiner_gate.py
# SUMMARY: PASS=13 FAIL=0, ready=46/63, combined_rows_written=false

python3 scripts/frontier_yt_pr230_strict_scalar_lsz_moment_fv_authority_gate.py
# SUMMARY: PASS=13 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_schur_subblock_witness.py
# SUMMARY: PASS=16 FAIL=0, ready=46/63

python3 scripts/frontier_yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout.py
# SUMMARY: PASS=14 FAIL=0, ready=46/63

python3 scripts/frontier_yt_pr230_two_source_taste_radial_schur_abc_finite_rows.py
# SUMMARY: PASS=17 FAIL=0, ready=46/63

python3 scripts/frontier_yt_pr230_two_source_taste_radial_schur_pole_lift_gate.py
# SUMMARY: PASS=13 FAIL=0, ready=46/63

python3 scripts/frontier_yt_pr230_schur_complement_stieltjes_repair_gate.py
# SUMMARY: PASS=22 FAIL=0

python3 scripts/frontier_yt_pr230_schur_complement_complete_monotonicity_gate.py
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_schur_x_given_source_one_pole_scout.py
# SUMMARY: PASS=13 FAIL=0

python3 scripts/frontier_yt_source_higgs_production_readiness_gate.py
# SUMMARY: PASS=25 FAIL=0

python3 scripts/frontier_yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate.py
# SUMMARY: PASS=13 FAIL=0

python3 scripts/frontier_yt_pr230_orthogonal_top_coupling_exclusion_candidate_gate.py
# SUMMARY: PASS=12 FAIL=0
```

Aggregate gates remain open/support-only after refresh:

```bash
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=97 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=352 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=158 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=312 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=67 FAIL=0
```

## Non-Claim

This package is finite `C_ss/C_sx/C_xx` row support only.  It is not canonical
`O_H`, not canonical `C_sH/C_HH`, not physical `kappa_s`, not strict
scalar-LSZ/FV authority, not W/Z response evidence, and not retained or
`proposed_retained` top-Yukawa closure.
