# Physics Autopilot Handoff

## 2026-03-28 08:55 America/New_York

### Seam class
- order-parameter refinement

### Science impact
- science refined; headline accuracy unchanged

### Current state
- Reconciled lock/git and pre-step push state first (`main == origin/main`, push helper `nothing_to_push`).
- Added and ran `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_asymmetry_map.py` on frozen `5504` `rc0|ml0|c2`.
- The run adds a bounded support-layout asymmetry feature family on top of the existing coarse order-parameter map.

### Strongest confirmed conclusion
- Asymmetry improves physical readability and rule mix but not top-line closure:
  - `add1-sensitive`: best asymmetry-augmented split stays `27/32` and shifts toward `anchor_closure_intensity_gap` (`11/1/4`).
  - `add4-sensitive`: coarse separator remains `anchor_bridge_gap >= -0.500 and mid_anchor_closure_peak >= 9.000` (`27/32`, `8/5/0`).
  - `pair-only-sensitive`: broad split still `support_load <= 13.500` (`26/32`), with `anchor_deep_share_gap >= 0.450` as a narrow high-purity sentinel (`3/0/6`).

### Files/logs changed
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_asymmetry_map.py`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-asymmetry-map.txt`
- Validation:
  - `python3 -m py_compile` on touched script passed
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` passed (`benchmark regression audit: ok`)

### Remote sync status
- Pending: commit and push this bounded science step via `automation_push.py`.

### Remaining review seams
- closed: frozen `5504` deep-review lane remains closed

### Exact next step
- Stay in compression/translation mode and test whether compact asymmetric two-clause rules reduce `add4` vs `pair-only` confusion without dense laddering.

### First concrete action
- Run a restricted two-clause evaluator on `{support_load, mid_anchor_closure_peak, anchor_closure_intensity_gap, anchor_deep_share_gap}` over the same frozen `5504` bucket.
