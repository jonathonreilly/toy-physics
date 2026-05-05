# Audit Queue

**Total pending:** 1144
**Ready (all deps already at retained-grade or metadata tiers):** 290

By criticality:
- `critical`: 772
- `high`: 25
- `medium`: 139
- `leaf`: 208

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `fifth_family_radial_boundary_note` | bounded_theorem | audit_in_progress | critical | 296 | 8.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FIFTH_FAMILY_RADIAL_FAILURE_AUDIT.py` |
| 2 | `source_resolved_wavefield_v2_note` | bounded_theorem | audit_in_progress | critical | 295 | 8.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_wavefield_v2.py` |
| 3 | `signed_gravity_response_lane_status_note_2026-04-26` | no_go | audit_in_progress | critical | 289 | 12.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_signed_gravity_response_lane_status.py` |
| 4 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 288 | 10.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 5 | `universal_gr_polarization_frame_bundle_blocker_note` | bounded_theorem | audit_in_progress | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_polarization_frame_bundle.py` |
| 6 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 280 | 14.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 7 | `charged_lepton_two_higgs_canonical_reduction_note` | positive_theorem | audit_in_progress | critical | 277 | 13.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_two_higgs_canonical_reduction.py` |
| 8 | `s3_cap_uniqueness_note` | positive_theorem | unaudited | critical | 275 | 14.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 9 | `yt_color_projection_correction_note` | positive_theorem | unaudited | critical | 275 | 12.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 10 | `pmns_uniform_scalar_deformation_boundary_note` | positive_theorem | unaudited | critical | 275 | 11.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_uniform_scalar_deformation_boundary.py` |
| 11 | `dm_neutrino_weak_vector_theorem_note_2026-04-15` | positive_theorem | unaudited | critical | 275 | 8.61 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `axiom_first_lattice_noether_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 274 | 12.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_lattice_noether_check.py` |
| 13 | `dm_leptogenesis_ne_projected_source_law_derivation_note_2026-04-16` | positive_theorem | unaudited | critical | 274 | 12.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_ne_projected_source_law_derivation.py` |
| 14 | `neutrino_dirac_z3_support_trichotomy_note` | bounded_theorem | unaudited | critical | 274 | 11.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_dirac_z3_support_trichotomy.py` |
| 15 | `koide_q_background_zero_z_erasure_criterion_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 273 | 15.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_background_zero_z_erasure_criterion.py` |
| 16 | `pmns_oriented_cycle_channel_value_law_note` | positive_theorem | unaudited | critical | 273 | 12.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_oriented_cycle_channel_value_law.py` |
| 17 | `pmns_c3_nontrivial_current_boundary_note` | positive_theorem | unaudited | critical | 273 | 11.60 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `neutrino_majorana_nur_character_boundary_note` | bounded_theorem | unaudited | critical | 273 | 9.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_nur_character_boundary.py` |
| 19 | `neutrino_majorana_nur_charge2_primitive_reduction_note` | bounded_theorem | unaudited | critical | 273 | 9.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py` |
| 20 | `pmns_sole_axiom_hw1_source_transfer_boundary_note` | bounded_theorem | unaudited | critical | 273 | 9.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py` |
| 21 | `rconn_derived_note` | bounded_theorem | unaudited | critical | 272 | 14.59 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 22 | `koide_q_onsite_source_domain_no_go_synthesis_note_2026-04-25` | no_go | unaudited | critical | 272 | 13.59 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py` |
| 23 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 272 | 11.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 24 | `quark_bimodule_lo_shell_normalization_theorem_note_2026-04-19` | positive_theorem | unaudited | critical | 272 | 10.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_bimodule_lo_shell_normalization_theorem.py` |
| 25 | `dm_leptogenesis_ne_charged_source_response_reduction_note_2026-04-16` | positive_theorem | unaudited | critical | 271 | 12.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_ne_charged_source_response_reduction.py` |
| 26 | `lepton_single_higgs_pmns_triviality_note` | positive_theorem | unaudited | critical | 271 | 12.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lepton_single_higgs_pmns_triviality.py` |
| 27 | `pmns_selector_unique_amplitude_slot_note` | positive_theorem | unaudited | critical | 271 | 11.59 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_selector_unique_amplitude_slot.py` |
| 28 | `s3_time_constructed_support_tensor_primitive_note` | bounded_theorem | unaudited | critical | 271 | 9.59 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 29 | `s3_time_tensor_primitive_prototype_note` | bounded_theorem | unaudited | critical | 271 | 9.59 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 30 | `wave_retardation_lab_prediction_note` | positive_theorem | unaudited | critical | 271 | 8.59 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_retardation_velocity_sweep.py` |
| 31 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 270 | 14.58 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 32 | `restricted_strong_field_closure_note` | positive_theorem | unaudited | critical | 270 | 12.08 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 33 | `ckm_from_mass_hierarchy_note` | bounded_theorem | unaudited | critical | 270 | 11.08 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_from_mass_hierarchy.py` |
| 34 | `ckm_down_type_scale_convention_support_note_2026-04-22` | bounded_theorem | unaudited | critical | 270 | 10.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_down_type_scale_convention_support.py` |
| 35 | `oh_static_constraint_lift_note` | positive_theorem | unaudited | critical | 270 | 10.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_oh_static_constraint_lift.py` |
| 36 | `star_supported_bridge_class_note` | positive_theorem | unaudited | critical | 270 | 10.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_star_supported_bridge_class.py` |
| 37 | `work_history.ckm.ckm_mass_basis_nni_note` | bounded_theorem | unaudited | critical | 270 | 10.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_mass_basis_nni.py` |
| 38 | `pmns_selector_three_identity_support_note_2026-04-21` | positive_theorem | unaudited | critical | 270 | 10.08 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 39 | `linear_response_true_kubo_note` | bounded_theorem | unaudited | critical | 270 | 9.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/linear_response_true_kubo.py` |
| 40 | `unit_singlet_overlap_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 270 | 9.08 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_unit_singlet_overlap_narrow.py` |
| 41 | `universal_gr_tensor_action_blocker_note` | bounded_theorem | unaudited | critical | 270 | 9.08 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `koide_q_delta_closure_package_readme_2026-04-21` | positive_theorem | unaudited | critical | 269 | 14.08 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_Q_eq_3delta_identity.py` |
| 43 | `quark_route2_exact_readout_map_note_2026-04-19` | positive_theorem | unaudited | critical | 269 | 12.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_route2_exact_readout_map.py` |
| 44 | `planck_target3_phase_unit_edge_statistics_boundary_note_2026-04-25` | no_go | unaudited | critical | 269 | 11.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_phase_unit_edge_statistics.py` |
| 45 | `dm_neutrino_exact_h_source_surface_theorem_note_2026-04-16` | positive_theorem | unaudited | critical | 269 | 11.08 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_exact_h_source_surface_theorem.py` |
| 46 | `gravity_full_self_consistency_note` | positive_theorem | unaudited | critical | 269 | 10.08 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `tensor_support_center_excess_law_note` | bounded_theorem | unaudited | critical | 269 | 9.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_tensor_support_center_excess_law.py` |
| 48 | `dm_candidate_mass_window_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 269 | 9.08 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_candidate_mass_window_theorem.py` |
| 49 | `higgs_mass_hierarchy_correction_note` | bounded_theorem | unaudited | critical | 269 | 9.08 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `ew_higgs_gauge_mass_diagonalization_theorem_note_2026-04-26` | positive_theorem | unaudited | critical | 268 | 14.07 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_higgs_gauge_mass_diagonalization.py` |

## Citation cycle break targets

192 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 412 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 2 | `cycle-0002` | 7 | 412 | `anomaly_forces_time_theorem` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 299 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 299 | `universal_qg_projective_schur_closure_note` | critical | unaudited |
| 5 | `cycle-0005` | 3 | 299 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 279 | `higgs_from_lattice_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 279 | `higgs_mass_derived_note` | critical | audited_conditional |
| 8 | `cycle-0008` | 2 | 276 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 273 | `yt_explicit_systematic_budget_note` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 269 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 269 | `koide_gamma_orbit_cyclic_return_candidate_note_2026-04-18` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 269 | `universal_gr_tensor_quotient_uniqueness_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 269 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | critical | unaudited |
| 14 | `cycle-0014` | 2 | 268 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 267 | `quark_issr1_bicac_forcing_theorem_note_2026-04-19` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 266 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 264 | `abcc_cp_phase_no_go_theorem_note_2026-04-19` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 264 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 264 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 264 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 21 | `cycle-0021` | 2 | 264 | `dm_pmns_graph_first_ordered_chain_nonzero_current_activation_theorem_note_2026-04-21` | critical | unaudited |
| 22 | `cycle-0022` | 2 | 264 | `hadron_mass_lane1_theorem_plan_support_note_2026-04-27` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 264 | `koide_a1_fractional_topology_no_go_synthesis_note_2026-04-24` | critical | unaudited |
| 24 | `cycle-0024` | 2 | 264 | `koide_eigenvalue_q23_surface_theorem_note_2026-04-20` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 264 | `koide_berry_phase_theorem_note_2026-04-19` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
