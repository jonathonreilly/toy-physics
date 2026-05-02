# Retained-Positive Opportunity Queue (post-cycle-4 snapshot)

**Date:** 2026-05-02
**Campaign:** retained-positive-rescope-20260502
**Source ledger:** `docs/audit/data/audit_ledger.json` at HEAD of `origin/main`
**Framework:** scope-aware claim typing (commit 011e433c2 + later audit lands)

## Executive summary

Under the new framework, **582 rows** are candidates for retained-family status
if an independent audit ratifies the local claim and any dependency chain closes:

| Predicted effective_status | Count | Reason |
|---|---:|---|
| `retained` | 323 | `positive_theorem` + 0 or all-retained deps |
| `retained_bounded` | 227 | `bounded_theorem` + 0 or all-retained deps |
| `retained_no_go` | 32 | `no_go` + 0 or all-retained deps |

These are rows where the audit chain appears structurally plausible under the
new framework's scope-aware rubric. This is a prioritization snapshot, not an
author-side audit verdict.

## Cycles 1-4 contributed 4 new retained-eligible primitives

| Cycle | PR | Type | Lane | Lever | Verification |
|---|---|---|---|---|---|
| 1 | [#292](https://github.com/jonathonreilly/cl3-lattice-framework/pull/292) | positive_theorem | LH-doublet hypercharge | eigenvalue ratio 1:(−3) on Sym²:Anti² | PASS=23/0 |
| 2 | [#293](https://github.com/jonathonreilly/cl3-lattice-framework/pull/293) | bounded_theorem | Koide cyclic Wilson | conditional 3-response reduction | PASS=38/0 |
| 3 | [#294](https://github.com/jonathonreilly/cl3-lattice-framework/pull/294) | positive_theorem | Schur representation theory | covariance inheritance lemma | PASS=22/0 |
| 4 | [#297](https://github.com/jonathonreilly/cl3-lattice-framework/pull/297) | positive_theorem | Three-generation observable | algebra-generation no-proper-quotient | PASS=33/0 |

Each excludes its known conditional bridge and declares graph-visible one-hop
dependencies; retained-family status remains audit-lane/pipeline-derived.

## Top 30 highest-leverage candidates (by transitive descendants)

| Rank | claim_id | claim_type | td | predicted | current as |
|---:|---|---|---:|---|---|
| 1 | observable_principle_from_axiom_note | positive_theorem | 325 | retained | audited_conditional |
| 2 | left_handed_charge_matching_note | positive_theorem | 304 | retained | unaudited |
| 3 | physical_lattice_necessity_note | no_go | 345 | retained_no_go | audited_conditional |
| 4 | generation_axiom_boundary_note | bounded_theorem | 347 | retained_bounded | audited_conditional |
| 5 | gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note | positive_theorem | 298 | retained | audited_conditional |
| 6 | ew_current_fierz_channel_decomposition_note_2026-05-01 | positive_theorem | 297 | retained | unaudited |
| 7 | gauge_vacuum_plaquette_constant_lift_obstruction_note | positive_theorem | 297 | retained | audited_conditional |
| 8 | yukawa_color_projection_theorem | positive_theorem | 297 | retained | audited_conditional |
| 9 | gauge_vacuum_plaquette_mixed_cumulant_audit_note | positive_theorem | 296 | retained | audited_conditional |
| 10 | higgs_mass_from_axiom_note | positive_theorem | 296 | retained | audited_conditional |
| 11 | gauge_vacuum_plaquette_framework_point_underdetermination_note | positive_theorem | 295 | retained | audited_conditional |
| 12 | g_bare_derivation_note | positive_theorem | 294 | retained | audited_conditional |
| 13 | g_bare_rigidity_theorem_note | positive_theorem | 292 | retained | audited_conditional |
| 14 | higgs_mechanism_note | positive_theorem | 291 | retained | audited_conditional |
| 15 | yt_color_projection_correction_note | positive_theorem | 291 | retained | audited_conditional |
| 16 | higgs_from_lattice_note | bounded_theorem | 291 | retained_bounded | audited_conditional |
| 17 | taste_scalar_isotropy_theorem_note | bounded_theorem | 291 | retained_bounded | audited_conditional |
| 18 | yt_explicit_systematic_budget_note | positive_theorem | 290 | retained | audited_conditional |
| 19 | yt_qfp_insensitivity_support_note | bounded_theorem | 290 | retained_bounded | audited_conditional |
| 20 | neutrino_majorana_operator_axiom_first_note | positive_theorem | 185 | retained | audited_conditional |
| 21 | ckm_from_mass_hierarchy_note | bounded_theorem | 154 | retained_bounded | audited_conditional |
| 22 | dm_neutrino_cascade_geometry_note_2026-04-14 | positive_theorem | 153 | retained | audited_conditional |
| 23 | ckm_schur_complement_theorem | bounded_theorem | 147 | retained_bounded | audited_conditional |
| 24 | dm_neutrino_z3_circulant_mass_basis_no_go_note_2026-04-15 | no_go | 144 | retained_no_go | audited_conditional |
| 25 | dm_neutrino_source_surface_carrier_normal_form_theorem_note_2026-04-16 | positive_theorem | 134 | retained | audited_conditional |
| 26 | dm_neutrino_source_surface_intrinsic_slot_theorem_note_2026-04-16 | positive_theorem | 134 | retained | audited_conditional |
| 27 | dm_neutrino_source_surface_shift_quotient_bundle_theorem_note_2026-04-16 | positive_theorem | 134 | retained | audited_conditional |
| 28 | dm_neutrino_z3_character_transfer_theorem_note_2026-04-15 | positive_theorem | 134 | retained | audited_conditional |
| 29 | dm_neutrino_dirac_bridge_theorem_note_2026-04-15 | positive_theorem | 115 | retained | audited_conditional |
| 30 | dm_neutrino_positive_polar_h_cp_theorem_note_2026-04-15 | positive_theorem | 119 | retained | audited_conditional |

## Pattern observation

Most of the top-30 share two characteristics:

1. **`deps = []`** under the current ledger — meaning the row has no formal upstream chain dependency. Under the new framework, this means the row's `effective_status` depends only on its own `claim_type` + `audit_status`, not on any chain. A clean audit verdict alone flips it to retained-grade.

2. **Old framework `audited_conditional` verdicts** that flagged "undeclared upstream reads" or "support-tier authority not retained on the actual surface" — both diagnostics are obsolete under the new framework's scope-aware rubric. The new framework treats the audit row's content as primary; chain-level claims about upstream prose are no longer load-bearing for retention.

This is exactly the situation that motivated cycles 1-4: when an older
conditional row has graph-visible deps (or no deps) under the new framework, a
fresh-context re-audit on the source note's class-A/C load-bearing step can
decide whether the row lifts to retained-family status.

## Recommendations

For the audit lane:
- Prioritize the top-30 list above. Each row is one fresh-context re-audit away from retained-grade.
- For rows with `deps = []` under current ledger but UNDECLARED upstream reads (the old `physical_lattice_necessity_note` pattern), the new framework's scope-aware rubric considers only the source note's local content — so the verdict should not block on undeclared external reads.

For follow-up science cycles (if user requests):
- Cycles 1-4 demonstrate the **narrow-rescope pattern**: when a row's parent has scope creep blocking clean audit, write a sister NEW claim row that captures only the safe scope with retained-grade deps. The new row lands retained directly.
- The narrow-rescope pattern is most valuable for rows where the parent's load-bearing step is **class (E)/(F) renaming** (the LHCM pattern) — where carving out the algebraic content as class (A) creates a clean retainable primitive.
- Other targets for narrow-rescope: rows with renaming-style verdicts whose
  underlying algebra is class (A) on declared inputs.

## Anti-churn note

The campaign stopped at 4 substantive cycles per the `physics-loop` skill's late-campaign churn guard (added in commit 9b843f790). Each of cycles 1-4 introduced a distinct load-bearing premise on a different lane. Further cycles would risk the corollary-churn pattern flagged in `feedback_physics_loop_corollary_churn.md` memory.

The user can direct another wave of cycles (5+) targeting specific candidates from this opportunity queue.
