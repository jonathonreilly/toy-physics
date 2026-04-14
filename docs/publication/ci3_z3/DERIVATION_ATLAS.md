# Derivation Atlas

**Date:** 2026-04-14  
**Purpose:** canonical toolbox of reusable derivations and closed subderivations
on the current `main` branch.

**Last retained-claim coverage audit:** 2026-04-14 against
[CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
**Last import-discipline audit:** 2026-04-14, inline in this file

This file is **not** the manuscript claim surface.

Use this file when the question is:

- what has already been derived that we can reuse?
- what is the safe claim boundary of that subderivation?
- which note/runner is the canonical authority on `main`?

For paper claims and release evidence, use:

- [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)

## Canonicalization rule

This atlas is the canonical derivation stack.

If multiple route notes exist for the same result:

1. this atlas chooses one current authority surface on `main`
2. retained/publication docs should point to that canonical surface
3. older route variants belong in work history or route-history notes, not as
   competing authorities

## How to use this atlas

Each row below is a reusable tool or closed subderivation, not a manuscript
headline. The safe reuse question is:

1. what does the tool actually prove?
2. what claim level is safe?
3. what future lanes can build on it?
4. what import class applies?

The `Status / import class` field is part of the toolbox contract. If a row is
not marked `zero-input structural` or `axiom-dependent support`, do not reuse
it as a pure internal theorem without carrying its bridge/import conditions
forward explicitly.

## A. Core framework and observable tools

| Tool / subderivation | Safe statement | Status / import class | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Framework axiom | `Cl(3)` on `Z^3` is the working physical theory | retained; framework axiom | all lanes | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | n/a |
| Observable principle | `log|det(D+J)|` is the unique additive CPT-even scalar generator on the exact Grassmann Gaussian surface | retained; zero-input structural | hierarchy, future scalar observables, effective-action arguments | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py) |
| Single-axiom Hilbert/locality reduction | accepted Hilbert/locality surface can be taken as an internal framework reduction | retained / SI; zero-input structural | probability, measurement, interference framing | [SINGLE_AXIOM_HILBERT_NOTE.md](../../SINGLE_AXIOM_HILBERT_NOTE.md), [SINGLE_AXIOM_INFORMATION_NOTE.md](../../SINGLE_AXIOM_INFORMATION_NOTE.md) | [frontier_single_axiom_hilbert.py](../../../scripts/frontier_single_axiom_hilbert.py), [frontier_single_axiom_information.py](../../../scripts/frontier_single_axiom_information.py) |
| Exact `I_3 = 0` | no third-order interference on the accepted Hilbert surface | retained; zero-input structural | interference / probability arguments, experimental fingerprints | [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md) | [frontier_born_rule_derived.py](../../../scripts/frontier_born_rule_derived.py) |
| Exact CPT | exact free staggered-lattice CPT | retained; zero-input structural | symmetry constraints, matter/antimatter support arguments | [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md) | [frontier_cpt_exact.py](../../../scripts/frontier_cpt_exact.py) |

## B. Spacetime and topology tools

| Tool / subderivation | Safe statement | Status / import class | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Anomaly-forced time | codimension-1 single-clock closure forces effective `3+1` | retained; zero-input structural | chirality, hierarchy blocks, effective spacetime arguments | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md) | [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) |
| Generation axiom boundary | the physical-lattice axiom is the exact boundary that turns the triplet sectors into physical species structure rather than removable taste artifacts | retained support; axiom-dependent support | three-generation defense, anti-rooting arguments, flavor-lane reuse | [GENERATION_AXIOM_BOUNDARY_NOTE.md](../../GENERATION_AXIOM_BOUNDARY_NOTE.md) | [frontier_generation_axiom_boundary.py](../../../scripts/frontier_generation_axiom_boundary.py) |
| `S^3` boundary-link theorem | the accepted compactification surface is anchored by the boundary-link closure from the lattice/topological side | retained support; zero-input structural | `S^3` compactification chain, topology defenses, cosmology companions | [S3_BOUNDARY_LINK_THEOREM_NOTE.md](../../S3_BOUNDARY_LINK_THEOREM_NOTE.md) | [frontier_s3_boundary_link_theorem.py](../../../scripts/frontier_s3_boundary_link_theorem.py) |
| `S^3` cap uniqueness | the cone-cap closure is unique on the accepted surface | retained support; zero-input structural | compactification uniqueness, topology defenses | [S3_CAP_UNIQUENESS_NOTE.md](../../S3_CAP_UNIQUENESS_NOTE.md) | [frontier_s3_cap_uniqueness.py](../../../scripts/frontier_s3_cap_uniqueness.py) |
| `S^3` general-`R` extension | compact cone-cap family extends to the accepted `PL S^3` family | retained support; zero-input structural | cosmology, graviton-mass and `\Lambda` companions | [S3_GENERAL_R_DERIVATION_NOTE.md](../../S3_GENERAL_R_DERIVATION_NOTE.md) | [frontier_s3_general_r.py](../../../scripts/frontier_s3_general_r.py) |

## C. Gauge and matter tools

| Tool / subderivation | Safe statement | Status / import class | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Native weak algebra | exact cubic `SU(2)` / weak algebra | retained; zero-input structural | gauge backbone, matter charge structure | [BOUNDED_NATIVE_GAUGE_NOTE.md](../../BOUNDED_NATIVE_GAUGE_NOTE.md) | [frontier_non_abelian_gauge.py](../../../scripts/frontier_non_abelian_gauge.py) |
| Graph-first selector | canonical cube-shift selector is unique up to graph automorphism | retained; zero-input structural | `SU(3)` uniqueness defense, selector work, reviewer-facing framing | [GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md](../../GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md) | [frontier_graph_first_selector_derivation.py](../../../scripts/frontier_graph_first_selector_derivation.py) |
| Structural `SU(3)` closure | graph-first commutant closure gives safe structural `SU(3)` statement | retained; zero-input structural | color structure, future coupling normalization work | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| Left-handed charge matching | selected-axis surface gives safe `+1/3` / `-1` matching | retained; zero-input structural | hypercharge/charge bookkeeping | [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](../../LEFT_HANDED_CHARGE_MATCHING_NOTE.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| One-generation matter closure | anomaly cancellation fixes the one-generation right-handed completion on the SM branch once time/chirality are supplied | retained; zero-input structural | one-generation matter closure, anomaly bookkeeping | [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](../../ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | [frontier_right_handed_sector.py](../../../scripts/frontier_right_handed_sector.py), [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) |
| Three-generation matter structure | exact `8 = 1 + 1 + 3 + 3` orbit structure survives as physical species structure on the framework surface | retained; axiom-dependent support | flavor, generation hierarchy, anti-rooting / physical-lattice defense | [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md) | [frontier_generation_fermi_point.py](../../../scripts/frontier_generation_fermi_point.py), [frontier_generation_rooting_undefined.py](../../../scripts/frontier_generation_rooting_undefined.py), [frontier_generation_axiom_boundary.py](../../../scripts/frontier_generation_axiom_boundary.py) |

## D. Gravity tools

| Tool / subderivation | Safe statement | Status / import class | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Poisson self-consistency | Poisson is the unique local fixed point in the audited weak-field operator family | retained; zero-input structural | weak-field gravity, self-consistency framing, manuscript defense | [SELF_CONSISTENCY_FORCES_POISSON_NOTE.md](../../SELF_CONSISTENCY_FORCES_POISSON_NOTE.md), [POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md](../../POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md) | [frontier_self_consistent_field_equation.py](../../../scripts/frontier_self_consistent_field_equation.py), [frontier_poisson_exhaustive_uniqueness.py](../../../scripts/frontier_poisson_exhaustive_uniqueness.py) |
| Newton lattice Green function | lattice Green function yields inverse-square Newton law on `Z^3` | retained; zero-input structural | weak-field phenomenology, scaling arguments | [NEWTON_LAW_DERIVED_NOTE.md](../../NEWTON_LAW_DERIVED_NOTE.md) | [frontier_newton_derived.py](../../../scripts/frontier_newton_derived.py) |
| WEP / time-dilation corollaries | derived action yields weak-field WEP and time dilation | retained; zero-input structural | weak-field corollaries, comparison with GR | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md), [GRAVITY_CLEAN_DERIVATION_NOTE.md](../../GRAVITY_CLEAN_DERIVATION_NOTE.md) | [frontier_broad_gravity.py](../../../scripts/frontier_broad_gravity.py) |
| Restricted strong-field closure synthesis | the accepted strong-field theorem closes exactly on the star-supported finite-rank class under the static conformal bridge, using the shell class, static-constraint lift, and Schur action as one canonical stack | retained restricted theorem; zero-input structural | strong-field gravity, theorem-level reviewer framing, later tensor-frontier work | [RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](../../RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md), [STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md](../../STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md), [OH_STATIC_CONSTRAINT_LIFT_NOTE.md](../../OH_STATIC_CONSTRAINT_LIFT_NOTE.md), [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](../../OH_SCHUR_BOUNDARY_ACTION_NOTE.md) | [frontier_star_supported_bridge_class.py](../../../scripts/frontier_star_supported_bridge_class.py), [frontier_oh_static_constraint_lift.py](../../../scripts/frontier_oh_static_constraint_lift.py), [frontier_oh_schur_boundary_action.py](../../../scripts/frontier_oh_schur_boundary_action.py) |
| Restricted bridge-class theorem | exact strong-field source class on the accepted star-supported finite-rank surface | retained restricted support; zero-input structural | strong-field gravity, restricted-class generalization work | [STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md](../../STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md) | [frontier_star_supported_bridge_class.py](../../../scripts/frontier_star_supported_bridge_class.py) |
| Restricted static-constraint lift | exact shell-to-`3+1` static conformal lift on the accepted restricted class | retained restricted support; zero-input structural | strong-field gravity, shell-to-spacetime lift work | [OH_STATIC_CONSTRAINT_LIFT_NOTE.md](../../OH_STATIC_CONSTRAINT_LIFT_NOTE.md) | [frontier_oh_static_constraint_lift.py](../../../scripts/frontier_oh_static_constraint_lift.py) |
| Restricted Schur boundary action | microscopic boundary action reproduces the exact shell trace law on the accepted restricted class | retained restricted support; zero-input structural | strong-field gravity, boundary-action arguments | [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](../../OH_SCHUR_BOUNDARY_ACTION_NOTE.md) | [frontier_oh_schur_boundary_action.py](../../../scripts/frontier_oh_schur_boundary_action.py) |
| Scalar-only completion no-go | scalar shell data cannot determine the full `3+1` metric on the current restricted class | bounded but decisive; zero-input structural | full-GR attack plan, tensor completion | [SCALAR_TRACE_TENSOR_NO_GO_NOTE.md](../../SCALAR_TRACE_TENSOR_NO_GO_NOTE.md) | [frontier_scalar_trace_tensor_nogo.py](../../../scripts/frontier_scalar_trace_tensor_nogo.py) |
| Tensor source map `eta` | the remaining non-scalar source response on the restricted class is a rank-two tensor map into shift-like and traceless-shear channels | bounded frontier; zero-input structural | full-GR tensor matching, source/channel closure | [TENSOR_SOURCE_MAP_ETA_NOTE.md](../../TENSOR_SOURCE_MAP_ETA_NOTE.md) | [frontier_tensor_source_map_eta.py](../../../scripts/frontier_tensor_source_map_eta.py) |
| Tensor block closure test | the minimal rank-two tensor block is locally sufficient on each audited family but not yet universal across them | bounded frontier; zero-input structural | full-GR kernel search, family-universality tests | [TENSOR_BLOCK_CLOSURE_TEST_NOTE.md](../../TENSOR_BLOCK_CLOSURE_TEST_NOTE.md) | [frontier_tensor_block_closure_test.py](../../../scripts/frontier_tensor_block_closure_test.py) |
| Minimal tensor gap localization | remaining full-GR gap localizes to a rank-two tensor block plus a universal `K_tensor` / source law | bounded frontier; zero-input structural | current gravity frontier | [TENSOR_MATCHING_COMPLETION_THEOREM_NOTE.md](../../TENSOR_MATCHING_COMPLETION_THEOREM_NOTE.md) | [frontier_tensor_matching_completion_theorem.py](../../../scripts/frontier_tensor_matching_completion_theorem.py) |
| Frozen-star null-echo result | naive timing family exists, but evanescent barrier suppresses observable echo amplitude to effectively zero | bounded companion; companion-only phenomenology | gravity companion phenomenology, compact-object statements | [GW_ECHO_NULL_RESULT_NOTE.md](../../GW_ECHO_NULL_RESULT_NOTE.md) | [frontier_echo_null_result.py](../../../scripts/frontier_echo_null_result.py) |

## E. Electroweak and hierarchy tools

| Tool / subderivation | Safe statement | Status / import class | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Hierarchy dimensional-compression diagnostic | the final hierarchy correction acts like a dimension-4 intensive normalization, not a direct `1/16` scale-root correction | bounded support; zero-input structural | hierarchy interpretation, Higgs/effective-potential arguments | [HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md](../../HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md) | [frontier_hierarchy_dimensional_compression.py](../../../scripts/frontier_hierarchy_dimensional_compression.py) |
| Hierarchy exponent lock | the exact determinant exponent on the accepted minimal hierarchy block is fixed at `16 = 2 x 2^3` and survives the spatial-BC audit on that block | retained support; zero-input structural | hierarchy closure, block-normalization arguments, future Yukawa/scaling work | [HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md](../../HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md) | [frontier_hierarchy_spatial_bc_and_u0_scaling.py](../../../scripts/frontier_hierarchy_spatial_bc_and_u0_scaling.py) |
| Hierarchy Matsubara decomposition | determinant, free-energy density, and condensate on the minimal APBC block admit an exact temporal-mode decomposition | retained support; zero-input structural | hierarchy normalization, temporal-mode arguments | [HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md](../../HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md) | [frontier_hierarchy_matsubara_decomposition.py](../../../scripts/frontier_hierarchy_matsubara_decomposition.py) |
| Effective-potential endpoint coefficient | the small-`m` coefficient of the exact dimension-4 effective-potential density is explicit at `L_t=2`, `L_t=4`, and `L_t -> infinity` | retained support; zero-input structural | hierarchy endpoint normalization, effective-potential arguments | [HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md](../../HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md) | [frontier_hierarchy_effective_potential_endpoint.py](../../../scripts/frontier_hierarchy_effective_potential_endpoint.py) |
| Spatial-BC and `u_0` scaling rule | spatial APBC is selected by the existence of a finite intensive `3+1` limit, and the hierarchy observable carries one exact power of `u_0` per hopping amplitude | retained support; zero-input structural | hierarchy normalization, gauge/Yukawa matching arguments | [HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md](../../HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md) | [frontier_hierarchy_spatial_bc_and_u0_scaling.py](../../../scripts/frontier_hierarchy_spatial_bc_and_u0_scaling.py) |
| Bosonic-bilinear selector | the physical local bosonic CPT-even order parameter selects the unique minimal resolved APBC orbit at `L_t = 4` | retained support; zero-input structural | hierarchy selector arguments, future scalar-order-parameter work | [HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md](../../HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md) | [frontier_hierarchy_bosonic_bilinear_selector.py](../../../scripts/frontier_hierarchy_bosonic_bilinear_selector.py) |
| Observable-principle closure | the scalar order-parameter generator is forced by exact Grassmann factorization and yields the final hierarchy curvature kernel | retained; zero-input structural | electroweak hierarchy, future scalar observable closures | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py) |

## F. Flavor, Yukawa, and mass-lane tools

| Tool / subderivation | Safe statement | Status / import class | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| `y_t` boundary theorem | `v`, not `M_Pl`, is the physical crossover endpoint of the current lattice-to-EFT `y_t` chain | closed subderivation on open lane; bridge-conditioned | `y_t` closure, crossover consistency, future EFT matching cleanup | [YT_BOUNDARY_THEOREM.md](../../YT_BOUNDARY_THEOREM.md) | [frontier_yt_boundary_consistency.py](../../../scripts/frontier_yt_boundary_consistency.py) |
| `\alpha_s(M_Z)` determination chain | current strongest main-branch low-energy strong-coupling bridge sits on the lattice coupling-map route, but strict zero-import cleanliness remains under review and it is not yet safe as a fully internal closure tool | bounded/open; import-conditioned | `\alpha_s`, `y_t`, DM matching, coupling normalization | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) | [frontier_alpha_s_determination.py](../../../scripts/frontier_alpha_s_determination.py) |
| `y_t` zero-import 2-loop chain | current strongest bounded low-energy `\alpha_s` / `m_t` bridge on the present `y_t` lane; strict zero-import reuse remains unsafe until the bridge/import questions are fully closed | bounded/open; bridge-conditioned and not yet safe as a pure zero-input tool | `y_t`, `\alpha_s`, bridge debugging | [YT_ZERO_IMPORT_CLOSURE_NOTE.md](../../YT_ZERO_IMPORT_CLOSURE_NOTE.md) | [frontier_yt_2loop_chain.py](../../../scripts/frontier_yt_2loop_chain.py) |
| `y_t` vertex power | operator structure gives `n_link = 2` on the current lane | closed subderivation on open lane; zero-input structural | `y_t`, `\alpha_s`, matching/crossover work | [YT_VERTEX_POWER_DERIVATION.md](../../YT_VERTEX_POWER_DERIVATION.md) | [frontier_vertex_power.py](../../../scripts/frontier_vertex_power.py) |
| Gauge crossover theorem | one-shot gauge/taste crossover gives the current strongest import-allowed `m_t` route | bounded/open; import-conditioned | `y_t` import-allowed route, scheme/matching analysis | [YT_GAUGE_CROSSOVER_THEOREM.md](../../YT_GAUGE_CROSSOVER_THEOREM.md) | [frontier_yt_gauge_crossover_theorem.py](../../../scripts/frontier_yt_gauge_crossover_theorem.py) |
| Higgs / CW mass lane | current Higgs-mass route is bounded and useful as a working mass-lane toolbox, but not closed | open/bounded; bridge-conditioned | Higgs closure, mass-spectrum work | [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md) | [frontier_higgs_mass_derived.py](../../../scripts/frontier_higgs_mass_derived.py) |
| CKM from mass hierarchy | GST and hierarchy-ordering structure follow from the bounded mass-hierarchy route even before full coefficient closure | bounded/open; bridge-conditioned | CKM closure, Cabibbo/GST arguments | [CKM_FROM_MASS_HIERARCHY_NOTE.md](../../CKM_FROM_MASS_HIERARCHY_NOTE.md) | [frontier_ckm_from_mass_hierarchy.py](../../../scripts/frontier_ckm_from_mass_hierarchy.py) |
| CKM Schur complement theorem | the effective `1-3` coupling is generated by the NNI Schur-complement cascade | closed subderivation on open lane; zero-input structural | CKM closure, Wolfenstein-cascade arguments, `V_ub` route cleanup | [CKM_SCHUR_COMPLEMENT_THEOREM.md](../../CKM_SCHUR_COMPLEMENT_THEOREM.md) | [frontier_ckm_schur_complement.py](../../../scripts/frontier_ckm_schur_complement.py) |
| Cabibbo bounded companion | strongest current `main`-branch Cabibbo statement sits inside the mass-basis NNI package at `|V_us| = 0.2251` | bounded/open; bridge-conditioned | CKM closure, flavor hierarchy subresults | [CABIBBO_BOUND_NOTE.md](../../CABIBBO_BOUND_NOTE.md) | [frontier_ckm_mass_basis_nni.py](../../../scripts/frontier_ckm_mass_basis_nni.py) |
| CKM mass-basis route | strongest current magnitude package sits on the mass-basis NNI route | bounded/open; bridge-conditioned | CKM closure, flavor coefficient work | [CKM_MASS_BASIS_NNI_NOTE.md](../../CKM_MASS_BASIS_NNI_NOTE.md) | [frontier_ckm_mass_basis_nni.py](../../../scripts/frontier_ckm_mass_basis_nni.py) |
| Jarlskog phase companion | derived `Z_3` phase plus observed mixing angles gives the current strongest bounded CP-violation row | bounded/open; observation-conditioned | CKM phase work, flavor companion framing | [JARLSKOG_PHASE_BOUND_NOTE.md](../../JARLSKOG_PHASE_BOUND_NOTE.md) | [frontier_jarlskog_derived.py](../../../scripts/frontier_jarlskog_derived.py) |

## G. DM and cosmology tools

| Tool / subderivation | Safe statement | Status / import class | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| DM direct-observable bridge | the annihilation/relic route can be framed as a direct observable of the lattice Hamiltonian rather than only through a separate coupling label | bounded/open; zero-input structural | DM relic closure, invariant-coupling objections, `sigma v` derivations | [DM_DIRECT_OBSERVABLE_NOTE.md](../../DM_DIRECT_OBSERVABLE_NOTE.md) | [frontier_dm_sigma_v_lattice.py](../../../scripts/frontier_dm_sigma_v_lattice.py) |
| DM structural ratio | strongest current structural DM ratio result is `R = 5.48` with remaining relic bridge still bounded | bounded/open; import-conditioned | DM relic closure, cosmology chain | [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md) | [frontier_dm_relic_paper.py](../../../scripts/frontier_dm_relic_paper.py) |
| Conditional `\Omega_\Lambda` chain | current `\Omega_\Lambda` route is a bounded conditional chain from `R`, flatness, and observed `\eta` | bounded/conditional; observation-conditioned | cosmology closure, bookkeeping of conditional bridges | [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md) | [frontier_omega_lambda_derivation.py](../../../scripts/frontier_omega_lambda_derivation.py) |
| Spectral tilt companion | current `n_s` route is a bounded/conditional graph-growth result | bounded/conditional; observation-conditioned | cosmology model comparison, inflation-alternative framing | [PRIMORDIAL_SPECTRUM_NOTE.md](../../PRIMORDIAL_SPECTRUM_NOTE.md) | [frontier_primordial_spectrum.py](../../../scripts/frontier_primordial_spectrum.py) |
| Dark-energy EOS chain | current `w = -1` route is a bounded/conditional spectral-gap result | bounded/conditional; observation-conditioned | cosmology chain, topology/cosmology bookkeeping | [DARK_ENERGY_EOS_NOTE.md](../../DARK_ENERGY_EOS_NOTE.md) | [frontier_dark_energy_eos.py](../../../scripts/frontier_dark_energy_eos.py) |
| Cosmological-constant companion | current `\Lambda` route is a bounded/conditional topology/cosmology identification | bounded/conditional; observation-conditioned | cosmology chain, `S^3` companion work | [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md) | [frontier_cosmological_constant.py](../../../scripts/frontier_cosmological_constant.py) |
| Graviton-mass companion | `m_g` companion follows from retained `S^3` plus observed `H_0` on the current surface | bounded/conditional; observation-conditioned | topology/cosmology companions, long-range gravity phenomenology | [GRAVITON_MASS_DERIVED_NOTE.md](../../GRAVITON_MASS_DERIVED_NOTE.md) | [frontier_graviton_mass_derived.py](../../../scripts/frontier_graviton_mass_derived.py) |

## H. Companion and discriminator tools

| Tool / subderivation | Safe statement | Status / import class | Reusable for | Authority | Primary runner |
|---|---|---|---|---|---|
| Bekenstein-Hawking entropy companion | BH area-law companion remains bounded but concrete on the current identification surface | bounded companion; companion-only phenomenology | gravity/thermodynamics comparison, companion-paper planning | [BH_ENTROPY_DERIVED_NOTE.md](../../BH_ENTROPY_DERIVED_NOTE.md) | [frontier_bh_entropy_derived.py](../../../scripts/frontier_bh_entropy_derived.py) |
| Gravitational decoherence companion | BMV-class decoherence benchmark is concrete and mainline-captured, though not retained | bounded companion; observation-conditioned | experimental discriminator work, gravity companion framing | [GRAV_DECOHERENCE_DERIVED_NOTE.md](../../GRAV_DECOHERENCE_DERIVED_NOTE.md) | [frontier_grav_decoherence_derived.py](../../../scripts/frontier_grav_decoherence_derived.py) |
| Proton-lifetime companion | proton-lifetime route is a sharp bounded prediction layer | bounded companion; import-conditioned | future companion paper, discriminator framing | [PROTON_LIFETIME_DERIVED_NOTE.md](../../PROTON_LIFETIME_DERIVED_NOTE.md) | [frontier_proton_lifetime_derived.py](../../../scripts/frontier_proton_lifetime_derived.py) |
| Lorentz-violation fingerprint | cubic `(E/E_{Pl})^2` LV fingerprint is a sharp bounded companion result | bounded companion; companion-only phenomenology | experimental discriminator work | [LORENTZ_VIOLATION_DERIVED_NOTE.md](../../LORENTZ_VIOLATION_DERIVED_NOTE.md) | [frontier_lorentz_violation.py](../../../scripts/frontier_lorentz_violation.py) |
| Magnetic-monopole companion | monopole mass route is a sharp bounded companion result | bounded companion; companion-only phenomenology | companion-paper planning, discriminator framing | [MONOPOLE_DERIVED_NOTE.md](../../MONOPOLE_DERIVED_NOTE.md) | [frontier_monopole_derived.py](../../../scripts/frontier_monopole_derived.py) |

## Atlas rule

Before a subderivation is treated as reusable framework infrastructure:

1. it should have one current authority note on `main`
2. it should have one runner or explicit validation path
3. its safe claim boundary should be recorded here
4. if older route notes exist, this file should identify the canonical one

If a tool is only visible inside a longer narrative note and not discoverable
here, future lanes are likely to redo work unnecessarily.
