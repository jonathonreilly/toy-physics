## 2026-03-27 21:00 America/New_York

### Current state
- Continued the deep review thread on the frozen `5504` transfer/follow-on lane after the transfer-layer selector cleanups were synced.
- Closed the next shared-helper seam in the active exception-analysis path:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_add4_exception_scan.py`
  had a one-off local parser for the same compact rule language emitted by the shared support-topology evaluator.
- Moved that matcher into:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology.py`
  as shared `matches_rule_text(...)`.
- Repointed the add4 exception scan and the audit to that shared matcher, and extended the audit so the exception scan cannot silently drift back to a local `RULE_TERM_RE` / `_matches_rule_text` implementation.

### Strongest confirmed conclusion
- Science conclusions did not change; this is another transfer-layer / review-layer integrity cleanup.
- The active frozen `5504` transfer/follow-on lane now also shares one rule-text evaluator for compact support-topology rules, instead of letting the add4 exception scan own a separate parser.

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_add4_exception_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Validation:
  - `python3 -m py_compile` on touched scripts passed.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` passed (`benchmark regression audit: ok`).

### Exact next step
- Stay in deep review mode on the frozen `5504` transfer/follow-on lane.
- Review whether any remaining active transfer/follow-on scripts still duplicate live-rule selection logic or one-off branch selectors instead of importing them from the shared helper surface.

### First concrete action
- Search:
  - `rg -n 'evaluate_rules\\(|rule_text|selected_rule|best_rule|anchor_adj_bridge_count >= 3\\.5|def _peer_band' /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_*`

## 2026-03-27 20:40 America/New_York

### Current state
- Continued the deep review thread on the frozen `5504` support-family transfer / baseline follow-on layer under the `physics-science` worker lock.
- Closed one more duplicated selector seam in the active transfer lane:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_bucket_rules.py`
  was still excluding peer-band rows with a local `high_bridge_left_low_count >= 0.5` threshold literal.
- Repointed that exclusion to the shared helper in:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
  via `is_peer_band_like(...)`.
- Updated the cheap audit so this script cannot silently drift back to the local threshold literal.

### Strongest confirmed conclusion
- Science conclusions did not change; this is another transfer-layer integrity cleanup.
- The support-family transfer bucket-rule scan now uses the same shared peer-band selector as the rest of the active transfer surface.

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_bucket_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Validation:
  - `python3 -m py_compile` on touched scripts passed.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` passed (`benchmark regression audit: ok`).

### Exact next step
- Stay in deep review mode on the frozen `5504` transfer/follow-on lane.
- Review whether remaining active transfer scripts still carry single-use wrappers or local rule-text evaluators that should be centralized into the shared helper surface.

### First concrete action
- Search:
  - `rg -n 'def _peer_band|def _matches_rule_text|rule_text\.split\(" and "\)' /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_*`

## 2026-03-27 20:28 America/New_York

### Current state
- Continued the deep review thread on the frozen `5504` support-family transfer / baseline follow-on layer immediately after the shared `rc0|ml0|c2` selector cleanup passed validation.
- Closed one more duplicated-selector seam in the active transfer layer:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_primary_bucket_profiles.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_satellites.py`
  were still spelling the `peer-band` split locally through `high_bridge_left_low_count >= 0.5` / `< 0.5`.
- Centralized that split in:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
  via shared `is_peer_band_like(...)`, which now also lines up explicitly with the shared `rc0|ml0|c2` core threshold.
- Extended the cheap audit so those active transfer scripts cannot silently drift back to local `peer-band` threshold literals.

### Strongest confirmed conclusion
- Science conclusions did not change; this is another transfer-layer integrity cleanup.
- The active transfer layer now shares one source of truth for:
  - the primary support-family bucket set
  - the residual bucket thresholds/key builders
  - the non-peer core primary bucket-key helper
  - the `high-support ml0` branch thresholds
  - the `rc0|ml0|c2` core selector
  - the `peer-band` selector

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_primary_bucket_profiles.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_satellites.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Validation:
  - `python3 -m py_compile` on touched scripts passed.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` passed (`benchmark regression audit: ok`).

### Exact next step
- Stay in deep review mode on the frozen `5504` transfer/follow-on lane.
- Review whether any remaining active transfer/follow-on scripts still duplicate small branch selectors or live-rule selection logic instead of importing them from the shared helper surface.

### First concrete action
- Search:
  - `rg -n 'anchor_adj_bridge_count >= 3\\.5|def _peer_band|TARGET_BUCKET = \"rc0\\|ml0\\|c2\"|matches_rule_text|rule_text' /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_*`

## 2026-03-27 20:24 America/New_York

### Current state
- Continued the deep review thread on the frozen `5504` support-family transfer / baseline follow-on layer after confirming the worker lock was free and there was no conflicting active science job.
- Closed another duplicated-selector seam in the active `rc0|ml0|c2` transfer lane:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_topology_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_interaction_motif_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_contrast.py`
  were each rebuilding the same target bucket string and `high_bridge_left_low_count < 0.5` slice locally.
- Centralized that selector in:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
  via shared `RC0_ML0_C2_BUCKET`, `RC0_ML0_C2_MAX_LEFT_LOW`, and `is_rc0_ml0_c2_core_like(...)`.
- Extended the cheap audit so those three active `rc0|ml0|c2` scripts cannot silently drift back to local selector literals.

### Strongest confirmed conclusion
- Science conclusions did not change; this is another transfer-layer integrity cleanup.
- The active `rc0|ml0|c2` transfer lane now shares one source of truth for:
  - the primary support-family bucket set
  - the residual bucket thresholds/key builders
  - the non-peer core bucket-key helper
  - the `high-support ml0` branch thresholds
  - the `rc0|ml0|c2` core selector

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_topology_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_interaction_motif_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_contrast.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Validation:
  - `python3 -m py_compile` on touched scripts passed.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` passed (`benchmark regression audit: ok`).

### Exact next step
- Stay in deep review mode on the frozen `5504` transfer/follow-on lane.
- Review whether any remaining active transfer/follow-on scripts still duplicate local target-bucket constants, peer-band selectors, or small branch selectors instead of importing them from the shared helper surface.

### First concrete action
- Search:
  - `rg -n 'TARGET_BUCKET = \"rc0\\|ml0\\|c2\"|high_bridge_left_low_count < 0\\.5|peer-band|anchor_adj_bridge_count >= 3\\.5' /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_*`

## 2026-03-28 00:14 America/New_York

### Current state
- Continued the deep review thread on the frozen `5504` support-family transfer / baseline follow-on layer under the manual lock.
- Closed the next remaining local-threshold seam in the immediate follow-on stack:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_high_support_ml0_split.py`
  was already using the shared `19.0`/`71.0` residual thresholds
  - but it still carried its own local `3.0` target-branch cutoff and `3.5` `c3/c4p` split threshold
- Centralized those branch constants in:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
- Repointed the `high-support ml0` split follow-on to those shared constants and extended the cheap audit so it cannot silently drift back to local `3.0`/`3.5` branch literals.

### Strongest confirmed conclusion
- Science conclusions did not change; this is another transfer-layer integrity cleanup.
- The immediate baseline non-peer follow-on stack now shares one source of truth for:
  - the primary support-family bucket set
  - the residual bucket thresholds/key builders
  - the non-peer core primary bucket-key helper
  - the `high-support ml0` branch thresholds
- That closes another classification/branch-threshold drift seam in the frozen `5504` review layer.

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_high_support_ml0_split.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Validation:
  - `python3 -m py_compile` on touched scripts passed.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` passed (`benchmark regression audit: ok`).

### Exact next step
- Stay in deep review mode on the frozen `5504` transfer/follow-on lane.
- Review whether any remaining immediate follow-on scripts still duplicate local split constants or small branch selectors that should move into the shared helper surface.

### First concrete action
- Search:
  - `rg -n "3\\.0|3\\.5|SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD|EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD|HIGH_SUPPORT_ML0_MIN_CELL_COUNT|HIGH_SUPPORT_ML0_C4P_SPLIT_THRESHOLD" /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_*`

## 2026-03-28 00:04 America/New_York

### Current state
- Continued the deep review thread on the frozen `5504` support-family transfer / baseline follow-on layer under the manual lock after pushing the outstanding worker backlog.
- Closed the next immediate non-peer core duplication seam:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_buckets.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_family_rules.py`
  were still carrying their own local `_mid_low_bin`, `_cell_bin`, and `_bucket_key` builders.
- Repointed both scripts to the shared primary bucket-key helper in:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
- Extended the cheap audit so those scripts cannot silently regress to local bucket-bin builders later.

### Strongest confirmed conclusion
- Science conclusions did not change; this is another transfer-layer integrity cleanup.
- The active baseline non-peer follow-on stack now shares one source of truth for:
  - the primary support-family bucket set
  - the residual bucket thresholds/key builders
  - the non-peer core primary bucket-key helper
- That removes another classification-drift surface from the frozen `5504` review layer.

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_buckets.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_family_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Validation:
  - `python3 -m py_compile` on touched scripts passed.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` passed (`benchmark regression audit: ok`).

### Exact next step
- Stay in deep review mode on the frozen `5504` transfer/follow-on lane.
- Review whether the remaining immediate follow-on scripts still duplicate any local threshold or split constants that should move into the shared helper surface, especially the `high-support ml0` split branch.

### First concrete action
- Search:
  - `rg -n "3\\.0|3\\.5|SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD|EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD|family_bucket_key_like\\(" /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_*`

## 2026-03-27 19:43 America/New_York

### Current state
- Continued the deep review thread on the frozen `5504` support-family transfer / baseline follow-on layer under the `physics-science` lock.
- Completed one bounded integrity step on the immediate baseline follow-on surface:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_high_support_ml0_split.py` was still hard-coding residual-bucket threshold literals (`19.0`, `71.0`) in `_is_target_branch(...)`.
- Repointed that script to shared helper constants from:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
- Extended the cheap audit so this follow-on script cannot silently regress to local threshold literals.

### Strongest confirmed conclusion
- Science conclusions did not change; this is another integrity cleanup.
- The active support-family transfer lane now keeps residual-bucket threshold definitions shared not only in transfer/reconstruction helpers but also in the high-support ml0 split follow-on.
- This closes one more threshold-drift seam in the frozen-frontier `5504` transfer stack.

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_high_support_ml0_split.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Validation:
  - `python3 -m py_compile` on touched scripts passed.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` passed (`benchmark regression audit: ok`).

### Exact next step
- Stay in deep review mode on the frozen-frontier transfer / baseline follow-on layer.
- Continue searching immediate follow-on scripts for duplicated bucket-bin logic (`_mid_low_bin` / `_cell_bin`) that should use shared helper surfaces.

### First concrete action
- Inspect:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_buckets.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_family_rules.py`
- Then compare their local bucket-key builders against the shared transfer helper key functions.

## 2026-03-27 23:48 America/New_York

### Current state
- Continued the deep review thread on the frozen `5504` support-family transfer / baseline follow-on layer under the manual lock.
- Fixed the next duplicated classification seam after centralizing the primary bucket set:
  - the baseline non-peer residual follow-on was still rebuilding the same support-family bucket keys and residual-bucket thresholds locally
  - instead of consuming them from the shared transfer helper
- Centralized the remaining shared bucket-key logic and thresholds in:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
- Repointed the baseline residual follow-on to those shared key builders in:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_residual_families.py`
- Extended the cheap audit so this script cannot silently regress to local hard-coded residual bucket thresholds later.

### Strongest confirmed conclusion
- Science conclusions did not change; this is another transfer-layer integrity cleanup.
- The active support-family transfer and baseline follow-on layer now shares:
  - one source of truth for the primary family buckets
  - one source of truth for the residual bucket thresholds and key builders
- That removes another classification-drift surface in the frozen-frontier `5504` review stack.

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_residual_families.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`

### Exact next step
- Stay in deep review mode on the frozen-frontier suppressor transfer/follow-on layer.
- Review whether any remaining active follow-on scripts still duplicate other shared family-threshold constants or bucket builders instead of importing them from the transfer common helper.

### First concrete action
- Search the `support_family_transfer` lane and the immediate baseline/add4/pair follow-on scripts for local threshold literals like `3.5`, `19.0`, `71.0`, or repeated bucket-key reconstruction logic, then compare them against the shared helper surface.

## 2026-03-27 23:35 America/New_York

### Current state
- Continued the deep review thread on the frozen `5504` support-family transfer layer after reconciling git and worker state under the manual lock.
- Fixed one more shared-helper drift surface:
  - the active transfer scripts were each carrying their own copy of the “shared primary support-family buckets” set
  - instead of importing it from the shared transfer helper
- Centralized that bucket set in:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
- Repointed the active transfer/follow-on scripts to that shared constant:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_primary_bucket_profiles.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_satellites.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_residual_families.py`
- Added a cheap audit guard so those scripts cannot silently fork the primary-bucket definition later.

### Strongest confirmed conclusion
- Science conclusions did not change; this is another integrity cleanup.
- The shared support-family interpretation is now less brittle:
  - the primary bucket set `("rc0|ml0|c2", "rc0|ml1|c3")` now lives in one shared helper location
  - the main transfer scan, its primary-bucket profiles, the satellite summary, and the baseline non-peer residual follow-on all consume the same source of truth
- That closes one more low-grade drift surface in the active frozen-frontier transfer review layer.

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_primary_bucket_profiles.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_satellites.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_residual_families.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`

### Exact next step
- Stay in deep review mode on the frozen-frontier suppressor summary/reconstruction layer.
- Review whether any remaining active transfer/follow-on scripts still duplicate shared bucket logic or other classification constants instead of importing them from the shared helper path.

### First concrete action
- Search the `support_family_transfer` and immediate downstream baseline follow-on scripts for duplicated bucket literals or threshold constants, then compare them against the shared helper surface.

## 2026-03-27 23:07 America/New_York

### Current state
- Continued the deep review thread from the stable frozen `5504` checkpoint after reconciling git and worker state under the manual lock.
- Fixed one more stale-entrypoint issue in the suppressor latent-compression layer:
  - the older live latent-structure runner and helper were still defaulting to the older `480,672,912,1104` representative sample
  - but the repo’s current canonical compression-first workflow is now the frozen-frontier log-backed path
- Normalized the live sampler to the later completed representative sample `512,672,912,1168`, made its role explicit, and pointed it at the canonical frozen-frontier runner in:
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_latent_structure.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md`
- Added a cheap audit guard so the live latent-structure entrypoint cannot silently drift back into pretending it is the canonical frozen-frontier workflow.

### Strongest confirmed conclusion
- Science conclusions did not change; this is a review/integrity cleanup.
- The suppressor compression-first workflow is now explicit:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_frontier_compression.py` is the canonical current frozen-frontier entrypoint
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_latent_structure.py` is a historical live sampler with the later representative sample `512,672,912,1168`
- That closes one more stale-path ambiguity in the frozen-frontier review surface.

### Files and results changed in this run
- Repo-facing code/docs:
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_latent_structure.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`

### Exact next step
- Stay in deep review mode on the frozen-frontier suppressor summary/render layer.
- Review whether any remaining active entrypoints or summary helpers still describe old intermediate checkpoints as if they were canonical current workflow.

### First concrete action
- Search the frozen-frontier suppressor runner surface for older “representative” / “current” wording and compare each remaining live entrypoint against the now-explicit frontier-compression path.

## 2026-03-27 17:41 America/New_York

### Current state
- Resumed the deep review thread from the stable frozen `5504` checkpoint after protocol preflight, lock acquisition, and git reconciliation (`ahead 0 / behind 0`).
- Completed one bounded integrity step on the active low-overlap transfer review surface:
  - strengthened `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` with an execution-backed consistency check for the add4 exception scan path
- The new check now verifies that applying the live top add4 `rule_text` through the exception scan matcher reproduces the same `tp/fp/fn` confusion counts reported by `evaluate_rules(...)`.
- Ran the full audit after the change:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - result: `benchmark regression audit: ok`

### Strongest confirmed conclusion
- Science conclusions did not change; this is an integrity hardening step.
- The add4 exception scan is now guarded at two levels:
  - it derives the current best rule from the live helper path
  - and the audit now enforces that rule-text evaluation semantics stay consistent with the helper’s confusion counts
- This closes a remaining drift surface where parser/evaluator semantics could diverge silently even when both were still “live”.

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Runtime state docs:
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Verification:
  - full `benchmark_regression_audit.py` run passed after patch

### Exact next step
- Stay in deep review mode on the same low-overlap transfer helper surface.
- Continue searching for stale reconstruction/rendering assumptions that can drift away from live helper semantics without tripping current guards.

### First concrete action
- Inspect scripts that reconstruct bucket-local slices or parse rendered rule text in the `support_family_transfer` lane and add one more execution-backed guard where a helper/script semantic mismatch could still pass string-presence checks.
## 2026-03-27 18:42 America/New_York

### Current state
- Continued the deep review thread and found one more stale-default issue in the active suppressor entrypoints.
- The model helpers and script runners for the old mixed-bucket/residual-bucket path were still defaulting to the historical `1168` checkpoint even though the current frozen analysis surface is `5504`.
- Normalized these active defaults to `5504` in:
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_mixed_bucket_axes.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_rules.py`
- Added a cheap audit guard so those active defaults cannot silently drift back to `1168`.
- I also manually started the two no-arg script runs once to confirm they now enter the `5504` path, then stopped them after startup because they are much heavier at the frozen checkpoint and I did not want to leave unmanaged long jobs behind.

### Strongest confirmed conclusion
- The science interpretation did not change.
- The active suppressor entrypoint defaults are now aligned with the repo’s current frozen `5504` checkpoint instead of an old intermediate rung.
- Practical validation:
  - `py_compile` passed on the touched helper/script files
  - `benchmark_regression_audit.py` passed, including the new default-target guard
  - the two no-arg runners now start on the `5504` path, but they are runtime-heavy enough that the cheap audit should remain the confidence gate for this default-normalization fix

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_mixed_bucket_axes.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`

### Exact next step
- Stay in deep review mode.
- Review whether the older live latent-structure entrypoint should remain a historical live sampler or be redirected/clarified, since its defaults are still on an older representative ladder while the current compression-first science uses later frozen-frontier summaries.

### First concrete action
- Read:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_latent_structure.py`
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  around `pocket_wrap_suppressor_latent_structure_analysis(...)`, then compare that live default path against the current frozen-frontier compression workflow.

## 2026-03-27 18:35 America/New_York

### Current state
- Continued the deep review thread through the shared frozen-frontier reconstruction and summary helpers.
- Confirmed a real shared-parser drift:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_boundary_axes.py` still had its own weaker filename-only `variant_limit` parser
  - while `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_frontier_compression.py` had the shared parser used by the frontier-compression and physical-family-map layer
- When I added a renamed-log regression check, that surfaced a broader bug in the shared parser too:
  - it was only looking for `variant_limit=` on lines starting with `nonpocket_rows=...`
  - so renamed copies of valid frozen logs could still fail if filename fallback was unavailable
- Fixed the shared parser in `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_frontier_compression.py` to read `variant_limit=` directly from log text
- Then removed the duplicate weak parser from `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_boundary_axes.py` and reused the shared parser there
- Added a cheap audit guard so renamed frozen logs must still parse correctly

### Strongest confirmed conclusion
- The science interpretation did not change.
- The frozen-log helper layer is now materially safer:
  - the same `variant_limit` parser is shared across compression, physical-family reporting, and low-overlap reconstruction
  - renamed copies of valid frozen subtype logs now parse correctly without depending on filename shape

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_frontier_compression.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_boundary_axes.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Validation:
  - `python3 -m py_compile` on the touched parser/audit scripts passed
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` passed, including the new renamed-log parser check

### Exact next step
- Stay in deep review mode.
- Continue reviewing the remaining frozen-`5504` summary/render layer for helper/report drift, especially places where one script still duplicates logic that should now live in shared helpers.

### First concrete action
- Search the active frozen-`5504` review surface for any remaining duplicated parsing or reconstruction helpers, then compare them against the shared frontier-compression / low-overlap boundary helper path.

## 2026-03-27 17:36 America/New_York

### Current state
- Continued the deep review thread after pushing the live-rule exception-scan fix.
- Confirmed one more reporting-only drift in `/Users/jonreilly/Projects/Physics/README.md`:
  - the lay summary still described the frozen `5504` `00` core as ending in an “exact-but-fragile” closure family
  - that wording is stale relative to the current helper-backed result, where the rescue side is broad and only the baseline density cut remains locally tight

### Strongest confirmed conclusion
- The science read did not change.
- The honest current summary for the frozen `5504` center-spine `00` core is:
  - exact closure family
  - broad rescue side
  - locally tight baseline cut
- So the README now matches the technical section instead of understating the stability of the rescue family.

### Files and results changed in this run
- Repo-facing docs:
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`

### Exact next step
- Stay in deep review mode.
- Continue looking for stale summary/rendering language or small helper drift in the frozen `5504` low-overlap review surface, especially where older intermediate interpretations may still be present.

### First concrete action
- Search the README and active low-overlap scripts for remaining stale terms like `fragile`, `current best`, `residual`, or other older intermediate mechanism language, then compare them against the current helper-backed result.

## 2026-03-27 17:33 America/New_York

### Current state
- Continued the queued deep review thread from the stable `5504` checkpoint after reconciling worker state and refreshing the manual lock.
- Confirmed one more real helper/driver drift issue in the active low-overlap transfer layer:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_add4_exception_scan.py` claimed to inspect the current best add4 anchored-contrast rule, but it was actually hard-coded to one old conjunction instead of deriving the live top rule from the current bucket helper output
- Fixed the exception scan to derive the current best add4 rule via the live `evaluate_rules(...)` path and match rows from the returned `rule_text`, then added an audit guard so it cannot silently regress back to a frozen rule

### Strongest confirmed conclusion
- The science interpretation did **not** change, but the add4 exception scan is now trustworthy against future helper drift.
- After the fix, the live top add4 rule on the frozen `5504` `rc0|ml0|c2` bucket is still:
  - `delta_mid_left_bridge_bridge_closed_pair_max >= -1.000 and mid_candidate_bridge_bridge_closed_pair_max >= 9.000`
- The important change is operational:
  - the exception scan now recomputes that rule from the current helper output instead of silently assuming it
  - the benchmark audit now guards against the scan slipping back to a stale hard-coded conjunction

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_add4_exception_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Refreshed result:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-rc0-ml0-c2-add4-exception-scan-5504.txt`

### Exact next step
- Stay in deep review mode.
- Continue reviewing shared helper/render drift in the active low-overlap transfer layer, especially:
  - scripts that claim to inspect the “current best” rule but may still be pinning old thresholds or subsets
  - shared reconstruction / rendering helpers that can silently drift from the frozen `5504` checkpoint interpretation

### First concrete action
- Search the active low-overlap review surface for any remaining stale “current best” or hard-coded exception/closure drivers, then compare their output path against the live helper they are supposed to summarize.

## 2026-03-27 17:23 America/New_York

### Current state
- Started the queued deep review thread from the stable `5504` checkpoint.
- Reconciled worker/lock state first, then reviewed the active low-overlap / transfer helper path before making changes.
- Confirmed and fixed two real review issues:
  - duplicate edge-identity helpers were allowing `edge_identity_candidate_closed_fraction` / `open_fraction` to exceed `1.0`
  - shared support-family bucket rules were mixing peer-band rows back into the very buckets the rest of the analysis explicitly treats as non-peer-band

### Strongest confirmed conclusion
- The current science story did **not** change, but the helper layer is now more trustworthy.
- Review finding 1:
  - the edge-identity candidate fraction metrics were overcounting candidates because pocket and deep family passes incremented the same candidate cell separately
  - fixed in:
    - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector.py`
    - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_deltas.py`
  - regression guard added:
    - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
- Review finding 2:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_bucket_rules.py` was grouping raw family buckets without excluding `peer-band` rows, even though the transfer interpretation and follow-on scans explicitly excluded them
  - fixed so shared bucket scans now stay on the same non-peer-band slice as the rest of the bucket analysis
  - regression guard added in the audit
- After reruns:
  - the fixed `rc0|ml0|c2` topology scan still supports the same qualitative read
  - the fixed shared-bucket rules are now aligned with the non-peer-band interpretation used elsewhere

### Files and results changed in this run
- Repo-facing code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_deltas.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_bucket_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- Refreshed logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-bucket-rules-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-rc0-ml0-c2-topology-scan-5504.txt`

### Exact next step
- Continue the deep review thread rather than extending the bucket science thread.
- Review the shared helper path in `/Users/jonreilly/Projects/Physics/toy_event_physics.py` and the active transfer scripts for:
  - duplicated logic that can silently drift again
  - stale rendering/reporting helpers
  - helper/script mismatches that are not yet covered by cheap guards

### First concrete action
- Read the active low-overlap helper sections in `/Users/jonreilly/Projects/Physics/toy_event_physics.py`, then compare them against the current transfer scripts and README conclusions before deciding whether more fixes are needed.

## 2026-03-27 17:02 America/New_York

### Current state
- Reconciled worker state before continuing:
  - there was one unpushed local science commit (`7225b17`) from the hourly worker
  - reviewed it, pushed it, then acquired a clean manual lock for this continuation
- Completed two more bounded same-thread steps on the frozen `5504` low-overlap transfer thread:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_contrast.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_add4_exception_scan.py`

### Strongest confirmed conclusion
- In the shared `rc0|ml0|c2` bucket, candidate-anchored contrasts make the subtype drift substantially clearer even though they still do not fully close the bucket.
- add1 is now the left-dominant branch:
  - `delta_mid_left_bridge_bridge_closed_pair_max <= -1.000 and support_role_bridge_count >= 14.500`
  - `10/15` TP, `0` FP
- add4 is now the mid-dominant closed-bridge branch:
  - `delta_mid_left_bridge_bridge_closed_pair_max >= -1.000 and mid_candidate_bridge_bridge_closed_pair_max >= 9.000`
  - `8/8` TP, `5` FP
  - so this contrast removes all add4 false negatives
- pair-only remains the lower-support branch:
  - `support_role_bridge_count <= 13.500`
  - `8/9` TP, `5` FP
- The add4 exception scan then showed the remaining `5` false positives are structured, not noisy:
  - `3` are pair-only rows with the same strong mid-dominant closed-bridge signature but lower total support (`support_role_bridge_count = 13`)
  - `2` are add1 rows with balanced mid/left bridge-bridge closure (`delta_mid_left_bridge_bridge_closed_pair_max = 0`) at higher support (`support_role_bridge_count = 16`)
- Current best read:
  - the largest mixed shared bucket is no longer a vague residual
  - it is now a three-way overlap of:
    - true add4 mid-dominant closed-bridge rows
    - lower-support pair-only mimics
    - higher-support balanced add1 mimics

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_contrast.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_add4_exception_scan.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-rc0-ml0-c2-candidate-anchor-contrast-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-rc0-ml0-c2-add4-exception-scan-5504.txt`

### Exact next step
- Natural stopping point reached on the active `5504` bucket thread.
- Switch the main thread to a deep code review of the model and analysis layer.
- Treat the current `rc0|ml0|c2` result as the stable science checkpoint to review against, not the immediate next extension target.

### First concrete action
- Run a findings-first deep review pass over:
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - the active low-overlap / transfer scripts under `/Users/jonreilly/Projects/Physics/scripts`
  - `/Users/jonreilly/Projects/Physics/README.md`
- Focus on:
  - silent helper drift
  - duplicated analysis logic
  - stale conclusions or mismatched summaries
  - places where the current stable bucket/taxonomy read is not reflected honestly in code or docs

## 2026-03-27 16:44 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - repo preflight showed `main...origin/main` and `ahead 0 / behind 0`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap transfer thread:
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_interaction_motif_scan.py`
  - ran it to produce `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-rc0-ml0-c2-interaction-motif-scan-5504.txt`.

### Strongest confirmed conclusion
- In the largest mixed shared bucket (`rc0|ml0|c2`), enriching the basis with parsed candidate/support interaction motifs did **not** produce a new compact add4 separator.
- Added motifs included deep-vs-pocket event family ratios, bridge-role pairing present ratios, edge-length bins, and far-offset ratios.
- Best partial add4 behavior remained on the same branch already seen in the prior pass:
  - `edge_identity_closed_pair_count >= 57.500 and edge_identity_closed_pair_ratio >= 0.452` (`2/8` TP, `0` FP)
  - `edge_identity_closed_pair_count >= 57.500 and high_bridge_mid_count >= 0.500` (`4/8` TP, `2` FP)
- So the current read is sharper: bucket-local topology and interaction motifs are informative, but this motif family still does not close add4 inside the shared `rc0|ml0|c2` bucket.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_interaction_motif_scan.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-rc0-ml0-c2-interaction-motif-scan-5504.txt`

### Exact next step
- Stay on the frozen `5504` low-overlap basin and keep `rc0|ml0|c2` as the active mixed bucket.
- Move from aggregate motif counts toward candidate-anchored subtype contrasts inside the bucket, with emphasis on finding add4-specific closed-mid motifs that remain sparse in add1/pair-only.

### First concrete action
- Add one bounded `rc0|ml0|c2` candidate-anchored contrast pass that scores per-candidate bridge-neighborhood closures (mid vs left loading at matched closed-pair levels), then test compact subtype rules on those anchored contrasts.

## 2026-03-27 16:06 America/New_York

### Current state
- Checked worker/lock state before continuing:
  - repo was synced
  - no active Physics science child was running
  - a fresh manual lock was acquired for this continuation
- Added a reusable frozen-row transfer helper:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
- Then ran several bounded same-thread transfer steps on the frozen `5504` low-overlap rows:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_bucket_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_satellites.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_primary_bucket_profiles.py`

### Strongest confirmed conclusion
- The solved baseline-covered add1 family map does transfer into the broader frozen `5504` low-overlap basin at the coarse support-family level.
- All three low-overlap subtypes (`add1`, `add4`, `pair-only`) occupy the same main support buckets:
  - `rc0|ml0|c2`
  - `rc0|ml1|c3`
- They also all appear in the same left/lower `peer-band`:
  - `high_bridge_left_low_count >= 0.500`
- Shared primary-bucket occupancy is substantial:
  - `rc0|ml0|c2`: `15` add1, `8` add4, `9` pair-only
  - `rc0|ml1|c3`: `12` add1, `9` add4, `7` pair-only
- So the main transfer answer is now:
  - yes, the family map transfers
  - no, subtype identity does not collapse to a tiny exact rule **inside** those shared buckets
- The remaining divergence now lives inside shared primary buckets, not in subtype-exclusive branches.
- Bucket-local profile summaries already show the internal drift:
  - `rc0|ml0|c2`: add4 is more mid-loaded, add1 is more left-loaded, pair-only is the lower-support branch
  - `rc0|ml1|c3`: add4 is the strongest mid-loaded subtype, add1 keeps the stronger left-loading, pair-only is the higher-support / more right-loaded branch
- One bounded bucket-local topology scan on the largest mixed shared bucket (`rc0|ml0|c2`) now sharpens that drift:
  - add1 improves when support-edge density is low and left-loading is retained:
    - `edge_identity_support_edge_density <= 0.188 and high_bridge_left_count >= 0.500`
  - pair-only improves when support is lower and the local edge-identity layout stays more open:
    - `edge_identity_open_pair_count <= 62.500 and support_role_bridge_count <= 14.500`
  - add4 is still the hardest branch there, but its best partial rules are now clearly the more mid-loaded / more internally closed rows:
    - `edge_identity_closed_pair_count >= 57.500 and high_bridge_mid_count >= 0.500`
- So the next unresolved structure is no longer “does the family map transfer?”; it is “can the shared-bucket subtype drift be closed by richer bucket-local support-layout topology?”

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_common.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_bucket_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_satellites.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_support_family_transfer_primary_bucket_profiles.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-scan-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-bucket-rules-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-satellites-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-primary-bucket-profiles-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-support-family-transfer-rc0-ml0-c2-topology-scan-5504.txt`

### Exact next step
- Stay on the frozen `5504` low-overlap basin.
- Treat global family transfer as answered at the coarse support-bucket level.
- Move to the largest mixed shared bucket first:
  - `rc0|ml0|c2`
- Keep `rc0|ml0|c2` as the active mixed bucket.
- Move beyond scalar edge-density/open-ratio summaries and test richer bucket-local support-layout / topology features there.

### First concrete action
- Add one bounded `rc0|ml0|c2` continuation that augments the current topology scan with richer support-edge layout summaries or candidate/support interaction motifs, then test whether add4 can be separated more cleanly than the current partial mid-loaded/closed-support rules.

## 2026-03-27 15:47 America/New_York

### Current state
- Checked worker/lock state before continuing:
  - repo was synced
  - stale worker lock was released and replaced with a clean manual lock for this continuation
- Treated the baseline-covered add1 peer branch as solved at the coarse-band level and moved on to the remaining `35`-row non-peer baseline core.
- Added:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_buckets.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_family_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_residual_families.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_high_support_ml0_split.py`
- Also patched:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_band_scan.py`
  so it exports reusable baseline-band rows for follow-on decomposition work.

### Strongest confirmed conclusion
- The remaining non-peer baseline core is not one amorphous residual.
- Two dominant families already occupy `20/35` rows:
  - `rc0|ml0|c2` (`12` rows)
  - `rc0|ml1|c3` (`8` rows)
- On that dominant `20`-row subset, the split is exact on `high_bridge_cell_count` alone:
  - `<= 2.500` isolates the compact `c2` family
  - `>= 2.500` isolates the `c3` / mid-low family
- The remaining `15` rows then break into a few small satellites instead of a diffuse cloud:
  - right-center low-support `c2` triplet:
    - exact via `edge_identity_closed_pair_count <= 61.000`
  - low-support `ml2p` `c3` pair:
    - exact via `high_bridge_low_count >= 1.500`
  - high-support `ml0` branch:
    - `c3` triplet and `c4p` pair
    - exact branch-local size split via `high_bridge_cell_count <= 3.500` vs `>= 3.500`
  - high-support `ml1` `c4p` pair:
    - exact via `edge_identity_closed_pair_count >= 83.000 and high_bridge_mid_low_count >= 0.500`
- Current best read:
  - the baseline-covered add1 side now has a real solved family map:
    - peer branch
    - two dominant non-peer families
    - a few small satellites

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_band_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_buckets.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_family_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_residual_families.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_high_support_ml0_split.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-nonpeer-core-buckets-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-nonpeer-core-family-rules-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-nonpeer-core-residual-families-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-nonpeer-core-high-support-ml0-split-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep dense laddering paused.
- Treat the baseline-covered add1 family map as solved enough locally.
- Test whether the same family structure transfers into the broader low-overlap basin or is specific to the baseline-covered add1 slice.

### First concrete action
- Add one bounded transfer scan that compares:
  - the solved baseline-covered add1 families
  - against add4-sensitive and pair-only rows on the same frozen `5504` core
  - using the same baseline-band / closed-pair / support-bridge coordinates

## 2026-03-27 14:57 America/New_York

### Current state
- Checked worker/lock state before continuing:
  - worker had left real local science progress on the same frozen `5504` thread
  - that backlog was pushed first so remote matched the real current state
  - no active Physics worker was running
- Then manual continuation completed several bounded same-thread steps on the frozen `5504` center-spine `00` hard core.
- Added:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_agnostic_local_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_agnostic_residual_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_agnostic_top_cell_generalization.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_band_scan.py`

### Strongest confirmed conclusion
- The broader baseline-covered add1 peer branch now has both an exact anchor-local law and an exact coarse-band translation.
- Worker result that is now synced:
  - exact anchor-local closure on the `40` baseline-covered add1 rows:
    - `anchor_adj_bridge_count >= 3.500` (`5/5` TP, `0` FP)
- Manual continuation then tested whether that law was really coordinate-agnostic:
  - it is not
  - `max_candidate_adj_bridge_count >= 6.500` hits all `40/40` baseline-covered add1 rows
  - so dense candidate-local bridge neighborhoods are ubiquitous across this pool, not specific to the peer branch
- But one bounded coarse-band scan *does* recover an exact non-anchor statement:
  - `high_bridge_left_low_count >= 0.500` (`5/5` TP, `0` FP)
  - complement: `high_bridge_left_low_count <= 0.500` (`35/35` non-peer TP, `0` FP)
- Current best physical read:
  - dense local bridge neighborhoods are common across the whole baseline-covered add1 pool
  - the peer branch is the subset where that dense high-bridge local neighborhood appears in the left/lower candidate band

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_agnostic_local_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_agnostic_residual_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_agnostic_top_cell_generalization.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_band_scan.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-coordinate-agnostic-local-scan-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-coordinate-agnostic-residual-scan-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-coordinate-agnostic-top-cell-generalization-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-coordinate-band-scan-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep dense laddering paused.
- Treat the baseline-covered add1 peer branch as solved at the coarse-band level.
- Move on to the remaining `35`-row non-peer baseline core and test whether it has a comparable small family decomposition.

### First concrete action
- Add one bounded non-peer baseline-core decomposition pass seeded by:
  - `edge_identity_closed_pair_count`
  - `support_role_bridge_count`
  - `high_bridge_left_count`
  - `high_bridge_mid_low_count`
  - `high_bridge_right_center_count`

## 2026-03-27 14:41 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main` ahead by `2`.
  - pre-step helper push attempt failed with transient DNS resolution (`failure_kind=dns_failure`, host `github.com`), so run continued with one bounded same-thread science step.
- Completed one bounded same-thread continuation on the frozen `5504` center-spine `00` hard core:
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_candidate_anchor_residual_scan.py`
  - ran it to produce `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-candidate-anchor-residual-scan-5504.txt`.

### Strongest confirmed conclusion
- The broader baseline-covered add1 `(1, -2)` peer branch now has an exact closure on the same `40`-row pool (`5` peer vs `35` non-peer) under a bounded candidate-anchored local topology basis.
- Exact peer separator:
  - `anchor_adj_bridge_count >= 3.500` (`5/5` TP, `0` FP).
- Exact complement separator:
  - `anchor_adj_bridge_count <= 3.500` (`35/35` TP, `0` FP).
- Physical read:
  - peer rows are exactly those where anchor cell `(1, -2)` exists and is adjacent to a dense bridge neighborhood (at least four bridge support nodes; observed `7-8`), whereas non-peer rows keep this anchor-local bridge count at `0`.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_candidate_anchor_residual_scan.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-candidate-anchor-residual-scan-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep dense laddering paused.
- Test whether the new anchor-local exact branch law compresses further into a translation-invariant local support-neighborhood rule (without naming fixed candidate coordinates).

### First concrete action
- Add one bounded coordinate-agnostic local-neighborhood scan that searches for the same peer/non-peer closure pattern over all candidate cells, then check whether `(1, -2)` is uniquely singled out or part of a broader invariant class.


## 2026-03-27 13:41 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main` ahead by `1`.
  - pre-step helper push attempt failed with transient DNS resolution (`failure_kind=dns_failure`, host `github.com`), so run continued with one bounded same-thread science step.
- Completed one bounded same-thread continuation on the frozen `5504` center-spine `00` hard core:
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_topology_residual_scan.py`
  - ran it to produce `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-topology-residual-scan-5504.txt`.

### Strongest confirmed conclusion
- The broader baseline-covered add1 `(1, -2)` peer branch still has no exact closure under a richer bounded support-layout topology basis.
- On the same `40` baseline-covered add1 rows (`5` peer vs `35` non-peer), adding bridge-degree bins plus support-edge span/orientation bins (including bridge-bridge-only variants) leaves the best peer rule partial (`2/5` TP with `1` FP) and no exact separator appears.
- The newly tested coarse layout bins are mostly collapsed across this pool (`span>=4` and `skew` support-edge counts stay `0`), so these signatures do not supply the missing discriminator.
- Current best read: the peer marker `(1, -2)` is still real but broader baseline-side closure needs finer topology coordinates than support totals + sparse motifs + coarse span/orientation bins.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_topology_residual_scan.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-topology-residual-scan-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep dense laddering paused.
- Preserve sparse sentinels as guardrails only.
- Probe finer baseline-side support topology descriptors beyond coarse span/orientation bins (for example candidate-anchored edge-identity subevents or local two-hop bridge motifs).

### First concrete action
- Add one bounded candidate-anchored local-topology residual pass over the same baseline-covered add1 pool, then retest compact zero-FP closure for the `(1, -2)` peer branch.

## 2026-03-27 12:42 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main` with ahead/behind `0/0`.
- Completed one bounded same-thread continuation on the frozen `5504` center-spine `00` hard core:
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_branch_decomposition.py`
  - ran it to produce `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-branch-decomposition-5504.txt`.

### Strongest confirmed conclusion
- The broader baseline-covered add1 family does not close exactly under the seeded coarse basis (`edge_identity_closed_pair_count`, `support_role_bridge_count`) plus sparse branch-cell motifs.
- On the baseline-covered add1 pool (`40` rows), the `(1, -2)` peer branch is `5` rows and the complement is `35` rows.
- Using only support totals and non-target motif indicators (`(2, 1)`, `(4, 2)`, `(5, 0)`), the best predicates are partial (no exact separator):
  - best peer-branch rule reaches only `2/5` true positives (`motif_count >= 1.5`) with one false positive
  - support-total-only cuts are weaker (`edge_identity_closed_pair_count`/`support_role_bridge_count` each miss most peer rows)
- Current best read: the zero-distance peer branch marker `(1, -2)` is real but broader baseline-side closure now needs richer support-layout topology or additional coordinates beyond these sparse seeds.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_branch_decomposition.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-add1-branch-decomposition-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep dense laddering paused.
- Move from sparse motif checks to richer baseline-side support-layout topology for the broader baseline-covered add1 family.

### First concrete action
- Add one bounded baseline-covered add1 topology-residual pass that augments the current seed basis with support-edge layout signatures (e.g., bridge-bridge span/orientation bins or two-hop support motifs), then test whether any compact zero-FP closure appears for the `(1, -2)` peer branch.

## 2026-03-27 12:30 America/New_York

### Current state
- Checked worker/lock state before continuing:
  - no active Physics worker was running
  - stale manual lock from the previous baseline-side pass was released and reacquired cleanly for this session
- Stayed on the frozen `5504` center-spine `00` hard core and finished the baseline-side zero-distance continuation.
- Added:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_features.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_layout_diff.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_equivalence_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_physical_rule_card.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_candidate_cell_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_candidate_cell_generalization.py`
- Re-ran:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-zero-distance-features-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-zero-distance-layout-diff-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-zero-distance-equivalence-scan-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-zero-distance-physical-rule-card-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-zero-distance-candidate-cell-rules-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-baseline-candidate-cell-generalization-5504.txt`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` -> `ok`

### Strongest confirmed conclusion
- The baseline-side zero-distance branch is now compressed to a clear local family:
  - the rescued rows are a smaller all-bridge support graph than the basis-identical baseline peers
  - strongest exact local separator:
    - `edge_identity_closed_pair_count <= 62.000`
    - interval `[56.000, 68.000)`, width `12.000`
  - equivalent exact local cuts include:
    - `support_node_count <= 18.500`
    - `support_role_bridge_count <= 18.500`
    - `support_edge_count <= 31.500`
    - `support_edge_role_bridge__bridge_count <= 31.500`
- The candidate-cell side is narrower:
  - on the zero-distance subset, rescued rows exactly lack `pocket/deep cell (1, -2)`
  - but on the broader baseline-covered add1 pool that motif appears in only `5/40` rows
  - so `(1, -2)` is a local baseline-peer branch marker, not the broader baseline-side law
- Current best read:
  - broad baseline-side family: smaller, denser all-bridge support graph
  - local peer branch: extra `(1, -2)` plus occasional `(2, 1)`, `(4, 2)`, `(5, 0)` candidate cells

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_features.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_layout_diff.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_equivalence_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_physical_rule_card.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_candidate_cell_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_candidate_cell_generalization.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep dense laddering paused.
- Move from the zero-distance branch to the broader baseline-covered add1 family.
- Test whether that broader family still compresses on support-graph totals plus a small number of branch-cell motifs, or whether it needs a richer support-layout topology basis.

### First concrete action
- Add one bounded baseline-covered add1 branch decomposition pass seeded by:
  - `edge_identity_closed_pair_count`
  - `support_role_bridge_count`
  - presence/absence of `(1, -2)`, `(2, 1)`, `(4, 2)`, `(5, 0)` candidate cells

## 2026-03-27 11:55 America/New_York

### Current state
- Checked the worker state before continuing:
  - no detached Physics worker was active
  - worker had left real local science progress on the same frozen `5504` thread
  - pushed that backlog first so remote matched the real current state
- Then stayed on the frozen `5504` center-spine `00` hard core under the manual lock.
- Added:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_corridor_clause_robustness.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_neighbor_differences.py`
- Ran:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-corridor-clause-robustness-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-neighbor-differences-5504.txt`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` -> `ok`

### Strongest confirmed conclusion
- The canonical corridor-equivalence degeneracy is real, but not because the 1-term corridor clauses are row-drop fragile.
- The top 1-term corridor clauses all survive `45/45` single-row removals, and so does the interpretable 2-term role clause.
- The real difference is threshold slack:
  - 1-term corridor widths stay around `1.000`
  - the 2-term role clause keeps width `7.000`
- The neighbor-difference pass then sharpened the unresolved part:
  - there are baseline-covered add1 neighbors with **identical** visible pocket-basis coordinates to the rescued rows
  - `local-morph-Ǎ` and `local-morph-఩` are both at basis distance `0.000`
  - but they differ by concrete node-layout edits and are already captured by the baseline density clause
- So the current best read is:
  - rescue-side pocket/corridor laws are robust but highly non-unique
  - the visible rescue basis alone is not enough to explain rescued geometry
  - the remaining discriminating structure now lives on the baseline-density / finer support-layout side

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_corridor_clause_robustness.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_neighbor_differences.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-corridor-clause-robustness-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-neighbor-differences-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Stop searching for a unique rescue-side corridor law.
- Move the mechanism hunt to the discriminating baseline/finer-layout side.

### First concrete action
- Add one bounded baseline-side neighbor-difference pass comparing the rescued rows to the baseline-covered add1 neighbors at visible pocket-basis distance `0.000`, then identify which concrete support-edge density or layout edits separate them.

## 2026-03-27 11:41 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main` ahead by `2`.
  - pre-step helper push attempt failed with transient DNS resolution (`failure_kind=dns_failure`, host `github.com`), so run continued with one bounded same-thread science step.
- Completed one bounded same-thread continuation on the frozen `5504` center-spine `00` hard core:
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_corridor_equivalence_scan.py`
  - ran it to produce `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-corridor-equivalence-scan-5504.txt`.

### Strongest confirmed conclusion
- The bounded canonical corridor-equivalence pass settles minimality/non-uniqueness on this frozen core.
- Under scale/sign canonicalization over the corridor basis (weights in `{−2,−1,1,2}`, up to 3 terms):
  - `canonical_weight_classes_scanned = 656`
  - `exact_clauses_found = 796`
  - `exact_family_mask_matches = 796`
- Minimal exact family-mask closure is non-unique at one term (`minimal_term_count = 1`, `minimal_term_match_count = 5`), so the prior two-term role clause is interpretable but not minimal.
- Representative exact 1-term family-mask cuts include:
  - `delta_count_pocket_joined_bridge__pocket_only__present1 <= -2.500`
  - `delta_count_pocket_joined_pocket_only__pocket_only__present0 <= -6.500`
  - `delta_count_pocket_role_pocket_only__pocket_only <= -11.500`
- The current rescue closure therefore remains highly degenerate: joined-level corridor coordinates already carry exact rescue separation on the frozen core.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_corridor_equivalence_scan.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-corridor-equivalence-scan-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep dense laddering paused.
- Test whether the one-term exact corridor closures are structural or accidental by requiring support under small perturbations (e.g., leave-one-row-out / near-threshold stress) while preserving zero-FP add1 closure.

### First concrete action
- Add one bounded robustness pass that re-evaluates the top canonical 1-term corridor cuts under row-drop and ±0.5 threshold perturbation checks, then compare survival against the two-term role clause family.

## 2026-03-27 10:41 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main` ahead by `1`.
  - pre-step helper push attempt failed with transient DNS resolution (`failure_kind=dns_failure`, host `github.com`), so run continued with one bounded same-thread science step.
- Completed one bounded same-thread continuation on the frozen `5504` center-spine `00` hard core:
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_corridor_clause_scan.py`
  - ran it to produce `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-corridor-clause-scan-5504.txt`.

### Strongest confirmed conclusion
- The localized bridge-to-pocket / pocket-only deficit from the geometry-difference pass now closes directly in compact corridor language.
- On the same frozen core, an exact two-term role-level corridor clause matches the family-law rescue mask and width:
  - `delta_count_pocket_role_bridge__pocket_only + delta_count_pocket_role_pocket_only__pocket_only <= -14.500`
  - same rescued rows and same interval `[−18.000, −11.000)` (width `7.000`) as `delta_count_pocket_total <= -14.500`.
- Wider exact corridor clauses also exist within the bounded scan, for example:
  - `2*delta_count_pocket_role_bridge__pocket_only + delta_count_pocket_role_pocket_only__pocket_only <= -19.000`
  - interval `[−24.000, −14.000)` (width `10.000`).
- So the current rescue non-uniqueness remains, but the physical-language translation is stronger: the exact rescue family is expressible directly as a bridge-to-pocket plus pocket-only support deficit corridor.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_corridor_clause_scan.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-corridor-clause-scan-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep dense laddering paused.
- Test whether the role-level corridor closure can be made unique/minimal under canonical coefficient classes, or whether equivalent joined-level clauses remain unavoidable.

### First concrete action
- Add one bounded corridor minimality/equivalence pass that deduplicates scale/sign classes and reports exact family-mask matches ranked by term count then interval width for the corridor-only feature set.

## 2026-03-27 09:43 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main` with ahead/behind `0/0`.
- Completed one bounded same-thread continuation on the frozen `5504` center-spine `00` hard core:
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_basis_geometry_diff.py`
  - ran it to produce `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-basis-geometry-diff-5504.txt`.

### Strongest confirmed conclusion
- The low-tail geometry is now explicit rather than just basis-level.
- The exact nearest non-rescued cutoff anchor above the rescued corner is:
  - `base:taper-wrap:local-morph-௥`
  - with `(delta_count_pocket_present0, delta_count_pocket_present1, delta_count_pocket_role_pocket_only__pocket_only) = (-6, -5, -11)`.
- For both rescued rows (`base:taper-wrap:local-morph-ር`, `base:taper-wrap:local-morph-ᕚ`), the same concrete own-side pocket-support edit bundle closes that gap:
  - `+6` `count_pocket_role_bridge__pocket_only`
  - `+1` `count_pocket_role_pocket_only__pocket_only`
  - joined split: `+4` `count_pocket_joined_bridge__pocket_only__present0`, `+2` `count_pocket_joined_bridge__pocket_only__present1`, `+1` `count_pocket_joined_pocket_only__pocket_only__present1`
- Both rescued rows currently have only `bridge__bridge` pocket-role activity, so the non-uniqueness of visible-basis rescue masks is grounded in a specific missing bridge-to-pocket / pocket-only support corridor.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_basis_geometry_diff.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-basis-geometry-diff-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep dense laddering paused.
- Test whether the newly localized missing bridge-to-pocket / pocket-only support corridor can be captured by one compact signed corridor clause that keeps the same exact rescue mask without widening baseline leakage.

### First concrete action
- Add one bounded corridor-clause scan over `bridge__pocket_only` and `pocket_only__pocket_only` joined counts (present0/present1 split) and compare exact-mask reach and interval width against `delta_count_pocket_total <= -14.500`.

## 2026-03-27 08:51 America/New_York

### Current state
- Reconciled the worker’s signed-basis compression step before continuing:
  - local worker commit `436d724` (`Compress center-spine rescue into signed pocket basis`) was pushed successfully before new analysis
- Stayed on the same frozen `5504` center-spine `00` hard core under the manual lock.
- Added:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_basis_weight_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_basis_margin_profiles.py`
- Ran:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-basis-weight-scan-5504-canonical.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-basis-margin-profiles-5504.txt`

### Strongest confirmed conclusion
- The worker’s signed-basis result was real:
  - `delta_count_pocket_present0 + delta_count_pocket_present1 <= -14.500`
  - same rescue mask as `delta_count_pocket_total <= -14.500`
  - same width `7.000`
- But the canonical bounded weight scan showed that this two-term law is **not** unique.
- After removing coefficient-rescaling duplicates, the same exact family-mask match already appears in several visible-basis cuts, including 1-term laws:
  - `delta_count_pocket_present0 <= -8.000` with width `4.000`
  - `delta_count_pocket_present1 <= -6.500` with width `3.000`
- The margin-profile pass explains why:
  - the two rescued rows are isolated low-tail outliers on several pocket coordinates
  - next non-rescued values are already:
    - `present0 = -6`
    - `present1 = -5`
    - `pocket_only__pocket_only = -11`
    - `pocket_only__pocket_only__present0 = -6`
- So the current best read is:
  - the rescue side is genuinely robust
  - it compresses to the visible pocket basis
  - but the exact rescue mask is not unique there, because the rescued rows occupy an isolated low-tail corner across several pocket coordinates

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_basis_weight_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_basis_margin_profiles.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-basis-weight-scan-5504-canonical.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-basis-margin-profiles-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Treat the visible pocket-basis rescue mask as non-unique.
- Shift the question from “which basis law is minimal?” to “what geometric condition makes the rescued rows simultaneous low-tail outliers across several pocket coordinates?”

### First concrete action
- Add one bounded nearest-neighbor / geometry-difference pass comparing the two rescued rows to the nearest non-rescued rows just above the low-tail cutoffs, then identify which concrete pocket-support edits move `present0`, `present1`, and `pocket_only__pocket_only` together.

## 2026-03-27 08:41 America/New_York

### Current state
- Reconciled protocol preflight and state before mutation:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main` with ahead/behind `0/0`.
- Completed one bounded same-thread continuation on the frozen `5504` center-spine `00` hard core:
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_basis_composite_scan.py`
  - ran it to produce `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-basis-composite-scan-5504.txt`.

### Strongest confirmed conclusion
- The wide exact rescue law is already expressible in a small signed visible pocket basis on the same frozen core.
- The family-law reference remains:
  - `delta_count_pocket_total <= -14.500`
  - interval `[−18.000, −11.000)`, width `7.000`
- A compact two-term basis match achieves the same exact rescue mask and width:
  - `delta_count_pocket_present0 + delta_count_pocket_present1 <= -14.500`
  - same rescued rows, same interval `[−18.000, −11.000)`, width `7.000`
- A three-term composite from the bounded basis is exact with even larger interval slack:
  - `delta_count_pocket_present0 + delta_count_pocket_present1 + delta_count_pocket_role_pocket_only__pocket_only <= -26.000`
  - interval `[−30.000, −22.000)`, width `8.000`
- So the rescue side now compresses one level further into a small signed pocket basis, while the unresolved tight part remains the baseline density clause.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_basis_composite_scan.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-basis-composite-scan-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep the rescue side in compressed mode and test minimal signed-basis closure rather than widening frontier scans.
- Determine whether the `present0 + present1` exact rescue is the unique minimal two-term representation or one member of a small equivalent class under bounded coefficient choices.

### First concrete action
- Add one bounded minimality/equivalence pass over the same four pocket-basis features that:
  - includes integer weights in `{−2, −1, 1, 2}`,
  - limits to at most two nonzero terms,
  - and reports all exact zero-FP rescue forms that match the family-law rescue mask, ranked by term count then interval width.

## 2026-03-27 08:21 America/New_York

### Current state
- Continued the frozen `5504` center-spine `00` thread under the manual lock.
- Added:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_rescue_profiles.py`
- Ran both bounded passes plus the cheap audit:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-subfamily-decomposition-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-subfamily-rescue-profiles-5504.txt`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py` -> `ok`

### Strongest confirmed conclusion
- The wide exact rescue already compresses to a pocket-family deficit law:
  - `delta_count_family_pocket <= -14.500`
  - interval `[−18.000, −11.000)`, width `7.000`
- But it does not fully collapse to one tiny pocket micro-subfamily:
  - best exact single pocket-subfamily rescue is `delta_count_pocket_present0 <= -8.000`
  - interval `[−10.000, −6.000)`, width `4.000`
- The two rescued rows are not complementary edge cases; they share the same pocket-loss profile:
  - `delta_count_pocket_total = -18`
  - `delta_count_pocket_present0 = -10`
  - `delta_count_pocket_present1 = -8`
  - `delta_count_pocket_role_pocket_only__pocket_only = -12`
  - `delta_count_pocket_joined_pocket_only__pocket_only__present0 = -7`
- So the current best read is:
  - the rescue side is genuinely robust
  - it compresses to a pocket-family deficit
  - but the width-`7.000` rescue remains a stable composite pocket-loss pattern, not a single tiny micro-cause

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_rescue_profiles.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-subfamily-decomposition-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-pocket-subfamily-rescue-profiles-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Keep the rescue-side target narrowed to the composite pocket-loss law rather than the whole event family.
- Test whether that composite pocket-loss profile is already expressible as a small signed linear family over `present0/present1` and `pocket_only__pocket_only` counts, or whether it genuinely needs the broader `delta_count_family_pocket` aggregate.

### First concrete action
- Add one bounded composite-pocket profile pass that evaluates exact rescue predicates built from the small visible pocket basis:
  - `delta_count_pocket_present0`
  - `delta_count_pocket_present1`
  - `delta_count_pocket_role_pocket_only__pocket_only`
  - `delta_count_pocket_joined_pocket_only__pocket_only__present0`
then compare their exact-mask reach against `delta_count_family_pocket <= -14.500`.

## 2026-03-27 07:39 America/New_York

### Current state
- Reconciled lock/git state under the manual continuation session:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` showed the lock held by `manual-codex`.
  - git preflight showed `main...origin/main` with only the intended interval-fix edits in the working tree.
- Corrected the center-spine robustness method itself:
  - patched `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_rescue_window_scan.py`
  - patched `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_equivalence.py`
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_interval_priority_scan.py`
- Ran the corrected scans plus a bounded rule-card comparison against three exact rescues on the frozen `5504` center-spine `00` core.

### Strongest confirmed conclusion
- The overnight “exact-but-fragile” conclusion was overstated by a measurement bug.
- The old code counted sampled midpoint thresholds, not the actual mask-stable interval on the raw value axis, so binary event rescues and several numeric rescues were being misclassified as width `0`.
- After correction:
  - baseline remains `delta_edge_identity_support_edge_density <= 0.018`
  - exact add1 closure remains `42/0/0`, `45/45` overall
  - the strongest exact rescue is now clearly `delta_edge_identity_event_count <= -14.500`
    - interval `[−18.000, −11.000)`, width `7.000`
  - one more bounded decomposition step showed that this wide rescue already compresses to:
    - `delta_count_family_pocket <= -14.500`
    - same interval `[−18.000, −11.000)`, same rescued rows
  - other exact rescues also have real width:
    - `pair_selected_event_present_count >= 6.000` -> width `2.000`
    - `abs_delta_edge_identity_open_pair_count <= 22.500` -> width `1.000`
    - exact event predicates `ev_* >= 0.500` -> width `1.000`
- So the current best read is:
  - the closure family on the frozen `5504` center-spine `00` core is genuinely robust on the rescue side
  - the rescue family already compresses one level further into a pocket-family event deficit
  - the remaining locally tight part is the baseline density cut, not the rescue family

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_rescue_window_scan.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_equivalence.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_interval_priority_scan.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-rule-card-rescue-window-scan-5504-add1-vs-add4-corrected.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-rule-card-equivalence-5504-add1-vs-add4-corrected.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-interval-priority-5504-add1-vs-add4.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-rule-card-open-pair-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-rule-card-event-delta-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-rule-card-selected-events-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-event-family-decomposition-5504.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Treat dense laddering as paused for this thread.
- Keep the broad-rescue question narrowed to the pocket-family deficit law rather than the full event-count scalar.
- Decompose `delta_count_family_pocket <= -14.500` into smaller pocket-family role/presence subfamilies so we can see whether the same wide interval survives one more compression step.

### First concrete action
- Add one bounded pocket-family decomposition pass that splits the exact `delta_count_family_pocket <= -14.500` rescue into role-pair and `present0/present1` subfamilies on the same frozen `5504` bucket `00` rows, then test whether a still-smaller family-level summary preserves the exact width-`7.000` rescue mask.

## 2026-03-27 06:46 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main [ahead 10]` and clean tree.
- Required push-before-science reconcile attempted via helper and failed with transient DNS:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - result: `failure_kind=dns_failure`, `Could not resolve host: github.com`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_rescue_window_scan.py`

### Strongest confirmed conclusion
- With baseline fixed at `delta_edge_identity_support_edge_density <= 0.018` (`tp/fp/fn = 40/0/2`), there are multiple exact rescue-coordinate formulations that close add1 without add4 leakage (`42/0/0` add1, `45/45` overall), including:
  - `pair_distance_z >= {1.554, 1.584, 1.641, ...}`
  - `abs_delta_edge_identity_open_pair_count <= {19.000, 20.500, 21.500, 22.500, 24.000}`
- The best exact two-clause alternates therefore form a broader equivalent-family than one published cutpoint pair.
- But robustness remains locally brittle at this tested resolution:
  - every exact rescue clause has only one mask-stable threshold (`stable_thresholds=1`, width `0.000`);
  - no non-fragile multi-cutpoint exact interval was found.
- So the closure family is equivalent-but-fragile: exactness is preserved across many alternate rescue cutpoints, but each individual cutpoint remains locally tight.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_rescue_window_scan.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-rule-card-rescue-window-scan-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Run one bounded residual-boundary closure pass that searches for a compact two-clause closure where at least one clause has a genuinely non-fragile multi-cutpoint mask-stable interval (rather than a family of isolated exact cutpoints).

### First concrete action
- Add one bounded interval-aware clause scanner that treats threshold robustness as a first-class objective (maximize exact-closure mask stability window size before tie-breaking on rule simplicity), then re-evaluate rescue-coordinate and event-clause alternatives on the same fixed baseline.

## 2026-03-27 05:41 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main [ahead 9]` and clean tree.
- Required push-before-science reconcile attempted via helper and failed with transient DNS:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - result: `failure_kind=dns_failure`, `Could not resolve host: github.com`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_equivalence.py`

### Strongest confirmed conclusion
- The exact add1 closure now has a compact physical-language rule card on the same nearest-opposite edge-identity family:
  - `delta_edge_identity_support_edge_density <= 0.018 OR abs_delta_edge_identity_open_pair_count <= 22.500`.
- Closure remains exact on bucket `00`:
  - `tp/fp/fn = 42/0/0` on add1, `45/45` overall.
- Bounded neighboring-cutpoint equivalence did not reveal local threshold slack at this resolution:
  - baseline mask-stable window collapsed to `0.018` only;
  - rescue mask-stable window collapsed to `22.500` only.
- So the closure is now both exact and interpretable, but currently appears locally tight around both published cutpoints.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_equivalence.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-rule-card-equivalence-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Run one bounded closure-card robustness pass that checks equivalent rescue coordinates (`pair_distance_z` vs `abs_delta_edge_identity_open_pair_count`) and minimal two-clause alternates for any non-fragile cutpoint interval.

### First concrete action
- Add one small variant checker that fixes the baseline clause and scans rescue-coordinate formulations to report whether any exact zero-FP closure has a multi-cutpoint mask-stable window larger than the current single-threshold windows.

## 2026-03-27 04:40 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main [ahead 8]` and clean tree.
- Required push-before-science reconcile attempted via helper and failed with transient DNS:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - result: `failure_kind=dns_failure`, `Could not resolve host: github.com`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_residual_closure.py`

### Strongest confirmed conclusion
- Exception-local add1 residual closure now succeeds on the same nearest-opposite edge-identity family.
- Baseline add1 zero-FP rule remains:
  - `delta_edge_identity_support_edge_density <= 0.018` with `tp/fp/fn = 40/0/2` (`43/45`).
- A single bounded rescue clause closes both misses without add4 leakage:
  - `pair_distance_z >= 1.554` (equivalently `abs_delta_edge_identity_open_pair_count <= 22.500`).
  - Combined disjunction (`baseline OR rescue`) yields add1 exact closure `tp/fp/fn = 42/0/0` (`45/45` overall).
- So the dominant center-spine `00` hard core now has a compact symmetric closure in the current physical language.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_residual_closure.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-add1-residual-closure-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Translate the exact disjunction into a compact physical-language rule card and verify equivalent threshold variants remain stable under bounded predicate windows.

### First concrete action
- Add one small translation helper that emits a normalized two-clause rule card for the exact add1 closure (`density baseline + distance/open-pair rescue`) and runs a bounded threshold-equivalence check over neighboring cutpoints.

## 2026-03-27 03:40 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - git preflight showed `main...origin/main [ahead 7]` and clean tree.
  - required push reconcile before new science via helper failed with transient DNS:
    - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
    - failure: `failure_kind=dns_failure`, `Could not resolve host: github.com`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector.py`

### Strongest confirmed conclusion
- Add1-focused selector retuning on the same nearest-opposite edge-identity family does **not** close the remaining add1 misses.
- Best compact rows on this focused family are:
  - add1-side best remains `43/45` with `tp/fp/fn = 40/0/2`
    - `delta_edge_identity_support_edge_density <= 0.018`.
  - add4-side remains exact at `45/45` with `tp/fp/fn = 3/0/0`
    - `delta_edge_identity_support_edge_density >= 0.018 and pair_selected_event_present_count <= 6.000`.
- So the residual map stays one-sided: add4 closure is stable under selector-budget changes, but the add1-side two-row residual persists and likely needs explicit exception-local clause structure rather than more selector tuning.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-add1-selector-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Run one bounded exception-local add1 residual-closure pass that explicitly constructs clause candidates around the two surviving add1 misses against their nearest add4 anchors.

### First concrete action
- Add one bounded residual helper that materializes the two add1-miss neighborhoods in nearest-opposite edge-identity coordinates and tests whether a compact 1-2 clause disjunction can close `43/45` to exact without creating add4 false positives.

## 2026-03-27 02:43 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main [ahead 6]` and clean tree.
- Required push-before-science reconcile attempted via helper and failed with transient DNS:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - result: `failure_kind=dns_failure`, `Could not resolve host: github.com`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_deltas.py`

### Strongest confirmed conclusion
- Nearest-opposite candidate-local support-edge identity deltas close the add4 side of the `00` hard core exactly.
- Best compact rows on this family are:
  - add4-side exact best: `45/45` with `tp/fp/fn = 3/0/0`
    - `delta_edge_identity_support_edge_density >= 0.018 and pair_selected_event_present_count <= 3.500`.
  - add4-side single-feature near-best: `44/45` with `tp/fp/fn = 2/0/1`
    - `delta_edge_identity_closed_pair_count <= -20.500`.
  - add1-side best: `43/45` with `tp/fp/fn = 40/0/2`
    - `delta_edge_identity_support_edge_density <= 0.018`.
- Nearest-opposite anchors remain the same close triplet (`0.508`, `0.938`, `1.550`), but selected motifs now explicitly encode candidate-local pocket support-edge identity/presence signatures.
- So the residual map updates: the last add4 exception in the frozen `00` core is closed by local edge-pattern identity; the remaining non-exactness is now on the add1-side complement.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_deltas.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-edge-identity-deltas-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Run one bounded complementary closure pass focused on the remaining two add1 misses against nearest add4 anchors using the same edge-identity language.

### First concrete action
- Re-run the new edge-identity analyzer with a bounded add1-focused selector (same nearest-opposite map, same motif family) and test whether one compact add1-side clause lifts `43/45` toward exact closure without introducing add4 false positives.

## 2026-03-27 01:42 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main [ahead 5]` and clean tree.
- Required push-before-science reconcile attempted via helper and failed with transient DNS:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - result: `failure_kind=dns_failure`, `Could not resolve host: github.com`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_third_order_gated_deltas.py`

### Strongest confirmed conclusion
- Nearest-opposite third-order gated motif deltas (two-hop role motifs joined to local support-support edge co-presence) give a cleaner physical separator language but still do **not** close the dominant `00` hard core.
- Best compact rows on this family are:
  - add4-side best: `44/45` with `tp/fp/fn = 2/0/1`
    - `delta_third_order_gated_pair_count <= -2.500 and delta_third_order_support_edge_density >= 0.018`.
  - add4-side single-feature best: `43/45` with `tp/fp/fn = 1/0/2`
    - `delta_third_order_gated_pair_count <= -4.500`.
  - add1-side best: `43/45` with `tp/fp/fn = 40/0/2`
    - `delta_third_order_support_edge_density <= 0.018`.
- Nearest-opposite anchors remain the same close triplet (`0.508`, `0.938`, `1.550`), and selected motifs explicitly include gated third-order events like `tri:pocket:bridge:pocket_only:edge1`.
- So the residual separator tightens again: third-order gating improves physical interpretability (gated-pair deficit plus local support-edge-density contrast) but one add4 exception remains; the likely missing class is exception-focused local edge-pattern identity rather than more global scalar recombination.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_third_order_gated_deltas.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-third-order-gated-deltas-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Run a bounded single-exception closure pass that isolates the surviving add4 row against its nearest add1 neighbors using candidate-local support-edge identity motifs (not global delta scalars).

### First concrete action
- Add one `00`-bucket analyzer that emits per-candidate support-edge identity events around the nearest-opposite pair anchors (including explicit edge-presence/absence signatures for the final add4 survivor) and reruns compact closure search to test whether the last add4 exception closes beyond `44/45`.

## 2026-03-27 00:44 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main [ahead 4]` and clean tree.
  - required push reconcile before new science failed once with transient DNS via helper:
    - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
    - failure: `Could not resolve host: github.com`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_twohop_cooccurrence_deltas.py`

### Strongest confirmed conclusion
- Nearest-opposite two-hop support/candidate cooccurrence deltas improve the add4-side frontier but still do **not** close the dominant `00` center-spine hard core.
- Best compact rows on this new family are:
  - add4-side best: `44/45` with `tp/fp/fn = 2/0/1`
    - `delta_twohop_pair_count <= -2.500 and pair_distance_z <= 0.952`.
  - add4-side single-feature best: `43/45` with `tp/fp/fn = 1/0/2`
    - `delta_twohop_event_count <= -6.500`.
  - strongest zero-FP one-feature add4 row remains `41/45` with `0/1/3`
    - `abs_delta_twohop_candidate_touch_mean <= 0.133`.
  - add1-side best: `37/45` with `tp/fp/fn = 34/0/8`
    - `pair_distance_z >= 1.554`.
- The nearest-opposite anchors remain the same close triplet (`0.508`, `0.938`, `1.550`), while selected motifs now include higher-order candidate-local support-role cooccurrences (for example `twohop:pocket:bridge:pocket_only`) alongside support-touch count deltas.
- So the residual separator tightens again: two-hop matched interaction context is higher-signal than prior unary pair-delta summaries on add4 recall, but one add4 exception still survives; the likely missing class is third-order interaction context rather than additional scalar recombination.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_twohop_cooccurrence_deltas.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-twohop-cooccurrence-deltas-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Move from two-hop candidate-local support-role cooccurrence deltas to bounded third-order interaction context that joins those two-hop motifs with local support-support adjacency state.

### First concrete action
- Add one bounded `00`-bucket analyzer that emits nearest-opposite third-order motif deltas (two-hop candidate cooccurrence motifs gated by support-support edge co-presence) and reruns compact rule search to test whether the last add4 exception closes beyond the current `44/45` frontier.

## 2026-03-26 23:42 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - git preflight showed `main...origin/main [ahead 3]`.
  - required push reconcile before new science failed with transient DNS via helper:
    - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
    - failure: `Could not resolve host: github.com`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_pair_deltas.py`

### Strongest confirmed conclusion
- Nearest-opposite matched pair-delta support motifs add interpretable structure but still do **not** close the dominant `00` center-spine hard core.
- Best compact rows on this family are:
  - add4-side best: `43/45` with `tp/fp/fn = 1/0/2`
    - `delta_support_degree_mean >= 0.505`.
  - add4-side near-tie: `42/45` with `tp/fp/fn = 1/1/2`
    - `pair_distance_z <= 0.952 and pair_selected_event_present_count <= 4.500`.
  - strongest zero-FP add4 row remains `41/45` with `0/1/3`
    - `abs_delta_support_degree_mean <= 0.011`.
  - add1-side best: `40/45` with `tp/fp/fn = 37/0/5`
    - `pair_selected_event_present_count >= 4.500`.
- Nearest-opposite anchors stay the same close triplet for add4 rows (`0.508`, `0.938`, `1.550`), and selected signed-delta motifs are dominated by small `count_bridge_p2_d*` and local `pocket_only` offset swaps.
- So the residual separator tightens again: pair-conditioned nearest-opposite motif deltas add signal but still do not isolate the three add4 exceptions; the likely missing class is higher-order matched interaction context (for example two-hop support/candidate motif-cooccurrence deltas) rather than additional scalar recombination over current delta summaries.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_pair_deltas.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-pair-deltas-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Move from single signed motif deltas to higher-order matched interaction context (two-hop support/candidate motif-cooccurrence deltas) between each add4 row and its nearest add1 neighbor.

### First concrete action
- Add one bounded `00`-bucket analyzer that materializes nearest-opposite two-hop support/candidate cooccurrence-delta features and reruns compact rule search to test whether those higher-order deltas isolate the remaining three add4 exceptions beyond the current `43/45` frontier.

## 2026-03-26 22:40 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - git preflight showed `main...origin/main [ahead 2]`.
  - required push reconcile before new science failed with transient DNS via helper:
    - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
    - failure: `Could not resolve host: github.com`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_role_identity.py`

### Strongest confirmed conclusion
- Role-conditioned support-cell identity anchored to local candidate-family offset patterns adds interpretable local structure but still does **not** close the dominant `00` center-spine hard core.
- Best compact rows on this family are:
  - add4-side best: `41/45` with `tp/fp/fn = 0/1/3`
    - `identity_event_present_count >= 23.500` (equivalently `support_role_bridge_fraction <= 0.572` / `support_degree_mean >= 4.333`).
  - add1-side best: `19/45` with `tp/fp/fn = 16/0/26`
    - `identity_event_present_count <= 15.500`.
- Nearest-neighbor role-identity deltas remain narrow and local:
  - one add4 row differs by `count_bridge_p2_d2` versus nearby `pocket_only` signatures;
  - the other two are mostly swaps among a few anchored `bridge`/`pocket_only` offset signatures.
- So the residual separator tightens again: identity-conditioned support patterns are informative but still too coarse to isolate the three add4 exceptions; the likely missing class is finer matched-layout interaction identity across add4 rows and their nearest add1 neighbors.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_role_identity.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-role-identity-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Move from unary support-cell identity events to matched-pair interaction identity deltas keyed jointly to `(support role, support anchor, candidate-layout-difference signature)` for each add4 row versus its nearest add1 neighbor.

### First concrete action
- Add a bounded `00`-bucket analyzer that materializes pair-conditioned add4-vs-nearest-add1 motif-delta features and tests whether those delta motifs isolate add4 exceptions beyond the current `41/45` frontier.

## 2026-03-26 21:45 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main [ahead 1]`.
  - required push reconcile before new science failed with transient DNS via helper:
    - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
    - failure: `Could not resolve host: github.com`.
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_pair_context.py`

### Strongest confirmed conclusion
- Oriented support-pair and candidate-anchored support-subgraph context adds bounded structure but still does **not** close the dominant `00` center-spine hard core.
- Best compact rows on this new family are:
  - add4-side best: `42/45` with `tp/fp/fn = 1/1/2`
    - `candidate_shared_edge_fraction <= 0.684`
  - strongest zero-FP add4 rows remain at `41/45` with `0/1/3`.
  - add1-side best: `20/45` with `tp/fp/fn = 17/0/25`
    - `candidate_support_edge_mean >= 9.708`
- Nearest-neighbor oriented support-pair deltas remain narrow and mostly positional:
  - each add4 row differs from nearest add1 neighbors by one or a few oriented bridge-bridge events with shifted anchor coordinates.
- So the residual separator tightens again: oriented support-pair/subgraph context is informative but still too coarse to isolate the three add4 exceptions; the likely missing class is finer role-conditioned support-cell identity tied to specific candidate layouts.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_pair_context.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-27-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-pair-context-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Move from coarse oriented-pair summaries to role-conditioned support-cell identity anchored to matched candidate layouts for the three add4 exceptions versus nearest add1 neighbors.

### First concrete action
- Add a bounded `00`-bucket analyzer that keys support-cell identity by `(role, local anchor cell, adjacent candidate-family pattern)` and tests whether those identity-conditioned motifs isolate the add4 exception rows beyond the current `42/45` frontier.

## 2026-03-26 20:43 America/New_York

### Current state
- Reconciled protocol preflight in required order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git state before mutation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed clean sync (`main...origin/main`, ahead/behind `0/0`).
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap center-spine `00` hard core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_candidate_interactions.py`

### Strongest confirmed conclusion
- Explicit support-role/candidate-family interaction motifs (pair motifs plus local support `star` motifs) add bounded structure but still do **not** close the dominant `00` center-spine hard core.
- Best compact interaction rows are:
  - add4-side best: `41/45` with `tp/fp/fn = 0/1/3`
    - `bridge_pair_fraction <= 0.740` (or equivalent `pair_density` edge row)
  - add1-side best: `30/45` with `tp/fp/fn = 27/0/15`
    - `pair_density >= 1.047`
- Nearest-neighbor motif deltas are now explicit and small:
  - one add4 row has unique `star_bridge_p2_d2` vs nearest add1,
  - the other two add4 rows differ from nearest add1 neighbors by only one or two local `star` motifs.
- So the residual separator tightens again: pairwise support-candidate adjacency motifs are informative but still too coarse; the next likely missing class is finer support-cell interaction identity/context (oriented support-pair motifs or small support-subgraph context around matched candidate cells), not another scalar threshold recombination.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_candidate_interactions.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-candidate-interactions-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Move from pairwise support-candidate adjacency motifs to finer support-cell interaction identity/context around the matched candidate cells.

### First concrete action
- Build a bounded `00`-bucket runner that adds oriented support-pair / small support-subgraph context features anchored to the matched candidate layouts for the three add4 rows and their nearest add1 neighbors.

## 2026-03-26 19:35 America/New_York

### Current state
- Continued manually on the center-spine `00` hard core with the cooperative lock held as `manual-codex`.
- Completed a bounded bucket-specific cell-identity / candidate-layout block on the frozen `5504` low-overlap add1-vs-add4 core.
- New repo-facing scripts:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_candidate_identity.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_candidate_neighbors.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_identity_support_joined.py`

### Strongest confirmed conclusion
- The dominant `00` center-spine bucket (`42` add1, `3` add4) still does not close under the current summary families, but explicit candidate-cell identity is now the strongest family tested on that hard core.
- Bucket-specific candidate identity improves the add4 side to:
  - `43/45` with `tp/fp/fn = 1/0/2`
  - best rule: `deep_mirror_occ_dx4_dy3 >= 0.500 and pocket_mirror_void_right_fraction >= 0.292`
- The nearest-neighbor candidate-layout pass sharpens the mechanism:
  - all three add4 rows have `deep_only = []`
  - one add4 row has `pocket == deep`
  - the other two have `deep` as a strict subset of `pocket`
  - their nearest add1 neighbors instead retain larger or shifted deep/overlap layouts
- Joining the two strongest current families does **not** solve it:
  - joined add4 best falls back to `41/45`
  - joined add1 best stays `37/45`
- So the missing separator now looks specifically like explicit support-cell / candidate-cell interaction structure, not another threshold over current identity or support summaries.

### Files and results changed in this run
- Repo-facing files:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_candidate_identity.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_candidate_neighbors.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_bucket00_identity_support_joined.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-candidate-identity-5504-add1-vs-add4.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-candidate-neighbors-5504-add1-vs-add4.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-identity-support-joined-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` center-spine `00` hard core.
- Move past unary candidate/support summaries and probe explicit candidate-cell interaction structure between support cells and pocket/deep candidate cells.

### First concrete action
- Build a `00`-bucket runner that tests pairwise or small-subgraph support-cell / candidate-cell interaction motifs for the three add4 rows against their nearest add1 neighbors.

## 2026-03-26 19:14 America/New_York

### Current state
- Re-entered manually from the center-spine residual thread with repo sync intact and the cooperative lock acquired as `manual-codex`.
- Confirmed the new center-spine micro-bucket decomposition on the frozen `5504` low-overlap add1-vs-add4 core and then replaced the too-slow drafted hardest-bucket runner with a fast visible-field analyzer plus a nearest-neighbor pass.
- New repo-facing scripts:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_micro_buckets.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_neighbors.py`

### Strongest confirmed conclusion
- The `54`-row center-spine residual is already mostly decomposed:
  - `00`: `42` add1, `3` add4
  - `10`: `3` add1, `1` add4
  - `11`: pure add4 (`2`)
  - `01`: pure add1 (`3`)
- The tiny `10` bucket is actually solved on visible fields:
  - exact add4 rule: `id_deep_left_fraction >= 0.584`
- The dominant `00` bucket is the only truly hard residual:
  - best visible add1 row: `37/45`
  - no positive-recall exact visible add4 rule
- The three `00` add4 rows sit close to ordinary `00` add1 rows in the same visible space (nearest-neighbor distances `0.508`, `0.938`, `1.550`), so the remaining separator now looks like hidden support-cell / candidate-topology structure rather than one more missed visible threshold.
- A direct support-topology rerun on that same `00` core did not improve the frontier at all:
  - best add1 row is still `37/45`
  - add4 still has no positive-recall compact rule
  - `bridge_node_dx0_dy3` and `bridge_node_dx0_dy4` are already saturated across essentially the entire bucket
- So the residual target is now narrower and sharper: the missing separator is probably finer support-cell identity / candidate-topology interaction, not more bridge-density or bridge-event thresholding.

### Files and results changed in this run
- Repo-facing files:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_micro_buckets.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_neighbors.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-micro-buckets-5504-add1-vs-add4.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-hardest-bucket-rules-5504-add1-vs-add4.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-hardest-bucket-neighbors-5504-add1-vs-add4.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-bucket00-support-topology-5504-add1-vs-add4.txt`

### Exact next step
- Keep the center-spine filter fixed and drop the already-solved tiny buckets from the main thread.
- Stay only on the dominant `00` mixed core, and move past aggregate support-topology summaries into explicit support-cell identity / candidate-topology interaction structure.

### First concrete action
- Build a `00`-bucket runner keyed off the frozen center-spine micro-bucket membership that compares explicit support-cell identity patterns or candidate-cell interaction motifs for the three add4 rows against their nearest add1 neighbors.

## 2026-03-26 18:43 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled child/lock/git state before bounded work:
  - latest handoff reported no active detached science child.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed clean sync (`main...origin/main`, ahead/behind `0/0`).
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap add1-vs-add4 mixed core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_residual_bucket.py`

### Strongest confirmed conclusion
- Restricting to the translated central-spine regime (`bridge_center_spine_pair >= 0.500`) sharpens the residual target but still does **not** close it.
- The central-spine residual bucket has `54` rows (`48` add1, `6` add4).
- Best compact rows on joined identity+lobe+support features are still non-exact:
  - add4-side best: `50/54` with `tp/fp/fn = 2/0/4`
  - add1-side best: `43/54` with `tp/fp/fn = 37/0/11`
- So the bridge-language compression is stable, but the remaining add4 island inside that central-spine regime is still not closed by bounded scalar threshold recombination.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_center_spine_residual_bucket.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-residual-bucket-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap core and keep the central-spine regime fixed.
- Run one bounded residual-boundary continuation that tests a micro-bucket decomposition of the six central-spine add4 rows against nearby add1 neighbors (instead of global threshold recombination).

### First concrete action
- Add a residual micro-bucket decomposer keyed by central-spine add4 exception prototypes and rerun compact local closure per micro-bucket.

## 2026-03-26 17:43 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled child/lock/git state before bounded work:
  - latest handoff reported no active detached science child.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight showed `main...origin/main` ahead by `1`.
  - push reconcile attempt via helper failed with transient DNS (`Could not resolve host: github.com`).
- Completed one bounded same-thread continuation on the frozen `5504` low-overlap add1-vs-add4 mixed core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_identity_lobe_support_joined_closure.py`

### Strongest confirmed conclusion
- Joining candidate identity, lobe topology, and candidate-support bridge-event/subgraph features in one bounded closure pass still does **not** close the hard `87`-row mixed core.
- Best rows are unchanged from the support-subgraph step:
  - add1-side best: `82/87` with `tp/fp/fn = 48/5/0`
  - add4-side best: `75/87` with `tp/fp/fn = 27/0/12`
- The winning rows remain anchored by the same support bridge-event thresholds (`bridge_node_dx0_dy3`/`bridge_node_dx0_dy4`), so joined scalar recombination of current identity+lobe+support features appears saturated on this core.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_identity_lobe_support_joined_closure.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-identity-lobe-support-joined-closure-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap `87`-row core.
- Run one bounded residual-language continuation that translates the dominant support bridge-event thresholds into compact residual buckets and tests whether those buckets admit exact local closure beyond `82/87` and `75/87`.

### First concrete action
- Add a mixed-bucket residual translator keyed on `bridge_node_dx0_dy3` / `bridge_node_dx0_dy4` event states and rerun bucket-local closure within each residual bucket.


## 2026-03-26 16:40 America/New_York

### Current state
- Repo was clean and synced at start (`main...origin/main`, ahead/behind `0/0`) with no active detached science child in handoff state.
- Acquired the cooperative `physics-science` lock and completed exactly one bounded same-thread continuation on the frozen `5504` low-overlap add1-vs-add4 mixed core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_candidate_support_subgraph_bucket.py`

### Strongest confirmed conclusion
- Candidate-support subgraph/event topology adds real bounded signal but still does **not** close the hard `87`-row mixed core.
- Best rows on this new family are:
  - add1-side best: `82/87` with `tp/fp/fn = 48/5/0`
  - add4-side best: `75/87` with `tp/fp/fn = 27/0/12`
- So the read tightens again: per-event bridge participation and bridge-subgraph structure substantially improve separation (especially add1-side recall), but the unresolved boundary remains and likely needs a bounded joined closure with the existing identity+lobe features rather than this family in isolation.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_candidate_support_subgraph_bucket.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-candidate-support-subgraph-bucket-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap `87`-row core.
- Run one bounded joined closure continuation that combines:
  - candidate-identity event bits,
  - lobe/component bridge summaries,
  - and the new candidate-support bridge-event/subgraph features,
  then test whether compact 1-3 term clauses improve beyond `82/87` (add1) and `75/87` (add4).

### First concrete action
- Extend the existing identity+lobe two-clause closure runner with the new candidate-support bridge-event/subgraph feature block and rerun on the same `00` mixed bucket.

## 2026-03-26 18:04 America/New_York

### Current state
- Checked and reconciled worker state before new work:
  - there was no live worker after all
  - repo had two unpushed science commits from the worker and those are now pushed
  - `main...origin/main`, ahead/behind `0/0`
- Acquired a manual lock and completed three bounded same-thread continuations on the frozen `5504` low-overlap add1-vs-add4 mixed core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_bridge_event_translation.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_identity_bridge_language_closure.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_bridge_language_exceptions.py`

### Strongest confirmed conclusion
- The strongest support-subgraph signal compresses cleanly into a coarse bridge-language law.
- The dominant separator is a `center bridge spine`:
  - `bridge_node_dx0_dy3` and `bridge_node_dx0_dy4`
  - `add1` rows have that central spine essentially all the time (`center_pair~1.000`)
  - `add4` rows usually do not (`center_pair~0.154`)
- The translated bridge language retains almost all of the raw support-subgraph strength:
  - best add1 translated row: `82/87` via `bridge_center_spine_pair >= 0.500 and identity_deep_left_fraction >= 0.292`
  - best add4 translated row: `81/87` via `bridge_center_spine_pair <= 0.500`
- The residual structure is now sharply localized:
  - there are no add1 false negatives under the add1 translated rule
  - the remaining failures are a small island of add4 rows that already carry the full central bridge spine
- So the next science target is no longer the whole mixed bucket; it is the small add4 island inside the central-spine regime.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_bridge_event_translation.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_identity_bridge_language_closure.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_bridge_language_exceptions.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-bridge-event-translation-5504-add1-vs-add4.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-identity-bridge-language-closure-5504-add1-vs-add4.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-bridge-language-exceptions-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap `87`-row core.
- Restrict to the residual add4 island inside the central-bridge-spine regime and run one bounded micro-bucket probe:
  - central-spine-present rows only
  - compare the small add4 island against the dominant add1 set
  - test whether one extra subgraph or identity-topology clause closes just that island

### First concrete action
- Build a central-spine residual bucket runner keyed off `bridge_center_spine_pair >= 0.500` and classify the surviving add4 exceptions against the add1 core.

## 2026-03-26 16:30 America/New_York

### Current state
- Repo was clean and synced at start of this continuation (`main...origin/main`, ahead/behind `0/0`).
- No live worker was actually running; the remaining work was a synced handoff gap, not an active process.
- Acquired a manual lock and completed one bounded same-thread continuation on the frozen `5504` low-overlap add1-vs-add4 mixed core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_identity_lobe_two_clause_closure.py`

### Strongest confirmed conclusion
- Candidate identity remains the main low-overlap signal; lobe-topology interactions only weakly refine it.
- Joining identity and lobe topology still does **not** produce an exact add1/add4 split on the frozen `87`-row core.
- Best rows are:
  - add1-side: `69/87` via `deep_left_fraction >= 0.292 and event_present_count >= 1.500 and pocket_left_component_count <= 3.500`
  - add4-side: unchanged zero-FP identity anchor `event_present_count <= 1.500` (`16/0/23`)
- So the likely remaining signal is no longer “more scalar lobe topology.”
  - It is more explicit candidate-support subgraph structure or event-topology interactions.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_identity_lobe_two_clause_closure.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-identity-lobe-two-clause-closure-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap `87`-row core.
- Add one bounded candidate-support subgraph runner:
  - explicit pocket/deep candidate-support adjacency graph motifs,
  - per-event bridge participation rather than only aggregate bridge fractions,
  - small subgraph/lobe interaction signatures,
  - then rerun compact bucket-local closure on add1-vs-add4.

### First concrete action
- Implement a bucket-local candidate-support subgraph runner keyed off the completed `5504` log and the existing `00` mixed bucket split.

## 2026-03-26 14:41 America/New_York

### Current state
- Repo was clean and synced at start (`main...origin/main`, ahead/behind `0/0`) with no active detached science child in handoff state.
- Acquired the cooperative `physics-science` lock and completed exactly one bounded same-thread continuation on the frozen `5504` low-overlap add1-vs-add4 mixed core:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_candidate_lobe_topology_bucket.py`

### Strongest confirmed conclusion
- Candidate-lobe / support-graph topology is not the standalone missing law for the hard `87`-row mixed core.
- On this bounded lobe-topology family alone, best rows are weaker than the prior candidate-identity pass:
  - add1-side best: `56/87` with `tp/fp/fn = 23/6/25`
  - add4-side best: `62/87` with `tp/fp/fn = 32/18/7`
- Bridge-like means (`pocket~0.183`, `deep~0.233`, `support~0.407`) indicate real structure, but do not deliver compact closure by themselves.
- So the updated read is sharper: lobe topology contributes interpretable signal, but the unresolved separator likely requires bounded interaction terms between candidate-identity events and lobe-bridge topology, not either family in isolation.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_candidate_lobe_topology_bucket.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-candidate-lobe-topology-bucket-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap `87`-row core.
- Run one bounded closure continuation that joins:
  - existing candidate-identity features/events,
  - the new lobe/topology bridge/component features,
  - and compact local motif/visible terms,
  then test whether a small bounded two-clause family improves beyond the current `70/87` add1-side and `64/87` add4-side frontier.

### First concrete action
- Add a bounded identity-plus-lobe joined closure runner by extending the existing two-clause closure pipeline with the new candidate-lobe topology feature block.

## 2026-03-26 13:38 America/New_York

### Current state
- Repo was clean and synced at start of this continuation (`main...origin/main`, ahead/behind `0/0`) with no active worker lock.
- Stayed on the same frozen `5504` low-overlap add1-vs-add4 core and completed two bounded same-thread follow-ups:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_candidate_identity_bucket.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_candidate_identity_two_clause_closure.py`

### Strongest confirmed conclusion
- Candidate identity is real signal, but still not the whole hidden law.
- Side-resolved candidate-cell identity bits and mirrored-occupancy events improve the add1/add4 split:
  - candidate-identity best add1: `68/87` with `48/19/0`
  - candidate-identity best add4: `64/87` with `16/0/23`
- The strongest identity events are asymmetric placements like:
  - `deep_cell:dx1:dy4` / `pocket_cell:dx1:dy4` (add1-heavy)
  - `deep_cell:dx4:dy3` / `pocket_cell:dx4:dy3` (add4-heavier)
- Folding those identity bits back into a bounded two-clause closure still does **not** produce an exact add1/add4 split:
  - best add1-side row rises to `70/87`
  - best add4-side row stays the zero-FP identity cut `event_present_count <= 1.500` (`16/0/23`)
- So the hard low-overlap core still does not collapse into a tiny rule family even after adding candidate identity; the next likely missing class is explicit lobe/topology structure on the candidate support graph.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_candidate_identity_bucket.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_candidate_identity_two_clause_closure.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-candidate-identity-bucket-5504-add1-vs-add4.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-candidate-identity-two-clause-closure-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap `87`-row core.
- Add one bounded candidate-lobe / support-graph topology runner:
  - connected-component count on candidate-support neighborhoods,
  - left/right lobe symmetry and occupancy per candidate family,
  - bridge vs split support structure between pocket and deep candidate sets,
  - then rerun compact bucket-local closure on add1-vs-add4.

### First concrete action
- Implement a bucket-local candidate-lobe topology runner keyed off the completed `5504` log and the existing `00` mixed bucket split.

## 2026-03-26 13:25 America/New_York

### Current state
- Repo was clean and synced at start (`main...origin/main`, ahead/behind `0/0`) with no active worker lock.
- Continued on the same frozen `5504` low-overlap add1-vs-add4 core instead of widening the ladder.
- Added and ran one bounded same-thread closure probe:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_local_two_clause_closure.py`
  - log: `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-local-two-clause-closure-5504-add1-vs-add4.txt`

### Strongest confirmed conclusion
- The hard `87`-row low-overlap mixed bucket is **not** just waiting for a tiny disjunctive rewrite on the observables already in hand.
- On the joined bucket-local visible + motif + support-topology feature family, a bounded two-clause closure search over the top `24` single predicates still finds no exact zero-FP add1/add4 closure.
- Best rows remain partial:
  - add1-sensitive: `66/87` via `boundary_deep_fraction >= 0.392 and boundary_low_degree_fraction >= 0.309`
  - add4-sensitive: `62/87` via `boundary_deep_fraction <= 0.413 and core_deep_fraction <= 0.367`
- The surviving signal is still concentrated on local deep-boundary loading rather than on a new compact union-of-rules description.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_local_two_clause_closure.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-local-two-clause-closure-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap `87`-row core.
- Add one bounded candidate-identity / lobe-placement runner:
  - side-resolved pocket/deep candidate-cell identity bits,
  - column-band candidate occupancy / suppression structure,
  - small lobe-connectivity or mirrored-placement descriptors,
  - then rerun compact bucket-local closure on add1-vs-add4.

### First concrete action
- Implement a bucket-local candidate-identity runner keyed off the completed `5504` log and the existing `00` mixed bucket split.

## 2026-03-26 12:36 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and confirmed automation memory was absent at `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled child/lock/git state before bounded work:
  - latest handoff reported no active detached science child.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - git preflight was clean and synced (`main...origin/main`, ahead/behind `0/0`).
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
- One bounded same-thread science step was executed:
  - added and ran `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_local_support_topology_bucket.py` on the completed `5504` subtype log for `add1-sensitive` vs `add4-sensitive` inside the dominant `00` mixed bucket.

### Strongest confirmed conclusion
- The support-cell / candidate-topology family is now tested directly on the frozen `87`-row mixed core and remains non-closing under compact 1-3 term thresholds.
- The same dominant mixed bucket signature is unchanged:
  - `core_boundary_deficit_mean <= 0.222`
  - `boundary_fraction <= 0.826`
  - mixed bucket `00` with `87` rows (`48` add1, `39` add4)
- Bucket-local support-topology best rows are still partial:
  - add1 support-topology best: `66/87` (`41/14/7`)
  - add4 support-topology best: `63/87` (`19/4/20`)
- The envelope split is physically suggestive but not sufficient for closure:
  - add4 shows higher mirror-occupied candidate rates (`pmocc~0.750`, `dmocc~1.000`)
  - add1 keeps slightly higher boundary-neighbor overlap (`pbound~0.579`, `dbound~0.462`)
- So the remaining collision now points to finer candidate placement/identity structure rather than aggregate candidate-load or overlap fractions.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_local_support_topology_bucket.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-local-support-topology-bucket-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap core.
- Add one bounded candidate-identity refinement inside the dominant `00` mixed bucket:
  - candidate-cell column-band and side-resolved occupancy/suppression coordinates,
  - candidate-neighborhood identity features (which candidate cells are active, not just how many),
  - then rerun compact bucket-local closure for add1-vs-add4.

### First concrete action
- Implement a bucket-local candidate-identity runner keyed off the completed `5504` log and the existing `00` mixed bucket split.

## 2026-03-26 11:52 America/New_York

### Current state
- Continued on the localized `5504` low-overlap add1-vs-add4 thread without widening scope.
- Added two more bounded bucket-local probes:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_local_motif_bucket.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_local_combined_bucket.py`
- Both runs stayed inside the dominant mixed residual bucket from the prior split:
  - signature `core_boundary_deficit_mean <= 0.222`
  - `boundary_fraction <= 0.826`
  - mixed bucket `00` with `87` rows (`48` add1, `39` add4)

### Strongest confirmed conclusion
- The remaining low-overlap add1-vs-add4 collision is now sharply localized and still resistant to the current observable family.
- Bucket-local node-motif observables help a bit:
  - add1 local motif best improves to `69/87` (`35/5/13`)
  - add4 local motif best reaches `65/87`
- But even combining the strongest visible basin variables with the strongest bucket-local motif variables still does **not** close the core:
  - add1 local-combined best: `69/87`
  - add4 local-combined best: `66/87`
- So the next likely missing observable class is not “one more threshold on current summaries.”
  - It is more explicit support-cell / candidate-topology structure inside the mixed core.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_local_motif_bucket.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_local_combined_bucket.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-local-motif-bucket-5504-add1-vs-add4.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-local-combined-bucket-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap core.
- Add a support-cell / candidate-topology feature block inside the dominant mixed bucket:
  - pocket/deep-pocket candidate-cell counts
  - overlap of occupied nodes with pocket/deep candidate neighborhoods
  - mirrored candidate-cell occupancy / suppression structure
- Then rerun the bucket-local closure search on that same `87`-row core.

### First concrete action
- Implement a bucket-local support-topology runner keyed off the completed `5504` log and the existing `00` mixed bucket split.

## 2026-03-26 11:35 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled child/lock/git state before bounded work:
  - latest handoff reported no active detached science child.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - git preflight was clean and synced (`main...origin/main`, ahead/behind `0/0`).
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
- One bounded same-thread science step was executed:
  - added and ran `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_residual_buckets.py` on the completed `5504` subtype log for `add1-sensitive` vs `add4-sensitive`.

### Strongest confirmed conclusion
- The low-overlap unresolved boundary is now sharply localized rather than diffuse.
- On the frozen `5504` add1-vs-add4 table (`96` rows), the best 2-feature visible signature split is:
  - `core_boundary_deficit_mean <= 0.222`
  - `boundary_fraction <= 0.826`
- That split yields three buckets total:
  - two small pure add1 buckets (`7` rows and `2` rows)
  - one dominant mixed bucket (`87` rows: `48` add1, `39` add4)
- Inside that dominant mixed bucket, compact local closures remain partial:
  - best add1 local rule: `63/87` (`tp/fp/fn = 38/14/10`)
  - best add4 local rule: `64/87` (`tp/fp/fn = 18/2/21`)
- So the thread now tightens to a concrete target: the remaining collision is concentrated in one large low-overlap core bucket that likely needs more local/topological observables rather than more global threshold recombination.

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_residual_buckets.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-residual-buckets-5504-add1-vs-add4.txt`

### Exact next step
- Stay on the frozen `5504` low-overlap thread.
- Do one bounded refinement inside the dominant mixed bucket only:
  - add a genuinely local/topological observable family (for example local support-neighborhood motifs or pocket-boundary adjacency micro-structure),
  - then rerun the bucket-local closure search on those `87` rows.

### First concrete action
- Extend `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_residual_buckets.py` with a mixed-bucket-only feature block and rerun on `signature_key=00`.

## 2026-03-26 11:18 America/New_York

### Current state
- Stayed on the frozen `5504` low-overlap thread and took two more bounded latent-structure steps:
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_profile_axes.py`
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_combined_axes.py`
- Both runs reused the completed `5504` subtype log and avoided another classifier/frontier sweep.
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-profile-axes-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-combined-axes-5504.txt`

### Strongest confirmed conclusion
- The low-overlap basin is now better characterized, but still not compactly closed.
- Profile/asymmetry observables alone are informative but not sufficient:
  - best pairwise rows stay partial (`65/96`, `64/92`, `48/74`)
  - `pair-only` has the lowest profile asymmetry
  - `add4` has the strongest half-center imbalance / profile slope
- Combining the strongest visible boundary variables with the strongest visible profile variables still does **not** produce compact exact 1-3 term pairwise closures:
  - add1 vs add4: `71/96`
  - add1 vs pair-only: `70/92`
  - add4 vs pair-only: `61/74`
- So the best current hidden-driver read is:
  - `both-sensitive` is already a compactly solved loaded family
  - the low-overlap three-family basin is real
  - but it is not the shadow of a tiny single-conjunction rule family on the present observable set

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_profile_axes.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_combined_axes.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-profile-axes-5504.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-combined-axes-5504.txt`

### Exact next step
- Stay on the frozen `5504` low-overlap thread.
- Stop trying broader global threshold searches.
- Do a bucketwise residual decomposition inside the low-overlap basin:
  - split low-overlap rows by a small visible signature
  - then ask whether each bucket closes under compact exact rules
  - or identify which bucket is the real remaining collision

### First concrete action
- Implement a low-overlap residual-bucket runner keyed off the completed `5504` log, starting from the strongest mixed low-overlap pair.

## 2026-03-26 10:44 America/New_York

### Current state
- Stayed on the compression/order-parameter thread and avoided another ladder rung.
- Added a new frozen-row low-overlap boundary runner:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_boundary_axes.py`
- The runner reuses the completed `5504` subtype log for labels, reconstructs the corresponding geometries directly, and recomputes richer boundary observables without rerunning the expensive classifier sweep.
- Saved the result at:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-boundary-axes-5504.txt`

### Strongest confirmed conclusion
- The `5504` loaded-vs-boundary split is now stronger, not weaker:
  - `both-sensitive` remains the clean high-overlap loaded family
  - `add1`, `add4`, and `pair-only` remain the shared low-overlap boundary basin
- Adding richer visible boundary observables still does not collapse the three low-overlap families into compact exact 1-3 term pairwise rules:
  - add1 vs add4: best `71/96`
  - add1 vs pair-only: best `70/92`
  - add4 vs pair-only: best `61/74`
- The richer variables are informative, though:
  - `add1` carries the strongest low-degree and boundary-gap pressure
  - `pair-only` carries the strongest pocket gap
  - `add4` sits between them
- So the next hidden-driver target is now sharper again:
  - not more overlap-style observables
  - but profile/asymmetry variables that might resolve the low-overlap basin internally

### Files and results changed in this run
- Repo-facing science/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_low_overlap_boundary_axes.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-boundary-axes-5504.txt`

### Exact next step
- Stay on the same frozen `5504` low-overlap thread.
- Build a profile/asymmetry follow-up:
  - mirror asymmetry
  - left/right endpoint imbalance
  - centerline variation / span skew
  - any compact profile variable that can separate the low-overlap families once shell/core load is held fixed
- Keep sparse sentinels demoted to guardrails only.

### First concrete action
- Implement a focused low-overlap profile/asymmetry runner on top of the completed `5504` log and compare it against the current richer boundary-axis baseline.

## 2026-03-26 10:33 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled child/lock/git state before bounded work:
  - latest handoff reported no active detached science child; lock status was `free`.
  - git preflight was clean and synced (`main...origin/main`, ahead/behind `0/0`).
  - acquired worker lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
- One bounded same-thread science step was executed:
  - ran a new coarse physical-family translation pass on the completed `5504` subtype log:
    - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_physical_family_map.py --log /Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt`

### Strongest confirmed conclusion
- The stable four-family/two-regime read is now directly quantified in physical-language form at `5504`:
  - `both-sensitive` remains a compact exact loaded branch with `boundary_roughness >= 0.267 and deep_overlap_count >= 1.500` (`tp/fp/fn = 7/0/0`).
  - the other three families occupy the shared low-overlap boundary regime and still do not have compact exact pairwise splits on current coarse observables (best pairwise rows remain partial, topping out at `60/96`, `58/92`, and `47/74`).
- So the active unresolved target is unchanged but sharper: identify the smallest extra boundary variables that close add1/add4/pair-only separation inside that low-overlap regime.

### Files and results changed in this run
- Repo-facing science/integrity/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_physical_family_map.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-physical-family-map-5504.txt`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Stay on the same compression/order-parameter thread.
- Run one bounded low-overlap closure step using the `5504` table to test whether one additional boundary observable can exactly split one concrete low-overlap pair (start with add1 vs add4).

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_physical_family_map.py --log /Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt --max-terms 4 --rule-limit 4`

## 2026-03-26 09:48 America/New_York

### Current state
- Checked the overnight/early-morning worker state, released the stale `physics-science` lock from the finished `6016` timeout, and pushed the prior local backlog so `main` matched `origin/main` before new work.
- Tightened the widening runner itself:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py` now prints the parsed context before searching exact rules and no longer does an unbounded duplicate-heavy sweep of 1-2 term rule masks.
- Added a new log-backed compression/order-parameter pass:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_frontier_compression.py`
  - run on the completed `1232`, `3344`, `4992`, and `5504` frontier logs
  - saved at `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-frontier-compression-1232-3344-4992-5504.txt`
- Updated the automation plan so workers stop defaulting back to dense ladder chasing:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_JANITOR_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_SUMMARY_PROTOCOL.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/automation.toml`
  - `/Users/jonreilly/.codex/automations/physics-janitor/automation.toml`
  - `/Users/jonreilly/.codex/automations/physics-summary/automation.toml`

### Strongest confirmed conclusion
- The current phase is now much clearer:
  - stable four-family taxonomy
  - open and expanding membership boundary
  - frontier row count is mostly a coverage statistic, not the right scientific object
- The new compression pass makes that explicit:
  - rows `40 -> 84 -> 127 -> 138`
  - coarse signatures `17 -> 23 -> 25 -> 25`
  - after `3344`, almost every new row reuses an already-seen signature (`37/44`, `41/43`, `11/11`)
- The `5504` residual closure is therefore scientifically interesting, not just a system artifact:
  - the messy bucket collapsed into compact closures instead of forcing a fifth family
  - so the unresolved complexity looks like boundary structure inside the existing taxonomy, not a new mechanism family
- The visible frontier observables are still not the hidden exact law:
  - best two-axis compression on the `5504` logs reaches only `66/138`
  - best depth-2 tree reaches only `67/138`
  - both are anchored first on `deep_overlap_count`, then only weakly split by roughness/pocket/span

### Files and results changed in this run
- Repo-facing science/integrity/code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_frontier_compression.py`
  - `/Users/jonreilly/Projects/Physics/README.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_JANITOR_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_SUMMARY_PROTOCOL.md`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-frontier-compression-1232-3344-4992-5504.txt`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Stay in compression/order-parameter mode.
- Build a coarse physical family map for the stable `5504` regime:
  - translate `both-sensitive` as the high-overlap loaded family
  - translate the other three as low-overlap boundary families
  - then identify the smallest extra boundary variables needed to split `add1`, `add4`, and `pair-only`
- Use sparse sentinels only as guardrails after that translation step, not as the main thread.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_frontier_compression.py`

## 2026-03-26 07:33 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled carried-over child, lock, and git/push-first state before bounded work:
  - prior handoff named active child log `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt`.
  - `lsof` on that path showed no active writer; log tail includes completion trailer: `non-pocket suppressor subtype rules completed 2026-03-26T06:57:06 total_elapsed=4987.0s`.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `held` by `physics-science`.
  - git preflight: `main...origin/main [ahead 4]`; ahead/behind `4/0`.
  - required push-first helper attempt before bounded work: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics` -> `status=failed`, `failure_kind=dns_failure`, `ahead=4`, `behind=0`, `attempts_used=5`.
- One bounded same-thread completion step was executed:
  - parsed and classified the completed non-pocket subtype sweep at `variant_limit=5504`.
  - confirmed context remains `nonpocket_rows=138`, `subtype_count=4`.
  - extracted exact subtype rules: only `both-sensitive` yields exact compact 2-term rules (`tp=7`) with the anchored family `deep_overlap_count >= 1.500` paired with one secondary axis (including `boundary_roughness >= 0.299`, `core_boundary_deficit_mean >= 0.274`, `core_deep_fraction <= 0.443`, `mean_center <= -0.036`, `shell_boundary_deficit_mean >= 0.358`).

### Strongest confirmed conclusion
- Primary sparse-sentinel frontier conclusion remains unchanged at `4992` (`subtype_count=4`, non-pocket membership `127`, rotated exact both-sensitive 2-term family anchored on `deep_overlap_count >= 1.500`).
- New bounded continuation result at `5504`: the non-pocket subtype scan reproduces the same anchor-driven exact family for `both-sensitive`; no stronger closure across all non-pocket subtypes was established in this step.
- Prior finished `5504` mixed-bucket/residual conclusions remain in force.

### Files and results changed in this run
- Completed child result log parsed/classified:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Re-enter from lock/git preflight and run required push-first helper again.
- Once push is healthy, continue the same thread by widening the sparse-sentinel rung beyond `4992` with one bounded mechanism step and classify whether subtype count and non-pocket membership remain stable.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`

## 2026-03-26 03:35 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git/push-first state before bounded work:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - git preflight: `main...origin/main [ahead 3]`; ahead/behind `3/0`.
  - required push-first helper attempt before new work: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics` -> `status=failed`, `failure_kind=dns_failure`, `ahead=3`, `behind=0`, `attempts_used=5`.
  - acquired lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
- One bounded same-thread mechanism step was executed:
  - added and ran a focused add1-side disambiguation probe on the same frozen `5504` residual table for `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H`.
  - used a zero-FP add1 base clause (`abs_pocket_gap >= 0.058 and mean_center >= -0.035`) and tested one extra deterministic clause (`center_total_variation >= 1.5 and abs_low_gap in [0.145, 0.23] and mean_center <= -0.14`).
  - result: combined disjunctive add1 rule is exact on the frozen table (`tp/fp/fn = 9/0/0`, `remaining_add1_misses=0`).

### Strongest confirmed conclusion
- Primary sparse-sentinel frontier conclusion remains unchanged (`4992`, subtype count `4`, non-pocket membership `127`, rotated exact both-sensitive 2-term family anchored on `deep_overlap_count >= 1.500`).
- Mixed-bucket `5504` conclusion remains unchanged (one mixed add1/add4 bucket, exactly separable).
- Residual-thread conclusion advances: for `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H` at `5504`, compact two-clause disjunctive closures now exactly separate both sides on the frozen `13`-row table (`add4: 4/0/0`, `add1: 9/0/0`).

### Files and results changed in this run
- Added bounded same-thread add1 disambiguation probe utility:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_add1_disambiguation.py`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-residual-bucket-add1-disambiguation-5504-cross-n-span3plus-lowL-pocketH-overlap1-roughH.txt`
- Narrative update:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Re-enter from lock/git preflight and retry helper push first (`ahead` expected to increase by one commit).
- If push succeeds, return to the sparse-sentinel ladder and run one bounded wider rung beyond `4992`.
- If push remains DNS-blocked, avoid stacking extra metadata-only commits and continue with one bounded same-thread rung only when the repo state is otherwise reconciled.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`

## 2026-03-26 02:36 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git/push-first state before bounded work:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired lock: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - git preflight: `main...origin/main [ahead 2]`; ahead/behind `2/0`.
  - required push-first helper attempt: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics` -> `status=failed`, `failure_kind=dns_failure`, `ahead=2`, `behind=0`, `attempts_used=5`.
- One bounded same-thread mechanism step was executed:
  - isolated the lone false-negative row from the best add4-sensitive `12/13` latent-axis rule on the frozen `5504` residual table.
  - tested one additional deterministic disambiguation clause using existing observables (`low_core + low_shell` and `mean_center`) without rerunning the frontier.
  - result: the two-clause disjunctive add4 rule is exact on this table (`tp/fp/fn = 4/0/0`, `remaining_add4_misses=0`).

### Strongest confirmed conclusion
- Primary sparse-sentinel frontier conclusion remains unchanged (`4992`, subtype count `4`, non-pocket membership `127`, rotated exact both-sensitive 2-term family anchored on `deep_overlap_count >= 1.500`).
- Mixed-bucket `5504` conclusion remains unchanged (one mixed add1/add4 bucket, exactly separable).
- Residual-thread conclusion advances: for `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H` at `5504`, no exact single-conjunction 1-3 term separator was found, but the frozen `13`-row table is closed exactly by a compact two-clause disjunctive add4 rule after isolating the lone miss.

### Files and results changed in this run
- Added bounded same-thread disambiguation probe utility:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_fn_disambiguation.py`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-residual-bucket-fn-disambiguation-5504-cross-n-span3plus-lowL-pocketH-overlap1-roughH.txt`
- Narrative update:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Keep the same residual thread and test whether an analogous compact disjunctive closure exists for the add1 side on this same frozen `5504` table.
- If no similarly compact add1 closure appears, treat the add4 closure as the bounded endpoint and return to widening sparse-sentinel rungs from the `4992` anchor.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_fn_disambiguation.py --residual-log /Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-residual-bucket-rules-5504-cross-n-span3plus-lowL-pocketH-overlap1-roughH.txt`
  - then mirror that bounded check for an add1-targeted disambiguation clause on the same residual table.

## 2026-03-26 01:36 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled lock/git/push-first state before new science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired lock per protocol: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - `git status --short --branch` -> `main...origin/main [ahead 1]`; `git rev-list --left-right --count origin/main...main` -> `0 1`.
  - required push-first helper attempt: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics` -> `status=failed`, `failure_kind=dns_failure`, `ahead=1`, `behind=0`, `attempts_used=5`.
- One bounded same-thread mechanism step was executed:
  - added a targeted latent-axis probe script that operates on the completed `5504` residual case table rather than re-running the full frontier sweep.
  - executed the probe on `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-residual-bucket-rules-5504-cross-n-span3plus-lowL-pocketH-overlap1-roughH.txt`.
  - result: no exact 1-3 term add1/add4 separator on engineered thresholdable axes; best add4-sensitive row reaches `12/13` (`tp/fp/fn=3/0/1`) with `3` terms.

### Strongest confirmed conclusion
- No change to the primary sparse-sentinel frontier conclusion (`4992`, subtype count `4`, non-pocket membership `127`, rotated exact both-sensitive 2-term family anchored on `deep_overlap_count >= 1.500`).
- No change to mixed-bucket `5504` conclusion (one mixed add1/add4 bucket, exactly separable).
- Residual-thread conclusion tightened but unchanged: the unresolved coarse bucket `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H` remains non-exact at `5504`, and straightforward engineered latent axes on the frozen residual rows still do not yield an exact small separator.

### Files and results changed in this run
- Added same-thread latent-axis probe utility:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_latent_axes.py`
- New result log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-residual-bucket-latent-axes-5504-cross-n-span3plus-lowL-pocketH-overlap1-roughH.txt`
- Narrative update:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Stay on the same residual thread and run one bounded row-level disambiguation step on the lone remaining miss from the best `12/13` add4-sensitive latent-axis rule.
- If that miss can be isolated by one additional deterministic observable already present in the generator state, fold it into a compact exact rule and close the residual collision.
- If not, record this bucket as persistent non-exact behavior at `5504` under current thresholdable observables.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_latent_axes.py --residual-log /Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-residual-bucket-rules-5504-cross-n-span3plus-lowL-pocketH-overlap1-roughH.txt --max-terms 3 --rule-limit 12`
- Then inspect the single false-negative row under the best add4-sensitive `12/13` rule and test one extra bounded axis candidate on that same frozen table.

## 2026-03-26 00:33 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled active-child/lock/git state before new work:
  - `lsof /Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-residual-bucket-rules-5504-cross-n-span3plus-lowL-pocketH-overlap1-roughH.txt` shows no active writer, so the detached child finished.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired lock per protocol: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
  - `git status --short --branch` -> `main...origin/main` and `git rev-list --left-right --count origin/main...main` -> `0 0`.
- One bounded same-thread completion step was executed:
  - parsed the completed residual-bucket run at `variant_limit=5504` for `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H`.
  - residual table reports `13` rows and no exact small separator for add1-vs-add4 on the current observable family.

### Strongest confirmed conclusion
- Sparse-sentinel frontier conclusion remains unchanged: strongest confirmed frontier is still `4992` with subtype count `4`, non-pocket membership `127`, and rotated both-sensitive exact 2-term family anchored on `deep_overlap_count >= 1.500`.
- Mixed-bucket `5504` conclusion remains unchanged: one mixed add1/add4 bucket remains there and it is exactly separable.
- The residual follow-up adds a new bounded conclusion: the specific residual bucket `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H` is still non-exact at `5504` (`13` rows; best `12/13`; no exact 1-3 term rule).

### Files and results changed in this run
- Narrative update:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Completed log analyzed:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-residual-bucket-rules-5504-cross-n-span3plus-lowL-pocketH-overlap1-roughH.txt`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Stay on the same residual thread and run one targeted latent-axis or feature-augmentation probe inside this single unresolved `5504` coarse bucket to test whether exact add1-vs-add4 separation can be restored.
- If a candidate axis yields exact separation, record the compact rule and close the residual collision thread.
- If it remains non-exact, capture the best residual family and treat this as current observable-limit behavior at `5504`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_rules.py --variant-limit 5504 --coarse-signature 'cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H'`
  - with one added latent-axis candidate set (same thread) to test for exact closure.

## 2026-03-25 21:47 America/New_York

### Current state
- Investigated the seemingly stuck `5504` residual-bucket worker and confirmed it was CPU-bound inside the residual-rule search, not dead.
- Replaced that path with a repo-facing integrity/performance fix:
  - split residual-bucket row collection from rule search,
  - made the script print the residual case table before searching rules,
  - and changed the rule search to stop once the top exact rules are settled instead of exhaustively enumerating all 1/2/3-term combinations.
- Validated the change with:
  - `python3 -m py_compile /Users/jonreilly/Projects/Physics/toy_event_physics.py /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_rules.py`
  - a synthetic helper sanity check for `pocket_wrap_suppressor_residual_bucket_rule_rows(...)`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
- Intentionally stopped the manual `5504` rerun after validating the fix so the repo would not be left with an unmanaged long-running child under a manual lock.

### Strongest confirmed conclusion
- No mechanism conclusion changed in this integrity fix.
- The strongest confirmed sparse-sentinel frontier remains `4992`: subtype count `4`, non-pocket membership `127`, and the rotated both-sensitive exact 2-term family anchored on `deep_overlap_count >= 1.500`.
- The wider `5504` mixed-bucket conclusion also remains in force: exactly one mixed add1/add4 bucket remains there, and it is exactly separable.

### Files and results changed in this run
- Repo-facing integrity/performance fix:
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_rules.py`
- Partial rerun log intentionally abandoned after validation:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-residual-bucket-rules-5504-cross-n-span3plus-lowL-pocketH-overlap1-roughH-optimized.txt`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Re-run the `5504` residual-bucket search under the optimized flow:
  - `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H`
- If that residual bucket is now exactly separable with 1-2 terms, close the latent-collision thread at this rung and return to sparse sentinels.
- If it still needs 3 terms or remains non-exact, record the best residual rule family and then decide whether that bucket is a genuine remaining hidden-driver exception.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_rules.py --variant-limit 5504 --coarse-signature 'cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H'`

## 2026-03-25 13:32 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Reconciled active-child and lock state before any new work:
  - `lsof /Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-mixed-bucket-axes-5504.txt` reports no active writer (detached child completed).
  - completion trailer confirmed in log: `pocket-wrap suppressor mixed-bucket axes completed 2026-03-25T12:26:28 total_elapsed=5865.8s`.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`.
  - acquired lock per protocol: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`.
- Reconciled git state before finalization:
  - `git status --short --branch` -> `main...origin/main`
  - `git rev-list --left-right --count origin/main...main` -> `0 0`
  - `HEAD=ed10550`, `origin/main=ed10550`.
- One bounded same-thread completion/finalization step was executed:
  - parsed the finished mixed-bucket `5504` log and classified outcome.
  - result table reports `rows=1` mixed add1/add4 bucket and an exact 2-term separator (`7/7`, `tp/fp/fn = 4/0/0`) for `cross=n|span=<3|low=L|pocket=L|overlap=1|rough=L`, anchored on `boundary_fraction <= 0.895` plus one additional boundary-threshold term.
  - no detached child remains active after this step.

### Strongest confirmed conclusion
- The primary sparse-sentinel frontier conclusion is unchanged: strongest confirmed frontier remains `4992` with subtype count `4`, non-pocket membership `127`, and the rotated both-sensitive exact 2-term family anchored on `deep_overlap_count >= 1.500`.
- Mixed-bucket thread conclusion advanced: at `5504`, the active mixed add1/add4 bucket count is `1` and that remaining bucket is exactly separable, so the earlier mixed-bucket collision is not an exactness blocker at this wider rung.

### Files and results changed in this run
- Narrative update:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Completed log analyzed:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-mixed-bucket-axes-5504.txt`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Stay on the same mixed-bucket thread and run a bounded residual-bucket rule search at `variant_limit = 5504` for the historically unresolved `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H` coarse signature.
- If it is now exact with 1-2 terms, close the latent-collision thread and return to widening sparse-sentinel rungs.
- If still non-exact, capture the best residual predicates and queue a targeted feature-axis follow-up.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_rules.py --variant-limit 5504 --coarse-signature 'cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H'`

## 2026-03-25 08:10 America/New_York

### Current state
- Investigated whether the automation-flow fix also solved the repeated `dns_failure` push reports.
- Confirmed the lock/protocol fix was necessary but not sufficient:
  - it prevents overlapping workers and metadata churn,
  - but it does not by itself remove intermittent background resolver failures.
- Found one additional setup issue in `/Users/jonreilly/Projects/Physics/scripts/automation_push.py`:
  - the helper was doing its own preflight DNS lookup before attempting `git ls-remote`,
  - which could create false early `dns_failure` results in flaky network conditions.
- Patched the helper to:
  - remove the separate preflight DNS gate,
  - rely on real `git ls-remote` / `git push` attempts for classification,
  - and use a slightly longer retry ladder (`5` attempts, `2,5,15,30,60` seconds).

### Strongest confirmed conclusion
- No mechanism conclusion changed in this fix.
- The strongest confirmed frontier is still `4992`: subtype count `4`, non-pocket membership `127`, and the same rotated exact both-sensitive 2-term family anchored on `deep_overlap_count >= 1.500`.
- The DNS issue now looks like two layers:
  - fixed setup issue: premature helper-side DNS gating
  - remaining likely environment issue: intermittent background resolver/network instability during unattended runs

### Files and results changed in this run
- Repo-facing helper fix:
  - `/Users/jonreilly/Projects/Physics/scripts/automation_push.py`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Re-run `variant_limit = 5504` under the corrected worker protocol and hardened push helper.
- If the rerun completes, classify hold vs transition relative to `4992`.
- If higher bounded runs still die after startup, switch to debugging the runner lifecycle rather than the push path.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-25 08:03 America/New_York

### Current state
- Reviewed the overnight worker transcript and confirmed a real automation-flow bug:
  - a detached `5504` rerun was launched,
  - the worker then released the cooperative lock,
  - and tracked metadata commits were created while the rerun was still in progress.
- Patched the worker protocols so detached science children now keep the lock, in-progress runs update only runtime handoff/memory, and tracked work-log commits are reserved for finished stable results or real repo-facing integrity fixes.

### Strongest confirmed conclusion
- No mechanism conclusion changed in this fix.
- The strongest confirmed frontier is still `4992`: subtype count `4`, non-pocket membership `127`, and the same rotated exact both-sensitive 2-term family anchored on `deep_overlap_count >= 1.500`.
- The important change is operational: hourly workers should no longer advertise the repo as `free` while a detached science child is still running, and they should stop generating tracked metadata-only commits for in-progress reruns.

### Files and results changed in this run
- Repo-facing protocol fixes:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_JANITOR_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_SUMMARY_PROTOCOL.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Installed automation prompt fixes:
  - `/Users/jonreilly/.codex/automations/physics-autopilot/automation.toml`
  - `/Users/jonreilly/.codex/automations/physics-janitor/automation.toml`
  - `/Users/jonreilly/.codex/automations/physics-summary/automation.toml`

### Exact next step
- Resume the sparse-sentinel thread from a clean state.
- Re-run `variant_limit = 5504` under the corrected worker protocol.
- If the rerun completes, classify hold vs transition relative to `4992`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-25 07:18 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before new work:
  - `git status --short --branch` -> `main...origin/main`
  - `git rev-list --left-right --count origin/main...main` -> `0 0`
  - `HEAD=ab9df10`, `origin/main=ab9df10`.
- Push-first helper was not needed before new work because the repo was not ahead.
- One bounded same-thread integrity step was started:
  - prior `5504-max5600` log was confirmed incomplete (startup line only, no active writer).
  - launched a controlled rerun:
    - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 5504 --max-seconds 900 > /Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max900-rerun.txt`
  - rerun is active at handoff time (`lsof` shows `Python PID 23406` holding the rerun log).
- End-of-loop checkpointing:
  - committed run-state updates as `3b27c18` (`Record active 5504 bounded rerun state`), `54641d0` (`Finalize 5504 rerun checkpoint state`), and `88c100d` (`Reconcile rerun checkpoint push state`).
  - final helper push attempt: `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics` -> `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=3`, `behind=0`.
  - released cooperative lock (`python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py release --owner physics-science`) and verified final status `free`.

### Strongest confirmed conclusion
- No mechanism conclusion changed in this run.
- The strongest confirmed frontier remains `4992`: subtype count `4`, non-pocket membership `127`, and the same rotated exact both-sensitive 2-term family anchored on `deep_overlap_count >= 1.500`.

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Active rerun log path:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max900-rerun.txt`

### Exact next step
- Re-enter from lock preflight and check whether the active `5504-max900-rerun` process has completed.
- If complete, parse subtype/rule tables and classify hold vs transition relative to `4992`.
- If still active, continue to avoid overlap and defer launching any additional science run.

### First concrete action
- Execute:
  - `lsof /Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max900-rerun.txt`

## 2026-03-25 06:20 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 5]`
  - `git rev-list --left-right --count origin/main...main` -> `0 5`
  - `HEAD=d578d15`, `origin/main=0388355`.
- Required push-first helper attempt before new work:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=5`, `behind=0`.
- One bounded same-thread mechanism step was started:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 5504 --max-seconds 5600 > /Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt`
  - run remains active at handoff time (`lsof` shows `Python PID 11906` holding the log).
  - log currently contains startup line only (`non-pocket suppressor subtype rules started 2026-03-25T06:18:17`).
- End-of-loop checkpointing:
  - skipped creating a metadata-only commit while DNS failures still block pushing previously queued commits.
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics` -> `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=5`, `behind=0`.
  - released cooperative lock (`python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py release --owner physics-science`) and verified final status `free`.

### Strongest confirmed conclusion
- No mechanism conclusion changed in this run.
- The strongest confirmed frontier remains `4992`: subtype count `4`, non-pocket membership `127`, and the same rotated exact both-sensitive 2-term family anchored on `deep_overlap_count >= 1.500`.

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Active log path:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt`

### Exact next step
- Re-enter from lock preflight and check whether the active `5504-max5600` process has completed.
- If completed, parse subtype/rule tables and classify hold vs transition relative to `4992`.
- If still active, continue to avoid overlap and defer launching any additional science run.

### First concrete action
- Execute:
  - `lsof /Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt`

## 2026-03-25 05:19 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 3]` with local worklog edit pending
  - `git rev-list --left-right --count origin/main...main` -> `0 3`
  - `HEAD=602393e`, `origin/main=0388355`.
- Required push-first helper attempt before new work:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=3`, `behind=0`.
- One bounded same-thread mechanism/integrity step completed:
  - verified the in-flight `4992-max5600` run had completed (`lsof` no longer reports an active writer on `/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992-max5600.txt`).
  - parsed and compared the completed `4992` table against `4480` to classify frontier behavior.
- End-of-loop checkpointing:
  - committed updates as `5f13636` (`Record sparse-sentinel frontier extension through 4992`).
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics` -> `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=4`, `behind=0`.
  - released cooperative lock (`python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py release --owner physics-science`) and verified final status `free`.

### Strongest confirmed conclusion
- `4992` confirms continuation of the same post-`3984` rotated both-sensitive regime.
- Frontier summary at `4992`:
  - subtype count remains `4`
  - non-pocket membership grows `115 -> 127`
  - exact both-sensitive family remains 2-term and anchored on `deep_overlap_count >= 1.500` with `tp=7`
  - four of five best exact both-sensitive rules are unchanged versus `4480`; one shell term tightens slightly (`shell_boundary_deficit_mean >= 0.358` vs `>= 0.352`).

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Completed log analyzed:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992-max5600.txt`

### Exact next step
- Retry push helper first on the next loop while ahead.
- If push remains blocked only by transient DNS, run the next sparse sentinel rung at `variant_limit = 5504` with the same bounded guard and classify hold vs transition against `4992`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-25 04:18 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `held` (`owner=physics-science`)
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 3]` with local worklog edit pending
  - `git rev-list --left-right --count origin/main...main` -> `0 3`
  - `HEAD=602393e`, `origin/main=0388355`.
- Required push-first helper attempt before new work:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=3`, `behind=0`.
- One bounded same-thread integrity step completed:
  - verified in-flight `4992` status without overlap by checking open-handle/process ownership and log growth:
    - `lsof /Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992-max5600.txt` -> `Python PID 97603` still holding the log
    - `wc -c` + `tail` on the same log -> file remains `64` bytes with only startup line (`non-pocket suppressor subtype rules started 2026-03-25T03:18:15`).
  - skipped launching any second science run to avoid overlapping the active thread.

### Strongest confirmed conclusion
- No mechanism conclusion changed in this run.
- The strongest confirmed frontier remains `4480`: `4` subtypes, non-pocket membership `115`, and the same stable rotated 2-term both-sensitive exact family anchored on `deep_overlap_count >= 1.500` plus one boundary/core term.

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Active log path (unchanged, still in-flight):
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992-max5600.txt`

### Exact next step
- Re-enter from lock preflight and re-check completion of the active `4992-max5600` process.
- If complete, parse subtype/rule tables and classify hold vs transition relative to `4480`.
- If still active, continue to skip overlap and defer launching new science.

### First concrete action
- Execute:
  - `lsof /Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992-max5600.txt`

## 2026-03-25 03:27 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 3]`
  - `git rev-list --left-right --count origin/main...main` -> `0 3`
  - `HEAD=602393e`, `origin/main=0388355`.
- Push-first helper run before new work:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=3`, `behind=0`.
- One bounded same-thread mechanism step was started:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 4992 --max-seconds 5600 > /Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992-max5600.txt`
  - run is still active at handoff time (`lsof` shows `Python PID 97603` holding the log).
  - this sandbox denies process termination (`kill` not permitted), so final status/tables were not yet observable in this loop.

### Strongest confirmed conclusion
- No mechanism conclusion changed in this run.
- The strongest confirmed frontier remains `4480`: `4` subtypes, non-pocket membership `115`, and the same stable rotated 2-term both-sensitive exact family anchored on `deep_overlap_count >= 1.500` plus one boundary/core term.

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Active log path:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992-max5600.txt`

### Exact next step
- Re-enter from lock preflight and check whether the active `4992-max5600` process has completed.
- If completed, parse subtype/rule tables from the emitted log and classify hold vs transition against `4480`.
- If still active, avoid overlap and skip starting new science until that run exits.

### First concrete action
- Execute:
  - `lsof /Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992-max5600.txt`

## 2026-03-25 02:20 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 2]`
  - `git rev-list --left-right --count origin/main...main` -> `0 2`
  - `HEAD=c05f815`, `origin/main=0388355`.
- Push-first helper run before new work:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=2`, `behind=0`.
- One bounded same-thread integrity step completed:
  - hardened interrupt teardown in `scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py` so manual cancellation reports a single `interrupted` status and does not emit secondary teardown tracebacks.
  - verified syntax with `python3 -m py_compile /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py`.
- A manual bounded `4992` retry was started then intentionally interrupted after `147.8s` to avoid leaving an unattended long-running process under lock.

### Strongest confirmed conclusion
- No mechanism conclusion changed in this run.
- The strongest confirmed frontier remains `4480`: `4` subtypes, non-pocket membership `115`, and the same stable rotated 2-term both-sensitive exact family anchored on `deep_overlap_count >= 1.500` plus one boundary/core term.

### Files and results changed in this run
- Integrity code update:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Retry helper push first while ahead.
- Then execute one full bounded sparse-sentinel rerun at `variant_limit = 4992` with a larger `--max-seconds` guard and let it finish to obtain subtype/rule tables.
- If `4992` preserves the same 2-term both-sensitive family, widen again; if it changes, switch to focused both-sensitive rule-transition analysis.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-25 00:27 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main`
  - `git rev-list --left-right --count origin/main...main` -> `0 0`
  - `HEAD=0388355`, `origin/main=0388355`.
- Push-first helper was not needed before science because repo was not ahead.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 4992 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992.txt`
  - result: `status=timed_out`, `exit_code=124`, `elapsed_s=4200.0`.
- End-of-loop push helper after commit:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=1`, `behind=0`.

### Strongest confirmed conclusion
- No new mechanism conclusion is confirmed from `4992` yet because the bounded run hit the `--max-seconds 4200` guard before producing analysis tables.
- The strongest confirmed frontier read remains the prior `4480` result:
  - `4` subtypes
  - non-pocket membership `115`
  - stable rotated both-sensitive exact family (2-term only, anchored on `deep_overlap_count >= 1.500` plus a second boundary/core observable).

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992.txt`

### Exact next step
- Retry the same sparse sentinel at `variant_limit = 4992` with a slightly larger time guard so the run can finish and emit subtype/rule tables.
- If `4992` then preserves the same 2-term both-sensitive family, widen again.
- If `4992` changes the family, switch to focused both-sensitive rule-transition analysis.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 22:51 America/New_York

### Current state
- Picked up from the synced `4240` frontier with the manual lock still held.
- Completed one wider sparse-sentinel rung at `4480`:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 4480 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-4480.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=3989.5`

### Strongest confirmed conclusion
- The post-`3984` both-sensitive rule rotation is now confirmed as a stable higher-frontier regime rather than a transitional shoulder.
- `4480` preserves:
  - `4` subtypes
  - continued non-pocket membership growth (`109 -> 115`)
  - the same rotated both-sensitive exact family: 2-term only, anchored on `deep_overlap_count >= 1.500` plus a second boundary/core observable
- Four of the five best exact both-sensitive rules are unchanged versus `4240`, and the fifth only relaxes slightly (`core_deep_fraction <= 0.443` instead of `<= 0.433`).
- The exact both-sensitive family now covers `tp=7`.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-4480.txt`

### Exact next step
- Continue sparse sentinels rather than returning to tight laddering.
- The next best rung is a wider jump to `variant_limit = 4992`.
- If `4992` preserves the same 2-term both-sensitive family, widen again.
- If `4992` changes the family, switch from sentinel growth tracking to focused both-sensitive rule-transition analysis.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 21:44 America/New_York

### Current state
- Picked up from the synced overnight frontier at `3984`, with the manual lock held for an interactive sparse-sentinel continuation.
- Completed one bounded sparse-sentinel rung at `4112`:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 4112 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-4112.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=3661.3`
- Because `4112` changed the exact both-sensitive family, ran an immediate verification rung at `4240`:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 4240 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-4240.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=3766.0`

### Strongest confirmed conclusion
- The frontier is still growing, but the important change is structural rather than taxonomic.
- `4112` and `4240` both preserve:
  - `4` subtypes
  - active non-pocket membership growth (`101 -> 106 -> 109`)
  - a rotated exact both-sensitive family that is now stably 2-term only
- The old one-term both-sensitive anchor (`deep_overlap_count >= 1.500`) is no longer sufficient by itself.
- The new stable regime is:
  - exact both-sensitive rules still anchored on `deep_overlap_count >= 1.500`
  - plus a second boundary/core observable
  - four of the five best exact rules are unchanged between `4112` and `4240`

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-4112.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-4240.txt`

### Exact next step
- Do not resume tight `128`-step laddering immediately.
- The next best sparse sentinel is a wider jump to `4480`.
- If `4480` preserves the same 2-term both-sensitive family, treat the post-`3984` rule rotation as a stable new regime and widen again.
- If `4480` changes the family again, switch from laddering to a focused both-sensitive rule-transition analysis.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 18:18 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `held` (`owner=physics-science`)
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 4]`
  - `git rev-list --left-right --count origin/main...main` -> `0 4`
  - `HEAD=9085b6f`, `origin/main=9f879df`.
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=4`, `behind=0`.
- Reconciled stale tracker mismatch before advancing the thread:
  - prior memory/handoff still claimed a pending `3856` commit, but repo state was already committed at `9085b6f`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 3984 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3984.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=3551.8`.

### Strongest confirmed conclusion
- `3984` continues the active sparse-sentinel growth phase while preserving subtype count (`4`) and the post-`3856` both-sensitive exact family.
- Frontier state at `3984`:
  - non-pocket subtype membership rises from `97` to `101`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive two-term family is unchanged versus `3856`.
- New rows at `3984`:
  - `local-morph-\u0fa1` (`pair-only-sensitive`, `dpadj-only/dpadj-only`, `cross=n`)
  - `local-morph-\u0fb2` (`add1-sensitive`, `both/dpadj-only`, `cross=Y`)
  - `local-morph-\u0fbe` (`add1-sensitive`, `ge6-only/dpadj-only`, `cross=Y`)
  - `local-morph-\u0fd9` (`add1-sensitive`, `ge6-only/dpadj-only`, `cross=n`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3984.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 4112` using the same `--max-seconds` guard.
- Diff `4112` row/subtype/exact-rule sections against `3984` and `3856`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 17:15 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 3]`
  - `git rev-list --left-right --count origin/main...main` -> `0 3`
  - `HEAD=1350c7c`, `origin/main=9f879df`.
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=3`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 3856 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3856.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=3427.2`.

### Strongest confirmed conclusion
- `3856` continues active sparse-sentinel growth while preserving subtype count but rotating the both-sensitive two-term family.
- Frontier state at `3856`:
  - non-pocket subtype membership rises from `89` to `97`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive two-term family pivots from boundary-fraction/center-variation conditions to core/shell-deficit and center-location conditions, still anchored on `deep_overlap_count >= 1.500`.
- New rows at `3856`:
  - `local-morph-\u0f11` (`pair-only-sensitive`, `dpadj-only/dpadj-only`, `cross=Y`)
  - `local-morph-\u0f20` (`add4-sensitive`, `dpadj-only/ge6-only`, `cross=Y`)
  - `local-morph-\u0f37` (`add1-sensitive`, `neither/dpadj-only`, `cross=Y`)
  - `local-morph-\u0f38` (`add4-sensitive`, `dpadj-only/neither`, `cross=Y`)
  - `local-morph-\u0f54` (`add1-sensitive`, `neither/dpadj-only`, `cross=Y`)
  - `local-morph-\u0f57` (`add1-sensitive`, `neither/dpadj-only`, `cross=Y`)
  - `local-morph-\u0f65` (`pair-only-sensitive`, `dpadj-only/dpadj-only`, `cross=Y`)
  - `local-morph-\u0f6d` (`add1-sensitive`, `neither/dpadj-only`, `cross=n`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3856.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 3984` using the same `--max-seconds` guard.
- Diff `3984` row/subtype/exact-rule sections against `3856` and `3728`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 16:13 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 2]`
  - `git rev-list --left-right --count origin/main...main` -> `0 2`
  - `HEAD=f234077`, `origin/main=9f879df`.
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=2`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 3728 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3728.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=3313.0`.

### Strongest confirmed conclusion
- `3728` continues the active sparse-sentinel growth phase while preserving the same four-subtype law.
- Frontier state at `3728`:
  - non-pocket subtype membership rises from `85` to `89`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive two-term family is unchanged versus `3600` and `3472`.
- New rows at `3728`:
  - `local-morph-\u0e81` (`add1-sensitive`, `ge6-only/dpadj-only`, `cross=Y`)
  - `local-morph-\u0e86` (`add1-sensitive`, `neither/dpadj-only`, `cross=n`)
  - `local-morph-\u0ee7` (`add1-sensitive`, `neither/dpadj-only`, `cross=Y`)
  - `local-morph-\u0ee8` (`pair-only-sensitive`, `dpadj-only/dpadj-only`, `cross=Y`).

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3728.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 3856` using the same `--max-seconds` guard.
- Diff `3856` row/subtype/exact-rule sections against `3728` and `3600`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`
## 2026-03-24 15:16 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 1]`
  - `git rev-list --left-right --count origin/main...main` -> `0 1`
  - `HEAD=414d581`, `origin/main=9f879df`.
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=1`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 3600 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3600.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=3192.3`.

### Strongest confirmed conclusion
- `3600` breaks the `3344..3472` short hold by one row while preserving the same four-subtype law.
- Frontier state at `3600`:
  - non-pocket subtype membership rises from `84` to `85`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive two-term family is unchanged versus `3472` and `3344`.
- New row at `3600`:
  - `local-morph-\u0e40` (`add1-sensitive`, `neither/dpadj-only`, `cross=Y`).

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3600.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 3728` using the same `--max-seconds` guard.
- Diff `3728` row/subtype/exact-rule sections against `3600` and `3472`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 14:08 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main`
  - `git rev-list --left-right --count origin/main...main` -> `0 0`
  - `HEAD=9f879df`.
- Push-first helper was not needed before science because repo was not ahead.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 3472 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3472.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=3069.9`.

### Strongest confirmed conclusion
- `3472` is an exact hold of the `3344` frontier (aside from metadata):
  - non-pocket subtype membership remains `84`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive two-term family is unchanged versus `3344` and `3216`.
- No new non-pocket rows appear at `3472`; this confirms `3344..3472` as a short stability band after the six-row `3344` expansion.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3472.txt`

### Exact next step
- Continue sparse-sentinel with `variant_limit = 3600` using the existing `--max-seconds` guard.
- Diff `3600` row/subtype/exact-rule sections against `3472` and `3344`.
- If `3600` matches exactly, treat `3344..3600` as the next widened hold before probing deeper.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 13:06 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 8]`
  - `git rev-list --left-right --count origin/main...main` -> `0 8`
  - `HEAD=fc54868`.
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=8`, `behind=0`.
- Executed one bounded sparse-sentinel mechanism rung on the active thread:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 3344 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3344.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=3004.7`.
- Obvious same-thread continuation (integrity):
  - generated `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-sparse-sentinel-frontier-integrity-audit.txt`
  - confirmed frontier-wide row/subtype/anchor consistency and flagged one historical trailer anomaly (`2448` completion line missing).
- Committed intermediate tracked update:
  - `832d8ea` (`Record sparse sentinel frontier integrity audit`).
- End-of-loop helper push retry still failed with transient DNS:
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=9`, `behind=0`.
- Released cooperative lock at end of loop after `3344` completion was confirmed:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py release --owner physics-science` -> `status=released`.

### Strongest confirmed conclusion
- `3344` extends the `3216` sparse-sentinel frontier by six rows while preserving the same four-subtype law.
- Frontier state at `3344`:
  - non-pocket subtype membership rises from `78` to `84`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive two-term family is unchanged versus `3216`, `3088`, `2960`, `2832`, `2704`, `2576`, `2448`, and `2320`.
- New rows at `3344`:
  - `local-morph-\u0cf7` (`add1-sensitive`)
  - `local-morph-\u0d07` (`add1-sensitive`)
  - `local-morph-\u0d12` (`add4-sensitive`)
  - `local-morph-\u0d31` (`add4-sensitive`)
  - `local-morph-\u0d3b` (`add4-sensitive`)
  - `local-morph-\u0d40` (`pair-only-sensitive`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3344.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-sparse-sentinel-frontier-integrity-audit.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 3472` using `--max-seconds` guard.
- Diff `3472` row/subtype/exact-rule sections against `3344` and `3216`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 12:06 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 7]`
  - `git rev-list --left-right --count origin/main...main` -> `0 7`
  - `HEAD=66b7165`, `origin/main=2df2f78`.
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=7`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 3216 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3216.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=2884.7`

### Strongest confirmed conclusion
- `3216` extends the `3088` sparse-sentinel frontier by three rows while preserving the same four-subtype law.
- Frontier state at `3216`:
  - non-pocket subtype membership rises from `75` to `78`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive 2-term family is unchanged versus `3088`, `2960`, `2832`, `2704`, `2576`, `2448`, and `2320`.
- New rows at `3216` are:
  - `local-morph-\u0caa` (`add1-sensitive`)
  - `local-morph-\u0cb3` (`add4-sensitive`)
  - `local-morph-\u0cc9` (`add1-sensitive`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3216.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 3344` using `--max-seconds` guard.
- If `3344` changes the frontier, diff row/subtype/exact-rule sections against `3216` and `3088`.
- If `3344` matches exactly, treat `3216..3344` as the next short hold and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`


## 2026-03-24 11:04 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 5]`
  - `git rev-list --left-right --count origin/main...main` -> `0 5`
  - `HEAD=808497d`, `origin/main=2df2f78`.
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=5`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 3088 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3088.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=2771.0`
- Committed run updates:
  - `aab684d` (`Advance sparse sentinel frontier through variant limit 3088`)
- End-of-loop helper push retry failed with transient DNS:
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=6`, `behind=0`.

### Strongest confirmed conclusion
- `3088` extends the `2960` sparse-sentinel frontier by two rows while preserving the same four-subtype law.
- Frontier state at `3088`:
  - non-pocket subtype membership rises from `73` to `75`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive 2-term family is unchanged versus `2960`, `2832`, `2704`, `2576`, `2448`, and `2320`.
- New rows at `3088` are:
  - `local-morph-\u0c17` (`add1-sensitive`)
  - `local-morph-\u0c29` (`add1-sensitive`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3088.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 3216` using `--max-seconds` guard.
- If `3216` changes the frontier, diff row/subtype/exact-rule sections against `3088` and `2960`.
- If `3216` matches exactly, treat `3088..3216` as the next short hold and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 10:05 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 3]`
  - `git rev-list --left-right --count origin/main...main` -> `0 3`
  - `HEAD=d85ea36`, `origin/main=2df2f78`.
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=3`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 2960 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2960.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=2669.1`
- Committed run updates:
  - `59d16ed` (`Advance sparse sentinel frontier through variant limit 2960`)
- End-of-loop helper push retry failed with transient DNS:
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=4`, `behind=0`.
- Released cooperative lock:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py release --owner physics-science` -> `status=released`

### Strongest confirmed conclusion
- `2960` extends the `2832` sparse-sentinel frontier by one row while preserving the same four-subtype law.
- Frontier state at `2960`:
  - non-pocket subtype membership rises from `72` to `73`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive 2-term family is unchanged versus `2832`, `2704`, `2576`, `2448`, and `2320`.
- New row at `2960` is:
  - `local-morph-\u0be5` (`add1-sensitive`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2960.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 3088` using `--max-seconds` guard.
- If `3088` changes the frontier, diff row/subtype/exact-rule sections against `2960` and `2832`.
- If `3088` matches exactly, treat `2960..3088` as the next short hold and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`
## 2026-03-24 10:02 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 3]`
  - `git rev-list --left-right --count origin/main...main` -> `0 3`
  - `HEAD=d85ea36`, `origin/main=2df2f78`.
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=3`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 2960 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2960.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=2669.1`

### Strongest confirmed conclusion
- `2960` extends the `2832` sparse-sentinel frontier by one row while preserving the same four-subtype law.
- Frontier state at `2960`:
  - non-pocket subtype membership rises from `72` to `73`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive 2-term family is unchanged versus `2832`, `2704`, `2576`, `2448`, and `2320`.
- New row at `2960` is:
  - `local-morph-\u0be5` (`add1-sensitive`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2960.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 3088` using `--max-seconds` guard.
- If `3088` changes the frontier, diff row/subtype/exact-rule sections against `2960` and `2832`.
- If `3088` matches exactly, treat `2960..3088` as the next short hold and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`
## 2026-03-24 09:00 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - `git status --short --branch` -> `main...origin/main [ahead 2]`
  - `git rev-list --left-right --count origin/main...main` -> `0 2`
  - `HEAD=1dd3ea9`, `origin/main=2df2f78`.
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=2`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 2832 --max-seconds 4200 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2832.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=2559.0`

### Strongest confirmed conclusion
- `2832` extends the `2704` sparse-sentinel frontier by one row while preserving the same four-subtype law.
- Frontier state at `2832`:
  - non-pocket subtype membership rises from `71` to `72`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive 2-term family is unchanged versus `2704`, `2576`, `2448`, and `2320`.
- New row at `2832` is:
  - `local-morph-\u0b23` (`add1-sensitive`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2832.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 2960` using `--max-seconds` guard.
- If `2960` changes the frontier, diff row/subtype/exact-rule sections against `2832` and `2704`.
- If `2960` matches exactly, treat `2832..2960` as the next short hold and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 08:02 America/New_York

### Current state
- Reconciled required preflight context in canonical order:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`.
- Lock flow executed per protocol:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status` -> `free`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2` -> `acquired`
- Git reconciled before science:
  - initial `git status --short --branch` -> `main...origin/main [ahead 17]`
  - initial `git rev-list --left-right --count origin/main...main` -> `0 17`
- Push-first helper run before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`.
- Executed bounded same-thread mechanism continuation:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 2704 > /Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2704.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=2457.7`
- Obvious same-thread integrity continuation (bounded-run guard):
  - added `--max-seconds` wall-clock guard to `scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py`
  - smoke: `--variant-limit 8 --max-seconds 60` completed (`26.1s`)
  - timebox probe: `--variant-limit 2704 --max-seconds 120` cleanly exited with `code=124` and timeout marker log.
- Reconciled git again after steps:
  - `git status --short --branch` -> `main...origin/main`
  - `git rev-list --left-right --count origin/main...main` -> `0 0`
- Committed run updates:
  - `b61ff2a` (`Advance sparse sentinel frontier through variant limit 2704`)
- End-of-loop helper push retry failed with transient DNS:
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=1`, `behind=0`.
- Released cooperative lock:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py release --owner physics-science` -> `status=released`

### Strongest confirmed conclusion
- `2704` extends the `2576` sparse-sentinel frontier by two rows while preserving the same four-subtype law.
- Frontier state at `2704`:
  - non-pocket subtype membership rises from `69` to `71`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive 2-term family is unchanged versus `2576`, `2448`, and `2320`.
- New rows at `2704` are:
  - `local-morph-\u0ada` (`add4-sensitive`)
  - `local-morph-\u0aea` (`add1-sensitive`)
- Runner integrity is improved for future high-limit rungs: timeout-guarded runs now fail fast with explicit timeout output and exit code `124` instead of indefinite blocking.

### Files and results changed in this run
- Code:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py`
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2704.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2704-timebox120.txt`
  - `/tmp/2026-03-24-nonpocket-subtype-rules-8-timeout-guard-smoke.txt`

### Exact next step
- Continue the same sparse-sentinel thread at `variant_limit = 2832`, using `--max-seconds` for bounded automation safety while checking whether frontier growth persists or enters a short hold band after `2704`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 06:57 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 16]`
  - `git rev-list --left-right --count origin/main...main` -> `0 16`
  - `HEAD=ee28b31`, `origin/main=84b2558`.
- Per protocol, ran push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=16`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 2576`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=2325.8`

### Strongest confirmed conclusion
- `2576` extends the `2448` frontier by two rows while preserving the same four-subtype law.
- Frontier state at `2576`:
  - non-pocket subtype membership rises from `67` to `69`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive 2-term family is unchanged versus `2448` and `2320`
- New rows at `2576` are:
  - `local-morph-\u0a45` (`pair-only-sensitive`)
  - `local-morph-\u0a6e` (`add4-sensitive`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Run output:
  - stdout from `--variant-limit 2576` execution (no redirected log file written this run)

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 2704`.
- If `2704` changes the frontier, diff row/subtype/exact-rule sections against `2576` and `2448`.
- If `2704` matches exactly, treat `2576..2704` as the next stable band and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 05:55 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 14]`
  - `git rev-list --left-right --count origin/main...main` -> `0 14`
  - `HEAD=b9e866a`, `origin/main=84b2558`.
- Per protocol, ran push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=14`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 2448`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2448.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=2199.4`
- Committed run updates:
  - `db9ce38` (`Advance sparse sentinel frontier through variant limit 2448`)
- End-of-loop helper push retries failed with transient DNS:
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=15`, `behind=0`.

### Strongest confirmed conclusion
- `2448` extends the `2320` frontier by two rows while preserving the same four-subtype law.
- Frontier state at `2448`:
  - non-pocket subtype membership rises from `65` to `67`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive 2-term family is unchanged versus `2320`
- New rows at `2448` are:
  - `local-morph-\u09a3` (`pair-only-sensitive`)
  - `local-morph-\u09c4` (`add1-sensitive`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2448.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 2576`.
- If `2576` changes the frontier, diff row/subtype/exact-rule sections against `2448` and `2320`.
- If `2576` matches exactly, treat `2448..2576` as the next stable band and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 04:52 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 12]`
  - `git rev-list --left-right --count origin/main...main` -> `0 12`
  - `HEAD=33ca83e`, `origin/main=84b2558`.
- Per protocol, ran push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=12`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 2320`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2320.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=2092.1`
- Committed run updates:
  - `dc6c2a6` (`Advance sparse sentinel frontier through variant limit 2320`)
- End-of-loop helper push retries failed with transient DNS:
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=13`, `behind=0`.

### Strongest confirmed conclusion
- `2320` continues growth beyond `2192` by seven rows while preserving the same four-subtype law.
- Frontier state at `2320`:
  - non-pocket subtype membership rises from `58` to `65`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=5`)
  - both-sensitive 2-term family broadens slightly again (`boundary_roughness >= 0.299`, was `>= 0.305`) and rotates one rule (`boundary_fraction <= 0.988` replaces `crosses_midline = Y` in the deep-overlap pair).
- New rows at `2320` are:
  - `local-morph-\u08fb`, `local-morph-\u0935` (both `pair-only-sensitive`)
  - `local-morph-\u091b`, `local-morph-\u0924`, `local-morph-\u0937`, `local-morph-\u096d` (all `add1-sensitive`)
  - `local-morph-\u0939` (`both-sensitive`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2320.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 2448`.
- If `2448` changes the frontier, diff row/subtype/exact-rule sections against `2320` and `2192`.
- If `2448` matches exactly, treat `2320..2448` as the next stable band and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 03:51 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 11]`
  - `git rev-list --left-right --count origin/main...main` -> `0 11`
  - `HEAD=77daa0e`, `origin/main=84b2558`.
- Per protocol, ran push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=11`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 2192`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2192.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=1985.1`

### Strongest confirmed conclusion
- `2192` breaks the `1936..2064` hold by six rows while preserving the same four-subtype law.
- Frontier state at `2192`:
  - non-pocket subtype membership rises from `52` to `58`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=4`)
  - both-sensitive 2-term rule family broadens slightly: `boundary_roughness >= 0.305` (was `>= 0.311`) and `center_total_variation >= 1.500` (was `>= 2.500`)
- New rows at `2192` are:
  - `local-morph-\u0874` (`pair-only-sensitive`, `dpadj-only/dpadj-only`, `cross=Y`)
  - `local-morph-\u088d` (`both-sensitive`, `neither/neither`, `cross=Y`)
  - `local-morph-\u088f` (`add4-sensitive`, `dpadj-only/neither`, `cross=n`)
  - `local-morph-\u0892`, `local-morph-\u089b`, `local-morph-\u08ae` (all `add1-sensitive`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2192.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 2320`.
- If `2320` changes the frontier, diff row/subtype/exact-rule sections against `2192` and `2064`.
- If `2320` matches exactly, treat `2192..2320` as the next stable band and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 02:49 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 8]`
  - `git rev-list --left-right --count origin/main...main` -> `0 8`
  - `HEAD=90d43c2`, `origin/main=84b2558`.
- Per protocol, ran push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 2064`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2064.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=1848.3`
- Committed run updates:
  - `c194b0c` (`Confirm sparse sentinel hold through variant limit 2064`)
- End-of-loop helper push retries failed with transient DNS:
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`.

### Strongest confirmed conclusion
- `2064` is an exact hold of `1936`.
- Frontier state at `2064`:
  - non-pocket subtype membership remains `52`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=3`)
  - both-sensitive 2-term rule list is unchanged versus `1936` and `1808`
- So the frontier read tightens to: `1936` was a one-row expansion and `1936..2064` is now the next confirmed short hold.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-2064.txt`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, continue sparse-sentinel with `variant_limit = 2192`.
- If `2192` changes the frontier, diff row/subtype/exact-rule sections against `2064` and `1936`.
- If `2192` matches exactly, treat `1936..2192` as the next stable band and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 01:46 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 7]`
  - `git rev-list --left-right --count origin/main...main` -> `0 7`
  - `HEAD=515e535`, `origin/main=84b2558`.
- Per protocol, ran push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=7`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1936`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-1936.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=1737.5`

### Strongest confirmed conclusion
- `1936` continues the active sparse-sentinel growth phase by one row without subtype-map or exact-rule drift.
- Frontier state at `1936`:
  - non-pocket subtype membership rises from `51` to `52`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=3`)
  - both-sensitive 2-term rule list is unchanged versus `1808` and `1680`
- The lone new row at `1936` is:
  - `local-morph-\u0795` (`add4-sensitive`, `dpadj-only/neither`, `cross=Y`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-1936.txt`

### Exact next step
- Continue the same sparse-sentinel thread with a wider rung at `variant_limit = 2064`.
- If `2064` changes the frontier, diff row/subtype/exact-rule sections against `1936` and `1808`.
- If `2064` matches exactly, treat `1936..2064` as the next stable band and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-24 00:48 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 3]`
  - `git rev-list --left-right --count origin/main...main` -> `0 3`
  - `HEAD=75b1d46`, `origin/main=84b2558`.
- Per protocol, ran push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=3`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1808`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-1808.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=1643.1`
- Committed run updates:
  - `3c123af` (`Advance sparse sentinel frontier through variant limit 1808`)
  - `1183303` (`Record 1808 run push retry status`)
- End-of-loop helper push retries failed with transient DNS:
  - helper result remained `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com` (no remote sync in this run)

### Strongest confirmed conclusion
- `1808` extends the active sparse-sentinel growth phase without subtype-map or exact-rule drift.
- Frontier state at `1808`:
  - non-pocket subtype membership rises from `45` to `51`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=3`)
  - both-sensitive 2-term rule list is unchanged versus `1680`
- New rows at `1808` are:
  - `local-morph-\u0702` (`add4-sensitive`, `dpadj-only/ge6-only`, `cross=Y`)
  - `local-morph-\u070a` (`pair-only-sensitive`, `dpadj-only/dpadj-only`, `cross=Y`)
  - `local-morph-\u070b`, `local-morph-\u0723`, `local-morph-\u0733`, `local-morph-\u073d` (all `add1-sensitive`, `ge6-only/dpadj-only`)

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-1808.txt`

### Exact next step
- Continue the same sparse-sentinel thread with a wider rung at `variant_limit = 1936`.
- If `1936` changes the frontier, diff row/subtype/exact-rule sections against `1808` and `1680`.
- If `1936` matches exactly, treat `1808..1936` as the next stable band and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 23:43 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main`
  - `git rev-list --left-right --count origin/main...main` -> `0 0`
  - `HEAD` matched `origin/main` at `84b2558`.
- Per protocol, no push-first action was needed because the branch was not ahead.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1680`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1680.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=1528.6`
- Committed run updates:
  - `86814e3` (`Advance sparse sentinel frontier through variant limit 1680`)
- End-of-loop helper push retries failed with transient DNS:
  - helper result remained `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com` (no remote sync in this run)

### Strongest confirmed conclusion
- `1680` breaks the `1488..1552` hold by one row but keeps the same 4-subtype map.
- Frontier state at `1680`:
  - non-pocket subtype membership rises from `44` to `45`
  - subtype count remains `4`
  - both-sensitive one-term anchor remains exact: `deep_overlap_count >= 1.500` (`tp=3`)
- The lone new row is:
  - `local-morph-\u0690` (`pair-only-sensitive`, `dpadj-only/dpadj-only`, `cross=n`)
- Exact-rule table changed only inside one both-sensitive 2-term entry:
  - dropped: `boundary_fraction >= 0.942 and mean_center <= -0.036`
  - added: `crosses_midline = Y and deep_overlap_count >= 1.500`

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1680.txt`

### Exact next step
- Continue the same sparse-sentinel thread with a wider next rung at `variant_limit = 1808`.
- If `1808` changes the frontier, diff row/subtype/exact-rule sections against `1680` and `1552`.
- If `1808` matches exactly, treat `1680..1808` as the next stable band and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 23:16 America/New_York

### Current state
- Continued the active sparse-sentinel thread under the same manual lock after the completed `1488` bump.
- Confirmed `1488` introduced one new `add4-sensitive` row:
  - `local-morph-\u0614`
- Ran one follow-up rung to decide whether that was a one-step bump or a continuing band:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1552`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1552.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=1450.1`
- One earlier `1552` attempt dropped after writing only a start marker, so the rung was rerun cleanly with direct file redirection and completed successfully.

### Strongest confirmed conclusion
- `1552` exactly matches `1488`.
- Current frontier state:
  - non-pocket subtype membership stays at `44`
  - subtype count stays at `4`
  - exact-rule table is unchanged
  - both-sensitive anchor remains `deep_overlap_count >= 1.500` (`tp=3`)
- So the current frontier read is:
  - `1488` was a one-row add4-sensitive expansion
  - `1488..1552` is now the next confirmed short hold

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1552.txt`

### Exact next step
- Do not keep stepping by `64` indefinitely.
- Widen the next sparse sentinel to `variant_limit = 1680`.
- If `1680` changes the frontier, diff row/subtype/exact-rule sections against `1552` and `1488`.
- If `1680` still matches exactly, treat `1488..1680` as the next stable band and widen again.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 22:54 America/New_York

### Current state
- Picked up from the synced `1424` sparse-sentinel checkpoint with the manual lock already held for `interactive sparse sentinels 1488+`.
- First `1488` launch only wrote a start marker to the log, so the rung was rerun directly in the same repo context and the final output was written back into the canonical log path:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1488`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-1488.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=1447.2`
- While `1488` was running, a duplicate `1552` sparse-sentinel job started in parallel and was explicitly killed so the intended rung could finish without overlap.

### Strongest confirmed conclusion
- The frontier grows again at `1488`, but only inside the existing law:
  - non-pocket subtype membership rises from `43` to `44`
  - subtype count remains `4`
  - exact-rule table is unchanged
  - both-sensitive anchor remains `deep_overlap_count >= 1.500` (`tp=3`)
- The lone new row is `local-morph-\u0614`, which enters as `add4-sensitive` (`dpadj-only/neither`, `cross=n`).
- So the frontier read is now:
  - `1360..1424` was a short hold
  - `1488` starts the next growth phase
  - but still without subtype-map drift or exact-rule drift

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
- New/rewritten log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-1488.txt`

### Exact next step
- Do not keep micro-laddering by default.
- If we continue this thread, widen the next sparse sentinel materially rather than stepping immediately to `1552`.
- Prefer latent-structure work unless a later sentinel shows subtype-count or exact-rule drift.

### First concrete action
- Execute:
  - `git status --short --branch`

## 2026-03-23 22:21 America/New_York

### Current state
- Picked up from the latest sparse-sentinel worker state after confirming:
  - `git status --short --branch` -> `main...origin/main [ahead 5]`
  - the worker lock was `free`
  - `git ls-remote origin HEAD` succeeded immediately
- Re-ran the helper push manually in the same repo context:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=pushed`, `ahead=0`, `behind=0`, `attempts_used=1`
- Then executed the next bounded same-thread sparse-sentinel step:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1424`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1424.txt`
  - result: `status=completed`, `exit_code=0`, `elapsed_s=1316.8`

### Strongest confirmed conclusion
- The active sparse-sentinel frontier does not grow at `1424`.
- `1424` exactly matches `1360`:
  - non-pocket subtype membership stays at `43`
  - subtype count stays at `4`
  - exact-rule table is unchanged
  - both-sensitive anchor remains `deep_overlap_count >= 1.500` (`tp=3`)
- So the current frontier read tightens to:
  - `1232/1296/1360` was the last growth phase
  - `1360..1424` is now the next confirmed short hold

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1424.txt`

### Exact next step
- Resume sparse-sentinel laddering at `variant_limit = 1488`.
- If `1488` changes the frontier, diff row/subtype/exact-rule sections against `1424` and `1360`.
- If `1488` matches exactly, treat `1360..1488` as the next stable band and widen the next sentinel gap.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 21:38 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 4]`
  - `git rev-list --left-right --count origin/main...main` -> `0 4`
  - `HEAD=85995d1`, `origin/main=1b176af`.
- Per protocol, ran push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=4`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - command: `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1360`
  - hard timeout: `2400s`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-1360.txt`
  - diagnostics: `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-1360.meta.json`
  - outcome: `status=completed`, `exit_code=0`, `elapsed_s=1238.881`.

### Strongest confirmed conclusion
- The active sparse-sentinel frontier remains in live growth at `1360` with no subtype-map break.
- Non-pocket subtype membership grows from `41` rows (`1296`) to `43` rows (`1360`) while subtype count remains `4`.
- The two new rows at `1360` are `local-morph-\u0580` and `local-morph-\u0594`; both enter as `pair-only-sensitive` (`dpadj-only/dpadj-only`, `cross=Y`).
- The exact-rule table is unchanged versus `1296` and `1232`, with the both-sensitive anchor still exact:
  - `deep_overlap_count >= 1.500` (`tp=3`).

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/updated:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-1360.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-1360.meta.json`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, run one deeper same-thread sparse-sentinel rung at `variant_limit = 1424`, then diff non-pocket row/subtype/exact-rule sections against `1360` and `1296`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 20:38 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 3]`
  - `git rev-list --left-right --count origin/main...main` -> `0 3`
  - `HEAD=e750806`, `origin/main=1b176af`.
- Per protocol, ran push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=3`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step:
  - command: `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1296`
  - hard timeout: `2400s`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1296.txt`
  - diagnostics: `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1296.meta.json`
  - outcome: `status=completed`, `exit_code=0`, `elapsed_s=1184.559`.

### Strongest confirmed conclusion
- The active sparse-sentinel frontier remains in live growth at `1296` without a subtype-map break.
- Non-pocket subtype membership grows from `40` rows (`1232`) to `41` rows (`1296`) while subtype count remains `4`.
- The only new row at `1296` is `local-morph-\u0544` and it enters as `pair-only-sensitive` (`dpadj-only/dpadj-only`, `cross=Y`).
- The both-sensitive anchor remains unchanged and exact:
  - `deep_overlap_count >= 1.500` (`tp=3`).

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/updated:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1296.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1296.meta.json`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, run one deeper same-thread sparse-sentinel rung at `variant_limit = 1360`, then diff non-pocket row/subtype/exact-rule sections against `1296` and `1232`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 19:37 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 1]` with local `AUTOPILOT_WORKLOG.md` modification.
  - `git rev-list --left-right --count origin/main...main` -> `0 1`
  - `HEAD=0f74b0f`, `origin/main=1b176af`.
- Per protocol, ran push-first helper before new science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=1`, `behind=0`.
- Executed one bounded same-thread sparse-sentinel continuation step on the active thread:
  - command: `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1232`
  - bounded via wrapper timeout `2400s`
  - output: `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1232.txt`
  - diagnostic meta: `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1232.meta.json`
  - outcome: `status=completed`, `exit_code=0`, `elapsed_s=1156.333` (no timeout)
- Committed run updates:
  - `0c4feb9` (`Complete bounded 1232 sparse-sentinel rung`)
- End-of-loop helper push retry after commit failed with transient DNS:
  - `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=2`, `behind=0`.

### Strongest confirmed conclusion
- The blocked `1232` rung is now completed with explicit bounded diagnostics.
- Non-pocket subtype frontier grows from `36` rows at `1168` to `40` rows at `1232` while subtype count remains `4`.
- New rows at `1232` are:
  - `local-morph-\u04f2` (add4-sensitive)
  - `local-morph-\u0522` (pair-only-sensitive)
  - `local-morph-\u0523` (pair-only-sensitive)
  - `local-morph-\u0528` (both-sensitive)
- The both-sensitive exact one-term anchor remains stable:
  - `deep_overlap_count >= 1.500`
  - true positives rise from `2` (`1168`) to `3` (`1232`)
- So the current frontier read is updated to active growth at `1232`, not a hold.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/updated:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1232.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1232.meta.json`

### Exact next step
- Retry helper push first on the next loop if still ahead.
- If sync is available, run one deeper same-thread sparse-sentinel rung at `variant_limit = 1296`, then diff non-pocket row/subtype/exact-rule sections against `1232` and `1168`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 18:33 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was `free`, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main`
  - `git rev-list --left-right --count origin/main...main` -> `0 0`
  - `HEAD` matched `origin/main` at `1b176af`.
- Per protocol, no push-first action was needed because the branch was not ahead.
- Executed one bounded same-thread sparse-sentinel step on the active thread:
  - started `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1232 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1232.txt`
- In this environment the `1232` rung did not finish within the bounded interactive window; run was interrupted manually to prevent overlap with future loops:
  - partial log is start-marker only (`non-pocket suppressor subtype rules started ...`)
  - interrupt traceback shows active frontier evaluation stack (no crash signature prior to interrupt).
- Committed run tracking update:
  - `0f74b0f` (`Record blocked 1232 sparse-sentinel attempt`)
- End-of-loop helper push retry after commit failed with transient DNS:
  - `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=1`, `behind=0`.

### Strongest confirmed conclusion
- No mechanism conclusion changed in this run.
- The active next rung (`variant_limit = 1232`) remains unfinished; latest reliable frontier conclusion is still the completed `1168` closeout where mixed coarse bucket residuals are exactly resolved on the current finer observable family.

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log attempted/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1232.txt` (start marker only)

### Exact next step
- Retry the same sparse-sentinel rung at `variant_limit = 1232` with explicit runtime bounding/diagnostic capture so the run yields either a completed summary or a concrete timeout/failure status suitable for direct comparison against `1168`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 17:20 America/New_York

### Current state
- Reconciled canonical repo state, verified the worker lock was free, and acquired a manual interactive lock for one bounded same-thread residual-bucket step.
- Added a focused residual-bucket extractor:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_rules.py`
  - supporting helpers and renderers in `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
- Ran the full `1168` residual-bucket pass and saved the output to:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-residual-bucket-rules-1168.txt`
- Fixed a helper drift issue uncovered by the result:
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - `pocket_wrap_suppressor_mixed_bucket_axis_analysis()` now searches both target directions (`add1-sensitive` and `add4-sensitive`) instead of only the add1 side.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to replace the stale “one unresolved mixed bucket remains” claim with the corrected exact split.
- Committed and pushed the repo-facing update:
  - `15c5100` (`Resolve the last 1168 residual bucket`)
  - helper push status: `pushed`, `ahead=0`, `behind=0`

### Strongest confirmed conclusion
- The last `1168` add1-vs-add4 residual is not unresolved on the current finer observable family after all.
- Inside `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H`, the residual 3-row add1-vs-add4 set splits exactly via:
  - `core_low_degree_fraction >= 0.208`
- The exact row set is:
  - `local-morph-\u0428` add1-sensitive
  - `local-morph-\u04ab` add1-sensitive
  - `local-morph-\u04cc` add4-sensitive
- So at `1168`, all three add1-vs-add4 mixed coarse buckets are now exactly resolved by the current finer observable family. The missing signal remains low-degree shell/core geometry, not a fifth mechanism family.

### Files and results changed in this run
- Code/helpers:
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_residual_bucket_rules.py`
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-residual-bucket-rules-1168.txt`

### Exact next step
- Return to the sparse-sentinel ladder instead of more bucket archaeology:
  - run `variant_limit = 1232`
- Only rerun mixed-bucket or residual-bucket analysis if the `1232` frontier changes the collision summary or introduces a new mixed signature.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 16:19 America/New_York

### Current state
- Reconciled required preflight in canonical repo context (worklog, handoff, memory), verified lock free, and acquired `physics-science` lock.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main` (clean)
  - `git rev-list --left-right --count origin/main...main` -> `0 0`
  - `HEAD` matched `origin/main` at `878ce72` before this run.
- Per protocol, no push-first action was needed because the branch was not ahead.
- Performed one bounded same-thread integrity/conclusion step on the active `1168` mixed-bucket thread:
  - added `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-unresolved-bucket-decomposition-1168.txt`
  - decomposed the previously unresolved coarse bucket using the completed collision-axes output and confirmed an exact pair-only peel.
- Updated narrative/state tracking to match this tighter unresolved-target read.
- Committed the run update:
  - `4dfab91` (`Narrow unresolved 1168 mixed-bucket target`).
- End-of-loop helper push retry after commit failed with transient DNS:
  - `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=1`, `behind=0`.

### Strongest confirmed conclusion
- The unresolved `1168` coarse bucket (`cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H`) is not fully unresolved in subtype terms.
- Inside that bucket, `pair-only-sensitive` peels exactly via `core_low_degree_fraction >= 0.269` (`tp=1`, `fp=0`, `fn=0`, `4/4` accuracy).
- So the remaining latent separator problem is now the 3-row add1-vs-add4 residual only, which is the narrowest same-thread next target.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-unresolved-bucket-decomposition-1168.txt`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Retry helper push first on the next loop.
- If sync is available, run one bounded residual-bucket mechanism pass on only the 3-row add1-vs-add4 remainder inside `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H`.
- Prioritize compact separators on finer low-degree-shell/core placement and centerline profile asymmetry features.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`

## 2026-03-23 15:31 America/New_York

### Current state
- Manual follow-up resumed from the completed `1168` latent continuation and collision summary.
- Fixed a real automation issue in `/Users/jonreilly/Projects/Physics/scripts/automation_lock.py`:
  - the lock now behaves as TTL-based shared state again instead of treating the short-lived `acquire` helper PID as the live worker,
  - which was allowing duplicate long science jobs to start in parallel.
- Updated worker protocols so the science/janitor/summary loops treat the lock as TTL-based shared state and rely on explicit release:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_JANITOR_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_SUMMARY_PROTOCOL.md`
- Took the next same-thread science step after the `1168` latent continuation:
  - added `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_mixed_bucket_axes.py`
  - added shared mixed-bucket analysis helpers in `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - ran the targeted mixed-bucket split pass at `variant_limit=1168`

### Strongest confirmed conclusion
- The `1168` collision mass is narrower than “all mixed buckets.”
- There are three add1-vs-add4 mixed coarse signatures at `1168`.
- Two already split exactly on the current finer observable family:
  - `cross=Y|span=3+|low=L|pocket=H|overlap=1|rough=H`
    - exact 1-term split via `shell_low_degree_fraction >= 0.817`
  - `cross=n|span<3|low=L|pocket=L|overlap=1|rough=L`
    - exact 2-term split via a `boundary_roughness + mean_center` rule
- So the unresolved latent problem is now localized to one remaining mixed coarse bucket:
  - `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H`
- That means the next search should stay inside that one bucket instead of spending more compute on broad ladder growth.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Code/helpers:
  - `/Users/jonreilly/Projects/Physics/scripts/automation_lock.py`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_JANITOR_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_SUMMARY_PROTOCOL.md`
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_mixed_bucket_axes.py`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`

### Exact next step
- Push the local backlog first.
- If sync is available, run one bounded same-thread unresolved-bucket extraction step inside:
  - `cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H`
- Search for the next latent separator family on that bucket only, prioritizing:
  - finer low-degree geometry
  - shell/core boundary placement
  - centerline asymmetry/profile observables

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`

## 2026-03-23 14:34 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context (worklog, handoff, memory), verified lock free, and acquired `physics-science`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 8]`
  - `git rev-list --left-right --count origin/main...main` -> `0 8`
  - `HEAD=734b307`, `origin/main=4093732`.
- Ran required push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`.
- Performed one bounded same-thread collision/integrity step using completed `1168` latent output (without recomputing the full latent sweep):
  - parsed `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-structure-512-672-912-1168.txt` into `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-collision-summary-1168.txt`.
  - updated `/Users/jonreilly/Projects/Physics/README.md` and run-state files with the new collision concentration conclusion.
- Committed the run update:
  - `562c8fc` (`Summarize 1168 latent collision concentration`).
- End-of-loop helper push retry after commit also failed with transient DNS:
  - `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=9`, `behind=0`.

### Strongest confirmed conclusion
- At `1168`, subtype collisions are concentrated in a small subset of coarse signatures: `4/14` buckets are mixed but they contain `20/36` rows.
- Most collision mass is specifically add1-vs-add4 ambiguity (`18/20` mixed rows), with only `2/20` rows in add1-vs-pair-only collisions.
- This localizes the missing separator to finer latent detail inside add1/add4 mixed buckets that already match on all six coarse bits; the strongest next-axis family remains low-degree geometry (`core_low_degree_fraction`) with overlap/span context.
- Remote sync remains DNS-blocked while local branch is still ahead of `origin/main`.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-collision-summary-1168.txt`
- Input log reused:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-structure-512-672-912-1168.txt`

### Exact next step
- Retry helper push first on the next loop.
- If sync is available, run one bounded same-thread latent-axis extraction inside the three add1/add4 mixed `1168` coarse signatures to test whether a compact threshold on low-degree geometry can split them with fewer collisions.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 13:17 America/New_York

### Current state
- Reconciled required preflight in canonical repo context (worklog, handoff, memory), verified lock free, and acquired `physics-science`.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 7]`
  - `git rev-list --left-right --count origin/main...main` -> `0 7`
  - `HEAD=0f766c4`, `origin/main=4093732`.
- Ran required push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`.
- Performed one bounded same-thread integrity/conclusion step:
  - reconciled stale blocked-run state against the actual completed latent output in `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-structure-512-672-912-1168.txt`.
  - updated `/Users/jonreilly/Projects/Physics/README.md` and run-state files to reflect the completed `1168` latent summary (`rows=36`, `signatures=14`, `8/9` new rows on old signatures).

### Strongest confirmed conclusion
- The active latent continuation on `512,672,912,1168` is completed (not start-marker-only) and reinforces the existing mechanism direction.
- Late frontier growth remains mostly support-filling inside a stable four-subtype map: at `1168`, only one additional coarse signature appears while row count continues to expand.
- The coarse six-feature map still does not yield an exact low-dimensional subtype law (`best pair 23/36`, `best small tree 24/36`).
- Remote sync remains DNS-blocked while the branch is still ahead of `origin/main`.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log reconciled:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-structure-512-672-912-1168.txt` (completed summary present)

### Exact next step
- Retry helper push first on the next loop.
- If sync is available, run one bounded same-thread collision analysis inside shared `1168` coarse signatures to isolate which additional latent axis best separates subtype collisions where the current six-feature map remains inexact.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 12:21 America/New_York

### Current state
- Reconciled required preflight in canonical repo context (worklog, handoff, memory), verified lock free, and acquired `physics-science` lock.
- Reconciled git before new work:
  - `git status --short --branch` -> `main...origin/main [ahead 5]`
  - `git rev-list --left-right --count origin/main...main` -> `0 5`
  - `HEAD=7128864`, `origin/main=4093732`.
- Ran required push-first helper before science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`.
- Executed one bounded same-thread continuation step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_latent_structure.py --variant-limits 512,672,912,1168 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-structure-512-672-912-1168.txt`
- In this environment, the latent continuation again failed to produce summaries and remained at start-marker-only output (`pocket-wrap suppressor latent-structure started ...`).
- Recorded the blocked continuation state in tracked worklog commit:
  - `0faa61e` (`Record blocked latent continuation rerun status`).
- End-of-loop helper push retry after commit also failed with transient DNS:
  - `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`, `ahead=6`, `behind=0`.

### Strongest confirmed conclusion
- No mechanism conclusion changed in this run.
- The active same-thread latent continuation on `512,672,912,1168` remains blocked at start-marker-only output.
- Remote sync is still blocked by transient DNS while branch divergence is now `ahead=6`, `behind=0`.

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Log attempted/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-structure-512-672-912-1168.txt` (start marker only)

### Exact next step
- Retry helper push first on the next loop.
- If sync is available, rerun the same latent continuation with explicit runtime bounding/diagnostic capture so the run yields either a full summary or a concrete failure reason.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 11:39 America/New_York

### Current state
- Janitor reconciliation follow-up corrected tracked state after recording the DNS-blocked push attempt.
- No science or benchmark semantics changed; this was tracking-only integrity cleanup.
- Current git divergence after janitor tracking commit: `main...origin/main [ahead 4]`, `behind=0`.
- Per protocol, no second push attempt was made in this run after the initial transient DNS failure was recorded once.

### Strongest confirmed conclusion
- Local repo state is coherent and clean; remote sync is still blocked only by transient DNS resolution failure.

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-janitor/memory.md`

### Exact next step
- Start next loop with helper push retry:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 11:36 America/New_York

### Current state
- Reconciled janitor preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-janitor --purpose "janitor pass" --ttl-hours 1`.
- Reconciled git state before mutation:
  - `git status --short --branch` -> `main...origin/main [ahead 3]`.
  - `git rev-list --left-right --count origin/main...main` -> `0 3`.
  - `git log --oneline --decorate -n 8` confirms `HEAD=5e91daa`, `origin/main=4093732`.
- Ran required helper push-first step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `ahead=3`, `behind=0`, `attempts_used=4`.
- Per janitor protocol, stopped after recording the transient network failure once; no science code, benchmark artifacts, or README conclusions were changed.

### Strongest confirmed conclusion
- Repository integrity is clean locally, but sync is still blocked by transient DNS while branch remains `ahead=3` and `behind=0`.
- Janitor loop made no repo-facing fix beyond state reconciliation.

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` (write attempted; see run notes)
  - `/Users/jonreilly/.codex/automations/physics-janitor/memory.md`

### Exact next step
- Retry helper push first on the next loop.
- If sync is available, resume the pending same-thread latent continuation rerun on `512,672,912,1168`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 10:42 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - git state before science: `main...origin/main`, `ahead=0`, `behind=0`, clean tree.
- Completed the bounded same-thread sentinel step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1168 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1168.txt`
  - run completed (`total_elapsed=1104.3s`) with `nonpocket_rows=36`, `subtype_count=4`.
- Took the obvious same-thread continuation because frontier totals changed:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_latent_structure.py --variant-limits 512,672,912,1168 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-structure-512-672-912-1168.txt`
  - continuation exited abnormally in this environment and wrote only a start marker line.
- Committed the science update:
  - `3f83ac2` (`Extend sparse sentinel frontier through variant limit 1168`)
- Recorded DNS-blocked sync status in tracked state:
  - `d0232bd` (`Record DNS-blocked push state after 1168 run`)
- Final end-of-loop helper push still failed with transient DNS:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=failed`, `failure_kind=dns_failure`, `ahead=2`, `behind=0`, `attempts_used=4`.
- Updated `/Users/jonreilly/Projects/Physics/README.md` with the new `1168` frontier conclusion.

### Strongest confirmed conclusion
- The sparse sentinel at `1168` changes the active frontier: non-pocket overlap-positive membership rises from `34` to `36` while subtype count remains `4` and the both-sensitive exact-rule anchor stays unchanged (`deep_overlap_count >= 1.500`, `tp=2`).
- New rows at this rung are `local-morph-\u04cc` (add4-sensitive) and `local-morph-\u04cd` (add1-sensitive), so growth is continuing inside the same four-subtype regime.
- The latent-structure continuation on `512,672,912,1168` is still pending because this run produced only a start marker.
- Remote sync is temporarily blocked by DNS while the branch remains ahead of `origin/main`.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1168.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-structure-512-672-912-1168.txt` (start marker only)

### Exact next step
- Retry helper push first on the next loop.
- If sync is available, rerun the same-thread latent continuation and diff against the existing `1104` latent summary:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_latent_structure.py --variant-limits 512,672,912,1168 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-structure-512-672-912-1168.txt`

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 09:34 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - git state before science: `main...origin/main`, `ahead=0`, `behind=0`, clean tree.
- Ran handoff first concrete action before new science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=nothing_to_push`, `ahead=0`, `behind=0`.
- Attempted the bounded same-thread sentinel step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1168 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1168.txt`
- The sentinel command did not complete in-run and produced only a start marker line in the log file; no frontier summary was emitted in this loop.
- Recorded this blocked integrity outcome in tracked state and committed:
  - `5a758d5` (`Update blocked-run sync state after push retry`)
- Retried helper push after commit:
  - helper reported transient DNS failure (`failure_kind=dns_failure`, `ahead=2`, `behind=0`, `attempts_used=4`).

### Strongest confirmed conclusion
- No mechanism conclusion changed in this run because the `1168` sentinel did not complete.
- Repo integrity remains clean; remote sync is temporarily blocked by DNS (`ahead=2`, `behind=0`).

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1168.txt` (start marker only in this run)

### Exact next step
- Reacquire lock and rerun the same bounded sentinel command at `variant_limit=1168`.
- If `1168` finishes and changes non-pocket row count, subtype count, or coarse signature count versus `1104`, run the same-thread continuation latent-structure pass on `512,672,912,1168`.
- If `1168` finishes without changing frontier summaries, keep sparse-sentinel policy and proceed to focused collision analysis inside shared `1104` coarse signatures.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`

## 2026-03-23 09:08 America/New_York

### Current state
- Manual analysis session took the active non-pocket suppressor thread off dense laddering and onto latent-structure analysis.
- Repo-side helper drift was reduced:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py` now uses shared model-layer subtype labeling from `/Users/jonreilly/Projects/Physics/toy_event_physics.py`.
  - new analysis driver added at `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_latent_structure.py`.
- Completed a reduced smoke run at `variant_limits=480,512` and a representative broader run at `variant_limits=512,672,912,1104`.
- Validation passed:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/benchmark_regression_audit.py`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/check_feature_registry_alignment.py`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 64 --rule-limit 3`

### Strongest confirmed conclusion
- The four-subtype map is behaving like a stable taxonomy with expanding membership, not a new mechanism family every rung.
- Across representative four-subtype checkpoints (`512`, `672`, `912`, `1104`):
  - non-pocket rows grow `14 -> 15 -> 27 -> 34`
  - coarse signatures grow only `8 -> 9 -> 13 -> 14`
  - at `912`, `7/12` new rows land on already-seen signatures
  - at `1104`, `6/7` new rows land on already-seen signatures
- So late frontier growth is mostly support-filling inside existing signature basins.
- But the current coarse observable set is not yet the hidden exact law:
  - best two-axis partition at `1104` gets only `22/34`
  - best depth-2 small tree gets only `23/34`
  - best predicates are built from `core_low_degree_fraction`, `deep_overlap_count`, and `span_range`
  - so there is a finite core, but not an exact two-axis collapse on the present six coarse observables

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Code/helpers:
  - `/Users/jonreilly/Projects/Physics/toy_event_physics.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py`
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_latent_structure.py`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-latent-structure-512-672-912-1104.txt`

### Exact next step
- Retry helper push first.
- If sync is available, stop dense rung-by-rung laddering and use the ladder as a sparse sentinel:
  - run `variant_limit = 1168`
  - compare non-pocket row count, subtype count, and coarse signature count against `1104`
- If `1168` changes any of those frontier summaries, rerun latent-structure analysis on `512,672,912,1168`.
- If `1168` does not change them, stay off dense laddering and do focused collision analysis inside the shared `1104` coarse signatures instead.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1168 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1168.txt`

## 2026-03-23 07:35 America/New_York

### Current state
- Reconciled janitor preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-janitor --purpose "janitor pass" --ttl-hours 1`.
- Reconciled git state before mutation:
  - `git status --short --branch` -> `main...origin/main`.
  - `git rev-list --left-right --count origin/main...main` -> `0 0`.
  - `git log --oneline --decorate -n 8` -> `HEAD` and `origin/main` both at `161cf63` (`Extend nonpocket frontier through variant limit 1104`).
- Ran required helper push-first step:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper result: `status=nothing_to_push`, `ahead=0`, `behind=0`.
- Repaired stale state reporting only (no science or benchmark changes): updated tracked handoff/worklog state to current synced facts and recorded the autopilot-memory write as sandbox-blocked for this run.

### Strongest confirmed conclusion
- Repo is clean and synced (`ahead=0`, `behind=0`) at `161cf63`; no push retry or confidence pass is needed.
- Janitor loop found no additional cleanup work beyond state reconciliation.

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` (write blocked by sandbox permissions in this run)
  - `/Users/jonreilly/.codex/automations/physics-janitor/memory.md`

### Exact next step
- On the next loop, rerun janitor preflight and stop immediately if branch and state files remain aligned.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`
## 2026-03-23 06:33 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - git state before science: `main...origin/main [ahead 16]`, `behind=0`.
- Ran required push-first step before new science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper reported transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`).
- Continued the active same-thread mechanism step with one bounded deeper rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1104 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1104.txt`
- `1104` completed successfully (`total_elapsed=1012.1s`) and added one new non-pocket overlap-positive row relative to `1088`/`1072`.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the frontier expansion at `1104`.

### Strongest confirmed conclusion
- The growth phase continues one rung deeper after `1088`:
  - non-pocket overlap-positive rows rise from `33` to `34` at `1104`;
  - subtype count remains `4`;
  - the only new row is `local-morph-\u04ab` (`add1-sensitive`, `ge6-only/dpadj-only`, `cross=n`);
  - both-sensitive exact-rule anchor is unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `1056..1072` was a short hold, `1088` resumed growth, and `1104` continues that growth by adding a new add1-sensitive row.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1104.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1088.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1072.txt`

### Exact next step
- Retry helper push first on next loop.
- If sync is available, run one deeper rung (`variant_limit = 1120`) and diff subtype context/rule sections versus `1104` and `1088`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1120 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1120.txt`

## 2026-03-23 05:34 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - git state before science: `main...origin/main [ahead 15]`, `behind=0`.
- Ran required push-first step before new science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper reported transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`).
- Continued the active same-thread mechanism step with one bounded deeper rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1088 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1088.txt`
- `1088` completed successfully (`total_elapsed=993.5s`) and added one new non-pocket overlap-positive row relative to `1072`/`1056`.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the new frontier expansion at `1088`.

### Strongest confirmed conclusion
- The `1056..1072` short hold breaks at `1088` without changing subtype count or both-sensitive anchors:
  - non-pocket overlap-positive rows rise from `32` to `33` at `1088`;
  - subtype count remains `4`;
  - the only new row is `local-morph-\u0492` (`add4-sensitive`, `dpadj-only/ge6-only`, `cross=Y`);
  - both-sensitive exact-rule anchor is unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `1040/1056` was a growth phase, `1056..1072` was a short hold, and `1088` resumes growth by extending the add4-sensitive branch.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1088.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1072.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1056.txt`

### Exact next step
- Retry helper push first on next loop.
- If sync is available, run one deeper rung (`variant_limit = 1104`) and diff subtype context/rule sections versus `1088` and `1072`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1104 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1104.txt`

## 2026-03-23 04:32 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in required order.
  - lock was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - git state before science: `main...origin/main [ahead 14]`, `behind=0`.
- Ran required push-first step before new science:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper reported transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`).
- Continued the active same-thread mechanism step with one bounded deeper rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1072 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1072.txt`
- `1072` completed successfully (`total_elapsed=977.7s`) and exactly matched `1056` subtype membership and exact-rule behavior.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the newly confirmed `1056..1072` short hold.

### Strongest confirmed conclusion
- The `1040/1056` growth phase pauses at `1072`:
  - non-pocket overlap-positive rows remain `32` at `1072` (unchanged vs `1056`);
  - subtype count remains `4`;
  - no new row appears beyond `local-morph-\u047f`;
  - both-sensitive exact-rule anchor is unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `976..1024` was the prior hold, `1040/1056` resumed growth, and `1056..1072` is now the next confirmed short hold.

### Files and results changed in this run
- Narrative:
  - `/Users/jonreilly/Projects/Physics/README.md`
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1072.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1056.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1040.txt`

### Exact next step
- Retry helper push first on next loop.
- If sync is available, run one deeper rung (`variant_limit = 1088`) and diff subtype context/rule sections versus `1072` and `1056`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1088 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1088.txt`

## 2026-03-23 03:36 America/New_York

### Current state
- Janitor protocol preflight reconciled in canonical repo context:
  - read `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`, `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`, and `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` in order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-janitor --purpose "janitor pass" --ttl-hours 1`.
- Reconciled git state before mutation:
  - `git status --short --branch` -> `main...origin/main [ahead 12]` before janitor commit.
  - `git rev-list --left-right --count origin/main...main` -> `0 12` before janitor commit.
  - `git log --oneline --decorate -n 8` showed `d051a17` at pre-fix `HEAD`.
- Required helper push-first step executed:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper returned transient DNS failure (`failure_kind=dns_failure`, `error=DNS lookup failed for github.com`, `attempts_used=4`).
- Janitor repaired stale tracking state only (no new science) so worklog/handoff/memory agree on commit and sync facts.
- Committed repo-tracked janitor repair as `7a4082a` (`Janitor reconcile state after push retry`) and retried helper push; final result remained transient DNS failure with `ahead=13`, `behind=0`.

### Strongest confirmed conclusion
- Repo integrity is intact; only remote sync is blocked by transient DNS resolution.
- Local `main` remains `ahead 13`, `behind 0`; latest commit is `7a4082a` (`Janitor reconcile state after push retry`).
- No benchmark semantics changed in this janitor pass, so no confidence pass was needed.

### Files and results changed in this run
- Updated run tracking:
  - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-janitor/memory.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` (write blocked by sandbox permissions in this run)

### Exact next step
- Retry helper push first on the next loop.
- If helper push succeeds, continue from science handoff (`variant_limit=1072`); otherwise stop without widening scope.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`

## 2026-03-23 03:33 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read worklog, handoff, and autopilot memory in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - branch state before science: `main` ahead of `origin/main` by `11` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1056 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1056.txt`
- `1056` completed successfully (`total_elapsed=969.0s`) and added one new non-pocket row relative to `1040`/`1024`.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the `1056` frontier expansion.

### Strongest confirmed conclusion
- Growth continues one rung past `1040` with unchanged subtype map and unchanged both-sensitive exact-rule anchor:
  - non-pocket overlap-positive rows rise from `31` to `32` at `1056`;
  - subtype count remains `4`;
  - the only new row is `local-morph-\u047f` (`pair-only-sensitive`, `dpadj-only/dpadj-only`, `cross=Y`);
  - both-sensitive exact-rule anchor is unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `976..1024` was the last short hold, `1040` resumed growth, and `1056` continues the same growth phase.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1056.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1040.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1024.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 1072`) and diff subtype context/rule sections versus `1056` and `1040`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1072 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1072.txt`

## 2026-03-23 02:32 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read worklog, handoff, and autopilot memory in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - branch state before science: `main` ahead of `origin/main` by `9` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1040 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1040.txt`
- `1040` completed successfully (`total_elapsed=952.4s`) and introduced one new non-pocket row relative to `1024`/`1008`.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the new frontier expansion at `1040`.
- Committed tracked science updates as `527e22b` (`Record nonpocket frontier expansion at variant limit 1040`).
- End-of-loop helper push retry failed again with transient DNS resolution (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), leaving `main` ahead of `origin/main` by `10`.

### Strongest confirmed conclusion
- `976..1024` was a short hold and growth resumes at `1040`:
  - non-pocket overlap-positive rows rise from `30` to `31`;
  - subtype count remains `4`;
  - the only new row is `local-morph-\u0461` (`add1-sensitive`, `neither/dpadj-only`, `cross=Y`);
  - both-sensitive exact-rule anchor is unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `976` was a two-row expansion, `976..1024` held, and `1040` starts the next add1-sensitive growth step.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1040.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1024.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1008.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 1056`) and diff subtype context/rule sections versus `1040` and `1024`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1056 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1056.txt`

## 2026-03-23 01:32 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read worklog, handoff, and autopilot memory in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - branch state before science: `main` ahead of `origin/main` by `8` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1024 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1024.txt`
- `1024` completed successfully (`total_elapsed=937.1s`) and exactly matched `1008` and `992` subtype membership/exact-rule behavior.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the newly confirmed `976..1024` short hold.

### Strongest confirmed conclusion
- `976` remains a two-row bump, not immediate further growth:
  - non-pocket overlap-positive rows remain `30` at `1024` (unchanged vs `1008` and `992`);
  - subtype count remains `4`;
  - no new row appears beyond `local-morph-\u0428` and `local-morph-\u0430`;
  - both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `944..960` was a short hold, `976` added two rows, and `976..1024` is now the next confirmed short hold.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1024.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1008.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-992.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 1040`) and diff subtype context/rule sections versus `1024` and `1008`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1040 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1040.txt`

## 2026-03-23 00:32 America/New_York

### Current state
- Reconciled preflight first in canonical repo context:
  - read worklog, handoff, and autopilot memory in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - branch state before science: `main` ahead of `origin/main` by `6` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1008 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1008.txt`
- `1008` completed successfully (`total_elapsed=931.7s`) and exactly matched `992` and `976` subtype membership/exact-rule behavior.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the newly confirmed `976..1008` short hold.
- Committed tracked science updates as `5b2730f` (`Confirm nonpocket hold through variant limit 1008`).
- End-of-loop helper push retry failed again with transient DNS resolution (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), leaving `main` ahead of `origin/main` by `7`.

### Strongest confirmed conclusion
- `976` remains a two-row bump, not immediate further growth:
  - non-pocket overlap-positive rows remain `30` at `1008` (unchanged vs `992` and `976`);
  - subtype count remains `4`;
  - no new row appears beyond `local-morph-\u0428` and `local-morph-\u0430`;
  - both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `944..960` was a short hold, `976` added two rows, and `976..1008` is now the next confirmed short hold.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1008.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-992.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-976.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 1024`) and diff subtype context/rule sections versus `1008` and `992`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1024 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1024.txt`

## 2026-03-22 23:36 America/New_York

### Current state
- Ran janitor protocol preflight in canonical repo context (worklog, handoff, and autopilot memory reconciled first).
- Acquired cooperative lock with `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-janitor --purpose "janitor pass" --ttl-hours 1`.
- Re-ran required helper push first:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper reported transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so janitor stopped science advancement and only repaired state drift.
- Reconciled tracked state mismatch:
  - prior top worklog entry still reported `ahead ... by 4`, while real git state was already one commit further ahead (`4d2d4bb`) from same-loop bookkeeping.
  - refreshed handoff + autopilot memory to match real HEAD/sync condition and preserve correct next action.
- No benchmark or semantics change was introduced in this janitor pass, so no confidence check was required.

### Strongest confirmed conclusion
- Science frontier conclusions are unchanged: `variant_limit=992` still matches `976` (30 non-pocket rows, 4 subtypes, unchanged both-sensitive exact-rule anchor at `deep_overlap_count >= 1.500`).

### Files and results changed in this run
- `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
- `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Retry helper push first; if sync is available, continue with one bounded deeper rung at `variant_limit=1008` and compare against `992`/`976`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`

## 2026-03-22 23:31 America/New_York

### Current state
- Reconciled lock + git state first in canonical repo context:
  - lock was free, then acquired via `automation_lock.py acquire --owner physics-science`.
  - branch state before science: `main` ahead of `origin/main` by `2` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- Push helper again returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 992 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-992.txt`
- `992` completed successfully (`total_elapsed=918.1s`) and exactly matched `976` subtype membership and exact-rule behavior.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the newly confirmed `976..992` short hold.
- Committed tracked science updates as `7bc1725` (`Confirm nonpocket hold through variant limit 992`), then committed the final synced status note as `e348e79` (`Record push blockage after variant limit 992 update`).
- End-of-loop helper push retry failed again with transient DNS resolution (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), leaving `main` ahead of `origin/main` by `4`.

### Strongest confirmed conclusion
- `976` is currently a two-row bump, not immediate further growth:
  - non-pocket overlap-positive rows remain `30` at `992` (unchanged vs `976`);
  - subtype count remains `4`;
  - no new row appears beyond `local-morph-\u0428` and `local-morph-\u0430`;
  - both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `944..960` was a short hold, `976` added two rows, and `976..992` is now the next confirmed short hold.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-992.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-976.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-960.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 1008`) and diff subtype context/rule sections versus `992` and `976`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1008 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1008.txt`
## 2026-03-22 22:32 America/New_York

### Current state
- Reconciled lock + git state first in canonical repo context:
  - lock was free, then acquired via `automation_lock.py acquire --owner physics-science`.
  - branch state before science: `main` ahead of `origin/main` by `1` commit (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- Push helper again returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 976 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-976.txt`
- `976` completed successfully (`total_elapsed=907.6s`) and expanded non-pocket subtype membership relative to `960`/`944`.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the new frontier expansion at `976`.

### Strongest confirmed conclusion
- `944..960` was a short hold, and growth resumes at `976` without a subtype-map change:
  - non-pocket overlap-positive rows increase from `28` to `30`;
  - subtype count remains `4`;
  - new rows are `local-morph-\u0428` (`add1-sensitive`, `ge6-only/dpadj-only`) and `local-morph-\u0430` (`add4-sensitive`, `dpadj-only/ge6-only`);
  - both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-976.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-960.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 992`) and diff subtype context/rule sections versus `976` and `960`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 992 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-992.txt`
## 2026-03-22 21:32 America/New_York

### Current state
- Reconciled lock + git state first in canonical repo context:
  - lock was free, then acquired via `automation_lock.py acquire --owner physics-science`.
  - branch state before science: `main` ahead of `origin/main` by `4` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- Push helper again returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 960 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-960.txt`
- `960` completed successfully (`total_elapsed=895.3s`) and exactly matched the `944` subtype membership and exact-rule table.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the newly confirmed `944..960` short hold.

### Strongest confirmed conclusion
- `944` is currently a one-row bump, not immediate further growth:
  - non-pocket overlap-positive rows remain `28` at `960` (unchanged vs `944`);
  - subtype count remains `4`;
  - no new row appears beyond `local-morph-\u040f`;
  - both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `896..928` was a `27`-row hold, `944` added one row, and `944..960` is now the next confirmed short hold.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-960.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 976`) and diff subtype context/rule sections versus `960` and `944`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 976 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-976.txt`
## 2026-03-22 20:31 America/New_York

### Current state
- Reconciled git and lock state first in canonical repo context:
  - lock was free, then acquired via `automation_lock.py acquire --owner physics-science`.
  - branch state before science: `main` ahead of `origin/main` by `2` commits.
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- Push helper returned transient DNS failure again (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so proceeded with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 944 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`
- `944` completed successfully (`total_elapsed=886.5s`) and introduced one new non-pocket row relative to `928/912`.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the new frontier behavior at `944`.
- Committed tracked science updates as `2a01cd5` (`Record nonpocket frontier expansion at variant limit 944`).
- End-of-loop helper push retry failed again with transient DNS resolution (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), leaving `main` ahead of `origin/main` by `3`.

### Strongest confirmed conclusion
- `896..928` was a real short stable hold at `27` rows, but `944` starts the next growth phase:
  - non-pocket overlap-positive rows rise from `27` to `28`;
  - the only new row at this rung is `local-morph-\u040f`;
  - subtype count remains `4`;
  - `pair-only-sensitive` expands from `4` to `5` rows;
  - the both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 960`) to determine whether `944` is a one-row bump or the start of another accelerating band.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 960 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-960.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`

## 2026-03-22 19:30 America/New_York

### Current state
- Reconciled the active branch before new work (`main` and `origin/main` were in sync at `47d1113`).
- Continued the active non-pocket subtype frontier thread with one bounded deeper rung in canonical repo context:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 928 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`
- Run completed successfully (`total_elapsed=867.8s`).
- `928` exactly matched `912` and `896` for non-pocket subtype membership and the exact-rule table.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to extend the confirmed `27`-row hold through `928`.
- End-of-loop push via `automation_push.py` failed with transient DNS resolution (`failure_kind=dns_failure`, `Could not resolve github.com`), so `main` remains ahead locally.

### Strongest confirmed conclusion
- `896..928` is now a confirmed stable hold at `27` non-pocket overlap-positive rows:
  - no new rows were added at `928` relative to `912/896`;
  - subtype count remains `4`;
  - `pair-only-sensitive` remains at `4` rows;
  - the both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-896.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 944`) to test whether the `896..928` stable band persists or the next growth phase resumes.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 944 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`

## 2026-03-22 19:01 America/New_York

### Current state
- Reconciled the synced `848` frontier first, then continued the active non-pocket subtype thread by executing four deeper rungs in canonical repo context:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 864 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-864.txt`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 880 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-880.txt`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 896 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-896.txt`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 912 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`
- `864` and `880` exactly matched the `832/848` frontier behavior.
- `896` introduced two new rows, and `912` exactly matched that expanded frontier.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to record the stable `832..880` band and the new `896/912` hold.

### Strongest confirmed conclusion
- `832..880` is now a real stable band:
  - non-pocket overlap-positive rows remain `25` across `832`, `848`, `864`, and `880`;
  - subtype count remains `4`;
  - the both-sensitive exact-rule family stays unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- `896` and `912` then form the next confirmed hold:
  - non-pocket overlap-positive rows rise from `25` to `27` by adding `local-morph-\u03d4` and `local-morph-\u03d8`;
  - subtype count still remains `4`;
  - `pair-only-sensitive` expands to `4` rows;
  - the both-sensitive exact-rule family remains unchanged.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-864.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-880.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-896.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 928`) to test whether `896/912` is another short stable band or whether the next growth phase resumes immediately.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 928 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-896.txt`

## 2026-03-22 17:30 America/New_York

### Current state
- Resumed the active non-pocket subtype frontier thread and executed one bounded deeper rung in canonical repo context:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 848 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-848.txt`
- Run completed successfully (`total_elapsed=817.7s`).
- Reconciled git before new work and retried push first; push remains unavailable in this environment (`Could not resolve host: github.com`).
- Updated `/Users/jonreilly/Projects/Physics/README.md` to reflect the newly confirmed `832/848` hold.

### Strongest confirmed conclusion
- `848` is an exact replication of the `832` frontier behavior except for the header limit value:
  - non-pocket overlap-positive rows remain `25` (no new rows);
  - subtype count remains `4`;
  - both-sensitive exact-rule family is unchanged and still anchored by `deep_overlap_count >= 1.500` (`2` true positives).
- So `752..832` remains the accelerating growth phase, and `832/848` is now the first confirmed hold at that new `25`-row level.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-848.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`

### Exact next step
- Reconcile/push `main` first, then run one deeper rung (`variant_limit = 864`) to test whether `832/848` is a stable band or the next growth step resumes immediately.

### First concrete action
- Execute:
  - `git -C /Users/jonreilly/Projects/Physics push`
  - If push succeeds:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 864 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-864.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-848.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`

## 2026-03-22 16:30 America/New_York

### Current state
- Resumed the active non-pocket subtype frontier thread and executed one bounded deeper rung in canonical repo context:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 832 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`
- Run completed successfully (`total_elapsed=814.3s`) and extended the active growth frontier.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to reflect the new rung and unchanged exact-rule behavior.
- Committed the repo updates locally, but push failed due network/DNS (`Could not resolve host: github.com`), so `main` remains ahead of `origin/main`.

### Strongest confirmed conclusion
- The accelerating non-pocket growth phase continues at `832` rather than settling:
  - non-pocket overlap-positive rows increase from `23` to `25`;
  - two new rows appear: `local-morph-\u0399` (add1-sensitive, `neither/dpadj-only`) and `local-morph-\u03a0` (add4-sensitive, `dpadj-only/neither`);
  - subtype count remains `4`;
  - both-sensitive exact-rule family remains unchanged and still anchored by `deep_overlap_count >= 1.500` (`2` true positives).

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-800.txt`

### Exact next step
- Reconcile/push `main` first, then run one deeper rung (`variant_limit = 848`) to test whether this accelerating phase continues immediately or starts to plateau.

### First concrete action
- Execute:
  - `git -C /Users/jonreilly/Projects/Physics push`
  - If push succeeds:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 848 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-848.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`

## 2026-03-22 15:45 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing three deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 784 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-784.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 800 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-800.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 816 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`
- All three runs completed successfully and each introduced additional non-pocket overlap-positive rows beyond the `752/768` frontier.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to record the accelerating `784..816` growth phase.

### Strongest confirmed conclusion
- The `752/768` expansion did not settle into a stable band. Instead, `784`, `800`, and `816` form a live accelerating growth phase:
  - `784` raises non-pocket overlap-positive rows from `18` to `20` by adding `local-morph-\u036c` and `local-morph-\u036f`;
  - `800` raises them again from `20` to `22` by adding `local-morph-\u0372` and `local-morph-\u037a`;
  - `816` raises them once more from `22` to `23` by adding `local-morph-\u0386`;
  - subtype count still remains `4` throughout.
- The subtype mix also tightened:
  - `pair-only-sensitive` now has `3` rows after `784`;
  - the both-sensitive exact rule family broadens from `1` true positive to `2` at `800` and stays there at `816`, still anchored by `deep_overlap_count >= 1.500`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-784.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-800.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 832`) to test whether this accelerating growth phase continues immediately or finally settles.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 832 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-800.txt`

## 2026-03-22 14:14 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing five deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 720 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-720.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 736 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-736.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 752 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-752.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 768 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-768.txt`
- `720` and `736` exactly matched the `688/704` breakpoint band.
- `752` and `768` then each introduced one new row beyond that band.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to record the stable `688..736` band and the new `752/768` growth phase.

### Strongest confirmed conclusion
- The next stable band after `528..672` now runs through `688..736`:
  - non-pocket overlap-positive rows remain `16` across `688`, `704`, `720`, and `736`;
  - subtype count remains `4`;
  - new row `local-morph-\u0310` persists as an add1-sensitive case with response `neither/dpadj-only`;
  - the old exact add1-sensitive rule remains absent from the exact-rule table, while the both-sensitive rule `deep_overlap_count >= 1.500` still holds.
- `752` and `768` then mark the next live growth phase:
  - `752` adds `local-morph-\u034b`, raising non-pocket overlap-positive rows from `16` to `17`;
  - `768` adds `local-morph-\u035b`, raising them again from `17` to `18`;
  - subtype count still remains `4`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-720.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-736.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-752.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-768.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 784`) to test whether the new `752/768` growth phase persists immediately or settles into another stable band.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 784 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-784.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-768.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-752.txt`

## 2026-03-22 13:22 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing four deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 656 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-656.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 672 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-672.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 688 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-688.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 704 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-704.txt`
- The first two runs exactly matched the `528/544/560/576/592/608/624/640` band.
- The next two runs matched each other and introduced the same new row `local-morph-\u0310`.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to extend the stable four-subtype checkpoint through `672` and record the new `688/704` breakpoint.

### Strongest confirmed conclusion
- The four-subtype regime is now stable through `672`:
  - non-pocket overlap-positive rows remain `15` across `528`, `544`, `560`, `576`, `592`, `608`, `624`, `640`, `656`, and `672`;
  - subtype count remains `4`;
  - the `pair-only-sensitive` subtype persists with two rows (`local-morph-\u0236`, `local-morph-\u026e`);
  - the exact add1-sensitive rule remains the 2-term low-degree cut `span_range >= 2.500 and core_low_degree_fraction >= 0.275`.
- `688` and `704` then mark the next confirmed breakpoint:
  - non-pocket overlap-positive rows rise from `15` to `16`;
  - new row `local-morph-\u0310` joins as an add1-sensitive case with response `neither/dpadj-only`;
  - subtype count stays `4`;
  - the old exact add1-sensitive rule drops out of the exact-rule table, while the both-sensitive rule `deep_overlap_count >= 1.500` still holds.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-656.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-672.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-688.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-704.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 720`) to test whether the new `688/704` breakpoint persists as a stable band or expands again immediately.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 720 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-720.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-704.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-688.txt`

## 2026-03-22 12:21 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing three deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 608 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-608.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 624 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-624.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 640 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-640.txt`
- All three runs completed successfully and exactly matched the `528/544/560/576/592` band.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to extend the stable four-subtype checkpoint through `640`.

### Strongest confirmed conclusion
- The four-subtype regime is now stable through `640`:
  - non-pocket overlap-positive rows remain `15` across `528`, `544`, `560`, `576`, `592`, `608`, `624`, and `640`;
  - subtype count remains `4`;
  - the `pair-only-sensitive` subtype persists with two rows (`local-morph-\u0236`, `local-morph-\u026e`);
  - the exact add1-sensitive rule remains the 2-term low-degree cut `span_range >= 2.500 and core_low_degree_fraction >= 0.275`.
- So `528..640` is now the first stable checkpoint of the new four-subtype regime.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-608.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-624.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-640.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 656`) to test whether the stable four-subtype band persists beyond `640`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 656 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-656.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-640.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-624.txt`

## 2026-03-22 11:25 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing one deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 592 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-592.txt`
- The run completed successfully and exactly matched the `528/544/560/576` band.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to extend the stable four-subtype checkpoint through `592`.

### Strongest confirmed conclusion
- The four-subtype regime is now stable through `592`:
  - non-pocket overlap-positive rows remain `15` across `528`, `544`, `560`, `576`, and `592`;
  - subtype count remains `4`;
  - the `pair-only-sensitive` subtype persists with two rows (`local-morph-\u0236`, `local-morph-\u026e`);
  - the exact add1-sensitive rule remains the 2-term low-degree cut `span_range >= 2.500 and core_low_degree_fraction >= 0.275`.
- So `528..592` is now the first stable checkpoint of the new four-subtype regime.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-592.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-576.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-560.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 608`) to test whether the stable four-subtype band persists beyond `592`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 608 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-608.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-592.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-576.txt`

## 2026-03-22 11:12 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing one deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 576 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-576.txt`
- The run completed successfully and exactly matched the `528/544/560` band.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to extend the stable four-subtype checkpoint through `576`.

### Strongest confirmed conclusion
- The four-subtype regime is now stable through `576`:
  - non-pocket overlap-positive rows remain `15` across `528`, `544`, `560`, and `576`;
  - subtype count remains `4`;
  - the `pair-only-sensitive` subtype persists with two rows (`local-morph-\u0236`, `local-morph-\u026e`);
  - the exact add1-sensitive rule remains the 2-term low-degree cut `span_range >= 2.500 and core_low_degree_fraction >= 0.275`.
- So `528..576` is now the first stable checkpoint of the new four-subtype regime.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-576.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-560.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-544.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 592`) to test whether the stable four-subtype band persists beyond `576`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 592 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-592.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-576.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-560.txt`

## 2026-03-22 10:14 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing one deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 544 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-544.txt`
- The run completed successfully and exactly matched the `528` rung.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to capture the first stable checkpoint of the four-subtype regime.

### Strongest confirmed conclusion
- The new four-subtype regime is now stable through `544`:
  - non-pocket overlap-positive rows remain `15` across `528` and `544`;
  - subtype count remains `4`;
  - the `pair-only-sensitive` subtype persists with two rows (`local-morph-\u0236`, `local-morph-\u026e`);
  - the exact add1-sensitive rule is now the single 2-term low-degree cut `span_range >= 2.500 and core_low_degree_fraction >= 0.275`.
- So `528/544` is the first stable checkpoint of the new four-subtype regime, not just another moving expansion front.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-544.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-528.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-512.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 560`) to test whether the stable four-subtype band persists beyond `544`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 560 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-560.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-544.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-528.txt`

## 2026-03-22 09:53 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing one deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 512 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-512.txt`
- The run completed successfully and extended the new four-subtype regime.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.

### Strongest confirmed conclusion
- The new four-subtype regime persists and is still actively growing at `512`:
  - non-pocket overlap-positive rows rise from `13` to `14`;
  - subtype count remains `4`;
  - new row: `base:taper-wrap:local-morph-\u025d` (add1-sensitive);
  - the `pair-only-sensitive` fourth subtype persists.
- Exact add1-sensitive rules remain 2-term low-degree-gated cuts, but the strongest exact form has now shifted to rules like `core_low_degree_fraction >= 0.275 and mean_center >= -0.321`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-512.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-496.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-480.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 528`) to test whether the four-subtype regime continues expanding immediately beyond `512`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 528 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-528.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-512.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-496.txt`

## 2026-03-22 09:43 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing two deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 480 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-480.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 496 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-496.txt`
- Both runs completed successfully and matched each other exactly.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to capture the new subtype-count regime.

### Strongest confirmed conclusion
- `480/496` marks the start of a new four-subtype regime:
  - non-pocket overlap-positive rows rise from `11` to `13`;
  - subtype count rises from `3` to `4`;
  - new rows include `local-morph-\u0232` and `local-morph-\u0236`;
  - the new fourth subtype is `pair-only-sensitive`, represented by `local-morph-\u0236`.
- The old crossing-based one-term add1 separator is no longer sufficient in this regime. Exact add1-sensitive rules are now low-degree-gated 2-term cuts, such as `pocket_fraction <= 0.128 and core_low_degree_fraction >= 0.275`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-480.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-496.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-464.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-448.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 512`) to test whether the new four-subtype regime persists beyond `496`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 512 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-512.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-496.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-480.txt`

## 2026-03-22 08:48 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing three deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 400 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-400.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 416 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-416.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 432 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-432.txt`
- All three runs completed successfully and matched the new `368/384` breakpoint band exactly.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.

### Strongest confirmed conclusion
- The new add1-sensitive branch growth is now stable through `432`:
  - non-pocket overlap-positive rows remain `9` across `368`, `384`, `400`, `416`, and `432`;
  - subtype count remains `3`;
  - the exact one-term add1-sensitive separator still holds via `crosses_midline = n`, now with `3` true positives and `0` errors.
- So the long `240..352` plateau has given way to a new stable band at `368..432`, and the change is still branch growth inside the existing add1-sensitive non-crossing family rather than a new subtype split.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-400.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-416.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-432.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-384.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-368.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 448`) to test whether the new `368..432` stable band still holds.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 448 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-448.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-432.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-416.txt`

## 2026-03-22 07:51 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing two deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 368 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-368.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 384 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-384.txt`
- Both runs completed successfully and matched each other exactly.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to capture the first post-`352` breakpoint.

### Strongest confirmed conclusion
- The long `240..352` plateau ends at `368/384` with the first new row after that band:
  - non-pocket overlap-positive rows rise from `8` to `9`;
  - subtype count remains `3`;
  - new row: `base:taper-wrap:local-morph-\u01cd` (add1-sensitive, non-crossing branch);
  - the exact one-term add1-sensitive separator still holds via `crosses_midline = n`, now with `3` true positives and `0` errors.
- So the new growth is inside the existing add1-sensitive non-crossing branch, not a new subtype family.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-368.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-384.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-352.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 400`) to test whether the new add1-sensitive branch growth persists beyond `384`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 400 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-400.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-384.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-368.txt`

## 2026-03-22 07:27 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing one deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 352 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-352.txt`
- The `352` run completed successfully and exactly matched the existing `288`/`304`/`320`/`336` subtype membership and exact-rule table.
- Tightened hourly automation behavior:
  - added [AUTOPILOT_PROTOCOL.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md)
  - updated `/Users/jonreilly/.codex/automations/physics-autopilot/automation.toml` to require sync reconciliation first, newest-first worklog updates, and one bounded step by default.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.

### Strongest confirmed conclusion
- The post-`208` add4-sensitive crossing expansion now remains plateaued through `352`:
  - non-pocket overlap-positive rows remain `8`;
  - subtype count remains `3`;
  - the add1-sensitive separator remains exact via `crosses_midline = n` (`2/2`, `0` FP, `0` FN).
- No subtype-membership or exact-rule-table changes appear across `288`, `304`, `320`, `336`, or `352`.
- The automation is now better aligned with this workflow because it will reconcile git/worklog/handoff state before new science work and will prepend the newest work-log entry instead of appending.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
  - [AUTOPILOT_PROTOCOL.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/automation.toml`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-352.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-336.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-320.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 368`) to test whether this stabilized `240..352` plateau still holds.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 368 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-368.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-352.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-336.txt`

## 2026-03-22 07:18 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing two deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 320 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-320.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 336 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-336.txt`
- Both runs completed successfully and matched the existing `288`/`304` outputs exactly.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to fold the deeper plateau into the tracked science story.

### Strongest confirmed conclusion
- The post-`208` add4-sensitive crossing expansion now remains plateaued through `336`:
  - non-pocket overlap-positive rows remain `8`;
  - subtype count remains `3`;
  - the add1-sensitive separator remains exact via `crosses_midline = n` (`2/2`, `0` FP, `0` FN).
- There were no subtype-membership or exact-rule-table changes across `288`, `304`, `320`, or `336`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-288.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-304.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-320.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-336.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 352`) to test whether this stabilized `240..336` plateau still holds.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 352 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-352.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-336.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-320.txt`

## 2026-03-22 07:16 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by validating and diffing the completed deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 288 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-288.txt`
- Confirmed the `288` run is complete (`total_elapsed=279.9s`) and compared against `272` and `256`; no subtype-membership or exact-rule-table changes were found.
- Updated mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to carry conclusions through `288`.
- Ran cheap audit smoke check after updates:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 8 > /tmp/2026-03-22-nonpocket-subtype-rules-8-post288-smoke.txt`
  - `real 27.110s`, `user 26.57s`, `sys 0.18s`.

### Strongest confirmed conclusion
- The post-`208` add4-sensitive crossing expansion is still plateaued through `288`:
  - non-pocket overlap-positive rows remain `8` (same as `240`/`256`/`272`);
  - subtype count remains `3`;
  - add1-sensitive separator remains exact via `crosses_midline = n` (`0` FP / `0` FN).
- Diffs versus `272` and `256` are metadata-only (start/end timestamps, elapsed runtime, and `variant_limit`).

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-288.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
  - `/tmp/2026-03-22-nonpocket-subtype-rules-8-post288-smoke.txt`
- Commit status:
  - Committed in this run: `1c2930c` (`Document nonpocket subtype plateau through variant limit 288`).
  - Push attempt failed in sandbox (`Could not resolve host: github.com`), so remote sync could not be refreshed from this run context.
  - Last known local/remote relation in git metadata: `origin/main...main = 0 behind / 1 ahead`.

### Exact next step
- Run one deeper rung (`variant_limit = 304`) to test whether the `240..288` plateau continues unchanged.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 304 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-304.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-288.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`

## 2026-03-22 06:19 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing the queued deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 272 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
- Run completed successfully:
  - `real 258.72s`, `user 258.34s`, `sys 0.27s`.
- Diffed `272` output against `256` and `240`, then updated mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.

### Strongest confirmed conclusion
- The non-pocket subtype plateau persists through `272`:
  - non-pocket overlap-positive rows remain `8` (same as `240` and `256`);
  - subtype count remains `3`;
  - add1-sensitive separator remains exact via `crosses_midline = n` (`0` FP / `0` FN).
- No subtype-membership or exact-rule-table changes were observed vs `256`/`240` beyond timestamp/runtime lines.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
  - `/tmp/2026-03-22-nonpocket-subtype-rules-8-post272-smoke.txt`
- Commit status:
  - Committed and pushed: `e67a152` (`Document nonpocket subtype plateau through variant limit 272`), `e25c121` (`Sync worklog with pushed 272 plateau commit state`).
  - Repository sync is current at this checkpoint: `main` == `origin/main` at `e25c121`.

### Exact next step
- Run one deeper rung (`variant_limit = 288`) to test whether the `240..272` plateau continues unchanged.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 288 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-288.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`

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
  - Committed and pushed: `5a29129` (`Document nonpocket subtype plateau through variant limit 256`).
  - Repository sync at end of run: `main` == `origin/main` at `5a29129`.

### Exact next step
- Run one deeper rung (`variant_limit = 272`) to test whether the add4-sensitive crossing branch remains plateaued after the `256` hold or resumes growth.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 272 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
- Then diff subtype context/exact-rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
