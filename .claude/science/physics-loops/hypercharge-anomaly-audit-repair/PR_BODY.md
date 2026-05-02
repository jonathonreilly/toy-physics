# PR Body

## Summary

This physics-loop block repairs the one-generation / hypercharge anomaly
audit boundary after the graph-first gauge repair.

It demotes stale source and runner language that described the package as
retained/proposed-retained, because the current support still depends on
neutral-singlet branch selection, SM electric-charge readout, and SM-definition
matter/charge conventions.

## Changes

- Demote `ONE_GENERATION_MATTER_CLOSURE_NOTE.md` to conditional support.
- Demote `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`
  to conditional exact support.
- Add bounded-theorem author hints so the audit queue seeds both changed rows
  as `bounded_theorem`.
- Update three runner summaries to avoid presenting conditional arithmetic as
  retained closure.
- Rerun the audit pipeline.
- Add a branch-local physics-loop handoff pack.

## Verification

```bash
python3 scripts/frontier_right_handed_sector.py
python3 scripts/frontier_anomaly_forces_time.py
PYTHONPATH=scripts python3 scripts/frontier_sm_hypercharge_uniqueness.py
PYTHONPATH=scripts python3 scripts/frontier_lhcm_y_normalization.py
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict
python3 -m py_compile scripts/frontier_right_handed_sector.py scripts/frontier_anomaly_forces_time.py scripts/frontier_sm_hypercharge_uniqueness.py
git diff --check
```

## Audit Result After Pipeline

- `one_generation_matter_closure_note`: `bounded_theorem`, `unaudited`,
  `unaudited`; ready and now queue rank #1.
- `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24`:
  `bounded_theorem`, `unaudited`, `unaudited`; queue rank #7.

Independent audit remains required. This PR does not apply an audit verdict.
