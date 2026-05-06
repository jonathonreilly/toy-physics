# Audit Queue

**Total pending:** 870
**Ready (all deps already at retained-grade or metadata tiers):** 52

By criticality:
- `critical`: 559
- `high`: 17
- `medium`: 96
- `leaf`: 198

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `staggered_dirac_realization_gate_note_2026-05-03` | open_gate | unaudited | critical | 598 | 25.73 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 2 | `su3_wigner_intertwiner_block1_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 558 | 13.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_intertwiner_engine.py` |
| 3 | `g_bare_constraint_vs_convention_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 557 | 9.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 4 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 546 | 11.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 5 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | unaudited | critical | 546 | 11.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 6 | `gate_b_farfield_note` | bounded_theorem | unaudited | critical | 540 | 16.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_farfield_harness.py` |
| 7 | `universal_qg_canonical_textbook_geometric_action_equivalence_note` | positive_theorem | unaudited | critical | 516 | 14.51 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 8 | `third_grown_family_sign_note` | bounded_theorem | unaudited | critical | 511 | 14.50 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/THIRD_GROWN_FAMILY_SIGN_SWEEP.py` |
| 9 | `alt_connectivity_family_basin_note` | bounded_theorem | unaudited | critical | 511 | 14.00 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/ALT_CONNECTIVITY_FAMILY_BASIN.py` |
| 10 | `universal_qg_smooth_gravitational_global_atlas_note` | positive_theorem | unaudited | critical | 511 | 13.50 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 11 | `dispersion_relation_note` | positive_theorem | unaudited | critical | 505 | 9.98 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_dispersion_relation.py` |
| 12 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 502 | 12.97 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 13 | `self_consistency_forces_poisson_note` | bounded_theorem | unaudited | critical | 500 | 13.47 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_self_consistent_field_equation.py` |
| 14 | `action_normalization_note` | bounded_theorem | unaudited | critical | 500 | 10.97 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_action_normalization.py` |
| 15 | `pmns_oriented_cycle_channel_value_law_note` | positive_theorem | unaudited | critical | 295 | 12.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_oriented_cycle_channel_value_law.py` |
| 16 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 294 | 11.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 17 | `wave_retardation_lab_prediction_note` | positive_theorem | unaudited | critical | 293 | 12.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_retardation_velocity_sweep.py` |
| 18 | `quark_route2_exact_readout_map_note_2026-04-19` | positive_theorem | unaudited | critical | 291 | 15.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_route2_exact_readout_map.py` |
| 19 | `pmns_uniform_scalar_deformation_boundary_note` | positive_theorem | unaudited | critical | 291 | 11.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_uniform_scalar_deformation_boundary.py` |
| 20 | `tensor_support_center_excess_law_note` | bounded_theorem | unaudited | critical | 291 | 9.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_tensor_support_center_excess_law.py` |
| 21 | `koide_q_onsite_source_domain_no_go_synthesis_note_2026-04-25` | no_go | unaudited | critical | 290 | 14.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py` |
| 22 | `dm_neutrino_cascade_geometry_note_2026-04-14` | positive_theorem | unaudited | critical | 289 | 10.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_cascade_geometry.py` |
| 23 | `hierarchy_spatial_bc_and_u0_scaling_note` | bounded_theorem | unaudited | critical | 289 | 10.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_spatial_bc_and_u0_scaling.py` |
| 24 | `dm_selector_first_shoulder_exit_threshold_support_note_2026-04-21` | open_gate | unaudited | critical | 289 | 9.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_selector_first_shoulder_exit_threshold_support_2026_04_21.py` |
| 25 | `koide_cyclic_wilson_descendant_law_note_2026-04-18` | positive_theorem | unaudited | critical | 288 | 10.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_cyclic_wilson_descendant_law.py` |
| 26 | `hierarchy_matsubara_decomposition_note` | positive_theorem | unaudited | critical | 288 | 10.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_matsubara_decomposition.py` |
| 27 | `dm_neutrino_odd_circulant_z2_slot_theorem_note_2026-04-15` | positive_theorem | unaudited | critical | 288 | 9.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_odd_circulant_z2_slot_theorem.py` |
| 28 | `dm_neutrino_z3_character_transfer_theorem_note_2026-04-15` | positive_theorem | unaudited | critical | 288 | 9.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_z3_character_transfer_theorem.py` |
| 29 | `dm_neutrino_z3_circulant_mass_basis_no_go_note_2026-04-15` | no_go | unaudited | critical | 288 | 9.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_z3_circulant_mass_basis_nogo.py` |
| 30 | `koide_z3_scalar_potential_lepton_mass_tower_note_2026-04-19` | positive_theorem | unaudited | critical | 288 | 9.68 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `koide_a1_radian_bridge_irreducibility_audit_note_2026-04-24` | no_go | unaudited | critical | 287 | 16.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_radian_bridge_irreducibility_audit.py` |
| 32 | `dm_wilson_direct_descendant_schur_feshbach_boundary_variational_theorem_note_2026-04-25` | open_gate | unaudited | critical | 287 | 13.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_wilson_direct_descendant_schur_feshbach_boundary_variational.py` |
| 33 | `koide_berry_bundle_obstruction_theorem_note_2026-04-19` | positive_theorem | unaudited | critical | 287 | 9.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_berry_bundle_obstruction_theorem.py` |
| 34 | `pmns_transfer_operator_dominant_mode_note` | positive_theorem | unaudited | critical | 287 | 9.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_transfer_operator_dominant_mode.py` |
| 35 | `su3_wigner_intertwiner_block2_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 557 | 13.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_4fold_haar_projector.py` |
| 36 | `su3_wigner_intertwiner_block3_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 556 | 9.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_geometry.py` |
| 37 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 555 | 10.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 38 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 551 | 12.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 39 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 546 | 11.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 40 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 546 | 11.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 41 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 546 | 11.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 42 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 546 | 11.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 43 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 518 | 17.52 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 518 | 15.52 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 514 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 513 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 512 | 14.00 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 512 | 10.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 49 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 511 | 13.50 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 511 | 13.50 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

192 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 518 | `universal_qg_projective_schur_closure_note` | critical | audited_conditional |
| 2 | `cycle-0002` | 3 | 518 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 510 | `yt_explicit_systematic_budget_note` | critical | audited_conditional |
| 4 | `cycle-0004` | 3 | 507 | `signed_gravity_native_boundary_complex_containment_note` | critical | unaudited |
| 5 | `cycle-0005` | 6 | 507 | `signed_gravity_cl3z3_source_character_derivation_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 499 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 499 | `broad_gravity_derivation_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 499 | `gravity_clean_derivation_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 499 | `gravity_clean_derivation_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 499 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 499 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 499 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 499 | `signed_gravity_aps_locked_axiom_extension_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 499 | `signed_gravity_aps_boundary_index_chi_probe_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 499 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 499 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 499 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 499 | `signed_gravity_aps_locked_source_action_proposal_note` | critical | unaudited |
| 19 | `cycle-0019` | 4 | 499 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 499 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 21 | `cycle-0021` | 4 | 499 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 499 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 499 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 499 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 499 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
