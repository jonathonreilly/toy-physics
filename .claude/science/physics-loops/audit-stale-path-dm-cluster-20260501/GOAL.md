# Audit Stale-Path DM Cluster Fix — 2026-05-01

**Mode:** session-bound campaign (5h budget)
**Worktree:** /tmp/physics-loop-12h-20260430
**Target status:** audit-clean for the affected DM-cluster runners

## Goal

Address a cluster of audit-failed/conditional rows whose runners contain stale
`read("docs/X.md")` references to notes deleted by commit `d2e754fdc`
(2026-04-16, "Trim DM package to science-only surface"). The deletions were
deliberate; the runners still try to verify content against those deleted
files and fail with `FileNotFoundError` (or, in restricted audit envs,
"primary runner returned nonzero").

## Affected runners and notes

Found by scanning all on-main runners cited in audit ledger for `read("docs/")`
calls where the target no longer exists at the cited path:

| runner | stale paths read | claim_id | criticality |
|---|---|---|---|
| `frontier_dm_neutrino_breaking_triplet_axiom_law_attempt.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md`, `DM_LEPTOGENESIS_NOTE.md` | `dm_neutrino_breaking_triplet_axiom_law_attempt_note_2026-04-15` | leaf |
| `frontier_dm_neutrino_triplet_normalization_target.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md`, `DM_LEPTOGENESIS_BENCHMARK_DECOMPOSITION_NOTE_2026-04-15.md` | `dm_neutrino_triplet_normalization_target_note_2026-04-15` | leaf |
| `frontier_dm_neutrino_triplet_character_source_theorem.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md` | `dm_neutrino_triplet_character_source_theorem_note_2026-04-15` | leaf |
| `frontier_dm_neutrino_triplet_even_response_theorem.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md` | `dm_neutrino_triplet_even_response_theorem_note_2026-04-15` | leaf |
| `frontier_dm_neutrino_breaking_triplet_cp_theorem.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md` | (multiple consumers) | leaf |
| `frontier_dm_neutrino_veven_bosonic_normalization_theorem.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md`, `DM_LEPTOGENESIS_NOTE.md` | (multiple consumers) | leaf |
| `frontier_dm_leptogenesis_projection_theorem.py` | `DM_LEPTOGENESIS_FULL_AXIOM_CLOSURE_NOTE_2026-04-16.md` (moved to `docs/work_history/dm/`) | `dm_leptogenesis_projection_theorem_note_2026-04-15` | leaf |
| `frontier_dm_leptogenesis_washout_axiom_boundary.py` | `DM_LEPTOGENESIS_EXACT_KERNEL_AUDIT_NOTE_2026-04-15.md` | `dm_leptogenesis_washout_axiom_boundary_note_2026-04-15` | leaf |

All affected claim rows are leaf-criticality, current_status=`support` or
`bounded`. Fixing the runners will not elevate any row to `retained`. The fix
clears `audited_conditional` / `audited_failed` verdicts caused purely by the
stale paths — it is audit-hygiene cleanup, not retention promotion.

## Strategy

For each runner:

1. Confirm the stale `read()` calls and the `check()` lines that depend on
   their content.
2. Decide per-check: does the deleted note's content represent
   - **deliberate retirement** (per the `d2e754fdc` "Trim DM package to
     science-only surface" intent)? → remove the read() and the dependent
     checks; record the removal in the runner's docstring.
   - **just relocated** (note moved to `docs/work_history/`)? → redirect the
     read() to the new path.
3. Re-run each runner; verify it terminates with PASS=N FAIL=0.
4. Record the fix in a paired audit-hygiene support note.
5. Single PR for the cluster.

## Honest scope

- This block does NOT propose retention for any leaf-criticality row.
- It does NOT promote any claim to a higher tier.
- It does NOT introduce new physics content.
- It removes runner code that references retired authority surfaces and
  documents the removal as deliberate hygiene, consistent with the original
  trim commit's intent.

## Stop conditions

- All affected runners pass with FAIL=0.
- One PR opened with the cluster fix.
- Followed by audit-finding note PR (Block 2) documenting the residual LHF
  cohort.
