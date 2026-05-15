# Audit Queue

**Total pending:** 1185
**Ready (all deps already at retained-grade or metadata tiers):** 5

By criticality:
- `critical`: 736
- `high`: 34
- `medium`: 153
- `leaf`: 262

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `charged_lepton_koide_review_packet_2026-04-18` | positive_theorem | unaudited | critical | 423 | 15.73 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 2 | `neutrino_mass_reduction_to_dirac_note` | positive_theorem | unaudited | critical | 420 | 15.22 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_mass_reduction_to_dirac.py` |
| 3 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 785 | 19.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 4 | `cpt_exact_note` | positive_theorem | unaudited | critical | 783 | 23.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 5 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 775 | 10.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 6 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 774 | 18.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 7 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 773 | 25.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 8 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 773 | 11.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 9 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 772 | 15.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 10 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 765 | 11.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 11 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 764 | 11.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 12 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 763 | 10.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 13 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 762 | 11.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 14 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 761 | 14.57 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 15 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 761 | 14.57 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 16 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 760 | 15.57 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 17 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 759 | 19.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 18 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 757 | 16.57 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 19 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 740 | 14.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 20 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 739 | 13.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 21 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 739 | 13.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 22 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | open_gate | unaudited | critical | 739 | 10.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_bridge_3plus1_native_tube_staging.py` |
| 23 | `su3_cube_index_graph_shortcut_open_gate_note_2026-05-03` | open_gate | unaudited | critical | 739 | 10.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py` |
| 24 | `su3_cube_perron_solve_combined_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 739 | 10.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_perron_solve.py` |
| 25 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 737 | 30.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 26 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 730 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 27 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 730 | 12.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 28 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 729 | 27.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 29 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 672 | 13.39 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 30 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 671 | 37.39 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 31 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 629 | 18.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 32 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 626 | 10.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 33 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 625 | 11.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 34 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 615 | 29.77 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 35 | `yt_vertex_power_derivation` | open_gate | unaudited | critical | 593 | 10.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_vertex_power.py` |
| 36 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 592 | 34.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 37 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 584 | 24.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 38 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 560 | 11.13 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 39 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 558 | 18.13 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 40 | `yt_color_projection_correction_note` | positive_theorem | unaudited | critical | 553 | 14.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 41 | `yt_qfp_insensitivity_support_note` | bounded_theorem | unaudited | critical | 552 | 17.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 42 | `yt_exact_schur_normal_form_uniqueness_note` | bounded_theorem | unaudited | critical | 552 | 16.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_schur_normal_form_uniqueness.py` |
| 43 | `yt_boundary_theorem` | open_gate | unaudited | critical | 552 | 15.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_boundary_consistency.py` |
| 44 | `yt_constructive_uv_bridge_note` | bounded_theorem | unaudited | critical | 552 | 15.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_constructive_uv_bridge.py` |
| 45 | `yt_interacting_bridge_locality_note` | bounded_theorem | unaudited | critical | 552 | 14.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_interacting_bridge_locality.py` |
| 46 | `yt_bridge_hessian_selector_note` | bounded_theorem | unaudited | critical | 552 | 14.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_hessian_selector.py` |
| 47 | `yt_bridge_rearrangement_principle_note` | bounded_theorem | unaudited | critical | 552 | 13.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_rearrangement_principle.py` |
| 48 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 552 | 13.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 49 | `yt_bridge_higher_order_corrections_note` | bounded_theorem | unaudited | critical | 552 | 12.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_higher_order_corrections.py` |
| 50 | `yt_bridge_nonlocal_corrections_note` | bounded_theorem | unaudited | critical | 552 | 12.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_nonlocal_corrections.py` |

## Citation cycle break targets

183 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 773 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 3 | 739 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 3 | `cycle-0003` | 4 | 739 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 4 | `cycle-0004` | 5 | 739 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 5 | `cycle-0005` | 6 | 739 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 552 | `yt_bridge_action_invariant_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 552 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 552 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 552 | `yt_ew_coupling_bridge_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 552 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 552 | `yt_bridge_moment_closure_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 552 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 13 | `cycle-0013` | 4 | 552 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 14 | `cycle-0014` | 4 | 552 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 15 | `cycle-0015` | 4 | 552 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 16 | `cycle-0016` | 8 | 552 | `yt_boundary_theorem` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 470 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 470 | `source_resolved_exact_green_pocket_note` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 470 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 437 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 21 | `cycle-0021` | 3 | 437 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 437 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 23 | `cycle-0023` | 6 | 437 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 24 | `cycle-0024` | 7 | 437 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 25 | `cycle-0025` | 8 | 437 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
