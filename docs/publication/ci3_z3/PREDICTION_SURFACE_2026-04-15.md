# Prediction Surface

**Date:** 2026-04-15  
**Purpose:** publication-facing summary of what the current `main` package
already predicts, how strongly each prediction is supported, and where the
current falsification surface actually lies.

This note is the shortest honest answer to:

> what does the current package already predict, beyond retrospective
> structural closure?

## Reading Rule

The current package has three predictive layers:

1. retained quantitative outputs already safe for the paper surface;
2. bounded secondary predictions already worth stating explicitly;
3. conditional cosmology predictions whose promotion still depends on the DM /
   matter bridge.

The point of this split is simple: the framework is already predictive. The
paper should not read as if prediction begins only after the remaining live
gate closes.

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
- CKM atlas/axiom closure package:
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
- CKM neutron EDM on the retained `theta_eff = 0` surface:
  - `d_n(CKM) ~ 8 x 10^-33 e cm`
  - authority:
    [CKM_NEUTRON_EDM_BOUND_NOTE.md](../../CKM_NEUTRON_EDM_BOUND_NOTE.md)
- vacuum critical stability:
  - the current `lambda(M_Pl) = 0` route lands on the critical /
    non-metastable side of the usual Standard Model comparison surface
  - authority:
    [VACUUM_CRITICAL_STABILITY_NOTE.md](../../VACUUM_CRITICAL_STABILITY_NOTE.md)
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

## Structural predictions with delayed observability

- emergent Lorentz invariance:
  - leading anisotropic correction first appears at dimension 6
  - unique cubic-harmonic `ell = 4` fingerprint
  - hierarchy-surface suppression `(E/M_Pl)^2`
  - authority:
    [EMERGENT_LORENTZ_INVARIANCE_NOTE.md](../../EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
- strong CP:
  - `theta_eff = 0` on the retained axiom-determined action surface
  - authority:
    [STRONG_CP_THETA_ZERO_NOTE.md](../../STRONG_CP_THETA_ZERO_NOTE.md)

These are part of the framework's falsification surface even when present
experimental sensitivity is limited.

## Conditional cosmology predictions

The cosmology side also carries predictions, but they remain package-conditional
because the matter bridge is still open.

- `Lambda` from the fixed-gap / de Sitter scale route
- `w = -1` on the same fixed-gap route
- graviton-mass companion from the same vacuum/topology scale
- present-day `Omega_Lambda` once the matter bridge closes

Authority:

- [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)
- [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md)
- [DARK_ENERGY_EOS_NOTE.md](../../DARK_ENERGY_EOS_NOTE.md)
- [GRAVITON_MASS_DERIVED_NOTE.md](../../GRAVITON_MASS_DERIVED_NOTE.md)

## What the current package still does not predict cleanly

The main missing flagship prediction remains:

- full DM relic mapping

That is the one live gate because it blocks the strongest matter/cosmology
promotion path. It does not erase the rest of the prediction surface.

## Bottom Line

The current package already has:

- a retained quantitative prediction surface;
- a sharp bounded secondary prediction surface;
- exact structural predictions with delayed observability;
- one live flagship gate.

The paper should therefore read as:

> exact discrete backbone + retained quantitative package + bounded prediction
> surface + one open flagship gate.
