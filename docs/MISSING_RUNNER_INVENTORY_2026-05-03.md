# Missing Runner Inventory — 2026-05-03 Audit-Repair Scan

**Type:** meta
**Status:** infrastructure inventory; not a claim

Repository-wide scan for `.py` script references in active claim notes (excluding
`docs/audit/`, `docs/work_history/`, `docs/ai_methodology/`, `docs/repo/`,
`docs/lanes/`, `docs/publication/`) that point to scripts not present in the
current `scripts/` tree. Output of the comprehensive scan run during the
2026-05-03 audit-repair lane.

## Tier 1: Primary runners missing on active claim rows

These rows have their canonical primary runner pointing at a non-existent file.
Each note has been annotated with a "MISSING — flagged for re-audit" callout in
a separate commit. The audit verdicts on these rows reset to `unaudited` due to
note-hash drift, queueing them for re-audit once a runner-rewrite or archival
decision is made.

| claim_id | note | runner | audit_status (pre-flag) |
|---|---|---|---|
| `g_bare_derivation_note` | `docs/G_BARE_DERIVATION_NOTE.md` | `frontier_g_bare_derivation.py` | `audited_conditional` |
| `gauge_vacuum_plaquette_first_sector_completed_triple_current_transfer_family_boundary_note_2026-04-19` | `docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_COMPLETED_TRIPLE_CURRENT_TRANSFER_FAMILY_BOUNDARY_NOTE_2026-04-19.md` | `frontier_gauge_vacuum_plaquette_first_sector_completed_triple_current_transfer_family_boundary_2026_04_19.py` | `audited_conditional` |
| `gauge_vacuum_plaquette_first_sector_first_hankel_to_dm_boundary_note_2026-04-19` | `docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_FIRST_HANKEL_TO_DM_BOUNDARY_NOTE_2026-04-19.md` | `frontier_gauge_vacuum_plaquette_first_sector_first_hankel_to_dm_boundary_2026_04_19.py` | `audited_conditional` |
| `gauge_vacuum_plaquette_first_symmetric_three_sample_minimal_positive_completion_note_2026-04-19` | `docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_MINIMAL_POSITIVE_COMPLETION_NOTE_2026-04-19.md` | `frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_minimal_positive_completion_2026_04_19.py` | `audited_conditional` |

## Tier 2: Body-only missing references (45 scripts)

Scripts referenced in note bodies (not as the canonical primary runner). These
do NOT affect the audit graph — only `runner_path` (canonical) is used by
`classify_runner_passes.py`. Body mentions are historical narrative and lower
priority. Listed here for the runner-rewrite batch to consume.

| script | first-listed referencing note |
|---|---|
| `frontier_asymmetry_scaling.py` | `docs/SESSION_SYNTHESIS_2026-04-11.md` |
| `frontier_charged_lepton_koide_cone_algebraic_equivalence.py` | `docs/KOIDE_LANE_AUDIT_BATCH_NOTE_2026-05-02.md` |
| `frontier_confinement_probe.py` | `docs/CONFINEMENT_STRING_TENSION_NOTE.md` |
| `frontier_critical_exponents_extended.py` | `docs/SESSION_SYNTHESIS_2026-04-11.md` |
| `frontier_dimension_emergence.py` | `docs/AXIOM_REDUCTION_NOTE.md` |
| `frontier_dm_chamber_signature_structure.py` | `docs/DM_CHAMBER_SIGNATURE_STRUCTURE_NOTE_2026-04-19.md` |
| `frontier_dm_dple_dimension_parametric_extremum_theorem.py` | `docs/SCALAR_SELECTOR_FULL_STACK_RECOVERY_NOTE_2026-04-19.md` |
| `frontier_dm_f4_discriminator_axiom_candidate.py` | `docs/DM_CHAMBER_SIGNATURE_STRUCTURE_NOTE_2026-04-19.md` |
| `frontier_emergent_gr_signatures.py` | `docs/AXIOM_REDUCTION_NOTE.md` |
| `frontier_frozen_stars.py` | `docs/FROZEN_STARS_RIGOROUS_NOTE.md` |
| `frontier_gap_asymmetry_test.py` | `docs/SESSION_SYNTHESIS_2026-04-11.md` |
| `frontier_geometry_superposition_sweep.py` | `docs/SESSION_SYNTHESIS_2026-04-11.md` |
| `frontier_gravitational_decoherence_rate.py` | `docs/SESSION_SYNTHESIS_2026-04-11.md` |
| `frontier_gravity_poisson_derived.py` | `docs/GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md` |
| `frontier_koide_matrix_unit_source_law_cyclic_projection.py` | `docs/KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md` |
| `frontier_koide_mru_weight_class_obstruction.py` | `docs/SCALAR_SELECTOR_FULL_STACK_RECOVERY_NOTE_2026-04-19.md` |
| `frontier_koide_observable_principle_cyclic_source_law.py` | `docs/KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md` |
| `frontier_koide_q_lie_clifford_radius_map_no_go.py` | `docs/KOIDE_HOSTILE_REVIEW_GUARD_NOTE_2026-04-24.md` |
| `frontier_koide_q_traceless_source_lagrange_multiplier_no_go.py` | `docs/KOIDE_HOSTILE_REVIEW_GUARD_NOTE_2026-04-24.md` |
| `frontier_koide_scalar_selector_direct_attack_scout.py` | `docs/KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md` |
| `frontier_lorentzian_k8_card.py` | `docs/SESSION_SYNTHESIS_2026-04-09.md` |
| `frontier_memory_sign_robustness.py` | `docs/MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md` |
| `frontier_newton_both_masses.py` | `docs/WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md` |
| `frontier_pmns_intrinsic_completion_boundary.py` | `docs/AUDIT_DM_GV_RUNNER_STALE_PATH_CLEANUP_BLOCK_TWO_NOTE_2026-05-01.md` |
| `frontier_product_law_no_ansatz.py` | `docs/NEWTON_LAW_DERIVED_NOTE.md` |
| `frontier_proton_decay.py` | `docs/PROTON_LIFETIME_DERIVED_NOTE.md` |
| `frontier_quantum_zeno.py` | `docs/SESSION_SYNTHESIS_2026-04-11.md` |
| `frontier_quark_bicac_residue_equivalence.py` | `docs/SCALAR_SELECTOR_FULL_STACK_RECOVERY_NOTE_2026-04-19.md` |
| `frontier_quark_jts_decomposition_theorem.py` | `docs/SCALAR_SELECTOR_FULL_STACK_RECOVERY_NOTE_2026-04-19.md` |
| `frontier_s3_cap_link_formal.py` | `docs/S3_CAP_UNIQUENESS_NOTE.md` |
| `frontier_s3_inductive_link.py` | `docs/S3_GENERAL_R_DERIVATION_NOTE.md` |
| `frontier_s3_pl_manifold.py` | `docs/S3_CAP_UNIQUENESS_NOTE.md` |
| `frontier_s3_recognition.py` | `docs/S3_GENERAL_R_DERIVATION_NOTE.md` |
| `frontier_s3_recognition_general.py` | `docs/S3_GENERAL_R_DERIVATION_NOTE.md` |
| `frontier_s3_shelling.py` | `docs/S3_GENERAL_R_DERIVATION_NOTE.md` |
| `frontier_signed_gravity_boundary_chi_candidate.py` | `docs/SIGNED_GRAVITY_NONLOCAL_BOUNDARY_CHI_TARGET_NOTE.md` |
| `frontier_signed_gravity_interacting_conservation.py` | `docs/SIGNED_GRAVITY_RESPONSE_BACKLOG_2026-04-25.md` |
| `frontier_spatial_metric_derivation.py` | `docs/AXIOM_REDUCTION_NOTE.md` |
| `frontier_spectral_geometry.py` | `docs/SESSION_SYNTHESIS_2026-04-11.md` |
| `frontier_su3_commutant.py` | `docs/HYPERCHARGE_IDENTIFICATION_NOTE.md` |
| `frontier_wilson_newton_law.py` | `docs/WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md` |
| `frontier_wilson_two_body.py` | `docs/WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md` |
| `frontier_wilson_two_body_open_refined.py` | `docs/WILSON_TWO_BODY_OPEN_REFINED_NOTE_2026-04-11.md` |
| `frontier_z2_sublattice_decoherence.py` | `docs/SESSION_SYNTHESIS_2026-04-11.md` |
| `toy_event_physics.py` | `docs/PERSISTENT_OBJECT_EXACT_LATTICE_PARK_NOTE_2026-04-16.md` |

## Tier 3: Already archived

Notes whose primary runner was missing have already been moved to
`archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/` or
similar locations. Their ledger rows preserve `audited_failed` as
negative-result history. No action needed.

## Next steps

Spin up a runner-rewrite batch that for each Tier 1 row decides one of:

1. **Restore from git history** — find the commit that deleted the script and
   resurrect it (use `git log --all --diff-filter=D -- scripts/<basename>`).
2. **Rewrite from note text** — the note body usually describes the test the
   runner was meant to perform; reconstruct from that description.
3. **Replace with a successor** — a canonical replacement script may already
   exist with a related name; update the note to reference it.
4. **Archive** — if the underlying claim is no longer active, move the note to
   `archive_unlanded/<cluster-tag>/` per `docs/audit/STALE_NARRATIVE_POLICY.md`.
