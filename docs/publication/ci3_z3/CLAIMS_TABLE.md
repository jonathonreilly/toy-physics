# Claims Table

Use [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) alongside
this table. This file says what the paper may claim. The derivation /
validation map says how each claim is evidenced and released.

For the full branch-audited publication capture, also use:

- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)
- [REMOTE_BRANCH_AUDIT_2026-04-14.md](./REMOTE_BRANCH_AUDIT_2026-04-14.md)

## External inputs

The current paper conditions phenomenology on two explicit cosmological
boundary conditions:

- `T_CMB = 2.7255 K`
- `H_0 = 67.4 km/s/Mpc`

Framework statement:

- the paper-level framework is the one-axiom reduction surface in
  [SINGLE_AXIOM_INFORMATION_NOTE.md](../../SINGLE_AXIOM_INFORMATION_NOTE.md)
  and
  [SINGLE_AXIOM_HILBERT_NOTE.md](../../SINGLE_AXIOM_HILBERT_NOTE.md)
- [MINIMAL_AXIOMS_2026-04-11.md](../../MINIMAL_AXIOMS_2026-04-11.md) is the
  operational package-boundary memo used to audit the current implementation
  surface

The electroweak scale is not an external input on the current paper surface.
The exact minimal hierarchy theorem fixes the source-response structure on the
minimal block; the quoted value
`v = 246.282818290129 GeV` (`+0.0255%` relative to `246.22 GeV`) is the
pinned numerical evaluation on the current `u_0` / plaquette surface.

## Retained core

| Claim | Status | Placement | Authority | Primary runner |
|---|---|---|---|---|
| `Cl(3)` on `Z^3` is the working physical theory | retained framework statement | main text | [Publication state](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | n/a |
| weak-field gravity from the Poisson self-consistency / Newton chain on `Z^3` | retained | main text | [Publication state](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | [frontier_self_consistent_field_equation.py](../../../scripts/frontier_self_consistent_field_equation.py), [frontier_poisson_exhaustive_uniqueness.py](../../../scripts/frontier_poisson_exhaustive_uniqueness.py), [frontier_newton_derived.py](../../../scripts/frontier_newton_derived.py) |
| weak-field WEP from the derived lattice action | retained corollary | main text or Extended Data corollary | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md) | [frontier_broad_gravity.py](../../../scripts/frontier_broad_gravity.py) |
| weak-field gravitational time dilation on the retained Poisson/Newton surface | retained corollary | main text or Extended Data corollary | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md), [GRAVITY_CLEAN_DERIVATION_NOTE.md](../../GRAVITY_CLEAN_DERIVATION_NOTE.md) | [frontier_broad_gravity.py](../../../scripts/frontier_broad_gravity.py) |
| restricted strong-field closure on the star-supported finite-rank class under the exact static conformal bridge | retained restricted theorem | Extended Data / arXiv theorem box | [RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](../../RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md), [OH_STATIC_CONSTRAINT_LIFT_NOTE.md](../../OH_STATIC_CONSTRAINT_LIFT_NOTE.md), [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](../../OH_SCHUR_BOUNDARY_ACTION_NOTE.md), [STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md](../../STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md) | [frontier_oh_static_constraint_lift.py](../../../scripts/frontier_oh_static_constraint_lift.py), [frontier_oh_schur_boundary_action.py](../../../scripts/frontier_oh_schur_boundary_action.py), [frontier_star_supported_bridge_class.py](../../../scripts/frontier_star_supported_bridge_class.py) |
| full discrete `3+1` GR on the project route | retained exact theorem | main text / theorem box | [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](../../UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md) | [frontier_universal_gr_discrete_global_closure.py](../../../scripts/frontier_universal_gr_discrete_global_closure.py), [frontier_universal_gr_lorentzian_global_atlas_closure.py](../../../scripts/frontier_universal_gr_lorentzian_global_atlas_closure.py), [frontier_universal_gr_lorentzian_signature_extension.py](../../../scripts/frontier_universal_gr_lorentzian_signature_extension.py) |
| UV-finite partition-density family whose mean/stationary sector reproduces the project’s discrete `3+1` GR route | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md](../../UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md) | [frontier_universal_qg_uv_finite_partition.py](../../../scripts/frontier_universal_qg_uv_finite_partition.py) |
| canonical geometric barycentric-dyadic refinement net for the exact discrete partition-density and stationary-section family on `PL S^3 x R` | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md](../../UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md) | [frontier_universal_qg_canonical_refinement_net.py](../../../scripts/frontier_universal_qg_canonical_refinement_net.py) |
| exact inverse-limit Gaussian cylinder closure for the canonical discrete QG family on `PL S^3 x R` | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md](../../UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md) | [frontier_universal_qg_inverse_limit_closure.py](../../../scripts/frontier_universal_qg_inverse_limit_closure.py) |
| exact abstract Gaussian / Cameron-Martin completion for the canonical discrete QG family on `PL S^3 x R` | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md](../../UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md) | [frontier_universal_qg_abstract_gaussian_completion.py](../../../scripts/frontier_universal_qg_abstract_gaussian_completion.py) |
| exact project-native PL field realization for the canonical discrete QG family on `PL S^3 x R` | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md](../../UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md) | [frontier_universal_qg_pl_field_interface.py](../../../scripts/frontier_universal_qg_pl_field_interface.py) |
| exact project-native PL weak/Dirichlet-form closure for the canonical discrete QG family on `PL S^3 x R` | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md](../../UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md) | [frontier_universal_qg_pl_weak_form.py](../../../scripts/frontier_universal_qg_pl_weak_form.py) |
| exact project-native PL `H^1`-type Sobolev interface for the canonical discrete QG family on `PL S^3 x R` | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md](../../UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md) | [frontier_universal_qg_pl_sobolev_interface.py](../../../scripts/frontier_universal_qg_pl_sobolev_interface.py) |
| exact external FE/Galerkin smooth weak-field and Gaussian measure equivalence for a chosen external smooth target of the canonical discrete QG family on `PL S^3 x R` | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_EXTERNAL_FE_SMOOTH_EQUIVALENCE_NOTE.md](../../UNIVERSAL_QG_EXTERNAL_FE_SMOOTH_EQUIVALENCE_NOTE.md) | [frontier_universal_qg_external_fe_smooth_equivalence.py](../../../scripts/frontier_universal_qg_external_fe_smooth_equivalence.py) |
| exact canonical textbook weak/measure equivalence for the canonical discrete QG family on `PL S^3 x R` | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_CANONICAL_TEXTBOOK_WEAK_MEASURE_EQUIVALENCE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_WEAK_MEASURE_EQUIVALENCE_NOTE.md) | [frontier_universal_qg_canonical_textbook_weak_measure_equivalence.py](../../../scripts/frontier_universal_qg_canonical_textbook_weak_measure_equivalence.py) |
| exact smooth local gravitational weak/Gaussian identification on the positive-background class | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_LOCAL_IDENTIFICATION_NOTE.md](../../UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_LOCAL_IDENTIFICATION_NOTE.md) | [frontier_universal_qg_smooth_gravitational_local_identification.py](../../../scripts/frontier_universal_qg_smooth_gravitational_local_identification.py) |
| exact smooth finite-atlas gravitational stationary-family identification on the chosen smooth realization | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_ATLAS_NOTE.md](../../UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_ATLAS_NOTE.md) | [frontier_universal_qg_smooth_gravitational_global_atlas_identification.py](../../../scripts/frontier_universal_qg_smooth_gravitational_global_atlas_identification.py) |
| exact smooth global weak gravitational stationary/Gaussian solution class on the chosen smooth realization of `PL S^3 x R` | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md](../../UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md) | [frontier_universal_qg_smooth_gravitational_global_solution_class.py](../../../scripts/frontier_universal_qg_smooth_gravitational_global_solution_class.py) |
| exact canonical smooth gravitational weak/measure equivalence on the chosen smooth realization | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_CANONICAL_SMOOTH_GRAVITATIONAL_WEAK_MEASURE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_SMOOTH_GRAVITATIONAL_WEAK_MEASURE_NOTE.md) | [frontier_universal_qg_canonical_smooth_gravitational_weak_measure.py](../../../scripts/frontier_universal_qg_canonical_smooth_gravitational_weak_measure.py) |
| exact canonical smooth geometric/action equivalence on the chosen smooth realization | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_CANONICAL_SMOOTH_GEOMETRIC_ACTION_NOTE.md](../../UNIVERSAL_QG_CANONICAL_SMOOTH_GEOMETRIC_ACTION_NOTE.md) | [frontier_universal_qg_canonical_smooth_geometric_action.py](../../../scripts/frontier_universal_qg_canonical_smooth_geometric_action.py) |
| exact canonical textbook Einstein-Hilbert-style geometric/action equivalence on the chosen smooth realization | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md) | [frontier_universal_qg_canonical_textbook_geometric_action_equivalence.py](../../../scripts/frontier_universal_qg_canonical_textbook_geometric_action_equivalence.py) |
| exact canonical textbook continuum gravitational weak/stationary action closure on the chosen smooth realization of `PL S^3 x R` | retained exact companion | Extended Data / arXiv theorem box | [UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md) | [frontier_universal_qg_canonical_textbook_continuum_gr_closure.py](../../../scripts/frontier_universal_qg_canonical_textbook_continuum_gr_closure.py) |
| continuum identification positioning across the current gravity and gauge package surface | retained positioning | main text / discussion | [CONTINUUM_IDENTIFICATION_NOTE.md](../../CONTINUUM_IDENTIFICATION_NOTE.md) | [frontier_continuum_identification_audit.py](../../../scripts/frontier_continuum_identification_audit.py) |
| exact native `SU(2)` from cubic `Cl(3)` | retained | main text | [BOUNDED_NATIVE_GAUGE_NOTE.md](../../BOUNDED_NATIVE_GAUGE_NOTE.md) | [frontier_non_abelian_gauge.py](../../../scripts/frontier_non_abelian_gauge.py) |
| graph-first structural `SU(3)` closure (selector unique up to graph automorphism) | retained | main text | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| exact `T = 0` confinement of the graph-first `SU(3)` gauge sector, with bounded `\sqrt{\sigma} \approx 465 MeV` | retained structural theorem + bounded quantitative prediction | main text / theorem box | [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md) | [frontier_confinement_string_tension.py](../../../scripts/frontier_confinement_string_tension.py) |
| left-handed `+1/3` / `-1` charge matching on the selected-axis surface | retained corollary | main text or SI corollary | [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](../../LEFT_HANDED_CHARGE_MATCHING_NOTE.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| anomaly-forced `3+1` closure | retained | main text | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md) | [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) |
| electroweak hierarchy / `v` scale on the exact minimal `3+1` block | retained exact theorem | main text or Extended Data theorem box | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py) |
| retained `S^3` compactification / topology closure | retained | main text or SI theorem box | [S3_GENERAL_R_DERIVATION_NOTE.md](../../S3_GENERAL_R_DERIVATION_NOTE.md), [S3_CAP_UNIQUENESS_NOTE.md](../../S3_CAP_UNIQUENESS_NOTE.md) | [frontier_s3_boundary_link_theorem.py](../../../scripts/frontier_s3_boundary_link_theorem.py), [frontier_s3_cap_uniqueness.py](../../../scripts/frontier_s3_cap_uniqueness.py), [frontier_s3_general_r.py](../../../scripts/frontier_s3_general_r.py) |
| full-framework one-generation matter closure | retained | main text | [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](../../ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | [frontier_right_handed_sector.py](../../../scripts/frontier_right_handed_sector.py), [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) |
| three-generation matter structure in the framework (physical species structure, not a taste artifact) | retained | main text | [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md) | [frontier_generation_fermi_point.py](../../../scripts/frontier_generation_fermi_point.py), [frontier_generation_rooting_undefined.py](../../../scripts/frontier_generation_rooting_undefined.py), [frontier_generation_axiom_boundary.py](../../../scripts/frontier_generation_axiom_boundary.py) |
| exact `I_3 = 0` / no third-order interference on the Hilbert surface | retained exact companion | main text or Extended Data | [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md) | [frontier_born_rule_derived.py](../../../scripts/frontier_born_rule_derived.py) (historical filename) |
| exact CPT on the free staggered lattice | retained exact companion | main text or Extended Data | [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md) | [frontier_cpt_exact.py](../../../scripts/frontier_cpt_exact.py) (even periodic lattices only) |
| emergent Lorentz invariance: leading correction is CPT-even, P-even, dimension-6 with unique cubic-harmonic `\ell = 4` signature, and is `(E/M_{Pl})^2`-suppressed on the retained hierarchy surface | retained exact structural theorem | main text / discussion | [EMERGENT_LORENTZ_INVARIANCE_NOTE.md](../../EMERGENT_LORENTZ_INVARIANCE_NOTE.md) | [frontier_emergent_lorentz_invariance.py](../../../scripts/frontier_emergent_lorentz_invariance.py) |
| strong CP / `θ_eff = 0` on the retained axiom-determined action surface | retained exact structural theorem | main text / theorem box | [STRONG_CP_THETA_ZERO_NOTE.md](../../STRONG_CP_THETA_ZERO_NOTE.md) | [frontier_strong_cp_theta_zero.py](../../../scripts/frontier_strong_cp_theta_zero.py) |
| single-axiom Hilbert/locality reduction | SI framing only | SI / framing box | [SINGLE_AXIOM_HILBERT_NOTE.md](../../SINGLE_AXIOM_HILBERT_NOTE.md), [SINGLE_AXIOM_INFORMATION_NOTE.md](../../SINGLE_AXIOM_INFORMATION_NOTE.md) | [frontier_single_axiom_hilbert.py](../../../scripts/frontier_single_axiom_hilbert.py), [frontier_single_axiom_information.py](../../../scripts/frontier_single_axiom_information.py) |

## Quantitative component stack

| Claim | Status | Placement | Authority | Primary runner |
|---|---|---|---|---|
| `alpha_s(M_Z) = 0.1181` | retained quantitative lane | quantitative table | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) | [frontier_yt_zero_import_chain.py](../../../scripts/frontier_yt_zero_import_chain.py) |
| `sin^2(theta_W) = 0.2306`, `1/alpha_EM = 127.67`, `g_1(v) = 0.4644`, `g_2(v) = 0.6480` | retained quantitative lane | quantitative table / SI | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) | [frontier_yt_ew_coupling_derivation.py](../../../scripts/frontier_yt_ew_coupling_derivation.py) |
| CKM atlas/axiom closure package (`|V_us|`, `|V_cb|`, `|V_ub|`, `\delta`, `J`) | promoted quantitative package | quantitative table / SI theorem box | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) | [frontier_ckm_atlas_axiom_closure.py](../../../scripts/frontier_ckm_atlas_axiom_closure.py), [frontier_ckm_no_import_audit.py](../../../scripts/frontier_ckm_no_import_audit.py) |
| `y_t(v) = 0.9176`, `m_t(pole) = 172.57-173.10 GeV` | bounded quantitative lane | quantitative table | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md), [YT_QFP_INSENSITIVITY_THEOREM.md](../../YT_QFP_INSENSITIVITY_THEOREM.md) | [frontier_yt_color_projection_correction.py](../../../scripts/frontier_yt_color_projection_correction.py), [frontier_yt_qfp_insensitivity.py](../../../scripts/frontier_yt_qfp_insensitivity.py) |
| `m_H = 119.8 GeV` (2-loop support route), `125.3 GeV` (framework-side 3-loop route), bounded vacuum stability readout | bounded quantitative lane | quantitative table / discussion | [HIGGS_VACUUM_PROMOTED_NOTE.md](../../HIGGS_VACUUM_PROMOTED_NOTE.md) | [frontier_higgs_mass_full_3loop.py](../../../scripts/frontier_higgs_mass_full_3loop.py), [frontier_yt_color_projection_correction.py](../../../scripts/frontier_yt_color_projection_correction.py) |

## Bounded companions

These lanes are intentionally kept out of the retained publication surface.
They remain matrix-tracked bounded companions until they are either promoted
cleanly or closed.

| Claim | Status | Placement | Authority |
|---|---|---|---|
| weak-field GR-signature companions beyond Newton/Poisson/WEP/time-dilation | bounded | arXiv / SI only | [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md) `F06` |
| direct lattice DM contact enhancement and bounded relic chain | bounded | arXiv / SI only | [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md), [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md) `F01` |
| cosmology windows (`Lambda`, `w=-1`, graviton mass, `Omega_Lambda`, `n_s`) | bounded / conditional | arXiv companion only | [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md), [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md), [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md), [PRIMORDIAL_SPECTRUM_NOTE.md](../../PRIMORDIAL_SPECTRUM_NOTE.md), [DARK_ENERGY_EOS_NOTE.md](../../DARK_ENERGY_EOS_NOTE.md), [GRAVITON_MASS_DERIVED_NOTE.md](../../GRAVITON_MASS_DERIVED_NOTE.md) |
| proton lifetime | bounded companion prediction | arXiv companion only | [PROTON_LIFETIME_DERIVED_NOTE.md](../../PROTON_LIFETIME_DERIVED_NOTE.md) |
| vacuum critical stability | bounded companion prediction | arXiv companion only | [VACUUM_CRITICAL_STABILITY_NOTE.md](../../VACUUM_CRITICAL_STABILITY_NOTE.md) |
| BH entropy / RT ratio | bounded companion | arXiv companion only | [BH_ENTROPY_DERIVED_NOTE.md](../../BH_ENTROPY_DERIVED_NOTE.md) |
| gravitational decoherence | bounded companion | arXiv companion only | [GRAV_DECOHERENCE_DERIVED_NOTE.md](../../GRAV_DECOHERENCE_DERIVED_NOTE.md) |
| magnetic monopole mass | bounded companion prediction | arXiv companion only | [MONOPOLE_DERIVED_NOTE.md](../../MONOPOLE_DERIVED_NOTE.md) |
| GW echo null result / observational silence of frozen stars | bounded / off-scope companion | later companion paper only | [GW_ECHO_NULL_RESULT_NOTE.md](../../GW_ECHO_NULL_RESULT_NOTE.md) |

The branch-audited quantitative portfolio behind these rows is catalogued in
[PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md). Every intentionally excluded
family is documented in [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md).

## Open paper gates

1. DM relic mapping

## Packaging rule

No manuscript claim is ready until it appears in both:

- this table
- [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
