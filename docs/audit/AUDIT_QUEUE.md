# Audit Queue

**Total pending:** 1150
**Ready (all deps already at retained-grade or metadata tiers):** 0

By criticality:
- `critical`: 715
- `high`: 33
- `medium`: 141
- `leaf`: 261

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 776 | 19.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 2 | `cpt_exact_note` | positive_theorem | unaudited | critical | 774 | 23.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 3 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 766 | 10.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 4 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 765 | 18.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 5 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 763 | 15.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 6 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 756 | 11.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 7 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 756 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 8 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 755 | 11.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 9 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 754 | 10.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 10 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 753 | 11.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 11 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 752 | 14.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 12 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 752 | 14.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 13 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 751 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 14 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 750 | 19.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 15 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 748 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 16 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 736 | 30.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 17 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 730 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 18 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 729 | 13.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 19 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 724 | 13.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 20 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 724 | 12.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 21 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 723 | 27.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 22 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 668 | 13.39 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 23 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 667 | 37.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 24 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 627 | 18.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 25 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 624 | 10.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 623 | 11.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 27 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 602 | 28.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 28 | `yt_vertex_power_derivation` | open_gate | unaudited | critical | 588 | 10.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_vertex_power.py` |
| 29 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 587 | 33.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 30 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 584 | 24.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 31 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 566 | 11.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 32 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 564 | 18.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 33 | `s3_time_transfer_matrix_bridge_note` | bounded_theorem | unaudited | critical | 555 | 11.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_transfer_matrix_bridge.py` |
| 34 | `s3_time_bilinear_tensor_primitive_note` | open_gate | unaudited | critical | 553 | 13.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_primitive.py` |
| 35 | `yt_color_projection_correction_note` | positive_theorem | unaudited | critical | 551 | 14.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 36 | `yt_qfp_insensitivity_support_note` | bounded_theorem | unaudited | critical | 550 | 17.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 37 | `yt_exact_schur_normal_form_uniqueness_note` | bounded_theorem | unaudited | critical | 550 | 16.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_schur_normal_form_uniqueness.py` |
| 38 | `yt_boundary_theorem` | open_gate | unaudited | critical | 550 | 15.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_boundary_consistency.py` |
| 39 | `yt_constructive_uv_bridge_note` | bounded_theorem | unaudited | critical | 550 | 15.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_constructive_uv_bridge.py` |
| 40 | `yt_interacting_bridge_locality_note` | bounded_theorem | unaudited | critical | 550 | 14.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_interacting_bridge_locality.py` |
| 41 | `yt_bridge_hessian_selector_note` | bounded_theorem | unaudited | critical | 550 | 14.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_hessian_selector.py` |
| 42 | `yt_bridge_rearrangement_principle_note` | bounded_theorem | unaudited | critical | 550 | 13.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_rearrangement_principle.py` |
| 43 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 550 | 13.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 44 | `yt_bridge_higher_order_corrections_note` | bounded_theorem | unaudited | critical | 550 | 12.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_higher_order_corrections.py` |
| 45 | `yt_bridge_nonlocal_corrections_note` | bounded_theorem | unaudited | critical | 550 | 12.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_nonlocal_corrections.py` |
| 46 | `yt_bridge_action_invariant_note` | bounded_theorem | unaudited | critical | 550 | 12.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_action_invariant.py` |
| 47 | `yt_bridge_moment_closure_note` | bounded_theorem | unaudited | critical | 550 | 12.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_moment_closure.py` |
| 48 | `yt_bridge_operator_closure_note` | bounded_theorem | unaudited | critical | 550 | 11.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_operator_closure.py` |
| 49 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 550 | 11.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 50 | `yt_exact_coarse_grained_bridge_operator_note` | bounded_theorem | unaudited | critical | 550 | 11.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_coarse_grained_bridge_operator.py` |

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
