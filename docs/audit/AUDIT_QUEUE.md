# Audit Queue

**Total pending:** 1172
**Ready (all deps already at retained-grade or metadata tiers):** 18

By criticality:
- `critical`: 730
- `high`: 33
- `medium`: 144
- `leaf`: 265

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | audit_in_progress | critical | 726 | 11.51 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 2 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 725 | 10.00 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 3 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 604 | 17.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 4 | `minimal_source_driven_field_probe_note` | bounded_theorem | unaudited | critical | 488 | 11.43 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/minimal_source_driven_field_probe.py` |
| 5 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 475 | 44.90 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 6 | `complex_action_note` | bounded_theorem | unaudited | critical | 448 | 11.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_harness.py` |
| 7 | `valley_linear_robustness_note` | bounded_theorem | unaudited | critical | 428 | 10.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/valley_linear_robustness_sweep.py` |
| 8 | `valley_linear_asymptotic_bridge_note` | bounded_theorem | audit_in_progress | critical | 428 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/valley_linear_asymptotic_bridge.py` |
| 9 | `persistent_object_inward_boundary_floor_diagnosis_note_2026-04-16` | bounded_theorem | audit_in_progress | critical | 425 | 9.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 10 | `lensing_beta_sweep_note` | bounded_theorem | unaudited | critical | 425 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_beta_sweep.py` |
| 11 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 424 | 9.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 12 | `wave_retarded_gravity_note` | bounded_theorem | unaudited | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_retarded_gravity.py` |
| 13 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 776 | 19.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 14 | `cpt_exact_note` | positive_theorem | unaudited | critical | 774 | 23.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 15 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 766 | 10.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 16 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 765 | 18.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 17 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 763 | 15.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 18 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 756 | 11.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 19 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 756 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 20 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 755 | 11.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 21 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 754 | 10.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 22 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 753 | 11.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 23 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 752 | 14.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 24 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 752 | 14.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 25 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 751 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 26 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 750 | 19.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 27 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 748 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 28 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 736 | 30.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 29 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 730 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 30 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 729 | 13.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 31 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 724 | 28.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 32 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 724 | 13.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 33 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 724 | 12.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 34 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 724 | 12.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 35 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 723 | 27.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 36 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 668 | 13.39 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 37 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 667 | 37.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 38 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 627 | 18.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 39 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 624 | 10.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 40 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 623 | 11.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 41 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 602 | 28.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 42 | `yt_vertex_power_derivation` | open_gate | unaudited | critical | 588 | 10.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_vertex_power.py` |
| 43 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 587 | 33.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 44 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 584 | 24.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 45 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 566 | 11.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 46 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 564 | 18.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 47 | `s3_time_transfer_matrix_bridge_note` | bounded_theorem | unaudited | critical | 555 | 11.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_transfer_matrix_bridge.py` |
| 48 | `s3_time_bilinear_tensor_primitive_note` | open_gate | unaudited | critical | 553 | 13.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_primitive.py` |
| 49 | `yt_color_projection_correction_note` | positive_theorem | unaudited | critical | 551 | 14.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 50 | `yt_qfp_insensitivity_support_note` | bounded_theorem | unaudited | critical | 550 | 17.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |

## Citation cycle break targets

257 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 550 | `yt_bridge_action_invariant_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 550 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 550 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 550 | `yt_ew_coupling_bridge_note` | critical | unaudited |
| 5 | `cycle-0005` | 3 | 550 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 550 | `yt_bridge_moment_closure_note` | critical | unaudited |
| 7 | `cycle-0007` | 3 | 550 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 8 | `cycle-0008` | 4 | 550 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 550 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 550 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 11 | `cycle-0011` | 8 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 12 | `cycle-0012` | 9 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 13 | `cycle-0013` | 9 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 14 | `cycle-0014` | 9 | 550 | `yt_bridge_uv_class_uniqueness_note` | critical | unaudited |
| 15 | `cycle-0015` | 9 | 550 | `yt_bridge_uv_class_uniqueness_note` | critical | unaudited |
| 16 | `cycle-0016` | 10 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 17 | `cycle-0017` | 10 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 18 | `cycle-0018` | 10 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 19 | `cycle-0019` | 10 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 472 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 21 | `cycle-0021` | 2 | 472 | `source_resolved_exact_green_pocket_note` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 472 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 23 | `cycle-0023` | 3 | 439 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 24 | `cycle-0024` | 9 | 438 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 429 | `pmns_active_four_real_source_from_transport_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
