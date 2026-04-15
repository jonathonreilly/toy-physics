# Full Claim Ledger

**Date:** 2026-04-14  
**Purpose:** narrative companion to the
[PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md).

The matrix is the canonical one-line capture surface. This ledger explains the
publication decision behind each captured family and makes the paper framework
explicitly cover the same science inventory.

If the matrix and this ledger ever disagree, the matrix wins until this ledger
is updated.

Use this file together with:

- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)
- [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md)
- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
- [PUBLICATION_CONTROL_PLANE.md](./PUBLICATION_CONTROL_PLANE.md)

## 1. How to read the package

The publication package now has four distinct layers:

1. **Retained core**
   - the claims the flagship paper may carry directly
2. **Observation-facing bounded portfolio**
   - quantitatively important results that reviewers will ask about even when
     they are not promoted
3. **Live flagship gates**
   - open lanes whose closure would materially change the paper
4. **Frozen-out families**
   - scientifically relevant work that is intentionally excluded from the
     flagship surface, but recorded so it is not lost

This ledger mirrors those four layers directly.

Positioning note: this package is deliberately narrower than a survey of all
discrete or unification programs. It compares against the standard alternatives
only at the level needed to justify the retained backbone and the bounded
companion portfolio.

## 2. Retained core aligned to the matrix

These rows correspond to Section A of
[PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md).

### Framework and spacetime backbone

| Claim family | Current decision | Why it is retained | Primary authority |
|---|---|---|---|
| `Cl(3)` on `Z^3` is the working physical theory | promoted | framework sentence and ontological surface for the manuscript | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) |
| anomaly-forced `3+1` | promoted | single-clock codimension-1 theorem survives direct audit | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md) |
| retained `S^3` compactification / topology closure | promoted | cone-cap family now clears the accepted topology bar and is no longer a live gate | [S3_GENERAL_R_DERIVATION_NOTE.md](../../S3_GENERAL_R_DERIVATION_NOTE.md), [S3_CAP_UNIQUENESS_NOTE.md](../../S3_CAP_UNIQUENESS_NOTE.md) |

### Gravity

| Claim family | Current decision | Why it is retained | Primary authority |
|---|---|---|---|
| weak-field Poisson / Newton chain | promoted | unique self-consistent local field equation plus lattice Green-function Newton law | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) |
| weak-field WEP | promoted corollary | survives on the same retained action surface | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md) |
| weak-field time dilation | promoted corollary | survives on the same retained action surface | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md) |
| restricted strong-field closure | promoted restricted theorem | exact on the current star-supported finite-rank class under the static conformal bridge; important enough to retain, but still source-class restricted | [RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](../../RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md) |
| full discrete `3+1` GR on the project route | promoted exact theorem | exact global Lorentzian Einstein/Regge stationary action family on `PL S^3 x R`; this is the direct-universal capstone on the discrete route | [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](../../UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md) |
| UV-finite partition-density family on the project route | promoted exact companion | the direct-universal GR action already defines an exact finite-dimensional partition-density family on the project’s discrete `3+1` route, and its mean/stationary sector is exactly the same discrete Einstein/Regge stationary family | [UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md](../../UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md) |
| canonical geometric refinement net on the project route | promoted exact companion | the exact discrete partition-density and stationary-section family sits on a canonical barycentric-dyadic refinement net on `PL S^3 x R`, supplying the geometric backbone for the now-closed inverse-limit, PL weak/Sobolev, and chosen canonical textbook continuum bridge chain | [UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md](../../UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md) |
| inverse-limit Gaussian cylinder closure on the project route | promoted exact companion | the canonical barycentric-dyadic discrete family now closes as a consistent inverse-limit Gaussian cylinder system with compatible stationary section and refinement-independent cylindrical observables | [UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md](../../UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md) |
| abstract Gaussian / Cameron-Martin completion on the project route | promoted exact companion | the exact inverse-limit Gaussian cylinder family already determines a refinement-independent covariance bilinear form, compatible stationary mean functional, and one abstract Gaussian limit object on the project route | [UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md](../../UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md) |
| project-native PL field realization on the project route | promoted exact companion | the exact abstract Gaussian limit object already has a canonical piecewise-linear field realization on the canonical barycentric-dyadic `PL S^3 x R` net | [UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md](../../UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md) |
| project-native PL weak/Dirichlet-form closure on the project route | promoted exact companion | the exact project-native PL carrier already supports a canonical coercive weak/Dirichlet form and exact stationary weak equation compatible with Schur coarse-graining | [UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md](../../UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md) |
| project-native PL `H^1`-type Sobolev interface on the project route | promoted exact companion | the exact project-native PL weak/Dirichlet system already has a canonical first-order weak-field carrier with refinement-invariant energy on the canonical barycentric-dyadic `PL S^3 x R` net | [UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md](../../UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md) |
| external FE/Galerkin smooth weak-field and Gaussian measure equivalence for a chosen external target on the project route | promoted exact companion | the exact project-native PL weak Gaussian Sobolev completion is already exactly the FE/Galerkin cylinder realization of a chosen external smooth Sobolev weak-field and Gaussian measure formulation on the same topology | [UNIVERSAL_QG_EXTERNAL_FE_SMOOTH_EQUIVALENCE_NOTE.md](../../UNIVERSAL_QG_EXTERNAL_FE_SMOOTH_EQUIVALENCE_NOTE.md) |
| canonical textbook weak/measure equivalence on the project route | promoted exact companion | the exact project-native PL weak Gaussian Sobolev completion is already canonically equivalent to the standard textbook closed-coercive weak Sobolev / Gaussian cylinder object on the completed carrier | [UNIVERSAL_QG_CANONICAL_TEXTBOOK_WEAK_MEASURE_EQUIVALENCE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_WEAK_MEASURE_EQUIVALENCE_NOTE.md) |
| smooth local gravitational weak/Gaussian identification on the project route | promoted exact companion | on the exact positive-background local class, the canonical textbook weak/Gaussian object is already exactly the local smooth gravitational weak/Gaussian object of the direct-universal route | [UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_LOCAL_IDENTIFICATION_NOTE.md](../../UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_LOCAL_IDENTIFICATION_NOTE.md) |
| smooth finite-atlas gravitational stationary-family identification on the project route | promoted exact companion | the canonical textbook weak/Gaussian object already patches as the same smooth finite-atlas gravitational stationary family on the chosen smooth realization | [UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_ATLAS_NOTE.md](../../UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_ATLAS_NOTE.md) |
| smooth global weak gravitational stationary/Gaussian solution class on the project route | promoted exact companion | the canonical textbook weak/Gaussian object already closes as one smooth global weak gravitational stationary/Gaussian solution class on the chosen realization of `PL S^3 x R` | [UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md](../../UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md) |
| canonical smooth gravitational weak/measure equivalence on the project route | promoted exact companion | the chosen smooth global gravitational weak/Gaussian realization is already exactly the same canonical textbook weak/Gaussian object, not an additional continuum target choice | [UNIVERSAL_QG_CANONICAL_SMOOTH_GRAVITATIONAL_WEAK_MEASURE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_SMOOTH_GRAVITATIONAL_WEAK_MEASURE_NOTE.md) |
| canonical smooth geometric/action equivalence on the project route | promoted exact companion | the chosen smooth realization already carries one canonical project-native geometric/action family whose convex positive sector is the canonical weak/Gaussian QG route and whose Lorentzian sector is the exact discrete Einstein/Regge stationary route | [UNIVERSAL_QG_CANONICAL_SMOOTH_GEOMETRIC_ACTION_NOTE.md](../../UNIVERSAL_QG_CANONICAL_SMOOTH_GEOMETRIC_ACTION_NOTE.md) |
| canonical textbook Einstein-Hilbert-style geometric/action equivalence on the project route | promoted exact companion | the already-closed project-native smooth geometric/action family is already one canonical textbook Einstein-Hilbert-style weak/stationary action family on the chosen smooth realization | [UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md) |
| canonical textbook continuum gravitational closure on the project route | promoted exact companion | the direct-universal route already closes as one canonical textbook continuum gravitational weak/stationary action family on the chosen smooth realization of `PL S^3 x R` | [UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md) |
| continuum identification positioning across gravity and gauge | promoted positioning row | this is the package-level synthesis note: gravity is exact on the chosen canonical textbook target, while the gauge side is positioned through the retained structural `SU(3)` / Wilson / `\alpha_s` / universality-EFT bridge; it is intentionally not a replacement for the underlying theorem rows | [CONTINUUM_IDENTIFICATION_NOTE.md](../../CONTINUUM_IDENTIFICATION_NOTE.md) |

### Gauge and matter structure

| Claim family | Current decision | Why it is retained | Primary authority |
|---|---|---|---|
| exact native `SU(2)` | promoted | exact weak algebra on the cubic Clifford surface | [BOUNDED_NATIVE_GAUGE_NOTE.md](../../BOUNDED_NATIVE_GAUGE_NOTE.md) |
| graph-first structural `SU(3)` | promoted | selector + commutant closure now defines the safe `SU(3)` statement; selector is unique up to graph automorphism | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| `SU(3)` confinement / `\sqrt{\sigma}` | promoted structural theorem + bounded quantitative prediction | graph-first `SU(3)` at canonical `g_bare^2 = 1` gives Wilson `beta = 6`; `T = 0` confinement is structural on that gauge sector, and the bounded string-tension readout is `\sqrt{\sigma} \approx 465 MeV` through the retained `\alpha_s` lane plus the standard low-energy EFT bridge | [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md) |
| left-handed charge matching | promoted corollary | safe selected-axis charge surface on the retained graph-first package | [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](../../LEFT_HANDED_CHARGE_MATCHING_NOTE.md) |
| one-generation closure | promoted | anomaly-complete right-handed completion now survives direct audit | [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](../../ONE_GENERATION_MATTER_CLOSURE_NOTE.md) |
| three-generation structure | promoted | exact orbit algebra `8 = 1 + 1 + 3 + 3` is retained as physical species structure, not as a taste artifact | [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md) |
| strong CP / `θ_eff = 0` | promoted exact structural theorem | the axiom-determined Wilson-plus-staggered action leaves no bare `θ`, the real-mass staggered determinant carries no phase, and CKM CP remains weak-sector only | [STRONG_CP_THETA_ZERO_NOTE.md](../../STRONG_CP_THETA_ZERO_NOTE.md) |

### Electroweak hierarchy and exact companions

| Claim family | Current decision | Why it is retained | Primary authority |
|---|---|---|---|
| electroweak scale `v` | promoted | exact minimal hierarchy theorem plus axiom-native observable principle now clear the paper bar; the numerical value is a pinned evaluation on the current `u_0` / plaquette surface | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) |
| exact `I_3 = 0` | promoted exact companion | safe statement is exact no-third-order interference on the Hilbert surface | [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md) |
| exact CPT | promoted exact companion | exact free staggered-lattice theorem on the retained framework surface | [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md) |
| emergent Lorentz invariance | promoted exact structural theorem | exact `O_h` symmetry and exact CPT/P protection force the first anisotropic correction to appear only at dimension 6 with unique `\ell = 4` cubic-harmonic signature; on the retained hierarchy surface the correction is `(E/M_{Pl})^2` suppressed | [EMERGENT_LORENTZ_INVARIANCE_NOTE.md](../../EMERGENT_LORENTZ_INVARIANCE_NOTE.md) |

## 3. Observation-facing bounded portfolio aligned to the matrix

These rows correspond to Section B of
[PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md). They matter because an
external reviewer will ask about them whether or not they are retained.

### DM and cosmology companions

| Quantity / lane | Current decision | Why not promoted | Primary authority | Matrix / freeze reference |
|---|---|---|---|---|
| Dark matter ratio `R` | bounded | structurally strong, but still tied to bounded relic/transport bridge | [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md) | matrix row `Dark matter ratio \`R\``, `F01` |
| `\Omega_\Lambda` conditional chain | bounded/conditional | after the fixed-gap/de-Sitter scale reduction, the remaining blocker is present matter content, so this row is now primarily the DM/matter bridge question | [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md), [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md) | matrix row `\Omega_\Lambda conditional chain`, `F01`, `F04` |
| Spectral tilt `n_s` | bounded/conditional | cosmology bridge remains conditional | [PRIMORDIAL_SPECTRUM_NOTE.md](../../PRIMORDIAL_SPECTRUM_NOTE.md) | matrix row `Spectral tilt \`n_s\``, `F04` |
| Dark energy EOS `w` | bounded/conditional | now best read as the EOS face of the same fixed-gap vacuum-scale route rather than a separate blocker | [DARK_ENERGY_EOS_NOTE.md](../../DARK_ENERGY_EOS_NOTE.md), [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md) | matrix row `Dark energy EOS \`w\``, `F04` |
| Cosmological constant `\Lambda` | bounded/conditional | exact retained-topology spectral-gap coefficient, with the remaining nontrivial step now narrowed to cosmological scale identification on the same vacuum surface | [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md), [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md) | matrix row `Cosmological constant \`\Lambda\``, `F04` |
| graviton mass `m_g` | bounded/conditional | sharp conditional prediction, now best read as another consequence of the same fixed `1/R^2` vacuum/topology scale | [GRAVITON_MASS_DERIVED_NOTE.md](../../GRAVITON_MASS_DERIVED_NOTE.md), [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md) | matrix row `graviton mass \`m_g\``, `F04` |

### Quantitative component stack

| Quantity / lane | Current decision | Why not promoted | Primary authority | Matrix / freeze reference |
|---|---|---|---|---|
| `alpha_s(M_Z)` | retained quantitative lane | standalone strong-coupling lane on `main` | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) | matrix row `\alpha_s(M_Z)`, n/a |
| EW normalization package | retained quantitative lane | standalone EW lane on `main`; independent of the Yukawa/Higgs chain | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) | matrix row `EW normalization package`, n/a |
| Yukawa / top package | bounded quantitative lane | zero SM imports, but still carries an approximately `3%` QFP/RGE-surrogate systematic | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md) | matrix row `Yukawa / top package`, n/a |

### Flavor / CKM portfolio

| Quantity / lane | Current decision | Why not promoted | Primary authority | Matrix / freeze reference |
|---|---|---|---|---|
| CKM closure package | closed promoted quantitative package | full no-import CKM package is now carried by the canonical CMT coupling, exact atlas counts, exact `1/6` projector, exact bilinear tensor carrier `K_R`, exact `Z_3` source, and exact Schur cascade; older bounded Cabibbo/NNI/Jarlskog notes are superseded as authority | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) | matrix row `CKM closure package`, n/a |

### Higgs and individual companion lanes

| Quantity / lane | Current decision | Why not promoted | Primary authority | Matrix / freeze reference |
|---|---|---|---|---|
| Higgs / vacuum package | bounded quantitative lane | mechanism derived and the framework-native 3-loop Higgs computation now exists, but exact mass and vacuum readout still inherit the bounded Yukawa / QFP route | [HIGGS_VACUUM_PROMOTED_NOTE.md](../../HIGGS_VACUUM_PROMOTED_NOTE.md) | matrix row `Higgs / vacuum package`, n/a |
| Bekenstein-Hawking entropy | bounded companion lane | useful companion signal, not part of flagship theorem spine | [BH_ENTROPY_DERIVED_NOTE.md](../../BH_ENTROPY_DERIVED_NOTE.md) | matrix row `Bekenstein-Hawking entropy` |
| gravitational decoherence | bounded companion lane | concrete BMV-class benchmark prediction, but still companion-only and unmeasured | [GRAV_DECOHERENCE_DERIVED_NOTE.md](../../GRAV_DECOHERENCE_DERIVED_NOTE.md) | matrix row `gravitational decoherence` |
| Proton lifetime | bounded companion lane | later companion or appendix material, not flagship core | [PROTON_LIFETIME_DERIVED_NOTE.md](../../PROTON_LIFETIME_DERIVED_NOTE.md) | matrix row `Proton lifetime` |
| Vacuum critical stability | bounded companion lane | extracted from the bounded Higgs / vacuum package and useful as a discriminator, but still inherits the bounded Yukawa / Higgs route | [VACUUM_CRITICAL_STABILITY_NOTE.md](../../VACUUM_CRITICAL_STABILITY_NOTE.md) | matrix row `Vacuum critical stability` |
| Magnetic monopole mass | bounded companion lane | imported phenomenology layer still present | [MONOPOLE_DERIVED_NOTE.md](../../MONOPOLE_DERIVED_NOTE.md) | matrix row `Magnetic monopole mass` |
| GW echo null result | bounded / off-scope companion lane | later work resolved the compact-object echo question to observational silence rather than a positive timing prediction; this remains companion-only material | [GW_ECHO_NULL_RESULT_NOTE.md](../../GW_ECHO_NULL_RESULT_NOTE.md) | matrix row `GW echo null result` |

## 4. Live flagship gates aligned to the matrix

These rows correspond to Section C of
[PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md).

| Gate | Current best read | Why still open | Main authority |
|---|---|---|---|
| DM relic mapping | structural ratio is strong, full relic bridge still bounded | graph-to-relic transport and normalization closure still missing | [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md), [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md) |

## 5. Frozen-out families aligned to the matrix

These rows correspond to Section D of
[PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md) and the family details in
[FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md).

| Frozen family | Current decision | Why frozen out | Registry ref |
|---|---|---|---|
| DM quantitative companion portfolio | frozen-out of flagship core | bounded relic bridge even though several numbers are strong | `F01` |
| superseded YT / EW / Higgs route-history stack | frozen-out as authority | useful for audit, unsafe as publication authority after the promoted quantitative package landed on `main` | `F02` |
| older CKM bounded route-history portfolio | frozen-out as superseded authority | retained only as route history after the promoted CKM closure package landed on `main` | `F03` |
| cosmology companion portfolio | frozen-out of flagship core | conditional/bounded companion layer | `F04` |
| Higgs and mass-spectrum companions beyond the promoted package | frozen-out of flagship core | the promoted Higgs/vacuum package is live, but the broader mass-spectrum and neutrino programs remain outside the flagship spine | `F05` |
| gravity companions beyond the retained core | frozen-out of flagship core | weak-field GR-signature companions and broader non-flagship gravity phenomenology remain outside the flagship core even though the direct-universal discrete GR and canonical textbook continuum-QG route are now promoted | `F06` |
| branch-local inventories and stale strategy docs | frozen-out as authority | useful for capture, unsafe as publication authority | `F08` |

## 6. Historical and stale surfaces not to confuse with the matrix

These are not missing science. They are just not part of the current flagship
paper authority path.

| Surface | Current status | Why it is not authority |
|---|---|---|
| older review packets and publication cards | stale / not-for-paper | often outran the audited claim surface |
| older bounded-only `S^3` notes before the general-`R` / cap-uniqueness harmonization | historical | useful route history, no longer the controlling topology authority |
| older full-closure notes for DM, `y_t`, CKM, gauge normalization | stale / not-for-paper | routinely promoted bounded sub-results too aggressively |
| misnamed “Born rule derived” surfaces | stale naming | safe claim is exact `I_3 = 0`, not a standalone derivation of the full Born rule |
| branch-local scorecards and inventories | inventory only | helpful for capture, not safe manuscript authority |

## 7. Ledger rule

Before a claim enters the manuscript:

1. it must appear in [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
2. it must be classified here in the same bucket family
3. if it is manuscript-facing, it must also appear in
   [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
4. it must have a paired derivation/validation entry in
   [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)

If a reviewer can find a result in the repo but not in the matrix and not in
this ledger, the package is incomplete.
