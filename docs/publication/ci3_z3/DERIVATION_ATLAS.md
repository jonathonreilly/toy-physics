# Derivation Atlas

**Date:** 2026-04-14  
**Purpose:** reusable theorem/subderivation atlas for continuing the framework
without redoing work that already exists.

This is **not** the manuscript claim surface.

Use this file when the question is:

- what tools have already been derived?
- what can we safely reuse in a new lane?
- which note/runner is the current authority for that tool?

For paper claims and release evidence, use:

- [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)

## How to use this atlas

Each row below is a reusable tool, not a manuscript headline. The safe reuse
question is:

1. what does the tool actually prove?
2. what claim level is safe?
3. what future lanes can build on it?

## A. Core framework and observable tools

| Tool / subderivation | Safe statement | Current status | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Framework axiom | `Cl(3)` on `Z^3` is the working physical theory | retained | all lanes | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | n/a |
| Observable principle | `log|det(D+J)|` is the unique additive CPT-even scalar generator on the exact Grassmann Gaussian surface | retained | hierarchy, future scalar observables, effective-action arguments | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py) |
| Single-axiom Hilbert/locality reduction | accepted Hilbert/locality surface can be taken as an internal framework reduction | retained / SI | probability, measurement, interference framing | [SINGLE_AXIOM_HILBERT_NOTE.md](../../SINGLE_AXIOM_HILBERT_NOTE.md), [SINGLE_AXIOM_INFORMATION_NOTE.md](../../SINGLE_AXIOM_INFORMATION_NOTE.md) | [frontier_single_axiom_hilbert.py](../../../scripts/frontier_single_axiom_hilbert.py), [frontier_single_axiom_information.py](../../../scripts/frontier_single_axiom_information.py) |
| Exact `I_3 = 0` | no third-order interference on the accepted Hilbert surface | retained | interference / probability arguments, experimental fingerprints | [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md) | [frontier_born_rule_derived.py](../../../scripts/frontier_born_rule_derived.py) |
| Exact CPT | exact free staggered-lattice CPT | retained | symmetry constraints, matter/antimatter support arguments | [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md) | [frontier_cpt_exact.py](../../../scripts/frontier_cpt_exact.py) |

## B. Spacetime and topology tools

| Tool / subderivation | Safe statement | Current status | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Anomaly-forced time | codimension-1 single-clock closure forces effective `3+1` | retained | chirality, hierarchy blocks, effective spacetime arguments | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md) | [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) |
| Compactification closure | cone-cap family yields `PL S^3` on accepted surface | retained | cosmology, topology, graviton-mass and `\Lambda` companions | [S3_GENERAL_R_DERIVATION_NOTE.md](../../S3_GENERAL_R_DERIVATION_NOTE.md), [S3_CAP_UNIQUENESS_NOTE.md](../../S3_CAP_UNIQUENESS_NOTE.md) | [frontier_s3_boundary_link_theorem.py](../../../scripts/frontier_s3_boundary_link_theorem.py), [frontier_s3_cap_uniqueness.py](../../../scripts/frontier_s3_cap_uniqueness.py), [frontier_s3_general_r.py](../../../scripts/frontier_s3_general_r.py) |

## C. Gauge and matter tools

| Tool / subderivation | Safe statement | Current status | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Native weak algebra | exact cubic `SU(2)` / weak algebra | retained | gauge backbone, matter charge structure | [BOUNDED_NATIVE_GAUGE_NOTE.md](../../BOUNDED_NATIVE_GAUGE_NOTE.md) | [frontier_non_abelian_gauge.py](../../../scripts/frontier_non_abelian_gauge.py) |
| Graph-first selector | canonical cube-shift selector is unique up to graph automorphism | retained | `SU(3)` uniqueness defense, flavor/generation selector work | [GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md](../../GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md), [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| Structural `SU(3)` closure | graph-first commutant closure gives safe structural `SU(3)` statement | retained | color structure, future coupling normalization work | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| Left-handed charge matching | selected-axis surface gives safe `+1/3` / `-1` matching | retained | hypercharge/charge bookkeeping | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| Right-handed completion | anomaly cancellation fixes the one-generation right-handed completion on the SM branch once time/chirality are supplied | retained | one-generation matter closure, anomaly bookkeeping | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | [frontier_right_handed_sector.py](../../../scripts/frontier_right_handed_sector.py) |
| Three-generation orbit algebra | exact `8 = 1 + 1 + 3 + 3` orbit structure | retained | flavor, generation hierarchy, anti-rooting / physical-lattice defense | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | [frontier_generation_fermi_point.py](../../../scripts/frontier_generation_fermi_point.py), [frontier_generation_rooting_undefined.py](../../../scripts/frontier_generation_rooting_undefined.py), [frontier_generation_axiom_boundary.py](../../../scripts/frontier_generation_axiom_boundary.py) |

## D. Gravity tools

| Tool / subderivation | Safe statement | Current status | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Poisson self-consistency | Poisson is the unique local fixed point in the audited weak-field operator family | retained | weak-field gravity, self-consistency framing, manuscript defense | [SELF_CONSISTENCY_FORCES_POISSON_NOTE.md](../../SELF_CONSISTENCY_FORCES_POISSON_NOTE.md), [POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md](../../POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md) | [frontier_self_consistent_field_equation.py](../../../scripts/frontier_self_consistent_field_equation.py), [frontier_poisson_exhaustive_uniqueness.py](../../../scripts/frontier_poisson_exhaustive_uniqueness.py) |
| Newton lattice Green function | lattice Green function yields inverse-square Newton law on `Z^3` | retained | weak-field phenomenology, scaling arguments | [NEWTON_LAW_DERIVED_NOTE.md](../../NEWTON_LAW_DERIVED_NOTE.md) | [frontier_newton_derived.py](../../../scripts/frontier_newton_derived.py) |
| WEP / time-dilation corollaries | derived action yields weak-field WEP and time dilation | retained | weak-field corollaries, comparison with GR | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md), [GRAVITY_CLEAN_DERIVATION_NOTE.md](../../GRAVITY_CLEAN_DERIVATION_NOTE.md) | [frontier_broad_gravity.py](../../../scripts/frontier_broad_gravity.py) |
| Restricted strong-field shell/junction package | exact shell source, bridge, static-constraint lift, and Schur boundary action on the restricted class | retained restricted theorem | strong-field gravity, tensor-completion search | [RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](../../RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md), [OH_STATIC_CONSTRAINT_LIFT_NOTE.md](../../OH_STATIC_CONSTRAINT_LIFT_NOTE.md), [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](../../OH_SCHUR_BOUNDARY_ACTION_NOTE.md), [STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md](../../STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md) | [frontier_oh_static_constraint_lift.py](../../../scripts/frontier_oh_static_constraint_lift.py), [frontier_oh_schur_boundary_action.py](../../../scripts/frontier_oh_schur_boundary_action.py), [frontier_star_supported_bridge_class.py](../../../scripts/frontier_star_supported_bridge_class.py) |
| Scalar-only completion no-go | scalar shell data cannot determine the full `3+1` metric on the current restricted class | bounded but decisive | full-GR attack plan, tensor completion | [SCALAR_TRACE_TENSOR_NO_GO_NOTE.md](../../SCALAR_TRACE_TENSOR_NO_GO_NOTE.md) | [frontier_scalar_trace_tensor_nogo.py](../../../scripts/frontier_scalar_trace_tensor_nogo.py) |
| Minimal tensor gap localization | remaining full-GR gap localizes to a rank-two tensor block plus a universal `K_tensor` / source law | bounded frontier | current gravity frontier | [TENSOR_MATCHING_COMPLETION_THEOREM_NOTE.md](../../TENSOR_MATCHING_COMPLETION_THEOREM_NOTE.md), [TENSOR_BLOCK_CLOSURE_TEST_NOTE.md](../../TENSOR_BLOCK_CLOSURE_TEST_NOTE.md) | [frontier_tensor_matching_completion_theorem.py](../../../scripts/frontier_tensor_matching_completion_theorem.py) |
| Frozen-star null-echo result | naive timing family exists, but evanescent barrier suppresses observable echo amplitude to effectively zero | bounded companion | gravity companion phenomenology, compact-object statements | [GW_ECHO_NULL_RESULT_NOTE.md](../../GW_ECHO_NULL_RESULT_NOTE.md) | [frontier_echo_null_result.py](../../../scripts/frontier_echo_null_result.py) |

## E. Hierarchy and quantitative-bridge tools

| Tool / subderivation | Safe statement | Current status | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Exact hierarchy selector chain | minimal `3+1` block plus APBC orbit structure fixes the hierarchy kernel and selects `L_t = 4` | retained | electroweak sector, bosonic observable arguments | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py) |
| `y_t` vertex power | operator structure gives `n_link = 2` on the current lane | bounded/open | `y_t`, `\alpha_s`, matching/crossover work | [YT_VERTEX_POWER_DERIVATION.md](../../YT_VERTEX_POWER_DERIVATION.md) | [frontier_vertex_power.py](../../../scripts/frontier_vertex_power.py) |
| DM structural ratio | strongest current structural DM ratio result is `R = 5.48` with remaining relic bridge still bounded | bounded/open | DM relic closure, cosmology chain | [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md) | [frontier_dm_relic_paper.py](../../../scripts/frontier_dm_relic_paper.py) |
| CKM mass-basis route | strongest current magnitude package sits on the mass-basis NNI route | bounded/open | CKM closure, flavor coefficient work | [CKM_MASS_BASIS_NNI_NOTE.md](../../CKM_MASS_BASIS_NNI_NOTE.md) | [frontier_ckm_mass_basis_nni.py](../../../scripts/frontier_ckm_mass_basis_nni.py) |

## Atlas rule

Before a subderivation is treated as reusable framework infrastructure:

1. it should have one current authority note
2. it should have one runner or explicit validation path
3. its safe claim boundary should be recorded here

If a tool is only visible inside a longer narrative note and not discoverable
here, future lanes are likely to redo work unnecessarily.
