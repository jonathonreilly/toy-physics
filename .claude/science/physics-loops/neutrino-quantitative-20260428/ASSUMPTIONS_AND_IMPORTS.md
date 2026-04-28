# Lane 4 Neutrino — Assumptions and Imports Ledger

**Date:** 2026-04-28
**Loop:** `neutrino-quantitative-20260428`
**Purpose:** explicit pre-cycle inventory. Feeds the dramatic-step gate.

## 1. Retained framework structure on `main` (theorem-grade)

| Identity | Authority |
|---|---|
| `Cl(3)` on `Z^3` minimal axiom stack | `MINIMAL_AXIOMS_2026-04-11.md` |
| Anomaly-forced 3+1 + retained three-generation structure | three-generation cluster |
| Exact PMNS selector / current-stack zero law | `PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md` |
| Exact Majorana zero law on current stack (suggests Dirac lane) | `NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md` |
| Neutrino mass reduction to Dirac lane | `NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` |
| Retained neutrino observable bounds | `NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md` |
| `delta_CP ≈ -81°` (DM closed package; falsifiable at DUNE/Hyper-K) | DM closed package |
| `theta_23 ≥ 0.5410` upper octant (DM closed package; falsifiable) | DM closed package |
| `N_eff = 3 + 0.046 = 3.046` from three generations + thermal correction | `N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md` |
| Retained two-amplitude last-mile reduction | `NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md` |

## 2. Bounded / partial on `main`

| Item | Status | Authority |
|---|---|---|
| Seesaw mass scale | retained partial (Phase 4 of mass-spectrum derived note) | `MASS_SPECTRUM_DERIVED_NOTE.md` Phase 4 |
| Solar/PMNS bounded support | bounded | `NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md` |
| Right-handed neutrino mass spectrum (M_R1, M_R2, M_R3) | scaffold/partial | `MASS_SPECTRUM_DERIVED_NOTE.md` |

## 3. External inputs ("different carriers" — absent)

These are the explicit observational pins Lane 4 aims to retire.

| Input | Value (PDG / global fits) | Role | Lane |
|---|---|---|---|
| `m_lightest` | bounded `< 0.8 eV` (KATRIN); Σm_ν `< 0.12 eV` (cosmology) | absolute mass scale | 4A |
| `Delta m^2_21` | `7.42 × 10^-5 eV^2` | solar mass-squared diff | 4B |
| `Delta m^2_31` | `2.515 × 10^-3 eV^2` (NO) | atmospheric mass-squared diff | 4C |
| Dirac vs Majorana global | undetermined (0νββ searches null so far) | mass mechanism | 4D |
| `alpha_21, alpha_31` | undetermined | Majorana phases (only if Majorana) | 4D consequence |

## 4. Bridge layers and admitted conventions

- Standard PMNS oscillation framework (textbook neutrino physics)
- Standard seesaw type-I formalism (Type II / Type III not in initial scope)
- Cosmological Σm_ν constraint via standard ΛCDM + CMB lensing
  (admitted; the cosmology bridge layer was extensively audited in the
  hubble-h0 loop)
- Standard Majorana mass insertion / 0νββ amplitude formalism

## 5. Workstream rule

A cycle that imports `m_lightest`, `Delta m^2_21`, or `Delta m^2_31`
from PDG / global fits as a derivation input fails the dramatic-step
gate. Comparators are used in runners' verification phase only.

The Dirac-lane retention (`NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md`)
indicates the framework expects neutrinos to be Dirac globally. A
4D global lift attempt should not pre-suppose Majorana.
