# Physics Autopilot Worklog

This is the tracked loop-by-loop status ledger for the Physics autopilot.

Each autopilot run should:
- read this file first
- finish the highest-signal unfinished step before widening scope
- append a new timestamped entry at the top
- keep all paths canonical to this repository, not worktree-local paths

## 2026-03-21 17:12 America/New_York

### Current state
- `main` is still synced to `origin/main` at run start; this loop continued the same pocket-wrap suppressor overlap-context mechanism thread.
- Executed the pending deeper overlap-context rule sweeps at:
  - `variant_limit = 72`
  - `variant_limit = 80`
- Both runs produced the same three overlap-positive rows and the same exact-rule counts as the `64` rung.
- Updated README mechanism language to mark those shell/profile separators as stable across `64/72/80`.

### Strongest confirmed conclusion
- The pocket-wrap suppressor split is still a single overwrite-trigger family, and the canonical pocket-signature branch remains exactly separable by shell/profile context alone.
- The one-feature separators `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` now hold exactly (`0` FP, `0` FN) not only at `64` but also at `72` and `80`.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-72.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-80.txt`
- Commit status:
  - No new commit yet in this run.

### Exact next step
- Probe the first deeper rung where overlap-positive membership might change, then re-check whether the same exact shell/profile separators survive that membership expansion.

### First concrete action
- Run `scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 96`, inspect whether any new overlap-positive row appears, and if yes, recompute which one-feature separators remain exact.

## 2026-03-21 16:53 America/New_York

### Current state
- `main` is now synced to `origin/main`.
- This loop reconciled and pushed the previously local suppressor-context commits:
  - `1efe351` `Compare suppressor pair-kill rows by context`
  - `4497b08` `Update autopilot worklog with commit status`
  - `b126b11` `Isolate pocket-wrap overlap-context separators`
- The active mechanism thread is still the pocket-wrap suppressor specificity line inside `base:taper-wrap` `local-morph`.
- Added a new overlap-context rule runner:
  - [scripts/pocket_wrap_suppressor_overlap_context_rules.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_overlap_context_rules.py)
- Logged the `variant_limit = 64` overlap-context sweep to:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-64.txt`

### Strongest confirmed conclusion
- Pair-kill is still the same coordinate-exact deep-support overwrite mechanism across all overlap-positive rows.
- The pocket-signature branch (`local-morph-a`) is not separated from the non-pocket overlap-positive rows by the overwrite trigger itself, but by broader shell/profile context.
- On the current `variant_limit = 64` overlap-positive set, exact one-feature separators already exist in shell/profile space alone:
  - `boundary_roughness <= 0.288`
  - `center_total_variation <= 2.500`
  - `shell_pocket_fraction >= 0.812`
- So the clean current read is: `local-morph-a` is the low-roughness, low-total-variation, shell-pocket-saturated tip of the same overwrite-trigger family, while `local-morph-v` and `local-morph-\x8e` are rougher or more internally varied contexts of that same mechanism.

### Files and results changed in this run
- Code:
  - [toy_event_physics.py](/Users/jonreilly/Projects/Physics/toy_event_physics.py)
  - [scripts/pocket_wrap_suppressor_overlap_context_rules.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_overlap_context_rules.py)
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Pushed commits:
  - `1efe351`
  - `4497b08`
  - `b126b11`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-pair-kill-row-compare-64.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-64.txt`

### Exact next step
- Test whether those exact shell/profile separators survive a deeper local-morph ladder, rather than only the current `variant_limit = 64` overlap-positive set.

### First concrete action
- Sweep the overlap-context rule analysis at `variant_limit = 72` and `80`, then check whether `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, or `shell_pocket_fraction >= 0.812` remain exact separators of the pocket-signature branch.

## 2026-03-21 16:18 America/New_York

### Current state
- `main` is synced to `origin/main` at commit `57be550`.
- The active mechanism thread is the pocket-wrap suppressor specificity line inside `base:taper-wrap` `local-morph`.
- The repo now contains suppressor coverage, injection, and specificity helpers plus deeper ladder sweeps through `variant_limit = 64`, along with a focused pair-kill diagnostic runner.

### Strongest confirmed conclusion
- The paired suppressors `(1,0)` and `(4,0)` are not a generic kill switch. On the tested `40/48/56` local-morph ladders, pair-kill occurs exactly when the added suppressor nodes overwrite active deep support.
- Full two-cell overlap is sufficient but not necessary: one deeper partial-overlap row appears by `variant_limit = 48`, so the tighter current rule is `deep_overlap_count > 0 => pair_kill` on the tested ladder.
- The focused pair-kill diagnostic confirms that this is coordinate-exact rather than just count-based: at `variant_limit = 56` and `64`, the kill coordinates match the overlapping deep-support coordinates for all `3/3` pair-kill rows, including the partial-overlap row `local-morph-\x8e`.

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
- Compare the non-pocket pair-kill rows (`local-morph-v` and `local-morph-\x8e`) against canonical `local-morph-a` to isolate what changes the route from pocket-signature to non-pocket while keeping the same deep-support overwrite mechanism.

### First concrete action
- Diff the baseline deep/pocket/low gaps and candidate-cell sets for `local-morph-a`, `local-morph-v`, and `local-morph-\x8e`, then check whether the non-pocket rows are missing only pocket signal or a larger shell/context property.
