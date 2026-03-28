# Physics Autopilot Handoff

## 2026-03-28 13:07 America/New_York

### Seam class
- outside-gate residual split

### Science impact
- science refined; headline accuracy unchanged

### Current state
- Picked up local continuation state first:
  - found unpushed local science commit `873a6fa`
  - pushed it successfully before new science so `main == origin/main`
- Acquired `manual-codex`, added and ran `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_outside_gate_low_closure_scan.py` on the frozen `5504` `rc0|ml0|c2` bucket.
- The run filters to rows outside the exact high-closure positive gate and searches the existing coarse asymmetry/order-parameter basis for the best compact low-closure separator of the remaining `pair-only-sensitive` residual.

### Strongest confirmed conclusion
- Outside the exact high-closure gate, the strongest compact residual separator is a pure low-closure cut:
  - `closure_load <= 46.500`
- On the outside-gate residual (`26` rows), that rule gives `23/26` for `pair-only-sensitive` (`5/2/1`):
  - two low-closure `add1-sensitive` false positives
  - one higher-closure `pair-only-sensitive` false negative
- So the remaining non-gated structure is now concentrated in three row-level exceptions rather than a broad mixed basin.

### Files/logs changed
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_outside_gate_low_closure_scan.py`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-outside-gate-low-closure-scan.txt`
- Validation:
  - `python3 -m py_compile /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_outside_gate_low_closure_scan.py`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` (`benchmark regression audit: ok`)

### Remote sync status
- Local gate-projection commit `873a6fa` has now been pushed; commit and push this bounded follow-on when ready.

### Remaining review seams
- closed: frozen `5504` deep-review lane remains closed

### Exact next step
- Stay in compression/translation mode and inspect the three outside-gate exceptions to the compact low-closure split.

### First concrete action
- Add one tiny outside-gate exception comparer for the two low-closure `add1-sensitive` false positives and the one higher-closure `pair-only-sensitive` false negative, then test whether one additional bounded structural feature resolves that `23/26` split.
