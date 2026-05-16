# Audit Queue

**Total pending:** 1181
**Ready (all deps already at retained-grade or metadata tiers):** 4

By criticality:
- `critical`: 735
- `high`: 34
- `medium`: 152
- `leaf`: 260

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `koide_q_readout_factorization_theorem_2026-04-22` | bounded_theorem | unaudited | critical | 775 | 11.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 2 | `generation_axiom_boundary_note` | bounded_theorem | unaudited | critical | 775 | 11.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 3 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 917 | 14.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 4 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 916 | 13.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 5 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 916 | 13.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 6 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | open_gate | unaudited | critical | 916 | 10.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_bridge_3plus1_native_tube_staging.py` |
| 7 | `su3_cube_index_graph_shortcut_open_gate_note_2026-05-03` | open_gate | unaudited | critical | 916 | 10.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py` |
| 8 | `su3_cube_perron_solve_combined_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 916 | 10.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_perron_solve.py` |
| 9 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 907 | 13.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 10 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 907 | 12.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 11 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 906 | 28.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 12 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 860 | 13.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 13 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 859 | 37.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 14 | `yt_vertex_power_derivation` | open_gate | unaudited | critical | 854 | 11.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_vertex_power.py` |
| 15 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 853 | 34.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 16 | `yt_color_projection_correction_note` | positive_theorem | unaudited | critical | 831 | 14.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 17 | `yt_qfp_insensitivity_support_note` | bounded_theorem | unaudited | critical | 830 | 17.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 18 | `yt_exact_schur_normal_form_uniqueness_note` | bounded_theorem | unaudited | critical | 830 | 16.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_schur_normal_form_uniqueness.py` |
| 19 | `yt_boundary_theorem` | open_gate | unaudited | critical | 830 | 16.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_boundary_consistency.py` |
| 20 | `yt_constructive_uv_bridge_note` | bounded_theorem | unaudited | critical | 830 | 16.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_constructive_uv_bridge.py` |
| 21 | `yt_interacting_bridge_locality_note` | bounded_theorem | unaudited | critical | 830 | 15.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_interacting_bridge_locality.py` |
| 22 | `yt_bridge_hessian_selector_note` | bounded_theorem | unaudited | critical | 830 | 14.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_hessian_selector.py` |
| 23 | `yt_bridge_rearrangement_principle_note` | bounded_theorem | unaudited | critical | 830 | 13.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_rearrangement_principle.py` |
| 24 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 830 | 13.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 25 | `yt_bridge_higher_order_corrections_note` | bounded_theorem | unaudited | critical | 830 | 13.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_higher_order_corrections.py` |
| 26 | `yt_bridge_nonlocal_corrections_note` | bounded_theorem | unaudited | critical | 830 | 13.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_nonlocal_corrections.py` |
| 27 | `yt_bridge_action_invariant_note` | bounded_theorem | unaudited | critical | 830 | 12.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_action_invariant.py` |
| 28 | `yt_bridge_moment_closure_note` | bounded_theorem | unaudited | critical | 830 | 12.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_moment_closure.py` |
| 29 | `yt_bridge_operator_closure_note` | bounded_theorem | unaudited | critical | 830 | 12.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_operator_closure.py` |
| 30 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 830 | 12.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 31 | `yt_exact_coarse_grained_bridge_operator_note` | bounded_theorem | unaudited | critical | 830 | 11.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_coarse_grained_bridge_operator.py` |
| 32 | `yt_exact_interacting_bridge_transport_note` | bounded_theorem | unaudited | critical | 830 | 11.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_interacting_bridge_transport.py` |
| 33 | `yt_bridge_endpoint_shift_bound_note` | bounded_theorem | unaudited | critical | 830 | 11.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_endpoint_shift_bound.py` |
| 34 | `yt_bridge_uv_class_uniqueness_note` | bounded_theorem | unaudited | critical | 830 | 11.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_uv_class_uniqueness.py` |
| 35 | `yt_ew_coupling_bridge_note` | positive_theorem | unaudited | critical | 830 | 11.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ew_coupling_derivation.py` |
| 36 | `yt_eft_bridge_theorem` | open_gate | unaudited | critical | 830 | 10.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_eft_bridge.py` |
| 37 | `gate_b_grown_joint_package_note` | bounded_theorem | unaudited | critical | 823 | 13.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_grown_joint_package.py` |
| 38 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 808 | 46.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 39 | `gate_b_weak_connectivity_note` | bounded_theorem | unaudited | critical | 807 | 12.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_weak_connectivity_harness.py` |
| 40 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 803 | 30.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 41 | `g_bare_rigidity_theorem_note` | positive_theorem | unaudited | critical | 803 | 13.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 42 | `gate_b_nonlabel_connectivity_v1_note` | bounded_theorem | unaudited | critical | 803 | 13.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1.py` |
| 43 | `g_bare_structural_normalization_theorem_note_2026-04-18` | positive_theorem | unaudited | critical | 802 | 18.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_structural_normalization.py` |
| 44 | `source_resolved_exact_green_pocket_note` | bounded_theorem | unaudited | critical | 800 | 12.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_exact_green_pocket.py` |
| 45 | `source_resolved_exact_green_scaling_note` | bounded_theorem | unaudited | critical | 800 | 11.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_exact_green_scaling.py` |
| 46 | `source_resolved_propagating_green_pocket_note` | positive_theorem | unaudited | critical | 800 | 11.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_propagating_green_pocket.py` |
| 47 | `source_resolved_exact_green_h025_pocket_note` | bounded_theorem | unaudited | critical | 800 | 10.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_exact_green_h025_pocket.py` |
| 48 | `gate_b_nonlabel_connectivity_v1_distance_note` | bounded_theorem | unaudited | critical | 796 | 10.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1_distance.py` |
| 49 | `gate_b_nonlabel_connectivity_v1_joint_note` | bounded_theorem | unaudited | critical | 796 | 10.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1_joint.py` |
| 50 | `minimal_absorbing_horizon_probe_note` | bounded_theorem | unaudited | critical | 795 | 11.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/minimal_absorbing_horizon_probe.py` |

## Citation cycle break targets

243 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 3 | 916 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 2 | `cycle-0002` | 4 | 916 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 3 | `cycle-0003` | 5 | 916 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 4 | `cycle-0004` | 6 | 916 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 830 | `yt_bridge_action_invariant_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 830 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 830 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 830 | `yt_ew_coupling_bridge_note` | critical | unaudited |
| 9 | `cycle-0009` | 3 | 830 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 830 | `yt_bridge_moment_closure_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 830 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 12 | `cycle-0012` | 4 | 830 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 13 | `cycle-0013` | 4 | 830 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 14 | `cycle-0014` | 4 | 830 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 15 | `cycle-0015` | 8 | 830 | `yt_boundary_theorem` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 800 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 800 | `source_resolved_exact_green_pocket_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 800 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 791 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 791 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 21 | `cycle-0021` | 6 | 791 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 22 | `cycle-0022` | 7 | 791 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 23 | `cycle-0023` | 8 | 791 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 24 | `cycle-0024` | 9 | 791 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 25 | `cycle-0025` | 9 | 791 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
