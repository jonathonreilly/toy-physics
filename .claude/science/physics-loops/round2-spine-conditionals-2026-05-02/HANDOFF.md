# Handoff — round2-spine-conditionals-2026-05-02

## Branch
`claude/round2-spine-conditionals-2026-05-02`
(based on `origin/main`)

## Commits
1. `audit-repair: narrow three_generation_structure + anomaly_forces_time`
   - Source-note narrowing for two of the three target rows.
2. `audit-repair: regenerated audit ledger after source-note narrowings`
   - Mechanical regeneration via `bash docs/audit/scripts/run_pipeline.sh`.

## Status
- 0 audit_lint errors
- 55 pre-existing legacy backfill warnings (unchanged)
- 2/3 target rows moved from audited_conditional -> unaudited
- 1/3 target row (yukawa) was already in unaudited state from prior
  commit d956cdd7d; no further source-note edit required.

## Per-row resolution

| Row | Resolution | claim_type change | Physics judgment |
|---|---|---|---|
| `three_generation_structure_note` (290 desc) | NARROW | `bounded_theorem` (no change in claim_type; verdict had already classified as bounded) | Source-note prose now matches audit verdict's explicit "narrow to corner/no-quotient algebra only" repair target. Substrate-physicality upgrade delegated to audited_conditional sibling notes. |
| `anomaly_forces_time_theorem` (287 desc) | NARROW + flip | `positive_theorem` -> `bounded_theorem` | Conditional 3+1 derivation under four named external admissions: ABJ inconsistency, opposite-chirality singlet completion, Clifford-volume chirality, ultrahyperbolic Cauchy obstruction. The unconditional first-principles version is explicitly out of scope and remains an open lane. |
| `yukawa_color_projection_theorem` (285 desc) | (already NARROWED by prior commit d956cdd7d) | `positive_theorem` (unchanged; narrowed scope is exact algebraic identity) | Class-A Fierz channel-fraction identity F_adjoint = (N_c² - 1)/N_c² = 8/9 at N_c = 3. Physical-Higgs-Z bridge (the class-F renaming step that the audit flagged) is now explicitly out of scope. All 3 deps retained_bounded. |

## Net audit count change

| Metric | Pre | Post | Delta |
|---|---:|---:|---:|
| `audited_conditional` | 635 | 633 | **-2** (cascade unblock) |
| `unaudited` | 544 | 546 | +2 |
| `bounded_theorem` (claim_type) | 517 | 518 | +1 |
| `positive_theorem` (claim_type) | 861 | 860 | -1 |

## Cascade impact
Combined transitive descendants: 248 + 299 + 119 = 666 rows now sit
under more honestly-narrowed claim scope, ready for retained_bounded
promotion if next independent audit ratifies.

## Honest open items per row

### three_generation_structure_note
- Substrate-physicality reading still requires retained-grade
  ratification of `PHYSICAL_LATTICE_NECESSITY_NOTE.md`,
  `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`,
  `THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md`,
  `ANOMALY_FORCES_TIME_THEOREM.md` (all currently audited_conditional).
- These bridge notes are themselves on the audit backlog; this branch
  does not unblock them, only narrows the load-bearing claim of the
  three-generation structure row away from depending on them.

### anomaly_forces_time_theorem
- The unconditional first-principles version (where the four external
  admissions are derived from framework primitives) remains an open
  lane.
- In particular, deriving the ultrahyperbolic Cauchy obstruction from
  framework lattice semantics (rather than importing Craig-Weinstein
  2009 as literature) is the largest remaining stretch target on this
  row.

### yukawa_color_projection_theorem
- The physical-Higgs-Z bridge (Z_phi^phys / Z_phi^lattice = R_conn ->
  sqrt(8/9) y_t correction) remains delegated to the lattice -> physical
  matching cluster obstruction (PR #274). It is not closed in this
  branch.
- The narrowed Fierz channel-fraction identity is structurally complete
  and should land cleanly as `retained_bounded` (or `retained` if the
  auditor classifies the exact algebraic identity as positive_theorem)
  on next audit pass.

## Proposed repo weaving (deferred)
None in this branch. Weaving deferred until next independent audit
lands the narrowed claims. After that audit lands, the repo-wide
authority surfaces (LANE_REGISTRY, LANE_STATUS_BOARD, etc.) can be
updated to reflect the new bounded scopes.

## Stop condition
Reached. All three rows have honest narrowed status, run_pipeline.sh
OK, branch pushed, PR opened.
