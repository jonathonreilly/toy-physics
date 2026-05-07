# PR230 Additive Response Aggregate Wiring

**Status:** exact support / aggregate gate wiring; closure not authorized.

**Runners updated:**

- `scripts/frontier_yt_pr230_assumption_import_stress.py`
- `scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py`
- `scripts/frontier_yt_retained_closure_route_certificate.py`
- `scripts/frontier_yt_pr230_positive_closure_completion_audit.py`

**Certificates consumed:**

- `outputs/yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json`
- `outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json`

## Result

The aggregate gates now load and assert the two additive-response blockers
directly:

1. The current additive source is incompatible with accepted radial-spurion
   action closure because the derivative contains `O_top_additive + O_H`, not
   a clean no-independent-top radial `O_H` spurion.
2. The subtraction identity is exact support only.  It becomes a candidate
   physical-response route only after same-surface additive-top Jacobian rows,
   W/Z response rows, matched covariance, strict non-observed `g2`, and an
   accepted action certificate exist.

This block does not create new physics closure evidence.  It prevents the
assembly, retained-route, and completion-audit surfaces from silently relying
on an additive-source shortcut or a subtraction formula without row authority.

## Validation

```text
python3 -m py_compile \
  scripts/frontier_yt_pr230_assumption_import_stress.py \
  scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py \
  scripts/frontier_yt_retained_closure_route_certificate.py \
  scripts/frontier_yt_pr230_positive_closure_completion_audit.py

python3 scripts/frontier_yt_pr230_additive_source_radial_spurion_incompatibility.py
# PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_additive_top_subtraction_row_contract.py
# PASS=21 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# PASS=100 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# PASS=352 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# PASS=160 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# PASS=314 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# PASS=69 FAIL=0

bash docs/audit/scripts/run_pipeline.sh
# OK; final rerun preserved the new note hash, 5 known warnings

python3 docs/audit/scripts/audit_lint.py --strict
# OK; 5 known warnings

git diff --check
# OK
```

The completion audit still reports:

```text
actual_current_surface_status = open / positive closure completion audit: retained closure not achieved
proposal_allowed = false
```

Chunks047 and 048 were still active during this block, so this wiring did not
touch the live two-source taste-radial chunk worker or package pending rows.
