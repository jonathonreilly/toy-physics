# Audit Queue

**Total pending:** 1168
**Ready (all deps already at retained-grade or metadata tiers):** 304

By criticality:
- `critical`: 801
- `high`: 24
- `medium`: 130
- `leaf`: 213

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `cl3_color_automorphism_theorem` | bounded_theorem | unaudited | critical | 393 | 17.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 2 | `gate_b_grown_distance_law_note` | bounded_theorem | audit_in_progress | critical | 328 | 12.36 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_grown_distance_law.py` |
| 3 | `oh_schur_boundary_action_note` | positive_theorem | unaudited | critical | 318 | 13.32 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_oh_schur_boundary_action.py` |
| 4 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 313 | 16.80 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 5 | `source_resolved_wavefield_mechanism_note` | positive_theorem | unaudited | critical | 301 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_wavefield_mechanism.py` |
| 6 | `claude_complex_action_carryover_note` | positive_theorem | unaudited | critical | 301 | 9.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/exact_lattice_complex_action_carryover.py` |
| 7 | `third_grown_family_boundary_note` | positive_theorem | unaudited | critical | 301 | 9.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/THIRD_GROWN_FAMILY_SIGN_SWEEP.py` |
| 8 | `alt_connectivity_family_basin_note` | bounded_theorem | unaudited | critical | 299 | 10.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/ALT_CONNECTIVITY_FAMILY_BASIN.py` |
| 9 | `fourth_family_quadrant_note` | positive_theorem | unaudited | critical | 297 | 9.22 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FOURTH_FAMILY_QUADRANT_SWEEP.py` |
| 10 | `fifth_family_radial_boundary_note` | bounded_theorem | audit_in_progress | critical | 296 | 8.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FIFTH_FAMILY_RADIAL_FAILURE_AUDIT.py` |
| 11 | `source_resolved_wavefield_v2_note` | positive_theorem | unaudited | critical | 295 | 8.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_wavefield_v2.py` |
| 12 | `shapiro_static_discriminator_note` | positive_theorem | unaudited | critical | 291 | 10.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_static_discriminator.py` |
| 13 | `signed_gravity_response_lane_status_note_2026-04-26` | no_go | audit_in_progress | critical | 289 | 12.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_signed_gravity_response_lane_status.py` |
| 14 | `gravitomagnetic_note` | positive_theorem | unaudited | critical | 289 | 9.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravitomagnetic_portable.py` |
| 15 | `causal_escape_window_note` | bounded_theorem | unaudited | critical | 289 | 8.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/causal_escape_window.py` |
| 16 | `single_axiom_hilbert_note` | positive_theorem | unaudited | critical | 288 | 12.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_single_axiom_hilbert.py` |
| 17 | `bell_inequality_derived_note` | bounded_theorem | unaudited | critical | 288 | 11.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bell_inequality.py` |
| 18 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 288 | 10.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 19 | `electrostatics_grown_sign_law_note` | bounded_theorem | unaudited | critical | 288 | 9.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py` |
| 20 | `quark_cp_carrier_completion_note_2026-04-18` | bounded_theorem | unaudited | critical | 287 | 13.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_cp_carrier_completion.py` |
| 21 | `universal_gr_polarization_frame_bundle_blocker_note` | bounded_theorem | unaudited | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_polarization_frame_bundle.py` |
| 22 | `scalar_trace_tensor_no_go_note` | bounded_theorem | unaudited | critical | 283 | 9.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_scalar_trace_tensor_nogo.py` |
| 23 | `yukawa_color_projection_theorem` | positive_theorem | unaudited | critical | 282 | 13.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_current_fierz_channel_decomposition.py` |
| 24 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 280 | 14.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 25 | `yt_bridge_nonlocal_corrections_note` | bounded_theorem | unaudited | critical | 280 | 10.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_nonlocal_corrections.py` |
| 26 | `yt_bridge_uv_class_uniqueness_note` | bounded_theorem | unaudited | critical | 279 | 9.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_uv_class_uniqueness.py` |
| 27 | `cosmology_scale_identification_and_reduction_note` | bounded_theorem | unaudited | critical | 277 | 14.62 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 28 | `charged_lepton_two_higgs_canonical_reduction_note` | positive_theorem | unaudited | critical | 277 | 13.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_two_higgs_canonical_reduction.py` |
| 29 | `neutrino_dirac_two_higgs_canonical_reduction_note` | positive_theorem | unaudited | critical | 277 | 12.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_dirac_two_higgs_canonical_reduction.py` |
| 30 | `graviton_mass_derived_note` | bounded_theorem | unaudited | critical | 277 | 12.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graviton_mass_derived.py` |
| 31 | `dark_energy_eos_note` | bounded_theorem | unaudited | critical | 277 | 9.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dark_energy_eos.py` |
| 32 | `strong_cp_theta_zero_note` | bounded_theorem | unaudited | critical | 276 | 15.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_strong_cp_theta_zero.py` |
| 33 | `universal_theta_induced_edm_vanishing_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 276 | 13.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_theta_induced_edm_vanishing.py` |
| 34 | `s3_cap_uniqueness_note` | positive_theorem | unaudited | critical | 275 | 14.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 35 | `yt_color_projection_correction_note` | positive_theorem | unaudited | critical | 275 | 12.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 36 | `pmns_uniform_scalar_deformation_boundary_note` | positive_theorem | unaudited | critical | 275 | 11.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_uniform_scalar_deformation_boundary.py` |
| 37 | `dm_neutrino_weak_vector_theorem_note_2026-04-15` | positive_theorem | unaudited | critical | 275 | 8.61 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 38 | `axiom_first_lattice_noether_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 274 | 12.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_lattice_noether_check.py` |
| 39 | `dm_leptogenesis_ne_projected_source_law_derivation_note_2026-04-16` | positive_theorem | unaudited | critical | 274 | 12.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_ne_projected_source_law_derivation.py` |
| 40 | `neutrino_dirac_z3_support_trichotomy_note` | bounded_theorem | unaudited | critical | 274 | 11.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_dirac_z3_support_trichotomy.py` |
| 41 | `koide_q_background_zero_z_erasure_criterion_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 273 | 15.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_background_zero_z_erasure_criterion.py` |
| 42 | `pmns_oriented_cycle_channel_value_law_note` | positive_theorem | unaudited | critical | 273 | 12.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_oriented_cycle_channel_value_law.py` |
| 43 | `pmns_c3_nontrivial_current_boundary_note` | positive_theorem | unaudited | critical | 273 | 11.60 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `neutrino_majorana_nur_character_boundary_note` | bounded_theorem | unaudited | critical | 273 | 9.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_nur_character_boundary.py` |
| 45 | `neutrino_majorana_nur_charge2_primitive_reduction_note` | bounded_theorem | unaudited | critical | 273 | 9.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_nur_charge2_primitive_reduction.py` |
| 46 | `pmns_sole_axiom_hw1_source_transfer_boundary_note` | bounded_theorem | unaudited | critical | 273 | 9.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py` |
| 47 | `koide_q_onsite_source_domain_no_go_synthesis_note_2026-04-25` | no_go | unaudited | critical | 272 | 13.59 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py` |
| 48 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 272 | 11.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 49 | `quark_bimodule_lo_shell_normalization_theorem_note_2026-04-19` | positive_theorem | unaudited | critical | 272 | 10.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_bimodule_lo_shell_normalization_theorem.py` |
| 50 | `dm_leptogenesis_ne_charged_source_response_reduction_note_2026-04-16` | positive_theorem | unaudited | critical | 271 | 12.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_ne_charged_source_response_reduction.py` |

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
