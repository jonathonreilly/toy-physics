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
  emergent Lorentz invariance, exact evanescent-barrier transfer-matrix bound +
  tortoise-length identity, BH-entropy Widom no-go on the current carrier

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
  one-generation closure, three-generation observable/species closure,
  exact `I_3 = 0`, exact CPT, Bell/CHSH support on explicit two-species
  lattice systems
- retained package-support lanes:
  `g_bare = 1` structural normalization and two-Ward 1PI closure
- package-support atlas:
  taste-cube/residual-symmetry flavor support and `Cl(3) -> SM` algebraic
  support packet

Start with:

- [NATIVE_GAUGE_CLOSURE_NOTE.md](../../NATIVE_GAUGE_CLOSURE_NOTE.md)
- [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
- [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md)
- [STRONG_CP_THETA_ZERO_NOTE.md](../../STRONG_CP_THETA_ZERO_NOTE.md)

Validate with:

- `python3 scripts/frontier_non_abelian_gauge.py`
- `python3 scripts/frontier_graph_first_su3_integration.py`
- `python3 scripts/frontier_generation_fermi_point.py`
- `python3 scripts/frontier_three_generation_observable_theorem.py`
- `python3 scripts/frontier_strong_cp_theta_zero.py`

## Quantitative Electroweak, QCD, Yukawa, and Higgs Package

- retained quantitative lanes:
  `alpha_s(M_Z)`, EW normalization, retained YT/top transport
- promoted quantitative flavor lane:
  CKM atlas/axiom package
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
  is accepted as the gravitational boundary/action carrier, while the
  minimal-stack derivation of that carrier identification remains open; the
  finite-automorphism-only response route and carrier-only parent-source scalar
  route are closed negatively

Start with:

- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [USABLE_DERIVED_VALUES_INDEX.md](./USABLE_DERIVED_VALUES_INDEX.md)
- [PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md](../../PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md)
- [PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md](../../PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md)
- [PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md](../../PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
- [PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md](../../PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md)
- [PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md](../../PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md)

Validate with:

- `python3 scripts/frontier_complete_prediction_chain.py`
- `python3 scripts/frontier_yt_ward_identity_derivation.py`
- `python3 scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py`
- `python3 scripts/frontier_higgs_mass_full_3loop.py`
- `python3 scripts/frontier_planck_scale_program_audit.py`
- `python3 scripts/frontier_planck_conditional_completion_audit.py`
- `python3 scripts/frontier_planck_boundary_density_extension.py`
- `python3 scripts/frontier_planck_finite_response_nogo.py`
- `python3 scripts/frontier_planck_parent_source_hidden_character_nogo.py`

## Flavor, CP, and Charged-Lepton Structure

- promoted quantitative flavor package:
  CKM atlas/axiom closure
- bounded secondary flavor lanes:
  down-type CKM-dual mass-ratio lane, bounded quark support packet
- retained corollary:
  CKM-only neutron EDM on the retained `theta_eff = 0` surface
- open flagship package:
  charged-lepton Koide `Q = 2/3`, `delta = 2/9`

Current charged-lepton status:

- `Q = 2/3` support is strong, but the physical/source-law bridge remains open
- `delta = 2/9` support is strong, but the physical Brannen-phase bridge
  remains open
- the separate overall lepton scale `v_0` also remains open

Start with:

- [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md](../../KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md)
- [CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md](../../CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md)

Validate with:

- `python3 scripts/frontier_ckm_atlas_axiom_closure.py`
- `python3 scripts/frontier_ckm_no_import_audit.py`
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
  identity
- bounded cosmology numerics:
  numerical `Lambda`, `Omega_Lambda`, numerical `m_g`, `n_s`, bounded `r`
- bounded phenomenology companions:
  proton lifetime, monopole mass, gravitational decoherence, GW echo null
  result, BH entropy companion

Start with:

- [PREDICTION_SURFACE_2026-04-15.md](./PREDICTION_SURFACE_2026-04-15.md)
- [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](../../COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
- [OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md](../../OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md)

Validate with:

- `python3 scripts/frontier_cosmological_constant_spectral_gap_identity.py`
- `python3 scripts/frontier_dark_energy_eos_retained_corollary.py`
- `python3 scripts/frontier_omega_lambda_matter_bridge.py`
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
