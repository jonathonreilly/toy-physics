# Audit Queue

**Total pending:** 1157
**Ready (all deps already at retained-grade or metadata tiers):** 298

By criticality:
- `critical`: 787
- `high`: 25
- `medium`: 137
- `leaf`: 208

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `g_bare_rescaling_freedom_removal_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 394 | 9.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 2 | `source_resolved_wavefield_mechanism_note` | positive_theorem | unaudited | critical | 301 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_wavefield_mechanism.py` |
| 3 | `claude_complex_action_carryover_note` | positive_theorem | unaudited | critical | 301 | 9.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/exact_lattice_complex_action_carryover.py` |
| 4 | `third_grown_family_boundary_note` | positive_theorem | unaudited | critical | 301 | 9.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/THIRD_GROWN_FAMILY_SIGN_SWEEP.py` |
| 5 | `alt_connectivity_family_basin_note` | bounded_theorem | unaudited | critical | 299 | 10.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/ALT_CONNECTIVITY_FAMILY_BASIN.py` |
| 6 | `fourth_family_quadrant_note` | positive_theorem | unaudited | critical | 297 | 9.22 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FOURTH_FAMILY_QUADRANT_SWEEP.py` |
| 7 | `fifth_family_radial_boundary_note` | bounded_theorem | audit_in_progress | critical | 296 | 8.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FIFTH_FAMILY_RADIAL_FAILURE_AUDIT.py` |
| 8 | `source_resolved_wavefield_v2_note` | positive_theorem | unaudited | critical | 295 | 8.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_wavefield_v2.py` |
| 9 | `signed_gravity_response_lane_status_note_2026-04-26` | no_go | audit_in_progress | critical | 289 | 12.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_signed_gravity_response_lane_status.py` |
| 10 | `causal_escape_window_note` | bounded_theorem | unaudited | critical | 289 | 8.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/causal_escape_window.py` |
| 11 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 288 | 10.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 12 | `universal_gr_polarization_frame_bundle_blocker_note` | bounded_theorem | audit_in_progress | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_polarization_frame_bundle.py` |
| 13 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 280 | 14.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 14 | `cosmology_scale_identification_and_reduction_note` | bounded_theorem | unaudited | critical | 277 | 14.62 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 15 | `charged_lepton_two_higgs_canonical_reduction_note` | positive_theorem | unaudited | critical | 277 | 13.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_two_higgs_canonical_reduction.py` |
| 16 | `neutrino_dirac_two_higgs_canonical_reduction_note` | positive_theorem | unaudited | critical | 277 | 12.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_dirac_two_higgs_canonical_reduction.py` |
| 17 | `graviton_mass_derived_note` | bounded_theorem | unaudited | critical | 277 | 12.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graviton_mass_derived.py` |
| 18 | `dark_energy_eos_note` | bounded_theorem | unaudited | critical | 277 | 9.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dark_energy_eos.py` |
| 19 | `strong_cp_theta_zero_note` | bounded_theorem | unaudited | critical | 276 | 15.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_strong_cp_theta_zero.py` |
| 20 | `universal_theta_induced_edm_vanishing_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 276 | 13.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_theta_induced_edm_vanishing.py` |
| 21 | `s3_cap_uniqueness_note` | positive_theorem | unaudited | critical | 275 | 14.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 22 | `yt_color_projection_correction_note` | positive_theorem | unaudited | critical | 275 | 12.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 23 | `pmns_uniform_scalar_deformation_boundary_note` | positive_theorem | unaudited | critical | 275 | 11.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_uniform_scalar_deformation_boundary.py` |
| 24 | `dm_neutrino_weak_vector_theorem_note_2026-04-15` | positive_theorem | unaudited | critical | 275 | 8.61 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 25 | `axiom_first_lattice_noether_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 274 | 12.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_lattice_noether_check.py` |
| 26 | `dm_leptogenesis_ne_projected_source_law_derivation_note_2026-04-16` | positive_theorem | unaudited | critical | 274 | 12.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_ne_projected_source_law_derivation.py` |
| 27 | `neutrino_dirac_z3_support_trichotomy_note` | bounded_theorem | unaudited | critical | 274 | 11.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_dirac_z3_support_trichotomy.py` |
| 28 | `koide_q_background_zero_z_erasure_criterion_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 273 | 15.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_background_zero_z_erasure_criterion.py` |
| 29 | `pmns_oriented_cycle_channel_value_law_note` | positive_theorem | unaudited | critical | 273 | 12.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_oriented_cycle_channel_value_law.py` |
| 30 | `pmns_c3_nontrivial_current_boundary_note` | positive_theorem | unaudited | critical | 273 | 11.60 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `neutrino_majorana_nur_character_boundary_note` | bounded_theorem | unaudited | critical | 273 | 9.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_nur_character_boundary.py` |
| 32 | `neutrino_majorana_nur_charge2_primitive_reduction_note` | bounded_theorem | unaudited | critical | 273 | 9.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py` |
| 33 | `pmns_sole_axiom_hw1_source_transfer_boundary_note` | bounded_theorem | unaudited | critical | 273 | 9.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py` |
| 34 | `rconn_derived_note` | bounded_theorem | unaudited | critical | 272 | 14.59 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 35 | `koide_q_onsite_source_domain_no_go_synthesis_note_2026-04-25` | no_go | unaudited | critical | 272 | 13.59 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py` |
| 36 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 272 | 11.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 37 | `quark_bimodule_lo_shell_normalization_theorem_note_2026-04-19` | positive_theorem | unaudited | critical | 272 | 10.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_bimodule_lo_shell_normalization_theorem.py` |
| 38 | `dm_leptogenesis_ne_charged_source_response_reduction_note_2026-04-16` | positive_theorem | unaudited | critical | 271 | 12.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_ne_charged_source_response_reduction.py` |
| 39 | `lepton_single_higgs_pmns_triviality_note` | positive_theorem | unaudited | critical | 271 | 12.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lepton_single_higgs_pmns_triviality.py` |
| 40 | `pmns_selector_unique_amplitude_slot_note` | positive_theorem | unaudited | critical | 271 | 11.59 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_selector_unique_amplitude_slot.py` |
| 41 | `s3_time_constructed_support_tensor_primitive_note` | bounded_theorem | unaudited | critical | 271 | 9.59 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `s3_time_tensor_primitive_prototype_note` | bounded_theorem | unaudited | critical | 271 | 9.59 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `wave_retardation_lab_prediction_note` | positive_theorem | unaudited | critical | 271 | 8.59 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_retardation_velocity_sweep.py` |
| 44 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 270 | 14.58 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `restricted_strong_field_closure_note` | positive_theorem | unaudited | critical | 270 | 12.08 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `ckm_from_mass_hierarchy_note` | bounded_theorem | unaudited | critical | 270 | 11.08 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_from_mass_hierarchy.py` |
| 47 | `ckm_down_type_scale_convention_support_note_2026-04-22` | bounded_theorem | unaudited | critical | 270 | 10.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_down_type_scale_convention_support.py` |
| 48 | `oh_static_constraint_lift_note` | positive_theorem | unaudited | critical | 270 | 10.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_oh_static_constraint_lift.py` |
| 49 | `star_supported_bridge_class_note` | positive_theorem | unaudited | critical | 270 | 10.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_star_supported_bridge_class.py` |
| 50 | `work_history.ckm.ckm_mass_basis_nni_note` | bounded_theorem | unaudited | critical | 270 | 10.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_mass_basis_nni.py` |

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
