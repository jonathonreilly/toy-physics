## 2026-03-22 04:19 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing the queued deeper rung:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 240 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
- Run completed successfully in canonical repo context:
  - `real 234.85s`, `user 234.49s`, `sys 0.25s`.
- Compared `240` output against completed `224` and `208` logs and updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.

### Strongest confirmed conclusion
- The `224` add4-sensitive expansion is persistent and continues at `240`:
  - non-pocket subtype rows increase from `6` to `8` (`224 -> 240`);
  - `local-morph-\u0133` persists;
  - two additional add4-sensitive crossing rows appear: `local-morph-\u014c` and `local-morph-\u014f`.
- Subtype count remains `3` and the add1-sensitive separator remains exact (`crosses_midline = n`, `0` FP / `0` FN).
- Equivalent 2-term add1 rule variants shift at `240` (e.g., shell-deep predicates replace prior core-deep/core-low-degree alternates), but the core subtype split structure is unchanged.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-208.txt`
- Commit status:
  - Pending commit for README + tracking updates in this run.
  - Current local head before committing this run: `676c438`.

### Exact next step
- Run one deeper rung (`variant_limit = 256`) to test whether add4-sensitive crossing expansion continues linearly and whether the add1 exact-rule table remains structurally stable.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 256 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
## 2026-03-22 03:20 America/New_York

### Current state
- Finished the previously blocked `variant_limit = 224` non-pocket subtype rung after adding per-call projection memoization in `/Users/jonreilly/Projects/Physics/toy_event_physics.py` (`project_metric_rows_and_anchor(...)`, cache keyed by `(metric_row, projection_matrix)`).
- Re-ran cheap audits and confirmed output stability:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 8` (`real 25.16s`)
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 32` (`real 45.32s`)
  - diffs vs prior runs are timestamp/elapsed-only.
- Completed the canonical blocked run:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
  - runtime: `real 221.79s`.

### Strongest confirmed conclusion
- The `224` rung is now completed and introduces the first post-`208` non-pocket expansion:
  - non-pocket subtype rows increase from `5` to `6`;
  - new row: `base:taper-wrap:local-morph-\u0133` (add4-sensitive, crossing branch);
  - subtype count remains `3`.
- The add1-sensitive separator remains exact and unchanged (`crosses_midline = n` still isolates `local-morph-\xe7` and `local-morph-\xe9` with `0` FP / `0` FN).
- So the mechanism state updates from “stable through `208`” to “breakpoint at `224` via add4-sensitive branch growth, with core add1 rule intact.”

### Files and results changed in this run
- Code:
  - [toy_event_physics.py](/Users/jonreilly/Projects/Physics/toy_event_physics.py)
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs touched/generated:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt` (completed run)
  - `/tmp/nonpocket8_after_projection_cache.txt`
  - `/tmp/nonpocket32_after_projection_cache.txt`
- Commit status:
  - Committed and pushed: `676c438` (`Unblock nonpocket 224 rung with projection caching`).
  - Repository sync is current at this checkpoint: `main` == `origin/main` at `676c438`.

### Exact next step
- Determine whether the new `224` add4-sensitive row (`local-morph-\u0133`) persists at the next rung or is transient by running and diffing one deeper rung (`variant_limit = 240`).

### First concrete action
- Run:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 240 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
- Then compare row membership/rule table against:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-208.txt`

## 2026-03-22 02:33 America/New_York

### Current state
- Resumed the same highest-signal blocked rung (`variant_limit = 224` non-pocket subtype-rule stability) and focused on `collect_self_maintenance_candidates(...)` / downstream derived-axis hotspots.
- Landed two runtime-oriented code changes in `/Users/jonreilly/Projects/Physics/toy_event_physics.py`:
  - added per-call seed/result dedup plumbing in `collect_self_maintenance_candidates(...)`:
    - `seen_seed_nodes` guard per interior seed node
    - `emergent_cache` memo keyed by `(seed_nodes, survive_counts, birth_counts)`
  - reduced object churn in `annotate_candidates_with_component_scores(...)` by replacing repeated multi-pass dataclass `replace(...)` calls with single-pass score assignment per candidate.
- Also switched `derive_emergent_persistent_nodes(...)` occupancy accumulation to sparse updates and `.get(..., 0.0)` downstream reads.
- Revalidated behavior with cheap audits (canonical repo):
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 8` (`real 26.09s`)
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 32` (`real 47.02s`)
  - Output parity checks vs previous canonical runs were clean (timestamp/elapsed-only diffs).
- Re-ran `variant_limit = 224` multiple times with canonical log redirection; run still did not complete in this cycle.

### Strongest confirmed conclusion
- Mechanism conclusions remain unchanged: non-pocket subtype membership/exact-rule mapping is still fully confirmed only through `variant_limit = 208`.
- Runtime state did improve in where the interrupted `224` run reaches:
  - prior blocked interrupts were in self-maintenance collection / candidate scoring setup;
  - this run reached deeper derived-axis projection code (`project_metric_rows_and_anchor`) before interruption.
- The blocker has shifted downstream, but a fully completed `224` rung is still pending.

### Files and results changed in this run
- Code:
  - [toy_event_physics.py](/Users/jonreilly/Projects/Physics/toy_event_physics.py)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs touched/generated:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt` (start marker only; incomplete reruns)
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-nonpocket-subtype-224-interrupt-traces.txt`
  - `/tmp/nonpocket8_after_hotfix.txt`
  - `/tmp/nonpocket32_after_hotfix.txt`
- Commit status:
  - Pending commit in this run for runtime optimizations + tracking updates.
  - Last known relation before this run: `origin/main...main = 0 behind / 6 ahead`.

### Exact next step
- Target the now-dominant derived-axis projection overhead (`project_metric_rows_and_anchor` / projection matrix applications) so a single full `variant_limit = 224` rung can complete.

### First concrete action
- Add a small per-call cache in `project_metric_rows_and_anchor(...)` for repeated row projections keyed by the metric row tuple and projection basis, then rerun:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`

## 2026-03-22 01:26 America/New_York

### Current state
- Continued the same highest-signal blocked rung (`variant_limit = 224` non-pocket subtype-rule stability) and applied targeted runtime reductions in the specificity pipeline path.
- Patched `toy_event_physics.py` to reuse per-graph neighbor adjacency in the self-maintenance search stack:
  - added `build_graph_neighbor_lookup(...)`
  - threaded optional `neighbor_lookup` reuse through `evolve_self_maintaining_pattern`, `derive_emergent_persistent_nodes`, `connected_components`, and `derive_persistence_support`
  - precomputed one lookup per `collect_self_maintenance_candidates(...)` call and reused it across all seed/rule trials.
- Revalidated behavior with smoke runs:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 8`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 32`
- Retried `variant_limit = 224` with log redirection to `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`; run still did not complete in this cycle.

### Strongest confirmed conclusion
- Mechanism conclusions remain unchanged: non-pocket subtype membership/exact separators are still fully confirmed through `variant_limit = 208` only.
- The new optimization is materially effective at lower rungs (same outputs, faster runtime):
  - `8`: `35.8s -> 26.6s`
  - `32`: `69.2s -> 48.3s`
- The unresolved `224` blocker remains in the specificity/candidate-pool path; subtype rule search itself is no longer the dominant issue.

### Files and results changed in this run
- Code:
  - [toy_event_physics.py](/Users/jonreilly/Projects/Physics/toy_event_physics.py)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs touched/generated:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt` (start marker only; incomplete rerun)
  - `/tmp/nonpocket8_after.txt` (smoke timing/output check)
  - `/tmp/nonpocket32_after.txt` (smoke timing/output check)
- Commit status:
  - Committed in this run: `d7e7606` (`Cache graph neighbors in self-maintenance candidate search`), `fab9f3f` (`Log neighbor-cache runtime progress for 224 subtype rung`), `766f207` (`Record push-blocked state for neighbor-cache run`), `7a7362e` (`Fix ahead count in latest autopilot worklog entry`), `3f5f31d` (`Sync latest worklog commit list and ahead count`), and `0b374ed` (`Align worklog commit metadata with final local state`).
  - Push attempt failed in sandbox (`Could not resolve host: github.com`), so remote sync could not be refreshed from this run context.
  - Last known local/remote relation in git metadata: `origin/main...main = 0 behind / 6 ahead`.

### Exact next step
- Reduce the remaining `variant_limit = 224` candidate search runtime by pruning repeated seed evaluations in `collect_self_maintenance_candidates(...)` (seed-builder de-dup and/or memoization of per-seed evolution outcomes), then rerun one full `224` rung.

### First concrete action
- Add a per-call memo in `collect_self_maintenance_candidates(...)` keyed by `(seed_nodes, survive_counts, birth_counts)` and skip duplicate seed-builder expansions before `derive_emergent_persistent_nodes(...)`, then run:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`

## 2026-03-22 00:27 America/New_York

### Current state
- Resumed the queued highest-signal mechanism step (`variant_limit = 224` non-pocket subtype-rule stability) and attempted controlled reruns:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
- The `224` rung still did not complete within this run window; interrupt traceback confirms the runtime hotspot is upstream in `pocket_wrap_suppressor_specificity_analysis` (deep candidate-pool/persistence search path), before subtype rule enumeration starts.
- Implemented and validated a rule-search efficiency patch in `scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py` (boundary-only thresholds + deduped bitmask predicate combinations), then smoke-checked at lower limits (`8` and `32`).

### Strongest confirmed conclusion
- Mechanism conclusions remain unchanged: non-pocket subtype membership and exact separators are still only fully confirmed through `variant_limit = 208`.
- The currently confirmed blocker for the `224` rung is not subtype rule combinatorics; it is the expensive overlap/specificity pipeline in `toy_event_physics.py` (`pocket_wrap_suppressor_specificity_analysis` stack).

### Files and results changed in this run
- Code:
  - [scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Attempted (incomplete) log target:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt` (start marker only)
- Commit status:
  - Committed and pushed: `04a60a1` (`Speed up nonpocket subtype rule search`), `99f0c73` (`Log 224 subtype runtime blocker and next profiling step`), `8410de1` (`Correct commit sync state in latest worklog entry`).
  - Repository is synced: `main` == `origin/main` at `8410de1`.

### Exact next step
- Isolate and reduce `variant_limit = 224` specificity runtime in `toy_event_physics.py` enough to complete one full non-pocket subtype run, then compare subtype rows/rules against `192/208`.

### First concrete action
- Profile one controlled run with:
  - `python3 -m cProfile -o /Users/jonreilly/Projects/Physics/logs/2026-03-22-nonpocket-subtype-224.profile scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224`
- Then inspect top cumulative hotspots (`pstats`) and patch the highest-cost function in the `pocket_wrap_suppressor_specificity_analysis` path.

## 2026-03-21 23:26 America/New_York

### Current state
- Resumed the queued highest-signal mechanism step (`variant_limit = 224` for non-pocket subtype-rule stability) and launched:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224`
- In this sandbox, long-running non-TTY jobs could not be interrupted or introspected (`ps`/`pkill`/`killall` were blocked), so no completed `224` result was obtained within this run window.
- No code or README conclusions were changed because there is no finished new rung output to justify a mechanism update.

### Strongest confirmed conclusion
- The last fully confirmed mechanism state remains unchanged from the prior completed run: the non-pocket subtype rule map is stable and exact through `variant_limit = 208`.
- A definitive `224` breakpoint/no-breakpoint conclusion is still pending completion of a single successful `224` rung run.

### Files and results changed in this run
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Commit status:
  - Committed and pushed: `905375a` (`Log blocked variant-limit 224 subtype rung attempt`).
  - Repository is synced: `main` == `origin/main` at `905375a`.

### Exact next step
- Complete a single successful `variant_limit = 224` non-pocket subtype-rule rung and compare subtype membership plus exact-rule tables against the completed `192/208` baselines.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224 > /Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt` in a controllable execution mode (interactive/killable), then diff the new log against:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-192.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-208.txt`

# Physics Autopilot Worklog

This is the tracked loop-by-loop status ledger for the Physics autopilot.

Each autopilot run should:
- read this file first
- finish the highest-signal unfinished step before widening scope
- append a new timestamped entry at the top
- keep all paths canonical to this repository, not worktree-local paths

## 2026-03-21 22:56 America/New_York

### Current state
- Implemented and ran the queued non-pocket subtype exact-rule extraction step from the stabilized `176/192` overlap-context thread.
- Added helper:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit <N>`
- Executed and logged both planned rungs:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 192`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 208`
- Updated README mechanism notes with the new rule-level result.

### Strongest confirmed conclusion
- Non-pocket overlap-positive membership and subtype behavior are unchanged between `192` and `208` (same `5` rows and same `3` suppressor-response subtypes).
- The add1-sensitive subtype (`local-morph-\\xe7`, `local-morph-\\xe9`) is exactly isolated by compact one-feature rules (`crosses_midline = n`, or equivalently `center_total_variation <= 2.500`).
- The crossing rows split exactly by overlap multiplicity: `deep_overlap_count = 2` isolates the single both-sensitive row (`local-morph-v`), while `crosses_midline = Y` with `deep_overlap_count = 1` isolates the add4-sensitive pair (`local-morph-\\x8e`, `local-morph-\\u0103`).
- So through `208`, the non-pocket branch is now rule-level explicit, not just qualitatively multi-subtype.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Added helper:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-192.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-208.txt`
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Commit status:
  - Committed and pushed: `a420284` (`Extract stable non-pocket subtype rules through variant limit 208`).

### Exact next step
- Stress-test whether the same non-pocket subtype rule map remains exact at the next ladder rung and detect the first rung where subtype membership or exact separators change.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224` and compare subtype rows plus exact-rule table against the `192/208` logs.

## 2026-03-21 21:14 America/New_York

### Current state
- Resumed the pending non-pocket subtype step from the `176/192` overlap-context thread and ran the queued focused compare at `variant_limit = 192`:
  - `python3 scripts/pocket_wrap_suppressor_pair_kill_row_compare.py --variant-limit 192 --targets 'local-morph-v' 'local-morph-\\x8e' 'local-morph-\\xe7' 'local-morph-\\xe9' 'local-morph-\\u0103'`
- Updated README mechanism language with the new subtype split interpretation from that compare.

### Strongest confirmed conclusion
- The broadened non-pocket branch is not one coherent subtype.
- `local-morph-\\xe7` and `local-morph-\\xe9` form a matched non-crossing branch (`crosses_midline = n`) that flips only when `(1,0)` is added (`add1 -> ge6-only`, `add4 -> dpadj-only`).
- `local-morph-\\u0103` instead aligns with the crossing branch (`crosses_midline = Y`) and flips on `(4,0)` (`add4 -> ge6-only`, `add1 -> dpadj-only`).
- So within the same overlap-trigger family, the newly added rows already split into at least two suppressor-response subtypes.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-pair-kill-row-compare-192-nonpocket.txt`
- Commit status:
  - Committed and pushed: `b7c0ce2` (`Document non-pocket suppressor subtypes at variant limit 192`).
  - `main` now matches `origin/main` at `b7c0ce2`.

### Exact next step
- Convert the non-pocket subtype split from qualitative to exact-rule form on the stabilized `192` family, then check whether that rule remains exact at `variant_limit = 208`.

### First concrete action
- Add a small helper script that labels non-pocket overlap-positive rows by suppressor-response subtype at `variant_limit = 192` and performs a one/two-feature threshold search for `0` FP / `0` FN separators, then rerun at `208`.

## 2026-03-21 20:59 America/New_York

### Current state
- Continued the overlap-context ladder through the next two queued rungs:
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 176`
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 192`
- No new helper code was needed in this pass; this was a pure ladder-extension and interpretation step.

### Strongest confirmed conclusion
- `176` adds one more non-pocket overlap-positive row: `local-morph-\\u0103`.
- `192` is identical to `176`, so the broadened overlap-positive family appears stable at least through `192`.
- Current stabilized family through `192`:
  - pocket-signature rows: `local-morph-a`, `local-morph-\\xf6`
  - non-pocket rows: `local-morph-v`, `local-morph-\\x8e`, `local-morph-\\xe7`, `local-morph-\\xe9`, `local-morph-\\u0103`
- The robust exact one-feature separators in that stabilized band are still:
  - `boundary_roughness <= 0.288`
  - `pocket_fraction <= 0.081`
- So the current best read is that the broadened family is real, but the pocket-signature subset remains a compact low-roughness / low-pocket-fraction edge of the same overwrite-trigger family.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-176.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-192.txt`

### Exact next step
- Explain the new stabilized non-pocket branch internally: identify whether the added rows `\\xe7`, `\\xe9`, and `\\u0103` split into one coherent non-pocket subtype or multiple subtypes under the same overwrite trigger.

### First concrete action
- Run a focused row compare at `variant_limit = 192` for `local-morph-v`, `local-morph-\\x8e`, `local-morph-\\xe7`, `local-morph-\\xe9`, and `local-morph-\\u0103`, then search for small exact predicates that separate those non-pocket rows into stable subgroups.

## 2026-03-21 20:15 America/New_York

### Current state
- `main` started this run at `1572d7d` with a local uncommitted `AUTOPILOT_WORKLOG.md` status edit.
- Continued the same pocket-wrap suppressor overlap-context mechanism thread and executed the queued deeper rung:
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 128`
- The `128` rung completed successfully and produced the expected overlap-context/rule table log (`total_elapsed=421.9s`).
- Updated README mechanism language to include the `128` rung stability result.

### Strongest confirmed conclusion
- Overlap-positive membership still does not expand at `variant_limit = 128`; it remains exactly `local-morph-a`, `local-morph-v`, and `local-morph-\x8e`.
- The same shell/profile separators remain exact one rung deeper: `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` still isolate the canonical pocket-signature branch with `0` FP and `0` FN.
- The mechanism read is unchanged but now verified through `128`: `local-morph-a` remains the low-roughness, low-total-variation, shell-pocket-saturated tip of the same coordinate-exact overwrite-trigger family.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-128.txt`
- Commit status:
  - Committed and pushed: `5b8fb7c` (`Validate overlap-context separators through variant limit 128`).
  - `main` now matches `origin/main` at `5b8fb7c`.

### Exact next step
- Probe the next deeper ladder rung to find the first point where overlap-positive membership changes or exact one-feature separator behavior degrades.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 144`, then check whether overlap-positive rows remain `3` and whether `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` remain `0` FP / `0` FN.

## 2026-03-21 19:18 America/New_York

### Current state
- `main` started this run at `b914026` with local uncommitted `README.md` and `AUTOPILOT_WORKLOG.md` edits from the prior `96` rung documentation pass.
- Continued the same pocket-wrap suppressor overlap-context mechanism thread and executed the planned deeper rung:
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 112`
- The `112` rung completed successfully and produced the expected overlap-context/rule table log (`total_elapsed=371.6s`).
- Updated README mechanism language to include the `112` rung stability result.

### Strongest confirmed conclusion
- Overlap-positive membership still does not expand at `variant_limit = 112`; it remains exactly `local-morph-a`, `local-morph-v`, and `local-morph-\\x8e`.
- The shell/profile separators remain exact one rung deeper: `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` still isolate the canonical pocket-signature branch with `0` FP and `0` FN.
- The strongest mechanism read is unchanged but now verified through `112`: `local-morph-a` remains the low-roughness, low-total-variation, shell-pocket-saturated tip of the same coordinate-exact overwrite-trigger family.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-112.txt`
- Commit status:
  - Committed and pushed: `1572d7d` (`Validate overlap-context separators through variant limit 112`).
  - `main` now matches `origin/main` at `1572d7d`.

### Exact next step
- Probe the next deeper ladder rung to find the first point where overlap-positive membership changes or exact one-feature separator behavior degrades.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 128`, then check whether overlap-positive rows remain `3` and whether `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` remain `0` FP / `0` FN.

## 2026-03-21 20:33 America/New_York

### Current state
- Continued the same pocket-wrap suppressor overlap-context mechanism ladder and executed three deeper rungs:
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 128`
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 144`
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 160`
- Added one focused follow-up compare at the first broadened pocket-signature rung:
  - `python3 scripts/pocket_wrap_suppressor_pair_kill_row_compare.py --variant-limit 160 --targets local-morph-a local-morph-v local-morph-\\x8e local-morph-\\xf6`

### Strongest confirmed conclusion
- `128` stays identical to the earlier ladder: still exactly `3` overlap-positive rows and the same exact one-feature separators.
- `144` is the first real breakpoint:
  - overlap-positive membership expands from `3` to `5`
  - two new non-pocket rows appear: `local-morph-\\xe7`, `local-morph-\\xe9`
  - the exact one-feature separator set shrinks from three older favorites to a different surviving pair/core, especially `boundary_roughness <= 0.288` and `pocket_fraction <= 0.081`
- `160` adds the first second pocket-signature row:
  - new row: `local-morph-\\xf6`
  - pocket-signature branch broadens from `1` to `2`
  - exact one-feature separators still exist, but the robust ones are now `boundary_roughness <= 0.288` and `pocket_fraction <= 0.081`
- The 160 row compare shows `local-morph-\\xf6` is not a different trigger. It is another anti-deep pocket branch of the same overwrite family, but even more compact than `local-morph-a`: lower roughness (`0.244`), lower total variation (`1.00`), no crossing, span `2`, and only one overlapping suppressor/deep coordinate `(4,0)`.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-128.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-144.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-160.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-pair-kill-row-compare-160.txt`

### Exact next step
- Determine whether the new `144/160` rows are the start of a stable broadened family or just a sparse transient band, and whether `boundary_roughness <= 0.288` plus `pocket_fraction <= 0.081` remains the right compact separator pair above `160`.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 176` and `--variant-limit 192`, then check:
  - whether overlap-positive membership expands again
  - whether pocket-signature membership stays at `2`
  - whether `boundary_roughness <= 0.288` and `pocket_fraction <= 0.081` remain exact one-feature separators.

## 2026-03-21 18:09 America/New_York

### Current state
- `main` started this run at `b914026` with a local uncommitted worklog edit.
- Continued the same pocket-wrap suppressor overlap-context mechanism thread and executed the planned deeper rung:
  - `scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 96`
- The `96` rung completed and produced the expected overlap-context/rule table log.
- Updated README mechanism language to include the `96` rung stability result.

### Strongest confirmed conclusion
- Overlap-positive membership did not expand at `variant_limit = 96`; it is still exactly the same three rows (`local-morph-a`, `local-morph-v`, `local-morph-\x8e`).
- The shell/profile separators remain exact at this deeper rung: `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` still isolate the canonical pocket-signature branch with `0` FP and `0` FN.
- So the strongest mechanism read is unchanged but now verified one rung deeper: `local-morph-a` remains the low-roughness, low-total-variation, shell-pocket-saturated tip of the same coordinate-exact overwrite-trigger family.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-96.txt`
- Commit status:
  - Pending in working tree (not committed yet in this run).

### Exact next step
- Probe the next deeper ladder rung to find the first point where overlap-positive membership or exact separator behavior changes.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 112` and check whether overlap-positive rows stay at `3` and whether the same one-feature exact separators remain `0` FP / `0` FN.

## 2026-03-21 17:12 America/New_York

### Current state
- `main` was synced to `origin/main` at run start; this loop continued the same pocket-wrap suppressor overlap-context mechanism thread.
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
  - Committed and pushed: `b914026` (`Validate overlap-context separators through variant limit 80`).
  - `main` now matches `origin/main` at `b914026`.

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

## 2026-03-22 05:19 America/New_York

### Current state
- Resumed the active non-pocket subtype stability thread and executed the queued deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 256 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
- Run completed successfully:
  - `real 246.81s`, `user 246.46s`, `sys 0.25s`.
- Compared `256` against `240`/`224` and updated mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.
- Ran a cheap audit smoke check after updates:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 8 > /tmp/2026-03-22-nonpocket-subtype-rules-8-post256-smoke.txt`
  - `real 24.51s`, `user 24.40s`, `sys 0.03s`.

### Strongest confirmed conclusion
- The post-`208` add4-sensitive crossing expansion does not extend immediately at `256`:
  - non-pocket subtype rows are unchanged from `240` (`8` rows, subtype count `3`);
  - add1-sensitive separation remains exact via `crosses_midline = n` (`2/2`, `0` FP, `0` FN);
  - `256` and `240` differ only in run metadata (`variant_limit`/timestamps/elapsed).
- The strongest mechanism read is now: expansion occurred at `224/240`, then stabilized through at least `256`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
  - `/tmp/2026-03-22-nonpocket-subtype-rules-8-post256-smoke.txt`
- Commit status:
  - Pending commit for README + tracking updates from this run.
  - Local head before committing this run: `676c438`.

### Exact next step
- Run one deeper rung (`variant_limit = 272`) to test whether the add4-sensitive crossing branch remains plateaued after the `256` hold or resumes growth.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 272 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
- Then diff subtype context/exact-rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
