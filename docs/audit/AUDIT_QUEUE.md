# Audit Queue

**Total pending:** 935
**Ready (all deps already at retained-grade or metadata tiers):** 73

By criticality:
- `critical`: 597
- `high`: 23
- `medium`: 120
- `leaf`: 195

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 308 | 10.77 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 2 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 3 | `persistent_object_top4_multistage_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 288 | 9.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 4 | `dm_selector_first_shoulder_exit_threshold_support_note_2026-04-21` | open_gate | audit_in_progress | critical | 287 | 9.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_selector_first_shoulder_exit_threshold_support_2026_04_21.py` |
| 5 | `koide_cyclic_wilson_descendant_law_note_2026-04-18` | positive_theorem | audit_in_progress | critical | 286 | 10.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_cyclic_wilson_descendant_law.py` |
| 6 | `hierarchy_matsubara_decomposition_note` | positive_theorem | audit_in_progress | critical | 286 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_matsubara_decomposition.py` |
| 7 | `dm_neutrino_odd_circulant_z2_slot_theorem_note_2026-04-15` | positive_theorem | audit_in_progress | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_odd_circulant_z2_slot_theorem.py` |
| 8 | `dm_neutrino_z3_character_transfer_theorem_note_2026-04-15` | positive_theorem | audit_in_progress | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_z3_character_transfer_theorem.py` |
| 9 | `dm_neutrino_z3_circulant_mass_basis_no_go_note_2026-04-15` | no_go | audit_in_progress | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_z3_circulant_mass_basis_nogo.py` |
| 10 | `generation_axiom_boundary_note` | bounded_theorem | audit_in_progress | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 11 | `koide_z3_scalar_potential_lepton_mass_tower_note_2026-04-19` | positive_theorem | audit_in_progress | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `matter_inertial_closure_note` | no_go | audit_in_progress | critical | 286 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/matter_inertial_closure.py` |
| 13 | `self_gravity_backreaction_closure_note` | no_go | audit_in_progress | critical | 286 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop_v3.py` |
| 14 | `persistent_object_compact_inertial_probe_note_2026-04-16` | bounded_theorem | audit_in_progress | critical | 286 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_compact_inertial_probe.py` |
| 15 | `koide_a1_radian_bridge_irreducibility_audit_note_2026-04-24` | no_go | audit_in_progress | critical | 285 | 16.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_radian_bridge_irreducibility_audit.py` |
| 16 | `dm_wilson_direct_descendant_schur_feshbach_boundary_variational_theorem_note_2026-04-25` | open_gate | audit_in_progress | critical | 285 | 13.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_wilson_direct_descendant_schur_feshbach_boundary_variational.py` |
| 17 | `koide_pointed_origin_exhaustion_theorem_note_2026-04-24` | no_go | audit_in_progress | critical | 285 | 13.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_pointed_origin_exhaustion_theorem.py` |
| 18 | `koide_native_dimensionless_review_packet_2026-04-24` | no_go | audit_in_progress | critical | 285 | 12.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py` |
| 19 | `self_consistency_forces_poisson_note` | bounded_theorem | audit_in_progress | critical | 285 | 12.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_self_consistent_field_equation.py` |
| 20 | `dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_note_2026-04-18` | positive_theorem | audit_in_progress | critical | 285 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_2026_04_18.py` |
| 21 | `koide_q23_oh_covariance_nogo_note_2026-04-22` | no_go | audit_in_progress | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q23_oh_covariance_nogo.py` |
| 22 | `koide_q_delta_residual_cohomology_obstruction_no_go_note_2026-04-24` | no_go | audit_in_progress | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py` |
| 23 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | positive_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_2026_04_18.py` |
| 24 | `koide_berry_bundle_obstruction_theorem_note_2026-04-19` | positive_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_berry_bundle_obstruction_theorem.py` |
| 25 | `planck_boundary_orientation_incidence_no_go_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_orientation_incidence_no_go.py` |
| 26 | `pmns_hw1_source_transfer_boundary_note` | bounded_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_hw1_source_transfer_boundary.py` |
| 27 | `pmns_transfer_operator_dominant_mode_note` | bounded_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_transfer_operator_dominant_mode.py` |
| 28 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 29 | `koide_cone_completing_root_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_cone_completing_root_narrow.py` |
| 30 | `koide_cone_three_form_equivalence_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_cone_three_form_equivalence_narrow.py` |
| 31 | `koide_q_bridge_single_primitive_note_2026-04-22` | bounded_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_bridge_single_primitive.py` |
| 32 | `koide_q_readout_factorization_theorem_2026-04-22` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 33 | `koide_transport_gap_constant_no_go_note_2026-04-20` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_transport_gap_constant_no_go.py` |
| 34 | `pmns_oriented_cycle_selection_structure_note` | positive_theorem | unaudited | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_oriented_cycle_selection_structure.py` |
| 35 | `s3_boundary_link_theorem_note` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_boundary_link_theorem.py` |
| 36 | `three_generation_observable_count_corollary_note_2026-05-03` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_count_corollary.py` |
| 37 | `yt_ew_m_residual_stretch_attempt_note_2026-05-02` | no_go | unaudited | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/yt_ew_m_residual_channel_check.py` |
| 38 | `affine_imaginary_slot_invariance_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_affine_imaginary_slot_invariance_narrow.py` |
| 39 | `background_independence_note` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_background_independence.py` |
| 40 | `block_gaussian_schur_marginalization_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_block_gaussian_schur_narrow.py` |
| 41 | `circulant_response_master_identity_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_circulant_response_master_identity_narrow.py` |
| 42 | `dm_leptogenesis_pmns_microscopic_d_last_mile_note_2026-04-16` | positive_theorem | unaudited | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_pmns_microscopic_d_last_mile.py` |
| 43 | `koide_cyclic_projector_block_democracy_note_2026-04-18` | bounded_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_cyclic_projector_block_democracy.py` |
| 44 | `koide_hostile_review_guard_note_2026-04-24` | no_go | unaudited | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_hostile_review_guard.py` |
| 45 | `koide_kappa_spectrum_operator_bridge_theorem_note_2026-04-19` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_kappa_spectrum_operator_bridge_theorem.py` |
| 46 | `kubo_range_of_validity_note` | positive_theorem | unaudited | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/kubo_range_of_validity.py` |
| 47 | `lattice_complementarity_note` | bounded_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_complementarity_sweep.py` |
| 48 | `lorentz_violation_derived_note` | bounded_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_violation.py` |
| 49 | `scalar_selector_synthesis_note_2026-04-19` | bounded_theorem | unaudited | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_z3_joint_projector_identity.py` |
| 50 | `tensor_block_closure_test_note` | bounded_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_tensor_block_closure_test.py` |

## Citation cycle break targets

168 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 437 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 2 | `cycle-0002` | 7 | 437 | `anomaly_forces_time_theorem` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 321 | `yt_explicit_systematic_budget_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 319 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 319 | `universal_qg_projective_schur_closure_note` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 319 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 302 | `higgs_from_lattice_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 302 | `higgs_mass_derived_note` | critical | audited_conditional |
| 9 | `cycle-0009` | 2 | 298 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 289 | `universal_gr_tensor_quotient_uniqueness_note` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 288 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 288 | `koide_gamma_orbit_cyclic_return_candidate_note_2026-04-18` | critical | unaudited |
| 13 | `cycle-0013` | 2 | 288 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 288 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 287 | `charged_lepton_ue_identity_via_z3_trichotomy_note_2026-04-17` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 287 | `quark_issr1_bicac_forcing_theorem_note_2026-04-19` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 286 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 284 | `abcc_cp_phase_no_go_theorem_note_2026-04-19` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 284 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 284 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 21 | `cycle-0021` | 2 | 284 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 22 | `cycle-0022` | 2 | 284 | `dm_pmns_graph_first_ordered_chain_nonzero_current_activation_theorem_note_2026-04-21` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 284 | `hadron_mass_lane1_theorem_plan_support_note_2026-04-27` | critical | unaudited |
| 24 | `cycle-0024` | 2 | 284 | `koide_a1_fractional_topology_no_go_synthesis_note_2026-04-24` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 284 | `koide_eigenvalue_q23_surface_theorem_note_2026-04-20` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
