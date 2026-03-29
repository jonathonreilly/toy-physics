# Physics Autopilot Handoff

## 2026-03-28 20:34 America/New_York

### Seam class
- generated-family transfer
- zero-support branch exposure

### Science impact
- science advanced; the exact historical low-overlap law fails immediately on nearby generated `taper-wrap` ensembles once zero-support rows are counted correctly

### Current state
- Repaired `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check.py` so undefined support-edge metrics fall back to zero-valued metrics instead of dropping the row.
- Added and ran `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_ensemble_eligibility_profile.py` to locate the first generated non-pocket cohort.
- Re-ran the repaired exact transfer check on canonical generated ensembles `default`, `broader`, `wider`.
- Canonical logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-ensemble-eligibility-profile.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-exact-law-generated-ensemble-transfer-check.txt`

### Strongest confirmed conclusion
- The earlier "vacuous transfer" result was a checker artifact.
- Eligibility appears immediately at `base:taper-wrap:default`:
  - `eligible_nonpocket_total = 2`
  - both rows are geometry variants `geometry-c` and `geometry-e`
  - both rows are actual `pair-only-sensitive`
- With zero-capable support metrics, the repaired canonical transfer fails immediately:
  - `ensembles = default, broader, wider`
  - `rows_total = 6`
  - `misclassified_total = 6`, `ambiguous_total = 0`, `unmatched_total = 0`
  - `first_failure_ensemble = default`
- All six failures are the repeated `geometry-c/e` rows, predicted as `add1-sensitive` via `outside-gate-add1-default` because the generated branch has `closure_load = 0` and `mid_anchor_closure_peak = 0`.

### Files/logs changed
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_ensemble_eligibility_profile.py`
- Updated narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-ensemble-eligibility-profile.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-exact-law-generated-ensemble-transfer-check.txt`
- Validation:
  - `python3 -m py_compile /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check.py /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_ensemble_eligibility_profile.py`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`

### Remaining review seams
- closed: first canonical generated-family transfer failure exists and is reproducible
- open: explain the zero-support `pair-only-sensitive` generated branch

### Exact next step
- Build one bounded comparer for `base:taper-wrap:geometry-c` and `base:taper-wrap:geometry-e`, then test whether the transfer failure is a true new pair-only branch or an out-of-domain support-collapse case.

### First concrete action
- Diff the generated failure rows against the historical pair-only branch on support-layout and anchor-closure observables, with special attention to why all current support metrics vanish.
