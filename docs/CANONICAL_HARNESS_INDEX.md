# Canonical Harness Index

**Date:** 2026-04-11  
**Purpose:** current retained runner map

This file is intentionally organized in two layers:

- current default reruns
- whole-repo historical retained entrypoints

That keeps the current program readable without losing the rest of `main`.

For lane status, use:

- [`docs/repo/LANE_STATUS_BOARD.md`](repo/LANE_STATUS_BOARD.md)

For retest workflow, use:

- [`docs/repo/RETEST_PLAYBOOK.md`](repo/RETEST_PLAYBOOK.md)

For lane-by-lane repo organization, use:

- [`docs/lanes/README.md`](lanes/README.md)

## 1. Primary Retained Surface

These are the first runners to trust for the current program:

- [`scripts/frontier_staggered_17card.py`](../scripts/frontier_staggered_17card.py)
- [`scripts/frontier_staggered_full_suite.py`](../scripts/frontier_staggered_full_suite.py)
- [`scripts/frontier_two_sign_parity.py`](../scripts/frontier_two_sign_parity.py)

Primary notes:

- [`docs/STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md)
- [`docs/FULL_TEST_MATRIX_2026-04-10.md`](FULL_TEST_MATRIX_2026-04-10.md)
- [`docs/GRAVITY_SIGN_AUDIT_2026-04-10.md`](GRAVITY_SIGN_AUDIT_2026-04-10.md)

Bounded primary-architecture companions:

- [`scripts/frontier_staggered_newton_reproduction.py`](../scripts/frontier_staggered_newton_reproduction.py)
- [`scripts/frontier_staggered_newton_blocking_sensitivity.py`](../scripts/frontier_staggered_newton_blocking_sensitivity.py)
- [`scripts/frontier_staggered_3d_self_gravity_sign.py`](../scripts/frontier_staggered_3d_self_gravity_sign.py)
- [`scripts/frontier_staggered_test_mass_companion.py`](../scripts/frontier_staggered_test_mass_companion.py)
- [`scripts/frontier_staggered_self_consistent_two_body.py`](../scripts/frontier_staggered_self_consistent_two_body.py)

Companion notes:

- [`docs/STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md`](STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md)
- [`docs/STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md`](STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md)
- [`docs/STAGGERED_3D_SELF_GRAVITY_SIGN_NOTE_2026-04-11.md`](STAGGERED_3D_SELF_GRAVITY_SIGN_NOTE_2026-04-11.md)
- [`docs/STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md`](STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md)
- [`docs/STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md`](STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md)

Reading boundary:

- these are the right reruns when you need the open-cubic trajectory story
  on the primary staggered architecture
- the static-source test-mass companion is a weak-field source-mass lane, not a
  both-masses or self-consistent two-body closure
- the self-consistent two-body companion is force-led, not trajectory-closed
- they are bounded open-cubic companions, not full both-masses closure

## 2. Retained Irregular-Graph Structural Surface

- [`scripts/frontier_staggered_cycle_battery.py`](../scripts/frontier_staggered_cycle_battery.py)
- [`scripts/frontier_staggered_cycle_battery_scaled.py`](../scripts/frontier_staggered_cycle_battery_scaled.py)
- [`scripts/frontier_staggered_self_gravity.py`](../scripts/frontier_staggered_self_gravity.py)
- [`scripts/frontier_staggered_self_gravity_scaling.py`](../scripts/frontier_staggered_self_gravity_scaling.py)
- [`scripts/frontier_self_gravity_entropy.py`](../scripts/frontier_self_gravity_entropy.py)
- [`scripts/frontier_two_field_wave.py`](../scripts/frontier_two_field_wave.py)
- [`scripts/frontier_two_field_retarded_family_closure.py`](../scripts/frontier_two_field_retarded_family_closure.py)
- [`scripts/frontier_staggered_dag.py`](../scripts/frontier_staggered_dag.py)
- [`scripts/frontier_staggered_graph_portable.py`](../scripts/frontier_staggered_graph_portable.py)
- [`scripts/frontier_staggered_geometry_superposition_retained.py`](../scripts/frontier_staggered_geometry_superposition_retained.py)
- [`scripts/frontier_holographic_probe.py`](../scripts/frontier_holographic_probe.py)
- [`scripts/frontier_gravitational_memory.py`](../scripts/frontier_gravitational_memory.py)
- [`scripts/frontier_bmv_entanglement.py`](../scripts/frontier_bmv_entanglement.py)
- [`scripts/frontier_bmv_threebody.py`](../scripts/frontier_bmv_threebody.py)

Key notes:

- [`docs/CYCLE_BATTERY_NOTE_2026-04-10.md`](CYCLE_BATTERY_NOTE_2026-04-10.md)
- [`docs/CYCLE_BATTERY_SCALED_NOTE_2026-04-10.md`](CYCLE_BATTERY_SCALED_NOTE_2026-04-10.md)
- [`docs/SELF_GRAVITY_SCALING_NOTE_2026-04-10.md`](SELF_GRAVITY_SCALING_NOTE_2026-04-10.md)
- [`docs/SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md`](SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md)
- [`docs/TWO_FIELD_RETARDED_FAMILY_CLOSURE_NOTE_2026-04-10.md`](TWO_FIELD_RETARDED_FAMILY_CLOSURE_NOTE_2026-04-10.md)
- [`docs/STAGGERED_DAG_NOTE_2026-04-10.md`](STAGGERED_DAG_NOTE_2026-04-10.md)
- [`docs/STAGGERED_GEOMETRY_SUPERPOSITION_NOTE_2026-04-11.md`](STAGGERED_GEOMETRY_SUPERPOSITION_NOTE_2026-04-11.md)
- [`docs/HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md`](HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md)
- [`docs/GRAVITATIONAL_MEMORY_NOTE_2026-04-11.md`](GRAVITATIONAL_MEMORY_NOTE_2026-04-11.md)
- [`docs/BMV_ENTANGLEMENT_NOTE_2026-04-11.md`](BMV_ENTANGLEMENT_NOTE_2026-04-11.md)
- [`docs/BMV_THREEBODY_NOTE_2026-04-11.md`](BMV_THREEBODY_NOTE_2026-04-11.md)

## 3. Irregular Direction / Portability Surface

These scripts should be run before making any new broad off-lattice
gravity-direction claim. The core-packet gate is the current bounded retained
positive on the audited irregular families; the rest remain the blocker /
portability surfaces around it.

- [`scripts/frontier_irregular_sign_core_packet_gate.py`](../scripts/frontier_irregular_sign_core_packet_gate.py)
- [`scripts/frontier_irregular_directional_observable.py`](../scripts/frontier_irregular_directional_observable.py)
- [`scripts/frontier_two_sign_comparison.py`](../scripts/frontier_two_sign_comparison.py)
- [`scripts/frontier_weak_coupling_retained.py`](../scripts/frontier_weak_coupling_retained.py)
- [`scripts/frontier_anderson_phase_unscreened_periodic.py`](../scripts/frontier_anderson_phase_unscreened_periodic.py)

Key notes:

- [`docs/IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md`](IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md)
- [`docs/IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md`](IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md)
- [`docs/TWO_SIGN_COMPARISON_NOTE_2026-04-10.md`](TWO_SIGN_COMPARISON_NOTE_2026-04-10.md)
- [`docs/WEAK_COUPLING_RETENTION_NOTE_2026-04-11.md`](WEAK_COUPLING_RETENTION_NOTE_2026-04-11.md)
- [`docs/ANDERSON_PHASE_MU2_0001_NOTE_2026-04-11.md`](ANDERSON_PHASE_MU2_0001_NOTE_2026-04-11.md)

## 4. Bounded Side Probes

- [`scripts/frontier_holographic_probe.py`](../scripts/frontier_holographic_probe.py)
- [`scripts/frontier_gravitational_memory.py`](../scripts/frontier_gravitational_memory.py)

## 5. Newton-Family Bounded Companions

- [`scripts/frontier_emergent_product_law.py`](../scripts/frontier_emergent_product_law.py)
- [`scripts/frontier_architecture_portability_sweep.py`](../scripts/frontier_architecture_portability_sweep.py)

Key notes:

- [`docs/EMERGENT_PRODUCT_LAW_NOTE.md`](EMERGENT_PRODUCT_LAW_NOTE.md)
- [`docs/EMERGENT_PRODUCT_LAW_AUDIT_2026-04-11.md`](EMERGENT_PRODUCT_LAW_AUDIT_2026-04-11.md)
- [`docs/ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md`](ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md)
- [`docs/ARCHITECTURE_PORTABILITY_AUDIT_2026-04-11.md`](ARCHITECTURE_PORTABILITY_AUDIT_2026-04-11.md)

Boundaries:

- these are bounded companions, not full Newton closure
- the product-law result is one audited open 3D staggered cross-field surface
- the portability result is source-mass / attraction portability only
- neither closes both-masses + distance-law portability across architectures
- [`scripts/frontier_bmv_entanglement.py`](../scripts/frontier_bmv_entanglement.py)
- [`scripts/frontier_bmv_threebody.py`](../scripts/frontier_bmv_threebody.py)

Key notes:

- [`docs/HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md`](HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md)
- [`docs/GRAVITATIONAL_MEMORY_NOTE_2026-04-11.md`](GRAVITATIONAL_MEMORY_NOTE_2026-04-11.md)
- [`docs/BMV_ENTANGLEMENT_NOTE_2026-04-11.md`](BMV_ENTANGLEMENT_NOTE_2026-04-11.md)
- [`docs/BMV_THREEBODY_NOTE_2026-04-11.md`](BMV_THREEBODY_NOTE_2026-04-11.md)

## 5. Exploratory Reopen Surface

- [`scripts/frontier_emergent_geometry_v2.py`](../scripts/frontier_emergent_geometry_v2.py)
- [`scripts/frontier_emergent_geometry_g_sweep.py`](../scripts/frontier_emergent_geometry_g_sweep.py)
- [`scripts/frontier_emergent_geometry_multisize.py`](../scripts/frontier_emergent_geometry_multisize.py)

Key note:

- [`docs/EMERGENT_GEOMETRY_GROWTH_NOTE_2026-04-10.md`](EMERGENT_GEOMETRY_GROWTH_NOTE_2026-04-10.md)

## 6. Wilson Bounded Calibration Surface

Use these when you need the bounded Wilson weak-field Newton-strengthening
package on `main`:

- [`scripts/frontier_wilson_two_body_open.py`](scripts/frontier_wilson_two_body_open.py)
- [`scripts/frontier_wilson_mu2_distance_sweep.py`](scripts/frontier_wilson_mu2_distance_sweep.py)
- [`scripts/frontier_wilson_two_body_laws.py`](scripts/frontier_wilson_two_body_laws.py)
- [`scripts/frontier_newton_systematic.py`](scripts/frontier_newton_systematic.py)
- [`scripts/frontier_test_mass_limit.py`](scripts/frontier_test_mass_limit.py)
- [`scripts/frontier_perturbative_mass_law.py`](scripts/frontier_perturbative_mass_law.py)
- [`scripts/frontier_continuum_limit.py`](scripts/frontier_continuum_limit.py)

Key notes:

- [`docs/WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md`](WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md)
- [`docs/WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md`](WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md)
- [`docs/WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md`](WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md)
- [`docs/WILSON_NORMALIZATION_RECONCILIATION_NOTE_2026-04-11.md`](WILSON_NORMALIZATION_RECONCILIATION_NOTE_2026-04-11.md)

Reading boundary:

- this is a bounded Wilson companion surface, not full Newton closure
- use it for same-convention open-Wilson calibration only
- do not read it as both-masses closure or architecture-wide closure

## 6B. 3D Path-Sum Distance Continuation

Use this when you need the bounded 64^3 path-sum continuation of the distance
story:

- [`scripts/distance_law_3d_64_closure.py`](../scripts/distance_law_3d_64_closure.py)

Key note:

- [`docs/DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md`](DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md)

Reading boundary:

- this is a bounded path-sum continuation, not full Newton closure
- use it for the 64^3 distance-story extrapolation only
- do not read it as both-masses closure or architecture-wide closure

## 7. Historical / Legacy Entrypoints

Use these when you are intentionally revisiting older lanes on `main`:

- mirror / exact geometry:
  - [`docs/UNIFIED_PROGRAM_NOTE.md`](UNIFIED_PROGRAM_NOTE.md)
  - [`scripts/mirror_2d_validation.py`](../scripts/mirror_2d_validation.py)
- ordered lattice / dense spent-delay:
  - [`docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md`](LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md)
  - [`scripts/lattice_3d_dense_10prop.py`](../scripts/lattice_3d_dense_10prop.py)
  - [`scripts/lattice_3d_dense_window_extension.py`](../scripts/lattice_3d_dense_window_extension.py)
- nearest-neighbor refinement:
  - [`docs/CONTINUUM_BRIDGE_NOTE.md`](CONTINUUM_BRIDGE_NOTE.md)
  - [`scripts/lattice_nn_continuum.py`](../scripts/lattice_nn_continuum.py)
  - [`scripts/lattice_nn_deterministic_rescale.py`](../scripts/lattice_nn_deterministic_rescale.py)
- structured chokepoint / generated-symmetry bridge:
  - [`docs/STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md`](STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md)
  - [`scripts/structured_chokepoint_bridge.py`](../scripts/structured_chokepoint_bridge.py)
  - [`scripts/structured_chokepoint_bridge_extension.py`](../scripts/structured_chokepoint_bridge_extension.py)
- ordered lattice / action-power / valley-linear:
  - [`docs/ACTION_ARCHITECTURE_MATRIX_NOTE.md`](ACTION_ARCHITECTURE_MATRIX_NOTE.md)
  - [`scripts/frontier_3plus1d_closure_card.py`](../scripts/frontier_3plus1d_closure_card.py)
- dimension-dependent kernel:
  - [`docs/DIMENSIONAL_GRAVITY_TABLE.md`](DIMENSIONAL_GRAVITY_TABLE.md)
  - [`scripts/frontier_dimension_dependent_kernel.py`](../scripts/frontier_dimension_dependent_kernel.py)
- coin / chiral lane:
  - [`docs/CHIRAL_WALK_SYNTHESIS_2026-04-09.md`](CHIRAL_WALK_SYNTHESIS_2026-04-09.md)
  - [`scripts/frontier_chiral_bottleneck_card.py`](../scripts/frontier_chiral_bottleneck_card.py)
- generated geometry / Gate B:
  - [`docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](GATE_B_GROWN_JOINT_PACKAGE_NOTE.md)
  - [`scripts/gate_b_grown_joint_package.py`](../scripts/gate_b_grown_joint_package.py)
- moonshots / horizon:
  - [`docs/NATURE_BACKLOG_2026-04-10.md`](NATURE_BACKLOG_2026-04-10.md)
  - [`scripts/frontier_emergent_schwarzschild.py`](../scripts/frontier_emergent_schwarzschild.py)

## 8. Bounded Frontier Probes (promoted 2026-04-12)

All claims below are bounded to the tested operator families and graph
surfaces. None restates full Newton closure, unconditional spatial-metric
derivation, or global Poisson uniqueness.

### Distance law / field equation family

- [`scripts/frontier_distance_law_definitive.py`](../scripts/frontier_distance_law_definitive.py)
- [`docs/DISTANCE_LAW_DEFINITIVE_NOTE.md`](DISTANCE_LAW_DEFINITIVE_NOTE.md)
- [`scripts/frontier_self_consistent_field_equation.py`](../scripts/frontier_self_consistent_field_equation.py)
- [`docs/SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`](SELF_CONSISTENCY_FORCES_POISSON_NOTE.md)
- [`scripts/frontier_poisson_exhaustive_uniqueness.py`](../scripts/frontier_poisson_exhaustive_uniqueness.py)
- [`docs/POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md`](POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md)

### Normalization and axiom reduction

- [`scripts/frontier_action_normalization.py`](../scripts/frontier_action_normalization.py)
- [`docs/ACTION_NORMALIZATION_NOTE.md`](ACTION_NORMALIZATION_NOTE.md)
- [`docs/AXIOM_REDUCTION_NOTE.md`](AXIOM_REDUCTION_NOTE.md)

### Born rule / nonlinearity / entanglement probes

- [`scripts/frontier_nonlinear_born_gravity.py`](../scripts/frontier_nonlinear_born_gravity.py)
- [`docs/NONLINEAR_BORN_GRAVITY_NOTE.md`](NONLINEAR_BORN_GRAVITY_NOTE.md)
- [`scripts/frontier_gravitational_entanglement.py`](../scripts/frontier_gravitational_entanglement.py)
- [`docs/GRAVITATIONAL_ENTANGLEMENT_NOTE.md`](GRAVITATIONAL_ENTANGLEMENT_NOTE.md)

### Wave equation / gravitational wave probes

- [`scripts/frontier_wave_equation_gravity.py`](../scripts/frontier_wave_equation_gravity.py)
- [`docs/WAVE_EQUATION_GRAVITY_NOTE.md`](WAVE_EQUATION_GRAVITY_NOTE.md)
- [`scripts/frontier_grav_wave_post_newtonian.py`](../scripts/frontier_grav_wave_post_newtonian.py)
- [`docs/GRAVITATIONAL_WAVE_PROBE_NOTE.md`](GRAVITATIONAL_WAVE_PROBE_NOTE.md)

### Differentiation and coexistence

- [`scripts/frontier_beyond_lattice_qcd.py`](../scripts/frontier_beyond_lattice_qcd.py)
- [`docs/BEYOND_LATTICE_QCD_NOTE.md`](BEYOND_LATTICE_QCD_NOTE.md)
- [`scripts/em_gravity_coexistence_2x2.py`](../scripts/em_gravity_coexistence_2x2.py)
- [`docs/EM_GRAVITY_COEXISTENCE_2X2_NOTE.md`](EM_GRAVITY_COEXISTENCE_2X2_NOTE.md)

### Bounded CI(3) / `Z^3` graph-first gauge surface

- [`scripts/frontier_non_abelian_gauge.py`](../scripts/frontier_non_abelian_gauge.py)
- [`scripts/frontier_graph_first_selector_derivation.py`](../scripts/frontier_graph_first_selector_derivation.py)
- [`scripts/frontier_graph_first_su3_integration.py`](../scripts/frontier_graph_first_su3_integration.py)
- [`docs/BOUNDED_NATIVE_GAUGE_NOTE.md`](BOUNDED_NATIVE_GAUGE_NOTE.md)
- [`docs/GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)
- [`docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)

### Dimension selection / bound states

- [`scripts/frontier_dimension_selection.py`](../scripts/frontier_dimension_selection.py)
- [`docs/DIMENSION_SELECTION_NOTE.md`](DIMENSION_SELECTION_NOTE.md)
- [`scripts/frontier_bound_state_selection.py`](../scripts/frontier_bound_state_selection.py)
- [`docs/BOUND_STATE_SELECTION_NOTE.md`](BOUND_STATE_SELECTION_NOTE.md)

### Background independence / tensor network

- [`scripts/frontier_background_independence.py`](../scripts/frontier_background_independence.py)
- [`docs/BACKGROUND_INDEPENDENCE_NOTE.md`](BACKGROUND_INDEPENDENCE_NOTE.md)
- [`scripts/frontier_tensor_network_connection.py`](../scripts/frontier_tensor_network_connection.py)
- [`docs/TENSOR_NETWORK_CONNECTION_NOTE.md`](TENSOR_NETWORK_CONNECTION_NOTE.md)

Reading boundary:

- these are bounded frontier probes, not full derivations
- distance law result is bounded to ordered-cubic/Dirichlet surface
- Poisson uniqueness is a 21-operator family audit, not a global theorem
- the bounded native gauge package now retains:
  - exact native cubic `Cl(3)` / `SU(2)`
  - a derived graph-first weak-axis selector
  - structural graph-first `su(3)` closure
- the abelian factor remains bounded as hypercharge-like / left-handed matched
- downstream CI(3) phenomenology is still not retained from this package alone
- dimension selection is bounded to the tested operator family
- bound state result is bounded to tested potentials at d<=3
- all wave/entanglement probes are bounded to the audited graph surfaces

## Reading Rule

If a claim is not represented in:

- a runner,
- a retained note,
- and the lane board,

then it is not yet organized enough to treat as stable repo state.
