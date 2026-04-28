# Lane 4F `Σm_ν` Theorem Plan: Cosmology-Bridge Closure Roadmap

**Date:** 2026-04-28
**Status:** retained branch-local theorem-plan note on
`frontier/neutrino-sigma-mnu-cosmology-20260428`. Reduces Lane 4 sub-
target 4F (`Σm_ν` cosmological constraint) to a sharp structural-
functional-form identity over the retained cosmology open-number
reduction surface, with explicit retained / admitted / open input
audit and Phase-1/Phase-2 ordering.
**Lane:** 4 — Neutrino quantitative closure (sub-target 4F)
**Loop:** `neutrino-sigma-mnu-cosmology-20260428`

---

## 0. Statement

Lane 4F closure (retained `Σm_ν` consistent with retained cosmology
bounded surface) decomposes into:

- **4F-α** Structural functional-form retention:
  `Σm_ν = (1 - L - R - Ω_b - Ω_DM) × 93.14 eV × h²` retained as an
  **exact algebraic identity** on the retained cosmology bounded
  surface. **Phase-1 priority of this loop.**
- **4F-β** Numerical retention via parallel-lane closures:
  retain `Σm_ν` as a number once `(h, Ω_b, Ω_DM)` move from admitted
  to retained/bounded. **Depends on Lane 5 (C1)+(C2)/(C3) gates plus
  admitted-input promotions.**

Per the retained cosmology open-number reduction theorem, the
late-time bounded surface has 2 structural dof `(H_0, L)` at fixed
admitted `R = Ω_r,0`. The matter-budget split adds three known
admitted observational layer numbers `(Ω_b, Ω_DM, h)` plus the
target `Σm_ν`, related by one algebraic constraint (4F-α). So at
fixed `(L, R)`, the matter-budget closure adds one admitted dof per
input plus one constraint.

This plan does not numerically retain `Σm_ν`. It produces the
structural plan and identifies the load-bearing dependencies.

## 1. Retained framework structure used

| Identity | Authority | Role in plan |
|---|---|---|
| `Cl(3)/Z^3 + g_bare=1` axioms | `MINIMAL_AXIOMS_2026-04-11.md` | substrate |
| Open-number reduction (`Ω_m,0 = 1 - L - R`) | `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md` | Phase-1 anchor |
| FRW kinematic forward reduction | `COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md` | matter-EOS substrate |
| Matter-radiation equality identity | `MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md` | early-time companion |
| `Λ = 3/R_Λ²` spectral-gap identity | `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` | dark-energy structural anchor |
| `H_inf = c/R_Λ` scale identification | `COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` | scale anchor |
| `w_Λ = -1` dark-energy EOS | `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` | EOS substrate |
| `Ω_Λ = (H_inf/H_0)²` matter bridge | `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` | matter-Λ structure |
| `N_eff = 3.046` from three generations | `N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md` | radiation-budget substrate |
| `H_0(z)` constancy at late times | `HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md` | Hubble structural lock |
| Neutrino retained observable bounds | `NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md` | bounded neutrino content |

## 2. The structural functional-form identity

### 2.1 Premise: matter-budget split

On the retained flat-FRW cosmology surface with three matter
components and admitted CMB neutrino-relic convention,

```text
(P1)  Ω_m,0  =  Ω_b  +  Ω_DM  +  Ω_ν,0                            (matter split)
(P2)  Ω_ν,0 h²  =  Σm_ν / (93.14 eV)                              (CMB neutrino convention)
(P3)  Ω_m,0  =  1 - L - R                                         (open-number reduction; retained)
```

Identities (P1) and (P2) are admitted cosmology-bookkeeping conventions
on the standard matter-budget surface. (P3) is the retained open-
number reduction theorem.

The standard 93.14 eV figure originates from the relic neutrino
number density at `T_ν = (4/11)^(1/3) T_γ` and admitted `T_CMB`. With
retained `N_eff = 3.046`, the precise normalization is

```text
Σm_ν / (93.14 eV)  =  Ω_ν h²                                       (4F-α-1)
```

with the 93.14 eV figure depending on admitted `T_CMB` only.

### 2.2 Theorem 4F-α (structural functional form)

Combining (P1)-(P3):

```text
1 - L - R  =  Ω_b  +  Ω_DM  +  Σm_ν / (93.14 eV h²)               (4F-α-2)
```

Solving for `Σm_ν`:

```text
Σm_ν  =  (1 - L - R - Ω_b - Ω_DM) × 93.14 eV × h²                 (4F-α-3)
```

This is an **exact algebraic identity** on the retained cosmology
bounded surface, valid pointwise across the 2-dof `(H_0, L)` family
at fixed admitted R. Equivalently, knowing `(L, R, Ω_b, Ω_DM, h)`
fixes `Σm_ν` exactly via (4F-α-3).

### 2.3 What is retained vs. admitted vs. open

| Variable | Status | Authority |
|---|---|---|
| `L = Ω_Λ,0` | retained (one of the 2 dof) | open-number reduction theorem |
| `R = Ω_r,0` | admitted (CMB temperature + retained N_eff bookkeeping) | open-number reduction theorem |
| `Ω_b` | admitted observational layer | cosmology open-number reduction §1 |
| `Ω_DM` | admitted observational layer | cosmology open-number reduction §1 |
| `h = H_0/(100 km/s/Mpc)` | open / research-level distant | Lane 5 two-gate dependency |
| `Σm_ν` | **target** | this loop |
| 93.14 eV neutrino-relic conversion | admitted convention | derived from `T_CMB` + retained `N_eff` |

The structural functional form (4F-α-3) is **retained as an
algebraic identity**. The numerical retention of `Σm_ν` requires
all of `(h, Ω_b, Ω_DM)` to be retained or bounded.

## 3. Why this is structurally analogous to Lane 5's open-number reduction

The Lane 5 open-number reduction theorem retained:

```text
S = {H_0, H_inf, R_Λ, Ω_Λ,0, Ω_m,0, q_0, z_*, z_mΛ, H(a)}
```

as **exact closed-form functions of (H_0, L)** at fixed admitted R.
This was a STRUCTURAL retention, not a numerical retention. The
numerical retention required retaining `H_0` independently.

Lane 4F (this plan) retains:

```text
Σm_ν  =  (1 - L - R - Ω_b - Ω_DM) × 93.14 eV × h²
```

as an **exact closed-form function of (L, R, Ω_b, Ω_DM, h)**. Same
posture: a structural retention of the functional form, with
numerical retention deferred until parallel-lane (Lane 5 +
admitted-input audit) closures land.

This is honest Phase-1 progress: it retires no numerical observable
but **structurally isolates the load-bearing dependencies** for the
4F target.

## 4. Phase ordering

### Phase 1 (this loop)

1. **4F-α structural functional form** — single-cycle theorem
   (Cycle 2 of this loop after the present Cycle 1 plan).
2. **4F audit:** which admitted observational layer numbers
   could be promoted to retained via existing framework structure?

### Phase 2 (parallel-lane prerequisites)

3. **Lane 5 (C1)+(C2)/(C3) gate closures** → bounded `h`.
4. **Ω_b retention candidate paths:** baryogenesis structural
   constraints? `η`-from-anomaly arguments? Currently scaffolded.
5. **Ω_DM retention candidate paths:** retained DM-relic structural
   identity? Connected to retained DM Schur-suppression cluster?
   Currently scaffolded.

### Phase 3 (after Phase 2)

6. **Numerical 4F-β retention:** `Σm_ν` retained as bounded interval
   under bounded `(h, Ω_b, Ω_DM)`.
7. **Cross-validation:** consistency with neutrino retained
   observable bounds + retained `δ_CP`/`θ_23` structure.

## 5. Stretch-attempt candidates (per Deep Work Rules)

If audit-quota threshold hits:
- **(SA-A) Functional-form theorem retention** — Phase-1 primary
  attempt (Cycle 2). Algebraically straightforward; honest output.
- **(SA-B) Bounded-envelope retention** — under bounded admitted
  inputs, retain `Σm_ν` interval. Depends on Lane 5 audit.
- **(SA-C) N_eff lower-bound** — using retained `N_eff = 3.046` plus
  retained mass-splitting bounds, derive a structural lower bound on
  `Σm_ν`. Depends on Lane 4 4B/4C status.
- **(SA-D) Ω_DM structural retention probe** — explore whether DM
  Schur-suppression retained content gives a structural `Ω_DM`
  identity. Pivot probe.

## 6. Closed-route inventory (cross-lane)

- **Direct neutrino-Yukawa Ward identity** — closed (Cycle 10
  neutrino loop): `ν_R` gauge-singlet, no YT analog.
- **Charged-lepton y_τ Ward identity gauge-anchor** — closed (Cycles
  2-5 charged-lepton loop): no Fierz-analog on (2,1) block, no
  abelian Fierz, no A_4 flavor sym in retained content. **Implication
  for 4F:** `V_0` lepton scale is research-level distant; cannot
  enter 4F as a retained input.
- **Hubble two-gate dependency** — `h` numerical retention requires
  both (C1) absolute-scale gate + (C2)/(C3) cosmic-L gate. Both gates
  isolated but neither closed.

## 7. What this plan closes and does not close

**Closes (claim-state movement):**

- 4F decomposition into 4F-α (structural functional form) and 4F-β
  (numerical retention).
- Phase ordering with explicit dependency map.
- Identification of `(h, Ω_b, Ω_DM)` as the load-bearing admitted
  inputs that must be retained for 4F-β.
- Stretch-attempt candidate inventory.
- Cross-lane closed-route inventory cross-referenced.

**Does not close:**

- 4F-α (Cycle 2 attempt).
- 4F-β (depends on Phase 2).
- Any numerical Σm_ν retention.

## 8. Falsifier

This plan is structural; not a numerical claim. Falsified if a
Phase-1 derivation succeeds without the listed retained prerequisites,
or if Lane 4F lands via a different methodology not enumerated here
(e.g., direct retained Ω_ν identity from the framework's
representation-theoretic structure that bypasses the matter-budget
split entirely).

## 9. Cross-references

- `docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md`
  §4F (sub-target target description and approachability).
- `docs/lanes/open_science/05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md`
  (Lane 5 two-gate dependency).
- `docs/COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`
  (primary retained cosmology surface used as Phase-1 anchor).
- `docs/HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md`
  (firewall on `h` numerical retention path).
- `docs/N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md`
  (retained radiation-budget substrate).
- `docs/MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`
  (matter-EOS substrate).
- `docs/CHARGED_LEPTON_Y_TAU_M3_PREMISE_SELF_CORRECTION_NOTE_2026-04-28.md`
  (cross-lane Lane 6 closure status; no `V_0` retained input
  available for 4F).
- `docs/NEUTRINO_LANE4_4A_M_LIGHTEST_WARD_IDENTITY_STRETCH_ATTEMPT_NOTE_2026-04-28.md`
  (cross-lane Lane 4 4A status; ν_R gauge-singlet finding).
- Loop pack at
  `.claude/science/physics-loops/neutrino-sigma-mnu-cosmology-20260428/`.

## 10. Boundary

This is a structural plan, not a theorem. It does not retain `Σm_ν`,
does not promote any claim, and does not replace the in-flight Koide
flagship lane or Lane 5 gate audits. It produces the loop's Phase-1
roadmap focused on 4F-α (structural functional form retention).

A runner is not authored.
