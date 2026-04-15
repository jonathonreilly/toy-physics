# Usable Derived Values Index

**Date:** 2026-04-15  
**Purpose:** one place to find the canonical numeric values on `main` that are
actually reused across lanes, together with their claim class and authority.

This is an **atlas helper index**, not a manuscript claim surface.

Use this file when the question is:

- what exact or retained numeric value should downstream work reuse?
- is that value zero-input structural, one-computed-input derived, or bounded?
- which note/runner is the current authority on `main`?

## Reading rule

- `exact / structural` means the quantity is fixed on the theorem surface
  without an external phenomenology bridge
- `retained / derived` means the quantity is numerically reusable on the
  current package surface and should be treated as canonical on `main`
- `bounded / derived` means the number is useful, but downstream reuse must
  carry its bounded qualifier explicitly
- `computed from axiom` means numerically evaluated from the framework rather
  than imported from experiment

## A. Core reusable numbers

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| plaquette `<P>` | `0.5934` | computed from axiom | one computed lattice input | tadpole improvement, coupling map, hierarchy baseline | [COMPLETE_PREDICTION_CHAIN_2026_04_15.md](../../COMPLETE_PREDICTION_CHAIN_2026_04_15.md) |
| `u_0 = <P>^{1/4}` | `0.877681381199` | retained / derived | one computed lattice input | coupling map, hierarchy, EW, Yukawa | [COMPLETE_PREDICTION_CHAIN_2026_04_15.md](../../COMPLETE_PREDICTION_CHAIN_2026_04_15.md) |
| `alpha_LM` | `0.0906678360173` | retained / derived | one computed lattice input | hierarchy baseline, taste thresholds, Planck-to-IR running | [COMPLETE_PREDICTION_CHAIN_2026_04_15.md](../../COMPLETE_PREDICTION_CHAIN_2026_04_15.md) |
| `R_conn` | `8/9 = 0.888888888889` | exact / structural | zero-input structural | EW color projection, Yukawa color projection, taste weights | [RCONN_DERIVED_NOTE.md](../../RCONN_DERIVED_NOTE.md) |
| APBC selector factor | `(7/8)^(1/4) = 0.967168210134` | exact / structural | zero-input structural | hierarchy selector and pre/post-selector normalization | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md), [HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md](../../HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md) |
| pre-selector hierarchy baseline `M_Pl * alpha_LM^16` | `254.643210673818 GeV` | retained / derived | one computed lattice input + framework `M_Pl` | hierarchy support analyses and endpoint comparisons | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) |
| electroweak scale `v` | `246.282818290129 GeV` | retained / derived | one computed lattice input + framework `M_Pl` | canonical EW scale across the repo | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md), [YT_ZERO_IMPORT_CHAIN_NOTE.md](../../YT_ZERO_IMPORT_CHAIN_NOTE.md) |
| `alpha_s(v)` | `0.103303816122` | retained / derived | one computed lattice input | strong-coupling lane, CKM, confinement, Yukawa/Higgs support | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) |

## B. Retained EW normalization package

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| `g_1(v)` | `0.4644` | retained / derived | one computed lattice input | EW normalization, Higgs/top support | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `g_2(v)` | `0.6480` | retained / derived | one computed lattice input | EW normalization, Higgs/top support | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `sin^2(theta_W)(M_Z)` | `0.2306` | retained / derived | one computed lattice input + running | reviewer-facing EW lane, low-energy comparison | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `1/alpha_EM(M_Z)` | `127.67` | retained / derived | one computed lattice input + running | reviewer-facing EW lane, low-energy comparison | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `alpha_s(M_Z)` | `0.1181` | retained / derived | one computed lattice input + running | standalone strong-coupling lane, confinement, continuum positioning | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) |

## C. Closed flavor package values

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| `|V_us|` | `0.22727` | closed / derived | no-import closure | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `|V_cb|` | `0.04217` | closed / derived | no-import closure | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `|V_ub|` | `0.003913` | closed / derived | no-import closure | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `delta_CKM` | `65.905157 deg` | closed / derived | no-import closure | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `J` | `3.331 x 10^-5` | closed / derived | no-import closure | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |

## D. Useful bounded downstream values

These are usable, but only with their qualifiers attached.

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| `y_t(v)` | `0.9176` | bounded / derived | zero SM imports, bounded surrogate systematic | bounded Yukawa/Higgs lane reuse only | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md) |
| `m_t(pole)` 2-loop | `172.57 GeV` | bounded / derived | inherits bounded `y_t` lane | bounded top-mass reuse only | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md) |
| `m_t(pole)` 3-loop | `173.10 GeV` | bounded / derived | inherits bounded `y_t` lane | bounded top-mass reuse only | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md) |
| `m_H` framework-side 3-loop | `125.3 GeV` | bounded / derived | inherits bounded `y_t` lane | bounded Higgs/vacuum reuse only | [HIGGS_VACUUM_PROMOTED_NOTE.md](../../HIGGS_VACUUM_PROMOTED_NOTE.md) |
| `sqrt(sigma)` | `465 MeV` | bounded / derived | retained `alpha_s` + EFT bridge | bounded confinement phenomenology only | [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md) |

## Rule for downstream work

Before reusing a number elsewhere in the repo:

1. take it from this file or from the authority linked here
2. carry its claim class with it
3. if it is bounded, keep the qualifier in the target note or table
4. do not copy older route-history values when a canonical value exists here
