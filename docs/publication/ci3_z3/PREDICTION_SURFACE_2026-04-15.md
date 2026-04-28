# Prediction Surface

**Date:** 2026-04-15  
**Purpose:** publication-facing summary of what the current `main` package
already predicts, how strongly each prediction is supported, and where the
current falsification surface actually lies.

This note is the shortest honest answer to:

> what does the current package already predict, beyond retrospective
> structural closure?

It is intentionally prediction-first: positive outputs, bounded companions,
structural signatures, and current pressure points are all part of the public
scientific surface.

## Reading Rule

The current package has four predictive layers:

1. retained quantitative outputs already safe for the paper surface;
2. bounded secondary predictions already worth stating explicitly;
3. structural predictions and signatures, including delayed-observability
   channels;
4. current pressure points and open bridges that define the falsification and
   completion surface.

The point of this split is simple: the framework is already predictive. The
paper should not read as if prediction begins only after every open bridge
closes.

## Retained quantitative outputs already on the paper surface

- electroweak hierarchy:
  - `v = 246.282818290129 GeV`
  - current comparator: `246.22 GeV`
  - authority:
    [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- strong coupling:
  - `alpha_s(M_Z) = 0.1181`
  - current comparator: `0.1179`
  - authority:
    [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md)
- EW normalization package:
  - `sin^2(theta_W)(M_Z) = 0.2306`
  - `1/alpha_EM(M_Z) = 127.67`
  - `g_1(v) = 0.4644`
  - `g_2(v) = 0.6480`
  - authority:
    [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md),
    [RCONN_DERIVED_NOTE.md](../../RCONN_DERIVED_NOTE.md)
- CKM atlas/axiom package on the canonical tensor/projector surface:
  - `lambda^2 = alpha_s(v)/2`
  - `A^2 = 2/3`
  - atlas-leading `|V_ud|_0 = 0.973824`
  - atlas-leading `|V_us|_0 = 0.22727`
  - atlas-leading `|V_cd|_0 = 0.22727`
  - atlas-leading `|V_cs|_0 = 0.97292`
  - `|V_cb| = 0.04217`
  - atlas-leading `|V_ub|_0 = 0.003913`
  - atlas-leading `|V_td|_0 = 0.008750`
  - atlas-leading `|V_ts|_0 = 0.04217`
  - atlas-leading `|V_tb|_0 = 0.99907`
  - atlas-leading B_s mixing phase
    `phi_s = -alpha_s(v) sqrt(5)/6 = -0.03850 rad`
  - Thales-mediated atlas-leading CP ratio
    `phi_s / sin(2 beta_d) = -alpha_s(v)/2 = -0.05165`
  - CP-product atlas-leading estimator
    `alpha_s(v) = (18/5) sin(2 beta_d) sin(2 beta_s)`, with
    PDG/LHCb 2024 baseline `0.098 +/- 0.056` versus canonical `0.10330`
  - kaon epsilon_K CKM-bracket factorization:
    `Im(lambda_c^2)=+2J_0`, `Im(lambda_c lambda_t)=-J_0`, and
    `Im(lambda_t^2)=-(5 alpha_s(v)^2/18)J_0` at atlas-leading order
  - NLO barred-triangle protected invariant
    `gamma_bar = gamma_0 = arctan(sqrt(5)) = 65.905 deg`, with
    `rho_bar = (4-alpha_s(v))/24`
  - `delta = arccos(1/sqrt(6)) = 65.905 deg`
  - `cos^2(delta) = 1/6`, `tan(delta) = sqrt(5)`
  - rescaled CKM atlas triangle: `alpha_0 = 90 deg`, `beta_0 =
    arctan(1/sqrt(5))`, `gamma_0 = arctan(sqrt(5))`, with finite-`lambda`
    barred-triangle corrections explicitly not promoted as an exact right angle
  - atlas/Wolfenstein area factor
    `J_0 = alpha_s(v)^3 sqrt(5)/72` (`3.4237 x 10^-5` on the
    retained `alpha_s(v)` surface), with the parent exact standard-matrix
    readout `J = 3.331 x 10^-5`
  - authority:
    [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md),
    [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md](../../WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md),
    [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md),
    [CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md),
    [CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md](../../CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md),
    [CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md),
    [CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md](../../CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md),
    [CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md](../../CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md),
    [CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md](../../CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md),
    [CKM_KAON_EPSILON_K_JARLSKOG_DECOMPOSITION_THEOREM_NOTE_2026-04-25.md](../../CKM_KAON_EPSILON_K_JARLSKOG_DECOMPOSITION_THEOREM_NOTE_2026-04-25.md),
    [CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md](../../CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
- confinement readout on top of the exact graph-first confinement theorem:
  - `sqrt(sigma) ≈ 465 MeV`
  - authority:
    [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md)
  - status boundary: bounded; the hadron-lane support audit isolates
    `(B2)` quenched-to-dynamical screening and `(B5)` framework-to-standard-YM
    validation as the remaining promotion gates.

These rows belong in the main manuscript quantitative section because they are
already part of the live paper surface.

## Sharp bounded secondary predictions already on `main`

These are not theorem-core rows, but they are real bounded predictions already
carried by the current package.

- proton lifetime:
  - `tau_p ~ 4 x 10^47 years`
  - on the current EFT bridge, observation of proton decay at any accessible
    lifetime scale would strongly disfavor the framework route
  - authority:
    [PROTON_LIFETIME_DERIVED_NOTE.md](../../PROTON_LIFETIME_DERIVED_NOTE.md)
- CKM-only neutron-EDM corollary on the retained `theta_eff = 0` surface:
  - exactly, `d_n(QCD) = 0` and the surviving neutron EDM is CKM-only
  - bounded continuation: `d_n(CKM) ~ 8 x 10^-33 e cm`
  - authority:
    [CKM_NEUTRON_EDM_BOUND_NOTE.md](../../CKM_NEUTRON_EDM_BOUND_NOTE.md)
- universal theta-induced EDM response:
  - exactly, every EDM component sourced by QCD `theta_eff` vanishes on the
    retained action surface
  - CKM weak EDMs and independent BSM CP-odd EFT sources are separate source
    directions and are not set to zero by this corollary
  - authority:
    [UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md](../../UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md)
- down-type flavor-mass CKM-dual lane:
  - `m_d/m_s = 0.05165`
  - `m_s/m_b = 0.02239`
  - `m_d/m_b = 0.001156`
  - current comparator: threshold-local self-scale down-type mass ratios
  - qualifier:
    threshold-local self-scale comparison is supported, but theorem-grade
    scale closure of the `5/6` bridge remains open
  - authority:
    [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](../../DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md)
- neutrino absolute-mass observable bounds:
  - `Σm_ν > 50.58 meV` as a strict retained-package floor
  - `m_β ≤ 50.58 meV` and `m_ββ ≤ 50.58 meV` as PMNS/phase-free ceilings
  - qualifier:
    these are bounds from the retained atmospheric scale plus retained normal
    ordering, not point predictions for the solar gap, PMNS angles, or
    Majorana phases
  - authority:
    [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](../../NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md)
- vacuum critical stability:
  - the current `lambda(M_Pl) = 0` route lands on the critical /
    non-metastable side of the usual Standard Model comparison surface
  - authority:
    [VACUUM_CRITICAL_STABILITY_NOTE.md](../../VACUUM_CRITICAL_STABILITY_NOTE.md)
- taste-scalar near-degeneracy companion:
  - exact taste-block fermion-CW isotropy plus bounded gauge-only split gives
    `m_taste = 124.91 GeV`
  - scalar-only thermal-cubic estimate gives `v_c/T_c = 0.3079`
  - authority:
    [TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md](../../TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md)
- benchmark gravitational decoherence:
  - at the original BMV geometry:
    - `gamma_grav = 0.253 Hz`
    - `Phi_ent = 12.4 rad`
  - authority:
    [GRAV_DECOHERENCE_DERIVED_NOTE.md](../../GRAV_DECOHERENCE_DERIVED_NOTE.md)
- magnetic monopole mass:
  - `M_mono ~ 0.80 M_Pl`
  - authority:
    [MONOPOLE_DERIVED_NOTE.md](../../MONOPOLE_DERIVED_NOTE.md)

These rows belong in a dedicated bounded-prediction section or appendix, not
in route history.

## Immediate falsification and pressure points

The prediction surface is not only the list of successful rows. It also
includes the places where the current package is already under quantitative or
conceptual pressure.

- hierarchy lane:
  the canonical electroweak row is numerically sharp, but the current package
  still imports `M_Pl` and still does not derive the exponent `16` from a
  closed first-principles hierarchy theorem
- CKM:
  the atlas/axiom package is quantitatively strong overall, but
  atlas-leading `|V_us|_0 = 0.22727` remains high against the PDG comparator
- strong CP:
  the exact statement is `theta_eff = 0` on the retained action surface;
  the universal EDM-response corollary is source-scoped to theta-induced
  components and is not a full instanton-measure, `eta'`, or independent
  CP-odd EFT operator-zero claim
- PMNS:
  the retained positive PMNS lane is still absent on current routes, with the
  current frontier reducing to the missing nonzero current `J_chi`; the
  absolute-mass lane nevertheless now carries retained-package observable
  bounds rather than a full PMNS or solar-gap closure
- charged-lepton Koide:
  both physical bridges remain open: physical source-free reduced-carrier
  selection behind `Q = 2/3` remains open after the exact background-zero /
  `Z`-erasure criterion theorem and the unique strict-onsite canonical
  descent theorem, and the selected-line local boundary-source plus
  based-endpoint law behind `delta = 2/9` remains open

## Structural predictions and signatures

- SM hypercharge uniqueness / electric-charge quantization:
  - under the retained one-generation hypotheses, anomaly cancellation and
    `Y(nu_R)=0` uniquely fix right-handed hypercharges
    `(4/3, -2/3, -2, 0)` up to the removed `u_R <-> d_R` label swap
  - the one-generation electric-charge set is therefore
    `{0, +/-1/3, +/-2/3, +/-1}`
  - the left-handed trace relation also packages a separate denominator rule:
    `Y(Q_L):Y(L_L) = 1:-N_c`, so the nonzero quark-charge denominator is
    `N_c` for odd `N_c` and `2 N_c` for even `N_c`; on the Witten-consistent
    retained-style set this reduces to denominator `N_c`, and retained
    graph-first `N_c=3` gives the observed third-integer pattern
  - authority:
    [STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md](../../STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
    and [FRACTIONAL_CHARGE_DENOMINATOR_FROM_N_C_THEOREM_NOTE_2026-04-24.md](../../FRACTIONAL_CHARGE_DENOMINATOR_FROM_N_C_THEOREM_NOTE_2026-04-24.md)
- B-L anomaly freedom / gaugeable option:
  - on the retained 16-state one-generation content including `nu_R`, all six
    anomaly traces needed to gauge `U(1)_{B-L}` alongside the retained SM gauge
    group vanish exactly
  - this proves the gaugeable option only; it does not predict that `B-L` is
    gauged, a `Z'` mass/coupling, or a Majorana structure
  - authority:
    [BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md](../../BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md)
- `SU(2)` Witten `Z_2` global anomaly cancellation:
  - on retained weak-doublet matter, `N_D = 4` per generation and `12` over
    three generations, so the nonperturbative `SU(2)` Witten anomaly cancels
  - this is a fundamental Weyl-doublet count; it does not constrain bosonic
    Higgs doublets or classify higher-isospin `SU(2)` representations
  - authority:
    [SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md](../../SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
- `SU(3)^3` cubic gauge anomaly cancellation:
  - on retained color-charged matter, the pure cubic color anomaly index is
    `+2 - 1 - 1 = 0`
  - this is a colored-sector anomaly closure; it does not derive `N_c=3`,
    the color-singlet lepton completion, or uniqueness among all
    `SU(3)^3`-free extensions
  - authority:
    [SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md](../../SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md)
- emergent Lorentz invariance:
  - leading anisotropic correction first appears at dimension 6
  - unique cubic-harmonic `ell = 4` fingerprint
  - hierarchy-surface suppression `(E/M_Pl)^2`
  - fixed-`H_lat` boost-covariance kernel closes as
    `U(a)=exp(-i a H_lat)` by Stone's theorem; the gravity-card
    directional-measure kernel remains separate/open
  - authority:
    [EMERGENT_LORENTZ_INVARIANCE_NOTE.md](../../EMERGENT_LORENTZ_INVARIANCE_NOTE.md),
    [LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md](../../LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md)
- strong CP:
  - retained action-surface `theta_eff = 0` on the retained
    axiom-determined Wilson-plus-staggered action surface
  - source-scoped vanishing of all theta-induced EDM response components
  - authority:
    [STRONG_CP_THETA_ZERO_NOTE.md](../../STRONG_CP_THETA_ZERO_NOTE.md),
    [UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md](../../UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md)

These are part of the framework's falsification surface; some are already
observed structural signatures, while others are delayed by present
experimental sensitivity.

## Mixed cosmology surface

The cosmology side no longer sits wholly in package-conditional prediction
space. The retained surface now carries:

- `Lambda_vac = lambda_1(S^3_R)` as an exact structural identity
- `w = -1` exactly on the same fixed-gap stationary-vacuum surface
- the TT compactness spectral tower on `S^3`, with exact rational
  squared-mass ratios and Higuchi margins, while numerical tower masses stay
  bounded by the same open `R` identification
- the vector gauge-field compactness spectral tower on `S^3`, with
  `m_l^2 = [l(l+2)-1] hbar^2/(c^2 R^2)` and exact rational squared-mass
  ratios; numerical masses and the 4D particle interpretation remain bounded
- the scalar harmonic compactness spectral tower on `S^3`, with
  `m_l^2 = l(l+2) hbar^2/(c^2 R^2)`, exact rational squared-mass ratios for
  non-zero modes, and first non-zero coefficient `m_1^2 = hbar^2 Lambda/c^2`;
  scalar-species existence and particle interpretation remain bounded
- the gravity/cosmology tower Lambda bridge, which rewrites all three compactness
  towers in pure-`Lambda` units, gives the structural ratio
  `m_TT(2)/m_vec(1) = sqrt(3)`, and keeps benchmark mass scales/GW comparisons
  conditional on the bounded particle-interpretation promotion
- `R_base = 31/9` as an exact group-theory support identity inside the
  bounded DM/cosmology cascade; the Sommerfeld factor and full
  `Omega_DM/Omega_b` value remain bounded
- FRW late-time kinematic identities reducing `q_0`, acceleration onset
  `z_*`, matter-Lambda equality `z_{mLambda}`, and asymptotic `H_inf` to the
  same open ratio `H_inf/H_0`; these are structural relations, not point
  predictions
- the late-time Hubble structural lock:
  on the retained `w=-1` plus admitted flat-FRW surface, all correctly
  reduced late-time `H(z)` probes imply the same scalar `H_0`; this rules out
  late-time-only tension fixes inside the current surface but does not predict
  numerical `H_0`
- the late-time open-number reduction:
  at fixed admitted `Omega_r,0`, the bounded cosmology surface has two
  structural degrees of freedom `(H_0, L)` with `L=(H_inf/H_0)^2`
- the early-time matter-radiation equality identity
  `1 + z_mr = Omega_m,0/Omega_r,0`; the comparator readout `z_mr ~= 3423`
  requires supplied `Omega_m,0` and observational `Omega_r,0`
- active-neutrino-count support for the standard radiation input:
  retained three-generation matter content gives `N_active = 3`, and standard
  thermal-history bookkeeping then gives `N_eff = 3.046`

The remaining numerical cosmology predictions remain bounded because the
cosmology-scale identification and broader matter/cosmology bridge remain
open:

- numerical `Lambda` from the fixed-gap / de Sitter scale route
- numerical graviton compactness-mass companion from the same
  vacuum/topology scale
- present-day `Omega_Lambda` once the matter bridge closes
- point values for `q_0`, `z_*`, and `z_{mLambda}` beyond the same open
  `H_inf/H_0` bridge

Authority:

- [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](../../COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
- [DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md](../../DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
- [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)
- [COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md](../../COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md)
- [MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- [N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md](../../N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md)
- [R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md](../../R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md)
- [GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md](../../GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md)
- [VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE_2026-04-24.md](../../VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE_2026-04-24.md)
- [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md)
- [DARK_ENERGY_EOS_NOTE.md](../../DARK_ENERGY_EOS_NOTE.md)
- [GRAVITON_MASS_DERIVED_NOTE.md](../../GRAVITON_MASS_DERIVED_NOTE.md)

## Open predictive bridges

The main remaining flagship bridge package is now the charged-lepton Koide
lane:

- `Q = 2/3` is conditionally reduced to zero background source, but retained
  completeness still carries the traceless `Z` source coordinate
- `delta = 2/9` is conditionally reduced to selected-line local boundary
  source plus based endpoint
- the A1/radian audit shows retained periodic phase sources remain `q*pi`;
  exact rational `2/9` witnesses do not remove the Type-B rational-to-radian
  readout primitive
- pointed-origin exhaustion proves origin-free retained data cannot select the
  closing representative; the remaining theorem must derive the physical
  source/boundary-origin laws themselves

Outside that flagship lane, the main open promotions are:

- a first-principles hierarchy closure that removes the imported `M_Pl`
  / exponent-`16` qualifiers
- a positive retained PMNS lane
- broader target-free dark-matter uniqueness beyond the exact PMNS-target
  manuscript package
- numerical cosmology promotion beyond the retained structural identities

## Bottom Line

The current package already has:

- a retained quantitative prediction surface;
- a sharp bounded secondary prediction surface;
- exact structural predictions and signatures;
- an explicit falsification and pressure surface;
- one remaining charged-lepton bridge package.

The paper should therefore read as:

> exact discrete backbone + retained quantitative package + bounded prediction
> surface + explicit pressure points + one remaining charged-lepton bridge
> package.
