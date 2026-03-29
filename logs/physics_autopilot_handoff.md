# Physics Autopilot Handoff

## 2026-03-28 21:28 America/New_York

### Seam class
- generated-family transfer
- first non-guarded generated failures

### Science impact
- science advanced; the zero-support guard isolates the original generated edge, but nearby generated transfer still fails immediately on non-guarded pair-only rows

### Current state
- Reused `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_support_collapse_guard_projection.py` for two follow-on sweeps:
  - `base:taper-wrap` through `default, broader, wider, ultra, mega`
  - `base:skew-wrap` through `default, broader, wider, ultra, mega`
- Canonical logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-support-collapse-guard-projection-taper-wrap-through-mega.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-support-collapse-guard-projection-skew-wrap-through-mega.txt`

### Strongest confirmed conclusion
- The minimal support-collapse guard isolates the original `geometry-c/e` edge but does not stabilize nearby generated transfer.
- On `base:taper-wrap` through `mega`:
  - `generated_rows_total = 12`
  - `generated_guarded_total = 10`
  - `generated_modeled_rows_total = 2`
  - `generated_modeled_misclassified_total = 2`
  - `first_modeled_failure_ensemble = ultra`
  - first non-guarded failure: `base:taper-wrap:mode-mix-f` (`pair-only-sensitive` actual, `add1-sensitive` predicted), repeated at `ultra` and `mega`
- On `base:skew-wrap` through `mega`:
  - `generated_rows_total = 9`
  - `generated_guarded_total = 0`
  - `generated_modeled_misclassified_total = 9`
  - `first_modeled_failure_ensemble = default`
  - failures begin immediately with `base:skew-wrap:local-morph-c`, and `base:skew-wrap:mode-mix-d` joins from `broader` onward
- In both sweeps, the historical frozen bucket remains unchanged (`historical_guarded_total = 0`, `historical_modeled_misclassified_total = 0`).

### Files/logs changed
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_generated_support_collapse_guard_projection.py`
- Updated narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-support-collapse-guard-projection-taper-wrap-through-mega.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-generated-support-collapse-guard-projection-skew-wrap-through-mega.txt`
- Validation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`

### Remaining review seams
- closed: determine whether the zero-support guard alone stabilizes nearby generated transfer
- open: explain the new non-guarded generated pair-only failures (`mode-mix-f`, `local-morph-c`, `mode-mix-d`)

### Exact next step
- Add one tiny row-level comparer for the new non-guarded generated failures and test whether they share a compact nonzero-support mechanism that the current law is missing.

### First concrete action
- Compare `base:taper-wrap:mode-mix-f`, `base:skew-wrap:local-morph-c`, and `base:skew-wrap:mode-mix-d` against the historical `pair-only-sensitive` rows on the current support/order-parameter basis.
