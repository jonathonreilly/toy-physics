# Science Map

This file is the domain-organized map of the current `main` package.

Use it when the question is:

- what scientific areas does the repo currently cover?
- what is the best current status in each area?
- where should I start if I want to validate one area rather than the whole repo?

For the paper-facing claim surface, use [CLAIMS_TABLE.md](./CLAIMS_TABLE.md).
For the full package inventory, use [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md).
For reproduction, use [REPRODUCE.md](./REPRODUCE.md).

## Framework and Scope

- working framework:
  `Cl(3)` on `Z^3` as the physical theory
- broad package shape:
  exact spacetime/gravity backbone, exact gauge/matter backbone, retained
  quantitative EW/QCD/flavor package, bounded companion phenomenology, one
  remaining charged-lepton flagship bridge package
- boundaries:
  explicit package inputs and non-claims are kept in
  [INPUTS_AND_QUALIFIERS_NOTE.md](./INPUTS_AND_QUALIFIERS_NOTE.md) and
  [WHAT_THIS_PAPER_DOES_NOT_CLAIM.md](./WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)

If you are arriving for the first time, start with:

- [ARXIV_DRAFT.md](./ARXIV_DRAFT.md)
- [PREDICTION_SURFACE_2026-04-15.md](./PREDICTION_SURFACE_2026-04-15.md)
- [REPRODUCE.md](./REPRODUCE.md)
- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)

Use [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md) only when you want the
full package-capture inventory rather than the shortest public route.

## Spacetime, Gravity, and Quantum Gravity

- retained weak-field gravity:
  Poisson uniqueness, Newton law, WEP, and time dilation
- retained strong-field/gravity backbone:
  restricted strong-field closure on the current supported class, exact discrete
  `3+1` GR on the project route, and the chosen continuum/QG identification
  chain through the canonical textbook weak/measure/action surface
- retained topology:
  `S^3` compactification/topology closure
- retained structural companions:
  emergent Lorentz invariance with fixed-`H_lat` unitary-kernel closure,
  exact evanescent-barrier transfer-matrix bound + tortoise-length identity,
  BH-entropy Widom no-go on the current carrier

Start with:

- [GRAVITY_PUBLICATION_PACKAGE_SUMMARY_2026-04-15.md](./GRAVITY_PUBLICATION_PACKAGE_SUMMARY_2026-04-15.md)
- [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)

Validate with:

- `python3 scripts/frontier_self_consistent_field_equation.py`
- `python3 scripts/frontier_newton_derived.py`
- `python3 scripts/frontier_universal_gr_discrete_global_closure.py`
- `python3 scripts/frontier_universal_qg_canonical_textbook_continuum_gr_closure.py`

## Gauge, Matter, and Structural Field Content

- retained gauge structure:
  exact native `SU(2)`, graph-first structural `SU(3)`, exact `T = 0`
  confinement on the graph-first color sector
- retained matter structure:
  one-generation closure, SM hypercharge uniqueness/electric-charge
  quantization, fractional-charge denominator from `N_c`, `SU(2)` Witten
  global-anomaly cancellation, `SU(3)^3` cubic gauge anomaly cancellation,
  B-L anomaly freedom as a gaugeable option, three-generation
  observable/species closure, exact `I_3 = 0`, exact CPT,
  Bell/CHSH support on explicit two-species lattice systems
- retained package-support lanes:
  `g_bare = 1` structural normalization and two-Ward 1PI closure
- package-support atlas:
  taste-cube/residual-symmetry flavor support and `Cl(3) -> SM` algebraic
  support packet

Start with:

- [NATIVE_GAUGE_CLOSURE_NOTE.md](../../NATIVE_GAUGE_CLOSURE_NOTE.md)
- [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
- [STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md](../../STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- [FRACTIONAL_CHARGE_DENOMINATOR_FROM_N_C_THEOREM_NOTE_2026-04-24.md](../../FRACTIONAL_CHARGE_DENOMINATOR_FROM_N_C_THEOREM_NOTE_2026-04-24.md)
- [SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md](../../SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
- [SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md](../../SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md)
- [BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md](../../BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md)
- [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md)
- [STRONG_CP_THETA_ZERO_NOTE.md](../../STRONG_CP_THETA_ZERO_NOTE.md)
- [UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md](../../UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md)

Validate with:

- `python3 scripts/frontier_non_abelian_gauge.py`
- `python3 scripts/frontier_graph_first_su3_integration.py`
- `python3 scripts/frontier_sm_hypercharge_uniqueness.py`
- `python3 scripts/frontier_fractional_charge_denominator_from_n_c.py`
- `python3 scripts/frontier_su2_witten_z2_anomaly.py`
- `python3 scripts/frontier_su3_cubic_anomaly_cancellation.py`
- `python3 scripts/frontier_bminusl_anomaly_freedom.py`
- `python3 scripts/frontier_generation_fermi_point.py`
- `python3 scripts/frontier_three_generation_observable_theorem.py`
- `python3 scripts/frontier_strong_cp_theta_zero.py`
- `python3 scripts/frontier_universal_theta_induced_edm_vanishing.py`

## Quantitative Electroweak, QCD, Yukawa, and Higgs Package

- retained quantitative lanes:
  `alpha_s(M_Z)`, EW normalization, retained YT/top transport
- promoted quantitative flavor lane:
  CKM atlas/axiom package, including the standalone Wolfenstein structural
  identities `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3`, and the CP-phase
  structural identity `cos^2(delta_CKM) = 1/6`, plus the rescaled
  atlas-triangle right-angle identity `alpha_0 = 90 deg`, atlas-leading
  first-row identities `|V_us|_0^2 = alpha_s(v)/2`,
  `|V_ub|_0^2 = alpha_s(v)^3/72`,
  `|V_ud|_0^2 = 1 - alpha_s(v)/2 - alpha_s(v)^3/72`,
  second-row identities `|V_cd|_0^2 = alpha_s(v)/2`,
  `|V_cs|_0^2 = 1 - alpha_s(v)/2 - alpha_s(v)^2/6`,
  `|V_cb|_0^2 = alpha_s(v)^2/6`, and atlas-leading third-row identities
  `|V_td|_0^2 = 5 alpha_s(v)^3/72`,
  `|V_ts|_0^2 = alpha_s(v)^2/6`, plus the atlas-leading B_s mixing phase
  `phi_s = -alpha_s(v) sqrt(5)/6` and the NLO barred-triangle protected
  invariant `gamma_bar = arctan(sqrt(5))`, the retained NLO beta-ratio
  corollary `sin(2 beta_bar)/sin(2 beta_0) = 1 - alpha_s(v)/5`, plus the
  Thales-mediated
  cross-system CP ratio `phi_s / sin(2 beta_d) = -alpha_s(v)/2`
  and CP-product estimator
  `alpha_s(v) = (18/5) sin(2 beta_d) sin(2 beta_s)` at atlas-leading order
  plus the
  kaon epsilon_K CKM-bracket factorization through atlas `J_0`
- derived quantitative lane:
  Higgs/vacuum package with explicit retention budget
- bounded quantitative companions:
  W-boson same-surface probe, taste-scalar near-degeneracy,
  vacuum critical stability
- absolute-scale scoping:
  the current package carries `a^(-1) = M_Pl` as a Planck-scale package pin on
  the accepted physical-lattice reading; the 2026-04-24 conditional-completion
  packet derives `c_cell = 1/4`, closes the unique finite-boundary density
  extension positively, and gives `a/l_P = 1` once the primitive boundary count
  is accepted as the gravitational boundary/action carrier; the 2026-04-25
  source-unit normalization support theorem on that same carrier surface
  separates the retained bare Green coefficient `G_kernel = 1/(4 pi)` from the
  conditional physical Newton coefficient `G_Newton,lat = 1`, resolving the old
  bare-source `2 sqrt(pi)` mismatch without removing the remaining carrier
  premise; the minimal-stack derivation of that carrier identification remains
  open; the finite-automorphism-only response route and carrier-only
  parent-source scalar route are closed negatively; the simple-fiber Widom
  entropy-carrier class is also closed negatively at `c_Widom <= 1/6`, so a
  positive `1/4` entropy route must use a physically selected
  multi-pocket/multi-interval carrier or a gapped horizon-sector
  primitive-boundary theorem

Start with:

- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [USABLE_DERIVED_VALUES_INDEX.md](./USABLE_DERIVED_VALUES_INDEX.md)
- [PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md](../../PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md)
- [PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md](../../PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md)
- [PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md](../../PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md)
- [PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md](../../PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
- [PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md](../../PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md)
- [PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md](../../PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md)
- [AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md](../../AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md)

Validate with:

- `python3 scripts/frontier_complete_prediction_chain.py`
- `python3 scripts/frontier_alpha_lm_geometric_mean_identity.py`
- `python3 scripts/frontier_wolfenstein_lambda_a_structural_identities.py`
- `python3 scripts/frontier_ckm_cp_phase_structural_identity.py`
- `python3 scripts/frontier_ckm_atlas_triangle_right_angle.py`
- `python3 scripts/frontier_yt_ward_identity_derivation.py`
- `python3 scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py`
- `python3 scripts/frontier_higgs_mass_full_3loop.py`
- `python3 scripts/frontier_planck_scale_program_audit.py`
- `python3 scripts/frontier_planck_conditional_completion_audit.py`
- `python3 scripts/frontier_planck_source_unit_normalization_support_theorem.py`
- `python3 scripts/frontier_planck_boundary_density_extension.py`
- `python3 scripts/frontier_planck_finite_response_nogo.py`
- `python3 scripts/frontier_planck_parent_source_hidden_character_nogo.py`
- `python3 scripts/frontier_area_law_quarter_broader_no_go.py`

## Flavor, CP, and Charged-Lepton Structure

- promoted quantitative flavor package:
  CKM atlas/axiom closure
- bounded secondary flavor lanes:
  down-type CKM-dual mass-ratio lane, bounded quark support packet
- retained corollaries:
  CKM-only neutron EDM on the retained `theta_eff = 0` surface, plus
  source-scoped vanishing of all theta-induced EDM response components
- open flagship package:
  charged-lepton Koide `Q = 2/3`, `delta = 2/9`

Current charged-lepton status:

- `Q = 2/3` support is strong, but the physical readout is still reduced to a
  source-free reduced-carrier selection theorem; the background-zero /
  `Z`-erasure algebra on that carrier is now an exact criterion theorem, and
  strict onsite `C3` source functions would erase `Z`; retained
  central/projected commutant sources still admit `Z`, so the source-domain
  theorem remains open
- `delta = 2/9` support is strong, but the physical Brannen endpoint is still
  reduced to the selected-line local boundary-source law plus based endpoint
  section
- the A1/radian audit shows retained periodic phase sources are `q*pi`, so the
  exact Type-B rational witnesses for `2/9` still need a rational-to-radian
  observable law
- pointed-origin exhaustion shows that origin-free retained data cannot select
  the simultaneous zero-source / real-primitive / unit-endpoint representative;
  the objection-closure review keeps the branch's source-domain closure claims
  as conditional support, not retained closure
- the separate overall lepton scale `v_0` also remains open

Start with:

- [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md](../../WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
- [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- [CKM_NEUTRON_EDM_BOUND_NOTE.md](../../CKM_NEUTRON_EDM_BOUND_NOTE.md)
- [UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md](../../UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md)
- [KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md](../../KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md)
- [KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md](../../KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md)
- [KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md](../../KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md)
- [CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md](../../CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md)
- [KOIDE_NATIVE_DIMENSIONLESS_REVIEW_PACKET_2026-04-24.md](../../KOIDE_NATIVE_DIMENSIONLESS_REVIEW_PACKET_2026-04-24.md)

Validate with:

- `python3 scripts/frontier_ckm_atlas_axiom_closure.py`
- `python3 scripts/frontier_wolfenstein_lambda_a_structural_identities.py`
- `python3 scripts/frontier_ckm_cp_phase_structural_identity.py`
- `python3 scripts/frontier_ckm_no_import_audit.py`
- `python3 scripts/frontier_ckm_neutron_edm_bound.py`
- `python3 scripts/frontier_universal_theta_induced_edm_vanishing.py`
- `python3 scripts/frontier_koide_native_zero_section_nature_review.py`
- `python3 scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py`
- `python3 scripts/frontier_koide_dimensionless_objection_closure_review.py`
- `python3 scripts/frontier_koide_hostile_review_guard.py`
- `python3 scripts/frontier_koide_reviewer_stress_test.py`
- `python3 scripts/frontier_koide_lane_regression.py`

## Neutrino and Dark-Matter Package

- flagship closed package on the manuscript surface:
  dark-matter exact-target PMNS package
- bounded retained/support packet:
  neutrino reduction/current/no-go stack plus retained-package absolute-mass
  observable bounds

Current status:

- dark matter is closed for the exact PMNS-target formulation treated in the
  manuscript
- broader target-free global uniqueness remains out of scope
- the neutrino positive retained lane remains absent; current retained routes
  reduce the open frontier to the missing nonzero current `J_chi`
- the retained atmospheric scale plus retained normal ordering force bounded
  neutrino-observable statements, including `Σm_ν > 50.58 meV`,
  `m_β ≤ 50.58 meV`, and `m_ββ ≤ 50.58 meV`; these are not point predictions
  for the solar gap, PMNS angles, or Majorana phases

Start with:

- [DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md](../../DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md)
- [NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md](../../NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md)
- [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](../../NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md)

Validate with:

- `python3 scripts/frontier_dm_leptogenesis_transport_status.py`
- `python3 scripts/frontier_dm_abcc_retained_measurement_closure_2026_04_21.py`
- `python3 scripts/frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py`
- `python3 scripts/frontier_neutrino_mass_reduction_to_dirac.py`
- `python3 scripts/frontier_pmns_selector_current_stack_zero_law.py`
- `python3 scripts/frontier_neutrino_retained_observable_bounds.py`

## Cosmology and Companion Phenomenology

- retained cosmology identities/corollaries:
  `Lambda_vac = lambda_1(S^3_R)`, `w = -1`, graviton spectral compactness-mass
  identity, the retained scalar/vector/TT compactness spectral towers, their
  pure-`Lambda` bridge with `m_TT(2)/m_vec(1)=sqrt(3)`, the exact
  `R_base = 31/9` group-theory support identity for the bounded
  DM/cosmology cascade, and the FRW kinematic reduction of `q_0`, `z_*`,
  `z_{mLambda}`, and asymptotic `H_inf` to the same open `H_inf/H_0` ratio,
  plus the early-time matter-radiation equality identity
  `1 + z_mr = Omega_m,0/Omega_r,0` and active-neutrino-count support for
  standard `N_eff = 3.046`
- bounded cosmology numerics:
  numerical `Lambda`, `Omega_Lambda`, numerical `m_g`, `n_s`, bounded `r`
- bounded phenomenology companions:
  proton lifetime, monopole mass, gravitational decoherence, GW echo null
  result, BH entropy companion

Start with:

- [PREDICTION_SURFACE_2026-04-15.md](./PREDICTION_SURFACE_2026-04-15.md)
- [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](../../COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
- [R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md](../../R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md)
- [OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md](../../OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md)
- [COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md](../../COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md)
- [MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- [N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md](../../N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md)
- [GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md](../../GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md)
- [VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE_2026-04-24.md](../../VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE_2026-04-24.md)
- [SCALAR_HARMONIC_TOWER_THEOREM_NOTE_2026-04-24.md](../../SCALAR_HARMONIC_TOWER_THEOREM_NOTE_2026-04-24.md)

Validate with:

- `python3 scripts/frontier_cosmological_constant_spectral_gap_identity.py`
- `python3 scripts/frontier_dark_energy_eos_retained_corollary.py`
- `python3 scripts/frontier_r_base_group_theory_derivation.py`
- `python3 scripts/frontier_omega_lambda_matter_bridge.py`
- `python3 scripts/frontier_cosmology_frw_kinematic_reduction.py`
- `python3 scripts/frontier_matter_radiation_equality_structural_identity.py`
- `python3 scripts/frontier_n_eff_from_three_generations.py`
- `python3 scripts/frontier_graviton_spectral_tower.py`
- `python3 scripts/frontier_vector_gauge_field_kk_tower.py`
- `python3 scripts/frontier_scalar_harmonic_tower.py`
- `python3 scripts/frontier_gravity_cosmology_tower_lambda_spectral_bridge.py`
- `python3 scripts/frontier_tensor_scalar_ratio_consolidation.py`

## Validation Paths

- fastest public overview:
  [README.md](../../../README.md),
  [README.md](./README.md),
  [PREDICTION_SURFACE_2026-04-15.md](./PREDICTION_SURFACE_2026-04-15.md)
- paper-facing claim/evidence path:
  [CLAIMS_TABLE.md](./CLAIMS_TABLE.md),
  [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md),
  [RESULTS_INDEX.md](./RESULTS_INDEX.md)
- reproduction path:
  [REPRODUCE.md](./REPRODUCE.md),
  [RELEASE_ENVIRONMENT.md](./RELEASE_ENVIRONMENT.md)
- reusable theorem/value path:
  [DERIVATION_ATLAS.md](./DERIVATION_ATLAS.md),
  [USABLE_DERIVED_VALUES_INDEX.md](./USABLE_DERIVED_VALUES_INDEX.md)

## Package Rule

- if a lane is manuscript-facing, it must appear in
  [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- if a lane is package-captured, it must appear in
  [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- if a lane is meant to be validated, it must be reachable from
  [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) and
  [REPRODUCE.md](./REPRODUCE.md)
