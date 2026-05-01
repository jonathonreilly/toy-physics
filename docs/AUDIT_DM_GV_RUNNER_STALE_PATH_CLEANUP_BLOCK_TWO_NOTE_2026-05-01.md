# Audit DM + Gauge-Vacuum Runner Stale-Path Cleanup (Block Two)

**Date:** 2026-05-01
**Status:** support / audit-hygiene cleanup. Companion to
[`docs/AUDIT_DM_RUNNER_STALE_PATH_CLEANUP_NOTE_2026-05-01.md`](AUDIT_DM_RUNNER_STALE_PATH_CLEANUP_NOTE_2026-05-01.md)
(Block One). This block extends the same audit-hygiene cleanup to a second
cluster of runners with stale `read("docs/X.md")` calls.
**Lane:** audit-hygiene. No physics claim is added or removed.

---

## 0. Why this note exists

After Block One landed (PR #246) covering 8 DM-cluster runners with stale
references to notes deleted by commit `d2e754fdc`, a comprehensive scan of
the remaining runners under `scripts/` found 8 more on-main runners that
still carried stale `read("docs/X.md")` calls. Each one's audit row was
landing as `audited_conditional` or `audited_failed` for reasons reducible
to `FileNotFoundError`.

This block addresses the second cluster.

## 1. Affected runners and changes

| runner | stale path(s) | action |
|---|---|---|
| `frontier_dm_neutrino_postcanonical_polar_section.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md` (deleted), atlas row `\| DM neutrino post-canonical positive polar section \|` (trimmed) | remove read + 2 dependent checks |
| `frontier_dm_neutrino_polar_aligned_core_nogo.py` | `DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md` (deleted), atlas row `\| DM neutrino positive-polar aligned-core no-go \|` (trimmed) | remove read + 2 dependent checks |
| `frontier_dm_neutrino_weak_triplet_coefficient_axiom_boundary.py` | `DM_NEUTRINO_WEAK_TRIPLET_COEFFICIENT_AXIOM_BOUNDARY_NOTE_2026-04-15.md` (archived to `archive_unlanded/dm-neutrino-stale-runners-2026-04-30/`) | redirect read to archive path (substring checks preserved) |
| `frontier_dm_neutrino_source_surface_z3_doublet_block_full_closure_boundary.py` | same archived note | redirect to archive path |
| `frontier_dm_neutrino_source_bank_z3_doublet_block_selection_obstruction_theorem.py` | same archived note | redirect to archive path |
| `frontier_dm_abcc_exact_target_surface_source_cubic_closure_2026_04_21.py` | `DM_ABCC_BASIN_ENUMERATION_COMPLETENESS_THEOREM_NOTE_2026-04-20.md` (archived to `archive_unlanded/dm-abcc-finite-search-salvage-2026-04-30/`) | redirect to archive path |
| `frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_principle_theorem_2026_04_19.py` | `GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TAIL_UNDERDETERMINATION_THEOREM_NOTE_2026-04-19.md` (archived to `archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/`) | redirect to archive path |
| `frontier_gauge_vacuum_plaquette_first_sector_zero_extension_factorized_class_theorem_2026_04_19.py` | `GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_RANK_ONE_FACTORIZED_CLASS_BOUNDARY_NOTE_2026-04-19.md` (same archive) | redirect to archive path |

The cluster naturally splits into two patterns:

- **Deleted-note removal** (postcanonical_polar_section, polar_aligned_core_nogo): the deleted notes (YUKAWA_BLOCKER) plus trimmed atlas rows are removed; the runner's surviving content checks verify the load-bearing claims directly.
- **Archived-note redirect** (six runners): the relevant note was moved to `archive_unlanded/<reason-tag>/` rather than deleted. Substring checks against archived note content are preserved by redirecting the `read()` to the archive path. This is the safer move because the archive preserves the historical content verbatim and the runners' verifications remain intact.

Every change is annotated in-source with the move/deletion provenance.

## 2. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_postcanonical_polar_section.py
# PASS=12 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_polar_aligned_core_nogo.py
# PASS=8 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_weak_triplet_coefficient_axiom_boundary.py
# PASS=14 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_full_closure_boundary.py
# PASS=14 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_bank_z3_doublet_block_selection_obstruction_theorem.py
# PASS=13 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_dm_abcc_exact_target_surface_source_cubic_closure_2026_04_21.py
# PASS=15 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_principle_theorem_2026_04_19.py
# PASS=7 FAIL=0
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_sector_zero_extension_factorized_class_theorem_2026_04_19.py
# PASS=6 FAIL=0
```

Total: **89 PASS / 0 FAIL** across the cluster.

## 3. What this changes for the audit ledger

Each affected claim row's `audit_status` was either `audited_conditional` or
`audited_failed` with rationale text reducible to "primary runner returned
nonzero in the restricted audit environment". After Block One + Block Two
land and the audit pipeline re-runs, **none** of the addressed runners
should fail with FileNotFoundError; the rows can re-audit on substantive
physics merits rather than file-availability noise.

Most of the affected claim rows are leaf or medium-criticality with
author-declared `support` / `bounded` / `unknown` status. This block does
NOT promote any claim to `retained`. It only removes the noise floor.

Two notable rows in this cluster carry `current_status: proposed_retained`:
- `dm_abcc_basin_enumeration_completeness_theorem_note_2026-04-20` — already at `effective_status: retained_no_go` (archived).
- `dm_neutrino_weak_triplet_coefficient_axiom_boundary_note_2026-04-15` — at `effective_status: retained_no_go` (archived).

For these archived rows, the redirected reads keep the runners self-contained
verification harnesses for the historical claim content; they do not
re-promote the archived rows.

## 4. Out of scope

- Restoring deleted notes or de-archiving moved notes (the trim and
  archival decisions were deliberate).
- Promoting any leaf row to `retained`.
- Modifying the audit pipeline runtime environment to ship the deleted
  files separately.
- The remaining 6 stale-path PMNS references in
  `frontier_pmns_intrinsic_completion_boundary.py`: that runner has already
  been hygiene-repaired (uses redirected reads to currently-existing notes);
  it now passes with PASS=14 FAIL=0 against the present `docs/` tree, so
  no further change is needed for that runner. Block 1+2 cover the
  remaining stale-path cluster reachable from on-main audit rows.

## 5. Forbidden-import role

This note introduces no new physical content, no new numerical comparators,
no new admitted observations. It is structural cleanup of runner code only.

## 6. Cross-references

- Block 1: PR #246 (open / review-only) — first half of the runner
  stale-path cleanup.
- This block: Block 2 of the audit-hygiene campaign.
- Original trim commit: `d2e754fdc` (2026-04-16, "Trim DM package to
  science-only surface").
- Original archive commits: 2026-04-30 stale-runners + missing-runners
  archive packets.
