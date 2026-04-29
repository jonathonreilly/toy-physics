# `Σm_ν` Structural Functional Form on Cosmology Bounded Surface — Support Note (4F-α)

**Date:** 2026-04-28
**Status:** support / branch-local **stretch-attempt** note on
`frontier/neutrino-sigma-mnu-cosmology-20260428`. Cycle 2 of the
neutrino-sigma-mnu-cosmology loop. **Result: structural functional
form `Σm_ν = (1 - L - R - Ω_b - Ω_DM) × C_ν × h²` recorded as a
support-level exact algebraic identity on the cosmology bounded surface,
where `C_ν` is the standard 93.14 eV admitted CMB-neutrino-relic
convention.** This is a **support-level structural form**, not a numerical
closure; numerical `Σm_ν` requires `(h, Ω_b, Ω_DM)` to move from
admitted to retained or bounded.
**Lane:** 4 — Neutrino quantitative closure (sub-target 4F-α)
**Loop:** `neutrino-sigma-mnu-cosmology-20260428`

---

## 0. First-principles reset (per Deep Work Rules)

### 0.1 `A_min` + retained content

Per `MINIMAL_AXIOMS_2026-04-11.md` axioms 1-4, plus retained:
- `Ω_m,0 = 1 - L - R` (open-number reduction theorem 2026-04-26).
- `N_eff = 3.046` from three-generation structure (2026-04-24).
- Flat FRW + standard matter/radiation EOS (admitted cosmology layer).
- `Λ = 3/R_Λ²`, `H_inf = c/R_Λ`, `w_Λ = -1`, `Ω_Λ = (H_inf/H_0)²`
  retained.
- Matter-radiation equality `1 + z_mr = Ω_m,0 / Ω_r,0` retained
  (admitted-FRW companion).

### 0.2 Forbidden imports

- No PDG `Σm_ν` upper bound as derivation input (cosmology surveys
  citation only as falsifier).
- No specific Planck `Ω_b h²` or `Ω_DM h²` numbers as derivation
  input.
- No fitted `H_0` numerical value.
- No external 0νββ rate as derivation input.

### 0.3 Goal

Construct an exact algebraic identity on the retained cosmology
bounded surface:

```text
Σm_ν  =  F(L, R, Ω_b, Ω_DM, h)                                    (T-4F-α)
```

with `F` a known closed-form function, where:
- `L`, `R` are the bounded-surface variables / admitted radiation
  fraction;
- `Ω_b`, `Ω_DM` are admitted observational layer numbers;
- `h = H_0 / (100 km/s/Mpc)` is currently open;
- `93.14 eV` is the standard CMB-neutrino-relic conversion, depending
  on admitted `T_CMB` and retained `N_eff`.

## 1. The matter-budget structural identity

### 1.1 Premises

(P1) **Flat FRW matter-budget split.** On the standard flat-FRW
cosmology surface, the present-day matter density partitions as

```text
Ω_m,0  =  Ω_b  +  Ω_DM  +  Ω_ν,0                                   (P1)
```

where `Ω_b` is the baryon density, `Ω_DM` is the cold dark matter
density, and `Ω_ν,0` is the present-day neutrino density (treating
neutrinos as nonrelativistic at present, valid for `Σm_ν > a few ×
10^{-2} eV`).

(P2) **Open-number reduction (retained).** Per
`COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`,

```text
Ω_m,0  =  1 - L - R                                                (P2)
```

with `L = Ω_Λ,0` retained on the late-time bounded surface and
`R = Ω_r,0` admitted from CMB temperature plus retained `N_eff`.

(P3) **CMB neutrino-relic convention.** With three neutrino species
and admitted Standard-Model relic-density bookkeeping (relativistic
decoupling at `T_dec ≈ 1 MeV`, `T_ν / T_γ = (4/11)^{1/3}` after
`e^+ e^-` annihilation, retained `N_eff = 3.046`):

```text
Ω_ν,0 h²  =  Σm_ν / C_ν                                           (P3)
```

where

```text
C_ν  =  93.14 eV                                                   (admitted)
```

is the standard numerical conversion derived from admitted `T_CMB`
plus the retained `N_eff` factor. Specifically

```text
C_ν  =  (8π G / 3) × (1 / (100 km/s/Mpc)²) × n_ν,total × (1 eV / m_ν normalization)
```

with `n_ν,total = (3/4) × N_eff × (4/11) × n_γ` and `n_γ ∝ T_CMB³`.
For admitted `T_CMB = 2.7255 K` and retained `N_eff = 3.046`,
`C_ν ≈ 93.14 eV` (numerical detail dependent on admitted `T_CMB`).

### 1.2 Theorem 4F-α

Combining (P1)-(P3):

```text
1 - L - R  =  Ω_b  +  Ω_DM  +  Σm_ν / (C_ν h²)                    (T-4F-α-1)
```

Solving for `Σm_ν`:

```text
Σm_ν  =  (1 - L - R - Ω_b - Ω_DM) × C_ν × h²                       (T-4F-α-2)
```

This is an **exact algebraic identity** on the cosmology bounded
surface. The review status is:

- The algebraic structure (T-4F-α-2) is a **support-level structural
  identity** under admitted premises (P1)-(P3).
- Numerical evaluation requires admitted/open inputs `(h, Ω_b, Ω_DM)`.
- The 93.14 eV figure is admitted convention (depends on admitted
  `T_CMB`).

### 1.3 Equivalent forms

```text
Σm_ν / (C_ν h²)  =  Ω_ν,0  =  Ω_m,0 - Ω_b - Ω_DM                  (T-4F-α-3)
                =  1 - L - R - Ω_b - Ω_DM
```

```text
Σm_ν h² / C_ν  =  h² × (1 - L - R - Ω_b - Ω_DM)
              =  Ω_m,0 h² - Ω_b h² - Ω_DM h²                      (T-4F-α-4)
```

(T-4F-α-4) shows that the natural "retained-friendly" combination
is `Σm_ν / C_ν` rather than `Σm_ν` alone, since `Ω_? h²`
combinations are the standard CMB/cosmology bookkeeping form.

## 2. Status audit per input

| Input | Tier | Source |
|---|---|---|
| `L` | retained (one of the 2 dof in S) | open-number reduction §0 |
| `R = Ω_r,0` | admitted (CMB-T + retained N_eff) | open-number reduction §0 |
| `Ω_b` | admitted observational layer | open-number reduction §0 |
| `Ω_DM` | admitted observational layer | open-number reduction §0 |
| `h = H_0/100` | open / research-level distant | Lane 5 two-gate dep |
| `C_ν = 93.14 eV` | admitted convention (depends on T_CMB) | standard cosmology |
| `Σm_ν` | **target** (this theorem) | — |

The structural identity (T-4F-α-2) is support-level on the bounded
surface in the sense that:
- The functional form is exact on flat FRW + standard matter/radiation
  EOS + retained `N_eff` + admitted `T_CMB`.
- It is compatible with `Ω_m,0 = 1 - L - R` and the open-number
  reduction theorem.

The numerical retention of `Σm_ν` requires `(h, Ω_b, Ω_DM)` to be
retained or bounded.

## 3. What this note establishes

**Support-level algebraic identity (this note):**

- `Σm_ν = (1 - L - R - Ω_b - Ω_DM) × C_ν × h²` exactly, on retained
  cosmology bounded surface plus admitted matter-budget split.
- `Σm_ν / C_ν = Ω_ν,0` as the dimensionless neutrino-relic density.
- `Σm_ν h² / C_ν = Ω_m,0 h² - Ω_b h² - Ω_DM h²` as the standard
  CMB-bookkeeping form.
- Functional structure: at fixed `(L, R, Ω_b, Ω_DM, h)`, `Σm_ν` is
  uniquely determined.

**Not retained (deferred to Phase 2):**

- Numerical `Σm_ν` value (depends on `h, Ω_b, Ω_DM` admitted/open
  inputs).
- Bounded `Σm_ν` interval (requires bounded-`h` from Lane 5 plus
  admitted-input bounds on `Ω_b, Ω_DM`).
- Lower bound from oscillation mass-splittings (depends on Lane 4
  4B/4C status).

## 4. Comparison with Lane 5 open-number reduction

Lane 5 retained `S = {H_0, H_inf, R_Λ, Ω_Λ,0, Ω_m,0, q_0, z_*,
z_mΛ, H(a)}` as exact closed-form functions of `(H_0, L)` at fixed
admitted `R`. That theorem reduced the late-time bounded surface
from 9 nominal variables to 2 structural dof.

This note (4F-α) extends that reduction to the matter-budget
split. Adding `(Σm_ν, Ω_b, Ω_DM, h, T_CMB, N_eff)` gives 6 new
nominal variables; (T-4F-α-1) gives 1 algebraic constraint; retained
`N_eff` and admitted `T_CMB` reduce by 2; so the matter-budget
extension adds **3 new structural dof** to S — typically taken to
be `(h, Ω_b h², Ω_DM h²)` or equivalents.

The full late-time + matter-budget bounded surface has

```text
2 (cosmology)  +  3 (matter-budget)  =  5 structural dof
```

at fixed admitted `R, T_CMB` and retained `N_eff`. `Σm_ν` is determined
algebraically once these 5 are fixed.

This is honest structural progress: it does not close `Σm_ν`
numerically, but **identifies the minimal admitted-input set**
required to pin `Σm_ν` exactly.

## 5. Structural falsifiers

The theorem is falsified by:

- A retained framework derivation showing `Ω_b`, `Ω_DM`, or `h` is
  retained (not admitted), which would promote (T-4F-α-2) toward
  numerical retention.
- A different retained matter-budget split (e.g., extra radiation
  species, modified gravity matter dilution) that contradicts (P1).
- An empirical 0νββ-positive measurement at any precision that
  contradicts the unconditional Dirac global lift theorem
  (`NEUTRINO_DIRAC_GLOBAL_LIFT_CURRENT_AXIOM_SET_THEOREM_NOTE_2026-04-28.md`).
  The matter-budget identity (T-4F-α-2) is independent of the
  Dirac/Majorana question; it concerns the cosmology relic density
  only. A Dirac/Majorana switch would not change (T-4F-α-2) but
  would change the interpretation of `Σm_ν` (mass-eigenstate vs.
  Majorana basis).

## 6. What this cycle closes and does not close

**Closes:**

- 4F-α (structural functional-form support): `Σm_ν` is recorded
  as an exact algebraic function `(1 - L - R - Ω_b - Ω_DM) × C_ν ×
  h²` on the cosmology bounded surface plus admitted
  matter-budget split.
- Identification that the matter-budget extension to the
  open-number-reduction surface adds 3 structural dof
  `(h, Ω_b h², Ω_DM h²)`.
- Status audit per input (retained / admitted / open).

**Does not close:**

- 4F-β (numerical retention): blocked on Lane 5 `h` retention plus
  `(Ω_b, Ω_DM)` promotion.
- Lane 4 4F sub-target overall.
- Numerical `Σm_ν` value or interval.

## 7. Cross-references

- Cycle 1 theorem plan:
  `docs/NEUTRINO_LANE4_4F_SIGMA_M_NU_THEOREM_PLAN_NOTE_2026-04-28.md`.
- Open-number reduction theorem (primary retained anchor):
  `docs/COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`.
- N_eff retained:
  `docs/N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md`.
- Matter-radiation equality (admitted-FRW companion):
  `docs/MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`.
- Lane 5 two-gate firewall (h retention dep):
  `docs/HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md`.
- Lane 4 unconditional Dirac global lift:
  `docs/NEUTRINO_DIRAC_GLOBAL_LIFT_CURRENT_AXIOM_SET_THEOREM_NOTE_2026-04-28.md`.
- Lane 4F sub-target description:
  `docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md` §4F.
- Loop pack:
  `.claude/science/physics-loops/neutrino-sigma-mnu-cosmology-20260428/`.

## 8. Boundary

This note records the **structural functional form** of `Σm_ν`
on the cosmology bounded surface. It does **not** close
`Σm_ν` numerically and does not promote `(h, Ω_b, Ω_DM)` from their
current admitted/open status. The 93.14 eV conversion `C_ν` is
used as the standard CMB-neutrino-relic convention dependent on
admitted `T_CMB` and retained `N_eff`.

A small algebraic-consistency runner is authored as
`scripts/frontier_neutrino_lane4_4f_sigma_m_nu_functional_form.py`.
The runner reports `TOTAL: PASS=4, FAIL=0` covering: (1) symbolic
forward identity from (P1)+(P2)+(P3); (2) equivalent-form consistency
across (T-4F-α-2)/(T-4F-α-3)/(T-4F-α-4); (3) self-consistent
admitted-input round-trip (target `Σm_ν` → back-solved `L` →
forward-evaluated `Σm_ν` matches at 1e-15 eV residual); (4)
limiting cases (matter exactly accounted ⇒ `Σm_ν = 0`; `h → 0` ⇒
`Σm_ν → 0` proportional to `h²`).
