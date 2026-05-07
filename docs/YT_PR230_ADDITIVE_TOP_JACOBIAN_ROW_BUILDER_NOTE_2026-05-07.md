# PR230 Additive-Top Jacobian Row Builder

**Status:** bounded support / additive-top row artifact; closure not authorized.

## Result

This block adds a concrete additive-top Jacobian row artifact:

- `scripts/frontier_yt_pr230_additive_top_jacobian_row_builder.py`
- `outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json`

The runner reads only the already packaged two-source taste-radial chunks001-046 and
extracts the preserved three-mass top correlator scan at
`m_bare = 0.45, 0.75, 1.05`.  It builds one chunk-level row per packaged chunk:

```text
A_top = dE_top / d m_bare
```

using the endpoint slope across the mass bracket.  It also records the selected
mass, seed-control metadata, CG residual bound, total current-source top
response `T_total = dE_top/ds`, and a diagnostic `T_total - A_top`.

The 46-row packet has:

```text
row_count = 46
A_top mean = 1.3265591120930125
A_top median = 1.3258405656745211
A_top sample stderr = 0.0015290010502665677
A_top weighted mean = 1.3267028918044805
T_total median = 1.424318655549806
diagnostic (T_total - A_top) median = 0.09765459978503321
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

Chunks beyond 046 were present only as live/untracked outputs or active workers
during this block.  The runner hard-limits consumption to chunks001-046 and
does not touch or package live-worker outputs.

## Validation

```text
python3 -m py_compile \
  scripts/frontier_yt_pr230_additive_top_jacobian_row_builder.py \
  scripts/frontier_yt_pr230_additive_top_subtraction_row_contract.py \
  scripts/frontier_yt_pr230_assumption_import_stress.py \
  scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py \
  scripts/frontier_yt_retained_closure_route_certificate.py \
  scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# OK

python3 scripts/frontier_yt_pr230_additive_top_jacobian_row_builder.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_pr230_additive_top_subtraction_row_contract.py
# SUMMARY: PASS=22 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=101 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=352 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=160 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=314 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=69 FAIL=0

bash docs/audit/scripts/run_pipeline.sh
# OK, final rerun newly seeded=0, re-audit required=0, 5 known warnings

python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 known warnings

git diff --check
# OK
```
