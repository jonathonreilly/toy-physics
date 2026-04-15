# Publication Matrix

**Date:** 2026-04-14  
**Purpose:** one canonical publication-capture table for the current flagship
paper package.

This matrix is stricter than a scorecard and broader than the retained theorem
surface. Every publication-relevant workstream audited across the current remote
branches should appear here exactly once with one of four dispositions:

- `promoted`
- `bounded`
- `open`
- `frozen-out`

Use this file together with:

- [REMOTE_BRANCH_AUDIT_2026-04-14.md](./REMOTE_BRANCH_AUDIT_2026-04-14.md)
- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)
- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- [PUBLICATION_CONTROL_PLANE.md](./PUBLICATION_CONTROL_PLANE.md)

## Capture Coverage

| Local package surface | Main contribution to publication package | Capture status |
|---|---|---|
| retained local authority notes | current theorem core and retained manuscript-facing rows | fully captured |
| bounded local authority notes | current EW / `y_t` / Higgs, DM, CKM, cosmology, and sharp companion rows | captured through bounded or frozen-out rows |
| local historical notes and inventories | route history and planning material | captured as superseded or non-authority history |

## A. Promoted retained publication core

| Lane | Result | Best current value / statement | Status | Import class | Placement | Authority | Validation / runner |
|---|---|---|---|---|---|---|---|
| Framework | `Cl(3)` on `Z^3` is the working physical theory | ontological framework sentence | promoted | framework axiom | main text | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | framework-level audit |
| Gravity | weak-field Poisson / Newton chain | Poisson uniqueness and inverse-square Newton law | promoted | zero-input structural | main text | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | `frontier_self_consistent_field_equation.py`, `frontier_poisson_exhaustive_uniqueness.py`, `frontier_newton_derived.py` |
| Gravity corollary | weak-field WEP | retained corollary on same action surface | promoted | zero-input structural | main text / ED | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md) | `frontier_broad_gravity.py` |
| Gravity corollary | weak-field time dilation | retained corollary on same action surface | promoted | zero-input structural | main text / ED | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md) | `frontier_broad_gravity.py` |
| Strong-field gravity | restricted strong-field closure | exact on current star-supported finite-rank class under static conformal bridge | promoted | zero-input structural | Extended Data / arXiv theorem box | [RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](../../RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md) | `frontier_oh_static_constraint_lift.py`, `frontier_oh_schur_boundary_action.py`, `frontier_star_supported_bridge_class.py` |
| Gravity | full discrete `3+1` GR on the project route | exact global Lorentzian Einstein/Regge stationary action family on `PL S^3 x R` | promoted | zero-input structural | main text / theorem box | [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](../../UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md) | `frontier_universal_gr_discrete_global_closure.py`, `frontier_universal_gr_lorentzian_global_atlas_closure.py`, `frontier_universal_gr_lorentzian_signature_extension.py` |
| Quantum-gravity support | UV-finite partition-density family on the project route | exact finite-dimensional partition-density family on discrete `3+1` route; mean/stationary sector equals the discrete Einstein/Regge stationary family on `PL S^3 x R` | promoted | zero-input structural | Extended Data / arXiv theorem box | [UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md](../../UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md) | `frontier_universal_qg_uv_finite_partition.py` |
| Quantum-gravity support | canonical geometric refinement net on the project route | exact barycentric spatial plus dyadic time refinement net on `PL S^3 x R`; local density/section pullback and Schur pushforward are exact on that net | promoted | zero-input structural | Extended Data / arXiv theorem box | [UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md](../../UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md) | `frontier_universal_qg_canonical_refinement_net.py` |
| Quantum-gravity support | inverse-limit Gaussian cylinder closure on the project route | exact projective-limit Gaussian cylinder family with compatible stationary section and refinement-independent cylindrical observables on the canonical barycentric-dyadic net | promoted | zero-input structural | Extended Data / arXiv theorem box | [UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md](../../UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md) | `frontier_universal_qg_inverse_limit_closure.py` |
| Quantum-gravity support | abstract Gaussian / Cameron-Martin completion on the project route | exact abstract Gaussian limit object with refinement-independent covariance bilinear form and compatible mean functional on the canonical barycentric-dyadic net | promoted | zero-input structural | Extended Data / arXiv theorem box | [UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md](../../UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md) | `frontier_universal_qg_abstract_gaussian_completion.py` |
| Quantum-gravity support | project-native PL field realization on the project route | exact canonical piecewise-linear carrier for the Gaussian limit object on the canonical barycentric-dyadic net | promoted | zero-input structural | Extended Data / arXiv theorem box | [UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md](../../UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md) | `frontier_universal_qg_pl_field_interface.py` |
| Quantum-gravity support | project-native PL weak/Dirichlet-form closure on the project route | exact canonical coercive weak/Dirichlet system for the Gaussian limit object on the canonical barycentric-dyadic net | promoted | zero-input structural | Extended Data / arXiv theorem box | [UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md](../../UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md) | `frontier_universal_qg_pl_weak_form.py` |
| Quantum-gravity support | project-native PL `H^1`-type Sobolev interface on the project route | exact canonical first-order weak-field carrier for the Gaussian/Dirichlet limit object on the canonical barycentric-dyadic net | promoted | zero-input structural | Extended Data / arXiv theorem box | [UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md](../../UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md) | `frontier_universal_qg_pl_sobolev_interface.py` |
| Quantum-gravity support | external FE/Galerkin smooth weak-field and Gaussian measure equivalence for a chosen external target on the project route | exact project-native PL weak Gaussian Sobolev completion is the FE/Galerkin cylinder realization of a chosen external smooth Sobolev weak-field and Gaussian measure formulation on the same topology | promoted | zero-input structural | Extended Data / arXiv theorem box | [UNIVERSAL_QG_EXTERNAL_FE_SMOOTH_EQUIVALENCE_NOTE.md](../../UNIVERSAL_QG_EXTERNAL_FE_SMOOTH_EQUIVALENCE_NOTE.md) | `frontier_universal_qg_external_fe_smooth_equivalence.py` |
| Gauge | exact native `SU(2)` | exact cubic `Cl(3)` / weak algebra | promoted | zero-input structural | main text | [BOUNDED_NATIVE_GAUGE_NOTE.md](../../BOUNDED_NATIVE_GAUGE_NOTE.md) | `frontier_non_abelian_gauge.py` |
| Gauge | graph-first structural `SU(3)` | retained selector + commutant closure | promoted | zero-input structural | main text | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | `frontier_graph_first_su3_integration.py` |
| Matter/gauge corollary | left-handed charge matching | retained `+1/3` / `-1` surface | promoted | zero-input structural | main text / SI | [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](../../LEFT_HANDED_CHARGE_MATCHING_NOTE.md) | `frontier_graph_first_su3_integration.py` |
| Spacetime | anomaly-forced `3+1` | retained single-clock codimension-1 theorem | promoted | zero-input structural | main text | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md) | `frontier_anomaly_forces_time.py` |
| Electroweak hierarchy | electroweak scale `v` | `245.080424447914 GeV` vs `246.22 GeV` (`-0.4628%`) | promoted | zero electroweak input | main text / ED theorem box | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) | `frontier_hierarchy_observable_principle_from_axiom.py` |
| Topology | retained `S^3` compactification / topology closure | compact cone-cap family retained as `PL S^3` on accepted bar | promoted | zero-input structural | main text / SI theorem box | [S3_GENERAL_R_DERIVATION_NOTE.md](../../S3_GENERAL_R_DERIVATION_NOTE.md), [S3_CAP_UNIQUENESS_NOTE.md](../../S3_CAP_UNIQUENESS_NOTE.md) | `frontier_s3_boundary_link_theorem.py`, `frontier_s3_cap_uniqueness.py`, `frontier_s3_general_r.py` |
| Matter | one-generation closure | left-handed surface + anomaly-fixed right-handed completion | promoted | zero-input structural | main text | [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](../../ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | `frontier_right_handed_sector.py`, `frontier_anomaly_forces_time.py` |
| Matter | three-generation structure | exact orbit algebra `8 = 1 + 1 + 3 + 3` | promoted | zero-input structural | main text | [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md) | `frontier_generation_fermi_point.py`, `frontier_generation_rooting_undefined.py`, `frontier_generation_axiom_boundary.py` |
| Exact support theorem | `I_3 = 0` | exact no-third-order-interference theorem | promoted | zero-input structural | main text / ED | [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md) | `frontier_born_rule_derived.py` |
| Exact support theorem | CPT | exact free staggered-lattice CPT | promoted | zero-input structural | main text / ED | [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md) | `frontier_cpt_exact.py` |

## B. Observation-facing quantitative portfolio

These rows are intentionally broader than the retained theorem core. They are
publication-relevant because reviewers will ask about them even when they are
not promoted.

| Quantity / lane | Workstream | Framework result | Observation / comparator | Status | Import class | Current publication decision | Authority / best source | Frozen-out ref |
|---|---|---|---|---|---|---|---|---|
| Dark matter ratio `R` | DM relic chain | `5.48` | `5.47` | bounded | one-parameter + imported perturbative pieces | arXiv companion only | [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md) | `F01` |
| `\Omega_\Lambda` conditional chain | cosmology from `R` | `0.686` | `0.685` | bounded/conditional | observed `\eta` + flatness + bounded `R` | arXiv companion only | [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md) | `F01`, `F04` |
| `\alpha_s(M_Z)` zero-import route | `y_t` / `\alpha_s` chain | `0.1181` | `0.1179` | bounded | zero-input chain, still bounded by review | review-only until closure | [YT_ZERO_IMPORT_CLOSURE_NOTE.md](../../YT_ZERO_IMPORT_CLOSURE_NOTE.md), [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md), [YT_VERTEX_POWER_DERIVATION.md](../../YT_VERTEX_POWER_DERIVATION.md) | `F02` |
| top mass `m_t` zero-import route | `y_t` / `\alpha_s` chain | `169.4 GeV` | `172.69 GeV` | bounded | zero-input 2-loop chain, still bounded | review-only until closure | [YT_ZERO_IMPORT_CLOSURE_NOTE.md](../../YT_ZERO_IMPORT_CLOSURE_NOTE.md), [YT_BOUNDARY_THEOREM.md](../../YT_BOUNDARY_THEOREM.md), [YT_EFT_BRIDGE_THEOREM.md](../../YT_EFT_BRIDGE_THEOREM.md) | `F02` |
| top mass `m_t` import-allowed route | gauge crossover route | `171.0 GeV` | `173.0 +/- 0.6 GeV` | bounded | imported matching coefficients | arXiv bounded appendix only | [YT_GAUGE_CROSSOVER_THEOREM.md](../../YT_GAUGE_CROSSOVER_THEOREM.md) | `F02` |
| CKM magnitudes | mass-basis NNI route | `|V_us|=0.2251`, `|V_cb|=0.0420`, `|V_ub|=0.00435` | PDG values `0.2243`, `0.0422`, `0.00382` | bounded | framework + bounded coefficient route | arXiv bounded appendix only | [CABIBBO_BOUND_NOTE.md](../../CABIBBO_BOUND_NOTE.md), [CKM_MASS_BASIS_NNI_NOTE.md](../../CKM_MASS_BASIS_NNI_NOTE.md) | `F03` |
| Jarlskog invariant | Z3 CP phase route | `3.145 x 10^-5` | `3.08 x 10^-5` | bounded / partial | derived phase + observed angles | bounded companion only | [JARLSKOG_PHASE_BOUND_NOTE.md](../../JARLSKOG_PHASE_BOUND_NOTE.md) | `F03` |
| Spectral tilt `n_s` | graph-growth cosmology | `0.9667` | `0.9649 +/- 0.0042` | bounded/conditional | growth-model assumptions | arXiv companion only | [PRIMORDIAL_SPECTRUM_NOTE.md](../../PRIMORDIAL_SPECTRUM_NOTE.md) | `F04` |
| Dark energy EOS `w` | spectral-gap cosmology | `w = -1` exactly | observationally near `-1` | bounded/conditional | topology/cosmology dependent | arXiv companion only | [DARK_ENERGY_EOS_NOTE.md](../../DARK_ENERGY_EOS_NOTE.md) | `F04` |
| Cosmological constant `\Lambda` | spectral-gap cosmology | `1.59 x 10^-52 m^-2` | `1.09 x 10^-52 m^-2` | bounded/conditional | depends on `S^3` / Hubble-scale identification | arXiv companion only | [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md) | `F04` |
| graviton mass `m_g` | `S^3` / topology cosmology | `3.52 x 10^-33 eV` | strongest current bound `m_g < 1.76 x 10^-23 eV` | bounded/conditional | conditional on retained `S^3` + observed `H_0` | arXiv companion only | [GRAVITON_MASS_DERIVED_NOTE.md](../../GRAVITON_MASS_DERIVED_NOTE.md) | `F04` |
| Higgs mass `m_H` | Higgs / CW lane | mechanism derived; exact mass bounded | `125 GeV` | open/bounded | multiple remaining assumptions and route ambiguity | not for flagship promotion | [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md), [HIGGS_MECHANISM_NOTE.md](../../HIGGS_MECHANISM_NOTE.md), [HIGGS_FROM_LATTICE_NOTE.md](../../HIGGS_FROM_LATTICE_NOTE.md) | `F05` |
| Bekenstein-Hawking entropy | BH entropy companion | `S/S_max = 0.2364` (`5.4%` from `1/4`) | BH area law target | bounded | companion identification layer | arXiv companion only | [BH_ENTROPY_DERIVED_NOTE.md](../../BH_ENTROPY_DERIVED_NOTE.md) | `F07` |
| gravitational decoherence | BMV-class gravity companion | `\gamma = 0.253 Hz`, `\Phi_{ent} = 12.4 rad` (BMV benchmark) | no direct measurement yet; benchmark budget `\gamma_{tot} < 0.5 Hz` | bounded | derived gravity chain + experimental benchmark geometry | later companion or arXiv appendix | [GRAV_DECOHERENCE_DERIVED_NOTE.md](../../GRAV_DECOHERENCE_DERIVED_NOTE.md) | `F07` |
| Proton lifetime | proton decay companion | `\tau_p ~ 4 x 10^47 yr` | lower bounds only | bounded sharp prediction | imported EFT decay-rate layer | later companion or arXiv appendix | [PROTON_LIFETIME_DERIVED_NOTE.md](../../PROTON_LIFETIME_DERIVED_NOTE.md) | `F07` |
| Lorentz-violation fingerprint | Lorentz companion | cubic `(E/E_{Pl})^2` fingerprint | experimental bounds only | bounded sharp prediction | companion phenomenology | later companion or arXiv appendix | [LORENTZ_VIOLATION_DERIVED_NOTE.md](../../LORENTZ_VIOLATION_DERIVED_NOTE.md) | `F07` |
| Magnetic monopole mass | monopole companion | `1.43 M_{Pl}` | lower bounds only | bounded sharp prediction | companion phenomenology | later companion or arXiv appendix | [MONOPOLE_DERIVED_NOTE.md](../../MONOPOLE_DERIVED_NOTE.md) | `F07` |
| GW echo null result | frozen-star / echo companion | no detectable echoes; the evanescent barrier drives coherent return effectively to zero | full-catalog stack remains null (`0.41 sigma` frozen-star, `1.29 sigma` Abedi-style) | bounded / off-scope companion | strong-field compact-object identification layer | later companion paper only | [GW_ECHO_NULL_RESULT_NOTE.md](../../GW_ECHO_NULL_RESULT_NOTE.md) | `F07` |

## C. Live flagship gates

| Gate | Best current read | Status | Main blocker | Best current branch / authority |
|---|---|---|---|---|
| DM relic mapping | structural ratio is strong; full relic bridge still bounded | open | graph-to-relic transport / normalization closure | [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md), [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md) |
| Renormalized `y_t` matching | zero-import 2-loop route now reaches `m_t = 169.4 GeV`; import-allowed route stays near `171 GeV` | open | current canonical component stack still keeps the low-energy bridge bounded and the Higgs lane non-final | [YT_ZERO_IMPORT_CLOSURE_NOTE.md](../../YT_ZERO_IMPORT_CLOSURE_NOTE.md), [YT_BOUNDARY_THEOREM.md](../../YT_BOUNDARY_THEOREM.md), [YT_EFT_BRIDGE_THEOREM.md](../../YT_EFT_BRIDGE_THEOREM.md), [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md), [YT_VERTEX_POWER_DERIVATION.md](../../YT_VERTEX_POWER_DERIVATION.md), [YT_GAUGE_CROSSOVER_THEOREM.md](../../YT_GAUGE_CROSSOVER_THEOREM.md), [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md), [HIGGS_MECHANISM_NOTE.md](../../HIGGS_MECHANISM_NOTE.md), [HIGGS_FROM_LATTICE_NOTE.md](../../HIGGS_FROM_LATTICE_NOTE.md) |
| CKM / quantitative flavor | some bounded magnitude matches are strong; phase/ab initio closure still absent | open | quantitative coefficient and phase closure | [CABIBBO_BOUND_NOTE.md](../../CABIBBO_BOUND_NOTE.md), [CKM_MASS_BASIS_NNI_NOTE.md](../../CKM_MASS_BASIS_NNI_NOTE.md), [JARLSKOG_PHASE_BOUND_NOTE.md](../../JARLSKOG_PHASE_BOUND_NOTE.md) |

## D. Workstreams intentionally frozen out of the flagship paper

| Workstream family | Why not in flagship paper | Registry entry |
|---|---|---|
| DM quantitative companion portfolio | bounded relic bridge | `F01` |
| `y_t` / `\alpha_s` quantitative companion portfolio | still a live gate | `F02` |
| CKM / flavor quantitative companion portfolio | still a live gate | `F03` |
| cosmology companion portfolio | conditional / bounded | `F04` |
| Higgs and mass-spectrum portfolio | not closed | `F05` |
| continuum / unrestricted gravity beyond the project's discrete `3+1` route, plus comparison to more canonical external continuum weak/measure formulations beyond the chosen external smooth FE/Galerkin realization of the exact discrete project-native PL weak Gaussian Sobolev completion | bounded / later-paper material | `F06` |
| sharp companion predictions (proton, Lorentz, BH, decoherence, monopole, null-echo phenomenology) | companion-only material | `F07` |
| branch-local inventories and stale strategy docs | inventory only, not authority | `F08` |

## Matrix rule

If a result family is not listed here, it is not yet publication-captured.

If it is listed here but not in [CLAIMS_TABLE.md](./CLAIMS_TABLE.md), then it is
not on the retained flagship claim surface.
