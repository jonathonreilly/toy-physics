# Audit Queue

**Total pending:** 952
**Ready (all deps already at retained-grade or metadata tiers):** 83

By criticality:
- `critical`: 614
- `high`: 23
- `medium`: 120
- `leaf`: 195

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 308 | 10.77 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 2 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 3 | `linear_response_true_kubo_note` | bounded_theorem | audit_in_progress | critical | 290 | 9.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/linear_response_true_kubo.py` |
| 4 | `unit_singlet_overlap_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 290 | 9.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_unit_singlet_overlap_narrow.py` |
| 5 | `wave_retardation_continuum_limit_note` | bounded_theorem | unaudited | critical | 290 | 9.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_retardation_continuum_limit.py` |
| 6 | `quark_route2_exact_readout_map_note_2026-04-19` | no_go | audit_in_progress | critical | 289 | 12.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_route2_exact_readout_map.py` |
| 7 | `planck_target3_phase_unit_edge_statistics_boundary_note_2026-04-25` | no_go | audit_in_progress | critical | 289 | 11.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_phase_unit_edge_statistics.py` |
| 8 | `pmns_uniform_scalar_deformation_boundary_note` | no_go | audit_in_progress | critical | 289 | 11.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_uniform_scalar_deformation_boundary.py` |
| 9 | `pmns_oriented_cycle_reduced_channel_nonselection_note` | positive_theorem | unaudited | critical | 289 | 10.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_oriented_cycle_reduced_channel_nonselection.py` |
| 10 | `tensor_support_center_excess_law_note` | bounded_theorem | audit_in_progress | critical | 289 | 9.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_tensor_support_center_excess_law.py` |
| 11 | `ew_higgs_gauge_mass_diagonalization_theorem_note_2026-04-26` | positive_theorem | audit_in_progress | critical | 288 | 14.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_higgs_gauge_mass_diagonalization.py` |
| 12 | `koide_q_onsite_source_domain_no_go_synthesis_note_2026-04-25` | no_go | audit_in_progress | critical | 288 | 14.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py` |
| 13 | `koide_dweh_cyclic_compression_note_2026-04-18` | positive_theorem | audit_in_progress | critical | 288 | 10.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_dweh_cyclic_compression.py` |
| 14 | `persistent_object_top4_multistage_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 288 | 9.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 15 | `dm_neutrino_cascade_geometry_note_2026-04-14` | bounded_theorem | audit_in_progress | critical | 287 | 10.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_cascade_geometry.py` |
| 16 | `hierarchy_spatial_bc_and_u0_scaling_note` | bounded_theorem | audit_in_progress | critical | 287 | 10.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_spatial_bc_and_u0_scaling.py` |
| 17 | `dm_selector_first_shoulder_exit_threshold_support_note_2026-04-21` | open_gate | unaudited | critical | 287 | 9.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_selector_first_shoulder_exit_threshold_support_2026_04_21.py` |
| 18 | `dm_selector_threshold_stabilization_support_theorem_note_2026-04-21` | open_gate | unaudited | critical | 287 | 8.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_selector_threshold_stabilization_support_2026_04_21.py` |
| 19 | `hierarchy_matsubara_decomposition_note` | positive_theorem | audit_in_progress | critical | 286 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_matsubara_decomposition.py` |
| 20 | `dm_neutrino_odd_circulant_z2_slot_theorem_note_2026-04-15` | positive_theorem | audit_in_progress | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_odd_circulant_z2_slot_theorem.py` |
| 21 | `dm_neutrino_z3_character_transfer_theorem_note_2026-04-15` | positive_theorem | audit_in_progress | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_z3_character_transfer_theorem.py` |
| 22 | `dm_neutrino_z3_circulant_mass_basis_no_go_note_2026-04-15` | no_go | audit_in_progress | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_z3_circulant_mass_basis_nogo.py` |
| 23 | `generation_axiom_boundary_note` | bounded_theorem | audit_in_progress | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 24 | `koide_z3_scalar_potential_lepton_mass_tower_note_2026-04-19` | positive_theorem | audit_in_progress | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 25 | `matter_inertial_closure_note` | no_go | audit_in_progress | critical | 286 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/matter_inertial_closure.py` |
| 26 | `self_gravity_backreaction_closure_note` | no_go | audit_in_progress | critical | 286 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop_v3.py` |
| 27 | `persistent_object_compact_inertial_probe_note_2026-04-16` | bounded_theorem | audit_in_progress | critical | 286 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_compact_inertial_probe.py` |
| 28 | `koide_a1_radian_bridge_irreducibility_audit_note_2026-04-24` | no_go | audit_in_progress | critical | 285 | 16.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_radian_bridge_irreducibility_audit.py` |
| 29 | `dm_wilson_direct_descendant_schur_feshbach_boundary_variational_theorem_note_2026-04-25` | open_gate | audit_in_progress | critical | 285 | 13.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_wilson_direct_descendant_schur_feshbach_boundary_variational.py` |
| 30 | `koide_pointed_origin_exhaustion_theorem_note_2026-04-24` | no_go | audit_in_progress | critical | 285 | 13.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_pointed_origin_exhaustion_theorem.py` |
| 31 | `koide_native_dimensionless_review_packet_2026-04-24` | no_go | audit_in_progress | critical | 285 | 12.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py` |
| 32 | `self_consistency_forces_poisson_note` | bounded_theorem | audit_in_progress | critical | 285 | 12.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_self_consistent_field_equation.py` |
| 33 | `dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_note_2026-04-18` | positive_theorem | audit_in_progress | critical | 285 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_2026_04_18.py` |
| 34 | `koide_q23_oh_covariance_nogo_note_2026-04-22` | no_go | audit_in_progress | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q23_oh_covariance_nogo.py` |
| 35 | `koide_q_delta_residual_cohomology_obstruction_no_go_note_2026-04-24` | no_go | audit_in_progress | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py` |
| 36 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | positive_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_2026_04_18.py` |
| 37 | `koide_berry_bundle_obstruction_theorem_note_2026-04-19` | positive_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_berry_bundle_obstruction_theorem.py` |
| 38 | `planck_boundary_orientation_incidence_no_go_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_orientation_incidence_no_go.py` |
| 39 | `pmns_hw1_source_transfer_boundary_note` | bounded_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_hw1_source_transfer_boundary.py` |
| 40 | `pmns_transfer_operator_dominant_mode_note` | bounded_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_transfer_operator_dominant_mode.py` |
| 41 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 42 | `koide_cone_completing_root_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_cone_completing_root_narrow.py` |
| 43 | `koide_cone_three_form_equivalence_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_cone_three_form_equivalence_narrow.py` |
| 44 | `koide_q_bridge_single_primitive_note_2026-04-22` | bounded_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_bridge_single_primitive.py` |
| 45 | `koide_q_readout_factorization_theorem_2026-04-22` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 46 | `koide_transport_gap_constant_no_go_note_2026-04-20` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_transport_gap_constant_no_go.py` |
| 47 | `pmns_oriented_cycle_selection_structure_note` | positive_theorem | unaudited | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_oriented_cycle_selection_structure.py` |
| 48 | `s3_boundary_link_theorem_note` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_boundary_link_theorem.py` |
| 49 | `three_generation_observable_count_corollary_note_2026-05-03` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_count_corollary.py` |
| 50 | `yt_ew_m_residual_stretch_attempt_note_2026-05-02` | no_go | unaudited | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/yt_ew_m_residual_channel_check.py` |

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
