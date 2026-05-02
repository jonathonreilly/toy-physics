# Audit Queue

**Generated:** 2026-05-02T20:51:29.841268+00:00
**Total pending:** 619
**Ready (all deps already at retained-grade or metadata tiers):** 135

By criticality:
- `critical`: 91
- `high`: 197
- `medium`: 166
- `leaf`: 165

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | - | unaudited | critical | 339 | 11.41 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 2 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | - | unaudited | critical | 337 | 10.90 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 3 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 337 | 10.90 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 4 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 337 | 10.90 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 5 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 337 | 10.90 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 6 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 337 | 10.90 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 7 | `yt_ward_identity_derivation_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 335 | 27.39 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 8 | `yukawa_color_projection_theorem` | - | unaudited | critical | 329 | 12.87 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_current_fierz_channel_decomposition.py` |
| 9 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | critical | 312 | 10.29 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 10 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 310 | 11.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 11 | `axiom_first_spin_statistics_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 309 | 9.78 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spin_statistics_check.py` |
| 12 | `planck_boundary_density_extension_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 307 | 14.27 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_density_extension.py` |
| 13 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 306 | 14.76 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 14 | `axiom_first_cluster_decomposition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 306 | 10.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cluster_decomposition_check.py` |
| 15 | `physical_hermitian_hamiltonian_and_sme_bridge_note_2026-04-30` | positive_theorem | unaudited | critical | 305 | 8.76 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_hermitian_hamiltonian_and_sme_bridge.py` |
| 16 | `physical_lattice_necessity_note` | no_go | unaudited | critical | 304 | 15.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_lattice_necessity.py` |
| 17 | `planck_parent_source_hidden_character_no_go_note_2026-04-24` | no_go | unaudited | critical | 303 | 13.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_parent_source_hidden_character_nogo.py` |
| 18 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 303 | 12.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 19 | `holographic_probe_note_2026-04-11` | bounded_theorem | unaudited | critical | 303 | 9.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_holographic_probe.py` |
| 20 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 302 | 15.24 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 21 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 302 | 14.74 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 22 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 302 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 23 | `staggered_fermion_card_2026-04-10` | bounded_theorem | unaudited | critical | 302 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_17card.py` |
| 24 | `area_law_algebraic_spectrum_entropy_no_go_note_2026-04-25` | bounded_theorem | unaudited | critical | 301 | 12.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_algebraic_spectrum_entropy_no_go.py` |
| 25 | `area_law_primitive_edge_entropy_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 301 | 12.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_edge_entropy_selector_no_go.py` |
| 26 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 301 | 12.74 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 27 | `i3_zero_exact_theorem_note` | positive_theorem | unaudited | critical | 301 | 12.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_born_rule_derived.py` |
| 28 | `action_normalization_note` | bounded_theorem | unaudited | critical | 301 | 10.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_action_normalization.py` |
| 29 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 301 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 30 | `architecture_note_directional_measure` | bounded_theorem | unaudited | critical | 301 | 8.74 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `first_order_coframe_unconditionality_no_go_theorem_note_2026-04-30` | no_go | unaudited | critical | 301 | 8.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_first_order_coframe_unconditionality_no_go.py` |
| 32 | `substrate_to_p_a_forcing_theorem_note_2026-04-30` | no_go | unaudited | critical | 301 | 8.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_substrate_to_p_a_forcing.py` |
| 33 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 54 | 13.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 34 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 339 | 11.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 35 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 338 | 9.40 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 36 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 337 | 10.90 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 37 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 336 | 16.90 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 38 | `g_bare_two_ward_rep_b_independence_theorem_note_2026-04-19` | positive_theorem | claim_type_backfill_reaudit | critical | 310 | 11.28 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 39 | `g_bare_structural_normalization_theorem_note_2026-04-18` | positive_theorem | unaudited | critical | 309 | 11.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_structural_normalization.py` |
| 40 | `g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19` | positive_theorem | claim_type_backfill_reaudit | critical | 309 | 10.78 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `g_bare_two_ward_closure_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 308 | 10.77 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_two_ward_closure.py` |
| 42 | `assumption_derivation_ledger` | bounded_theorem | unaudited | critical | 308 | 8.77 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 307 | 11.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 44 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 306 | 10.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 45 | `cpt_exact_note` | - | unaudited | critical | 304 | 16.75 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `planck_finite_response_no_go_note_2026-04-24` | no_go | unaudited | critical | 302 | 12.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_finite_response_nogo.py` |
| 47 | `boundary_law_robustness_note_2026-04-11` | bounded_theorem | unaudited | critical | 302 | 9.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_boundary_law_robustness.py` |
| 48 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 301 | 14.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 49 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 301 | 13.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 50 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 301 | 12.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |

Full queue lives in `data/audit_queue.json`.
