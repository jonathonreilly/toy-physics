# PR230 Additive-Top Jacobian Row Builder

**Status:** bounded support / additive-top row artifact; closure not authorized.

## Result

This block adds a concrete additive-top Jacobian row artifact:

- `scripts/frontier_yt_pr230_additive_top_jacobian_row_builder.py`
- `outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json`

The runner reads only the already packaged two-source taste-radial chunks001-052
reported by the committed chunk-package audit and extracts the preserved
three-mass top correlator scan at
`m_bare = 0.45, 0.75, 1.05`.  It builds one chunk-level row per packaged chunk:

```text
A_top = dE_top / d m_bare
```

using the endpoint slope across the mass bracket.  It also records the selected
mass, seed-control metadata, CG residual bound, total current-source top
response `T_total = dE_top/ds`, and a diagnostic `T_total - A_top`.

The 52-row packet has:

```text
row_count = 52
A_top mean = 1.32638198329744
A_top median = 1.3257396517244406
A_top sample stderr = 0.0014483006941081508
A_top weighted mean = 1.3263445336471822
A_top weighted stderr = 0.0004504696260217704
T_total mean = 2.489926106635367
T_total median = 1.424318655549806
diagnostic (T_total - A_top) mean = 1.163544123337927
diagnostic (T_total - A_top) median = 0.09907662065195189
```

## Boundary

These rows are not a physical top-Yukawa readout and are not strict
subtraction-closure rows.  They are chunk-level coarse mass-scan Jacobians, not
per-configuration matched covariance rows.

The W/Z physical-response route still needs:

- same-source W/Z response rows;
- per-configuration matched covariance for `T_total`, `A_top`, W/Z, and `g2`;
- strict non-observed `g2` authority;
- accepted same-source EW/Higgs action authority;
- final subtracted-response readout certificate.

No `kappa_s`, `c2`, `Z_match`, or `g2` value is set to one.  No `H_unit`,
`yt_ward_identity`, observed top/yukawa value, observed W/Z mass, observed `g2`,
`alpha_LM`, plaquette/u0, or reduced pilot is used as proof authority.

Chunks053-054 are active run-control only during this block.  The runner now
loads the committed chunk-package audit, consumes only its completed chunk IDs,
and explicitly excludes active chunks.  It does not touch or package
live-worker outputs.

## Validation

```text
python3 -m py_compile \
  scripts/frontier_yt_pr230_additive_top_jacobian_row_builder.py \
  scripts/frontier_yt_pr230_additive_top_subtraction_row_contract.py \
  scripts/frontier_yt_pr230_assumption_import_stress.py \
  scripts/frontier_yt_pr230_campaign_status_certificate.py \
  scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py \
  scripts/frontier_yt_retained_closure_route_certificate.py \
  scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# OK

python3 scripts/frontier_yt_pr230_additive_top_jacobian_row_builder.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_pr230_additive_top_subtraction_row_contract.py
# SUMMARY: PASS=22 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=104 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=356 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=163 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=317 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=72 FAIL=0

bash docs/audit/scripts/run_pipeline.sh
# OK, newly seeded=0, re-audit required=1 for this edited note hash,
# 5 known warnings, no errors

python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 known warnings

git diff --check
# OK
```
