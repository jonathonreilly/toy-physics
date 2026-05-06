# Handoff

## Summary

This block makes the source-resolved exact Green self-consistency pocket
auditable as a frozen bounded-support result.  The runner now fails closed if
zero-source exactness, TOWARD sign, exponent tolerances, calibrated-gain
boundary, or frozen table reproduction drift.

## Files To Review

- `scripts/source_resolved_exact_green_self_consistent.py`
- `docs/SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_NOTE.md`
- `outputs/source_resolved_exact_green_self_consistent_assertions_2026-05-06.txt`
- `docs/audit/data/audit_ledger.json`
- `docs/audit/data/citation_graph.json`
- `docs/audit/data/runner_classification.json`
- `docs/audit/data/effective_status_summary.json`

## Verification

```text
python3 scripts/source_resolved_exact_green_self_consistent.py
python3 -m py_compile scripts/source_resolved_exact_green_self_consistent.py
python3 docs/audit/scripts/build_citation_graph.py
python3 docs/audit/scripts/classify_runner_passes.py
python3 docs/audit/scripts/seed_audit_ledger.py
python3 docs/audit/scripts/compute_effective_status.py
python3 docs/audit/scripts/audit_lint.py
```

`audit_lint.py` reports existing warnings and no errors.

## PR

Opened: https://github.com/jonathonreilly/cl3-lattice-framework/pull/558
