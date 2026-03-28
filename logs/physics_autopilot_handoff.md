# Physics Autopilot Handoff

## 2026-03-28 10:57 America/New_York

### Seam class
- residual-boundary closure

### Science impact
- science refined; headline accuracy unchanged

### Current state
- Reconciled lock/git and pre-step push state first; repo is still `ahead 1` with transient DNS push failure from helper (`Could not resolve host: github.com`).
- Added and ran `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_two_clause_residuals.py` on frozen `5504` `rc0|ml0|c2`.
- The run enforces a restricted two-clause search on `{support_load, mid_anchor_closure_peak, anchor_closure_intensity_gap, anchor_deep_share_gap}` and reports residual subtype membership per candidate separator.

### Strongest confirmed conclusion
- Two-clause restricted separators did not close the `add4` vs `pair-only` boundary.
- Best `add4-sensitive` two-clause candidate remains `27/32` but keeps `pair-only` leakage (`6/3/2`).
- `pair-only-sensitive` remains partial at `26/32` with mixed residual membership; `add1-sensitive` holds `27/32` with asymmetry-plus-closure split.

### Files/logs changed
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_two_clause_residuals.py`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-two-clause-residuals.txt`
- Validation:
  - `python3 -m py_compile /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_two_clause_residuals.py`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` (`benchmark regression audit: ok`)

### Remote sync status
- Pending: local `main` remains ahead due helper-reported DNS failure; retry push via `automation_push.py` after committing this bounded step.

### Remaining review seams
- closed: frozen `5504` deep-review lane remains closed

### Exact next step
- Test a coarse closure-regime physical-language projection (`mid_anchor_closure_peak` bins crossed with asymmetry sign bands) to see whether residual subtype mixing collapses without widening feature soup.

### First concrete action
- Add one bounded scanner that reports subtype counts for `mid_anchor_closure_peak` bins (`<=9`, `9-11`, `>=11`) crossed with `anchor_closure_intensity_gap` sign bands on the same frozen `5504` bucket.
