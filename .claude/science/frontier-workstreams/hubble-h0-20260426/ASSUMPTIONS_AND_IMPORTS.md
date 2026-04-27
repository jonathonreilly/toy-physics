# Hubble H_0 — Assumptions and Imports Ledger

**Date:** 2026-04-26
**Workstream:** `hubble-h0-20260426`
**Purpose:** explicit pre-cycle inventory of what is taken as input, what is
already retained on the framework surface, and what bridge layers are in play.

This ledger feeds the dramatic-step gate. New cycles must retire an existing
import or add exact support; silent re-imports fail the gate.

## 1. Retained framework structure (already on `main`)

Theorem-grade; no additional support needed before citing.

| Identity | Authority |
|---|---|
| `Cl(3)` on `Z^3` (one-axiom physical theory) | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| `Lambda = 3 / R_Lambda^2` (spectral-gap identity) | `docs/COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` |
| `w_Lambda = -1` retained DE EOS | `docs/DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` |
| `H_inf = c / R_Lambda` (de Sitter scale) | `docs/COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` |
| `Omega_Lambda = (H_inf / H_0)^2` (matter-bridge identity) | `docs/OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` |
| Flat FRW: `Omega_Lambda + Omega_m + Omega_r = 1` | admitted textbook FRW |
| FRW kinematic forward reduction to single `H_inf/H_0` | `docs/COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md` |
| Single-ratio inverse reconstruction certificate | `docs/COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md` |
| `R_base = 31/9` group-theory derivation | `docs/R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md` |
| Matter-radiation equality `1 + z_mr = Omega_m / Omega_r` | `docs/MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md` |
| `N_eff = 3 + 0.046 = 3.046` (active-neutrino count + thermal correction) | `docs/N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md` |
| `Lambda` spectral tower bridge (`m_TT(2)/m_vec(1) = sqrt(3)`) | `docs/GRAVITY_COSMOLOGY_TOWER_LAMBDA_SPECTRAL_BRIDGE_THEOREM_NOTE_2026-04-25.md` |
| Neutrino retained observable bounds | `docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md` (cross-ref) |

## 2. External inputs on the current paper surface

Explicit observational pins. Lane 5's job is to retire as many as possible
without silently re-importing them under a different label.

| Input | Value | Role | Retirement candidate? |
|---|---|---|---|
| `H_0` | 67.4 km/s/Mpc | direct paper input for cosmology rows | **primary retirement target** |
| `T_CMB` | 2.7255 K | sets `Omega_r,0` via standard-species bookkeeping | secondary; lane defers (5E inflation territory) |
| `eta` (baryon asymmetry) | 6.12e-10 | BBN entry to bounded `Omega_b` cascade | retirement candidate via DM leptogenesis route |
| `alpha_GUT` | in `[0.03, 0.05]` | Sommerfeld correction to bounded `R = Omega_DM/Omega_b` | retirement candidate via gauge-coupling unification (separate lane) |
| Planck 2018 cosmology numbers | `Omega_Lambda=0.685`, `Omega_m=0.315`, `Omega_b=0.0493` | **comparator only**, never a derivation input | not an input; never a retirement target |
| PDG charged-lepton masses | observational pin | unrelated to cosmology row; Lane 6 owns | not in scope here |

## 3. Bridge layers and admitted conventions

Not raw observational inputs but standard physics layers used between the
retained core and the paper surface. None of these are derivation inputs in
their own right.

- Standard textbook FRW cosmology: Friedmann equations, density scalings
  (`rho_m a^-3`, `rho_r a^-4`, `rho_Lambda a^0`), flatness assumption
  (justified by `S^3` topology or inflation; flatness gate separate)
- Textbook BBN: `eta -> Omega_b` model-independent at percent level
- Sommerfeld enhancement formula for DM annihilation cross-section
- Standard `Omega_r,0` from `T_CMB` plus relativistic-species bookkeeping
  (photons + active neutrinos via `N_eff`)
- Late-time FRW geodesic / distance-redshift relations
- Primary energy condition implicit in retained `w = -1` (no exotic
  late-time DE behavior)

## 4. The reduced open-number target

Combining the matter-bridge identity and the single-ratio inverse
reconstruction certificate, the entire late-time bounded cosmology surface
reduces to:

```text
two open numbers:
  H_0      (overall expansion rate today)
  L = Omega_Lambda = (H_inf/H_0)^2

with the structural identity H_inf = c / R_Lambda providing the absolute scale
once R_Lambda is retained.
```

Every other late-time number is an exact function of `(H_0, L)` on the
retained surface:

- `H_inf = H_0 sqrt(L)`
- `Omega_m = 1 - L - Omega_r`
- `q_0 = (1 + Omega_r - 3 L) / 2`
- `1 + z_mLambda = (M / L)^(1/3) = ((1 - L - Omega_r) / L)^(1/3)`
- `1 + z_* = a_*^-1` solving `2 L a_*^4 - M a_* - 2 Omega_r = 0`
- `H(a)^2 / H_0^2 = Omega_r a^-4 + Omega_m a^-3 + L`

So Lane 5 closure ≡ retained `(H_0, L)` ≡ retained `(R_Lambda, L)` once
`R_Lambda` is anchored.

## 5. Workstream rule

A cycle that adds a new external input without retiring an existing one fails
the dramatic-step gate. Imports may be added only if the cycle explicitly
retires or strictly narrows another import already on this ledger.

## 6. Open status of imports — entry point summary

- `H_0`: open. No retained derivation. Goal of this workstream.
- `T_CMB`: deferred (5E). Out of initial Lane 5 scope.
- `eta`: open with strong support. The DM leptogenesis lane has an exact
  one-flavor branch reaching `eta/eta_obs = 0.1888` and a reduced-surface
  PMNS branch reaching `eta/eta_obs = 1.0`. Promotion to retained requires the
  selector/normalization closure of that lane.
- `alpha_GUT`: open. Bounded by gauge-coupling unification lane (separate).
- `R_Lambda`: open. Bounded by Planck-scale matching lane; multiple
  finite-response, parent-source, and entropy-carrier no-gos have closed easy
  routes (see `NO_GO_LEDGER.md`).
- Comparators (Planck 2018): never derivation inputs. Used only for
  consistency verification.
