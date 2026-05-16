# Audit Queue

**Total pending:** 1198
**Ready (all deps already at retained-grade or metadata tiers):** 19

By criticality:
- `critical`: 743
- `high`: 34
- `medium`: 151
- `leaf`: 270

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 919 | 13.35 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 2 | `poisson_self_gravity_loop_note` | bounded_theorem | unaudited | critical | 791 | 13.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 3 | `cpt_exact_real_anti_hermitian_d_narrow_theorem_note_2026-05-10` | bounded_theorem | audit_in_progress | critical | 782 | 14.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/audit_companion_cpt_exact_real_anti_hermitian_d_exact_2026_05_10.py` |
| 4 | `observable_principle_real_d_block_uniqueness_narrow_theorem_note_2026-05-10` | bounded_theorem | audit_in_progress | critical | 781 | 11.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/audit_companion_observable_principle_real_d_block_uniqueness_exact_2026_05_10.py` |
| 5 | `hierarchy_matsubara_free_energy_density_narrow_theorem_note_2026-05-16` | positive_theorem | unaudited | critical | 780 | 10.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_matsubara_free_energy_density_narrow.py` |
| 6 | `koide_q_readout_factorization_theorem_2026-04-22` | bounded_theorem | unaudited | critical | 779 | 12.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 7 | `s3_boundary_link_theorem_note` | bounded_theorem | unaudited | critical | 779 | 12.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_boundary_link_theorem.py` |
| 8 | `pmns_commutant_eigenoperator_selector_note` | bounded_theorem | unaudited | critical | 779 | 11.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_commutant_eigenoperator_selector.py` |
| 9 | `generation_axiom_boundary_note` | bounded_theorem | unaudited | critical | 778 | 11.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 10 | `koide_cl3_selector_gap_note_2026-04-19` | open_gate | unaudited | critical | 778 | 11.11 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 11 | `wave_static_direct_probe_fine_note` | positive_theorem | unaudited | critical | 778 | 10.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_direct_probe.py` |
| 12 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 916 | 14.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 13 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 915 | 13.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 14 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 910 | 13.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 15 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 910 | 12.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 16 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 909 | 28.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 17 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 863 | 13.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 18 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 862 | 37.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 19 | `yt_vertex_power_derivation` | open_gate | unaudited | critical | 857 | 11.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_vertex_power.py` |
| 20 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 856 | 34.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 21 | `yt_color_projection_correction_note` | bounded_theorem | unaudited | critical | 834 | 14.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 22 | `yt_qfp_insensitivity_support_note` | bounded_theorem | unaudited | critical | 833 | 17.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 23 | `yt_exact_schur_normal_form_uniqueness_note` | bounded_theorem | unaudited | critical | 833 | 16.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_schur_normal_form_uniqueness.py` |
| 24 | `yt_boundary_theorem` | open_gate | unaudited | critical | 833 | 16.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_boundary_consistency.py` |
| 25 | `yt_constructive_uv_bridge_note` | bounded_theorem | unaudited | critical | 833 | 16.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_constructive_uv_bridge.py` |
| 26 | `yt_interacting_bridge_locality_note` | bounded_theorem | unaudited | critical | 833 | 15.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_interacting_bridge_locality.py` |
| 27 | `yt_bridge_hessian_selector_note` | bounded_theorem | unaudited | critical | 833 | 14.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_hessian_selector.py` |
| 28 | `yt_bridge_rearrangement_principle_note` | bounded_theorem | unaudited | critical | 833 | 13.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_rearrangement_principle.py` |
| 29 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 833 | 13.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 30 | `yt_bridge_higher_order_corrections_note` | bounded_theorem | unaudited | critical | 833 | 13.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_higher_order_corrections.py` |
| 31 | `yt_bridge_nonlocal_corrections_note` | bounded_theorem | unaudited | critical | 833 | 13.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_nonlocal_corrections.py` |
| 32 | `yt_bridge_action_invariant_note` | bounded_theorem | unaudited | critical | 833 | 12.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_action_invariant.py` |
| 33 | `yt_bridge_moment_closure_note` | bounded_theorem | unaudited | critical | 833 | 12.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_moment_closure.py` |
| 34 | `yt_bridge_operator_closure_note` | bounded_theorem | unaudited | critical | 833 | 12.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_operator_closure.py` |
| 35 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 833 | 12.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 36 | `yt_exact_coarse_grained_bridge_operator_note` | bounded_theorem | unaudited | critical | 833 | 11.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_coarse_grained_bridge_operator.py` |
| 37 | `yt_exact_interacting_bridge_transport_note` | bounded_theorem | unaudited | critical | 833 | 11.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_interacting_bridge_transport.py` |
| 38 | `yt_bridge_endpoint_shift_bound_note` | bounded_theorem | unaudited | critical | 833 | 11.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_endpoint_shift_bound.py` |
| 39 | `yt_bridge_uv_class_uniqueness_note` | bounded_theorem | unaudited | critical | 833 | 11.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_uv_class_uniqueness.py` |
| 40 | `yt_ew_coupling_bridge_note` | positive_theorem | unaudited | critical | 833 | 11.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ew_coupling_derivation.py` |
| 41 | `yt_eft_bridge_theorem` | open_gate | unaudited | critical | 833 | 10.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_eft_bridge.py` |
| 42 | `gate_b_grown_joint_package_note` | bounded_theorem | unaudited | critical | 826 | 13.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_grown_joint_package.py` |
| 43 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 811 | 46.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 44 | `gate_b_weak_connectivity_note` | bounded_theorem | unaudited | critical | 810 | 12.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_weak_connectivity_harness.py` |
| 45 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 806 | 30.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 46 | `g_bare_rigidity_theorem_note` | positive_theorem | unaudited | critical | 806 | 13.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 47 | `gate_b_nonlabel_connectivity_v1_note` | bounded_theorem | unaudited | critical | 806 | 13.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1.py` |
| 48 | `g_bare_structural_normalization_theorem_note_2026-04-18` | positive_theorem | unaudited | critical | 805 | 18.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_structural_normalization.py` |
| 49 | `source_resolved_exact_green_pocket_note` | bounded_theorem | unaudited | critical | 803 | 12.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_exact_green_pocket.py` |
| 50 | `source_resolved_exact_green_scaling_note` | bounded_theorem | unaudited | critical | 803 | 11.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_exact_green_scaling.py` |

## Citation cycle break targets

242 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 833 | `yt_bridge_action_invariant_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 833 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 833 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 833 | `yt_ew_coupling_bridge_note` | critical | unaudited |
| 5 | `cycle-0005` | 3 | 833 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 833 | `yt_bridge_moment_closure_note` | critical | unaudited |
| 7 | `cycle-0007` | 3 | 833 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 8 | `cycle-0008` | 4 | 833 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 833 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 833 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 11 | `cycle-0011` | 8 | 833 | `yt_boundary_theorem` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 803 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 13 | `cycle-0013` | 2 | 803 | `source_resolved_exact_green_pocket_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 803 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 794 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 16 | `cycle-0016` | 4 | 794 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 17 | `cycle-0017` | 6 | 794 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 18 | `cycle-0018` | 7 | 794 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 19 | `cycle-0019` | 8 | 794 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 20 | `cycle-0020` | 9 | 794 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 21 | `cycle-0021` | 9 | 794 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 22 | `cycle-0022` | 10 | 794 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 789 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | audited_conditional |
| 24 | `cycle-0024` | 2 | 784 | `pmns_active_four_real_source_from_transport_note` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 780 | `lensing_finite_path_explanation_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
