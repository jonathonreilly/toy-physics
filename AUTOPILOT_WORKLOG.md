# Physics Autopilot Worklog

This is the tracked loop-by-loop status ledger for the Physics autopilot.

Each autopilot run should:
- read this file first
- finish the highest-signal unfinished step before widening scope
- append a new timestamped entry at the top
- keep all paths canonical to this repository, not worktree-local paths

## 2026-03-21 16:18 America/New_York

### Current state
- `main` is synced to `origin/main` at commit `57be550`.
- The active mechanism thread is the pocket-wrap suppressor specificity line inside `base:taper-wrap` `local-morph`.
- The repo now contains suppressor coverage, injection, and specificity helpers plus deeper ladder sweeps through `variant_limit = 64`, along with a focused pair-kill diagnostic runner.

### Strongest confirmed conclusion
- The paired suppressors `(1,0)` and `(4,0)` are not a generic kill switch. On the tested `40/48/56` local-morph ladders, pair-kill occurs exactly when the added suppressor nodes overwrite active deep support.
- Full two-cell overlap is sufficient but not necessary: one deeper partial-overlap row appears by `variant_limit = 48`, so the tighter current rule is `deep_overlap_count > 0 => pair_kill` on the tested ladder.
- The focused pair-kill diagnostic confirms that this is coordinate-exact rather than just count-based: at `variant_limit = 56` and `64`, the kill coordinates match the overlapping deep-support coordinates for all `3/3` pair-kill rows, including the partial-overlap row `local-morph-\\x8e`.

### Files and results already documented
- Narrative conclusions: [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Model/helper implementation: [toy_event_physics.py](/Users/jonreilly/Projects/Physics/toy_event_physics.py)
- Current suppressor runners:
  - [scripts/pocket_wrap_suppressor_coverage.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_coverage.py)
  - [scripts/pocket_wrap_suppressor_coverage_sweep.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_coverage_sweep.py)
  - [scripts/pocket_wrap_suppressor_injection.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_injection.py)
  - [scripts/pocket_wrap_suppressor_specificity.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_specificity.py)
  - [scripts/pocket_wrap_suppressor_specificity_sweep.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_specificity_sweep.py)
  - [scripts/pocket_wrap_suppressor_pair_kill_diagnostic.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_pair_kill_diagnostic.py)
- Latest logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-pair-kill-diagnostic-56.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-pair-kill-diagnostic-64.txt`

### Exact next step
- Compare the non-pocket pair-kill rows (`local-morph-v` and `local-morph-\\x8e`) against canonical `local-morph-a` to isolate what changes the route from pocket-signature to non-pocket while keeping the same deep-support overwrite mechanism.

### First concrete action
- Diff the baseline deep/pocket/low gaps and candidate-cell sets for `local-morph-a`, `local-morph-v`, and `local-morph-\\x8e`, then check whether the non-pocket rows are missing only pocket signal or a larger shell/context property.
