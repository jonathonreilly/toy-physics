# Physics Autopilot Handoff

## 2026-03-28 13:34 America/New_York

### Seam class
- outside-gate exception map

### Science impact
- science refined; headline accuracy unchanged

### Current state
- Reconciled lock/git for manual continuation, acquired `manual-codex`, and confirmed `main == origin/main` before new science.
- Added and ran `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_outside_gate_exception_compare.py` on the frozen `5504` `rc0|ml0|c2` bucket.
- The run compares the two low-closure `add1-sensitive` false positives and the one higher-closure `pair-only-sensitive` false negative to the current outside-gate rule `closure_load <= 46.500`, then tests a tiny added structural feature set for a better compact follow-on rule.

### Strongest confirmed conclusion
- No tiny follow-on rule in the added structural feature set beats the current compact outside-gate rule `closure_load <= 46.500`; the residual still tops out at `23/26`.
- The three remaining exceptions now look branch-like rather than threshold-like:
  - the two false-positive `add1-sensitive` rows are low-closure, have no right-side high-bridge structure, and stay on the left/low side
  - the one false-negative `pair-only-sensitive` row is the only exception with explicit right-side low high-bridge structure
  - one false-positive `add1-sensitive` row is additionally extreme in left-only candidate concentration (`mid_candidate_count = 0`)
- So the next science object is a branch-aware second pass, not a wider search for one better global low-closure cut.

### Files/logs changed
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_outside_gate_exception_compare.py`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-outside-gate-exception-compare.txt`
- Validation:
  - `python3 -m py_compile /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_outside_gate_exception_compare.py`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` (`benchmark regression audit: ok`)

### Remote sync status
- Repo is synced to `origin/main` before this bounded follow-on; commit and push this step when ready.

### Remaining review seams
- closed: frozen `5504` deep-review lane remains closed

### Exact next step
- Stay in compression/translation mode and test a branch-aware second pass for the three outside-gate exceptions.

### First concrete action
- Add one tiny outside-gate branch scan that checks whether right-low high-bridge presence recovers the missed `pair-only-sensitive` side branch and whether left-only candidate concentration isolates the low-closure `add1-sensitive` spillover rows.
