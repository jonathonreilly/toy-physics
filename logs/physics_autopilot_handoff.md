# Physics Autopilot Handoff

## 2026-03-28 14:12 America/New_York

### Seam class
- outside-gate branch closure

### Science impact
- science advanced; outside-gate residual exact-closed on frozen bucket

### Current state
- Reconciled protocol preflight (no active detached child), acquired `physics-science`, and confirmed `main == origin/main` before new science.
- Added and ran `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_outside_gate_branch_second_pass.py` on frozen `5504` `rc0|ml0|c2`.
- The run performed a bounded branch-aware second pass over outside-gate rows by combining low-closure pocket membership, a spillover carve-out, and a right-low side-branch recovery rule.

### Strongest confirmed conclusion
- Outside-gate `pair-only-sensitive` now exact-closes with a compact branch-aware rule:
  - `(closure_load <= 46.500 and not (mid_anchor_closure_peak <= 0 and high_bridge_right_count <= 0))`
  - `or (high_bridge_right_low_count >= 1 and support_load <= 14.500 and mid_anchor_closure_peak <= 1)`
- Outside-gate performance improved from `23/26` (`5/2/1`) to `26/26` (`6/0/0`).
- The two low-closure spillover rows are isolated as `add1-sensitive`, and the prior high-closure miss is recovered as a right-low side branch.

### Files/logs changed
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_outside_gate_branch_second_pass.py`
- Updated narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-28-low-overlap-order-parameter-outside-gate-branch-second-pass.txt`
- Validation:
  - `python3 -m py_compile /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_order_parameter_outside_gate_branch_second_pass.py`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` (`benchmark regression audit: ok`)

### Remote sync status
- Commit and push this bounded step when ready.

### Remaining review seams
- closed: frozen `5504` deep-review lane remains closed

### Exact next step
- Keep compression/translation mode and project the combined high-closure exact gate rules plus the new outside-gate branch rule in one full-bucket evaluator.

### First concrete action
- Add one tiny unified projection checker for frozen `5504` `rc0|ml0|c2` that applies both rule families and reports full-bucket misclassifications/unmatched rows.
