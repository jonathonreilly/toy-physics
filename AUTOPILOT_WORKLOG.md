## 2026-03-21 16:13 America/New_York

### Current state
- `main` is synced to `origin/main` at commit `16e8fe7`; this run is currently uncommitted with one README update and one new suppressor comparison script.
- The active mechanism thread remains the pocket-wrap suppressor specificity line inside `base:taper-wrap` `local-morph`.
- Added a focused row-compare runner for the pair-kill rows and logged the `variant_limit = 64` comparison for `local-morph-a`, `local-morph-v`, and `local-morph-\\x8e`.

### Strongest confirmed conclusion
- The kill trigger remains coordinate-exact deep-support overwrite, but the non-pocket pair-kill rows are not just `local-morph-a` with pocket signal removed.
- `local-morph-v` keeps pair-kill with both overlaps while starting from positive deep/low gaps (`+0.09/+0.24`) and an extra surviving deep cell `(2,-1)`.
- `local-morph-\\x8e` keeps pair-kill with one overlap while starting from negative pocket gap (`-0.07`), a different surviving deep cell `(2,2)`, and a wider span profile (`span=4`).
- Shell/core context also shifts between these rows (notably shell deep/low enrichment for `local-morph-v` and lower shell pocket share for `local-morph-\\x8e`), so pocket-signature vs non-pocket presentation depends on broader shell/profile context, not a one-bit pocket toggle.

### Files and results changed in this run
- New script: [scripts/pocket_wrap_suppressor_pair_kill_row_compare.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_pair_kill_row_compare.py)
- Updated narrative: [README.md](/Users/jonreilly/Projects/Physics/README.md)
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-pair-kill-row-compare-64.txt`

### Exact next step
- Quantify which shell/profile context features separate pocket-signature pair-kill (`local-morph-a`) from non-pocket pair-kill (`local-morph-v`, `local-morph-\\x8e`) while holding the same deep-overwrite trigger.

### First concrete action
- Build a small `variant_limit = 64` table over all overlap-positive `dpadj-only` rows with baseline and post-add-both shell/profile metrics, then run a tiny rule search for predicates that isolate the pocket-signature branch from the non-pocket branch.


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
