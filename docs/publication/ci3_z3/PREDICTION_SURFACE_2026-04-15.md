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
3. structural predictions with delayed observability;
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
  - `|V_us| = 0.22727`
  - `|V_cb| = 0.04217`
  - `|V_ub| = 0.003913`
  - `delta = 65.905 deg`
  - `J = 3.331 x 10^-5`
  - authority:
    [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- confinement readout on top of the exact graph-first confinement theorem:
  - `sqrt(sigma) ≈ 465 MeV`
  - authority:
    [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md)

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
  - `M_mono ~ 1.43 M_Pl`
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
  `|V_us| = 0.22727` remains high against the PDG comparator
- strong CP:
  the exact statement is `theta_eff = 0` on the retained action surface;
  this is not yet a full instanton-measure or `eta'` closure claim
- PMNS:
  the retained positive PMNS lane is still absent on current routes, with the
  current frontier reducing to the missing nonzero current `J_chi`
- charged-lepton Koide:
  both physical bridges remain open:
  the extremal/source-law bridge behind `Q = 2/3` and the physical
  Brannen-phase bridge behind `delta = 2/9`

## Structural predictions with delayed observability

- emergent Lorentz invariance:
  - leading anisotropic correction first appears at dimension 6
  - unique cubic-harmonic `ell = 4` fingerprint
  - hierarchy-surface suppression `(E/M_Pl)^2`
  - authority:
    [EMERGENT_LORENTZ_INVARIANCE_NOTE.md](../../EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
- strong CP:
  - retained action-surface `theta_eff = 0` on the retained
    axiom-determined Wilson-plus-staggered action surface
  - authority:
    [STRONG_CP_THETA_ZERO_NOTE.md](../../STRONG_CP_THETA_ZERO_NOTE.md)

These are part of the framework's falsification surface even when present
experimental sensitivity is limited.

## Mixed cosmology surface

The cosmology side no longer sits wholly in package-conditional prediction
space. The retained surface now carries:

- `Lambda_vac = lambda_1(S^3_R)` as an exact structural identity
- `w = -1` exactly on the same fixed-gap stationary-vacuum surface

The remaining numerical cosmology predictions remain bounded because the
cosmology-scale identification and broader matter/cosmology bridge remain
open:

- numerical `Lambda` from the fixed-gap / de Sitter scale route
- numerical graviton compactness-mass companion from the same
  vacuum/topology scale
- present-day `Omega_Lambda` once the matter bridge closes

Authority:

- [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](../../COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
- [DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md](../../DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
- [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)
- [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md)
- [DARK_ENERGY_EOS_NOTE.md](../../DARK_ENERGY_EOS_NOTE.md)
- [GRAVITON_MASS_DERIVED_NOTE.md](../../GRAVITON_MASS_DERIVED_NOTE.md)

## Open predictive bridges

The main remaining flagship bridge package is now the charged-lepton Koide
lane:

- `Q = 2/3` still requires a physical/source-law bridge
- `delta = 2/9` still requires the physical Brannen-phase bridge

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
- exact structural predictions with delayed observability;
- an explicit falsification and pressure surface;
- one remaining charged-lepton bridge package.

The paper should therefore read as:

> exact discrete backbone + retained quantitative package + bounded prediction
> surface + explicit pressure points + one remaining charged-lepton bridge
> package.
