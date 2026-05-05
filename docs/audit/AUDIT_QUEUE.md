# Audit Queue

**Total pending:** 918
**Ready (all deps already at retained-grade or metadata tiers):** 60

By criticality:
- `critical`: 580
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
| 4 | `dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_note_2026-04-18` | positive_theorem | audit_in_progress | critical | 285 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_2026_04_18.py` |
| 5 | `koide_q23_oh_covariance_nogo_note_2026-04-22` | no_go | audit_in_progress | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q23_oh_covariance_nogo.py` |
| 6 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | positive_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_2026_04_18.py` |
| 7 | `koide_berry_bundle_obstruction_theorem_note_2026-04-19` | positive_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_berry_bundle_obstruction_theorem.py` |
| 8 | `koide_circulant_wilson_target_note_2026-04-18` | positive_theorem | unaudited | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_wilson_target.py` |
| 9 | `planck_boundary_orientation_incidence_no_go_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_orientation_incidence_no_go.py` |
| 10 | `pmns_hw1_source_transfer_boundary_note` | bounded_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_hw1_source_transfer_boundary.py` |
| 11 | `pmns_transfer_operator_dominant_mode_note` | bounded_theorem | audit_in_progress | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_transfer_operator_dominant_mode.py` |
| 12 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 13 | `hierarchy_matsubara_determinant_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_matsubara_determinant_narrow.py` |
| 14 | `koide_cone_completing_root_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_cone_completing_root_narrow.py` |
| 15 | `koide_cone_three_form_equivalence_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_cone_three_form_equivalence_narrow.py` |
| 16 | `koide_q_bridge_single_primitive_note_2026-04-22` | bounded_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_bridge_single_primitive.py` |
| 17 | `koide_q_readout_factorization_theorem_2026-04-22` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 18 | `koide_transport_gap_constant_no_go_note_2026-04-20` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_transport_gap_constant_no_go.py` |
| 19 | `pmns_oriented_cycle_selection_structure_note` | positive_theorem | unaudited | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_oriented_cycle_selection_structure.py` |
| 20 | `s3_boundary_link_theorem_note` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_boundary_link_theorem.py` |
| 21 | `three_generation_observable_count_corollary_note_2026-05-03` | positive_theorem | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_count_corollary.py` |
| 22 | `yt_ew_m_residual_stretch_attempt_note_2026-05-02` | no_go | unaudited | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/yt_ew_m_residual_channel_check.py` |
| 23 | `affine_imaginary_slot_invariance_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_affine_imaginary_slot_invariance_narrow.py` |
| 24 | `background_independence_note` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_background_independence.py` |
| 25 | `block_gaussian_schur_marginalization_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_block_gaussian_schur_narrow.py` |
| 26 | `circulant_response_master_identity_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_circulant_response_master_identity_narrow.py` |
| 27 | `dm_leptogenesis_pmns_microscopic_d_last_mile_note_2026-04-16` | positive_theorem | unaudited | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_pmns_microscopic_d_last_mile.py` |
| 28 | `koide_cyclic_projector_block_democracy_note_2026-04-18` | bounded_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_cyclic_projector_block_democracy.py` |
| 29 | `koide_hostile_review_guard_note_2026-04-24` | no_go | unaudited | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_hostile_review_guard.py` |
| 30 | `koide_kappa_spectrum_operator_bridge_theorem_note_2026-04-19` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_kappa_spectrum_operator_bridge_theorem.py` |
| 31 | `kubo_range_of_validity_note` | positive_theorem | unaudited | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/kubo_range_of_validity.py` |
| 32 | `lattice_complementarity_note` | bounded_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_complementarity_sweep.py` |
| 33 | `lorentz_violation_derived_note` | bounded_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_violation.py` |
| 34 | `scalar_selector_synthesis_note_2026-04-19` | bounded_theorem | unaudited | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_z3_joint_projector_identity.py` |
| 35 | `tensor_block_closure_test_note` | bounded_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_tensor_block_closure_test.py` |
| 36 | `wave_equation_gravity_note` | bounded_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wave_equation_gravity.py` |
| 37 | `wave_equation_self_field_note` | bounded_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_equation_self_field.py` |
| 38 | `wave_radiation_note` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_radiation.py` |
| 39 | `z3_conjugate_support_trichotomy_narrow_theorem_note_2026-05-02` | positive_theorem | audit_in_progress | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_z3_conjugate_support_trichotomy_narrow.py` |
| 40 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 447 | 13.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 41 | `cpt_exact_note` | positive_theorem | unaudited | critical | 443 | 17.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 443 | 11.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 43 | `born_scattering_comparison_note` | positive_theorem | unaudited | critical | 442 | 10.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gaussian_beam_eikonal.py` |
| 44 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 438 | 14.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 45 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 438 | 14.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 46 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 438 | 13.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 47 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 438 | 12.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 48 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 437 | 25.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 49 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 437 | 16.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 50 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 437 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | - |

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
