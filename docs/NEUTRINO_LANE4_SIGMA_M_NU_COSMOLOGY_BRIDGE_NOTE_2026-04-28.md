# Lane 4 → Lane 5 `Σm_ν` Cosmology Bridge — Structural Couplings

**Date:** 2026-04-28
**Status:** retained branch-local **bridge audit note** on
`frontier/neutrino-quantitative-20260428`. Cycle 9 of the loop:
maps the structural coupling between Lane 4's neutrino mass spectrum
and Lane 5's retained late-time cosmology surface (matter-bridge +
open-number reduction + structural lock + matter-radiation equality
+ retained `N_eff`). Identifies the explicit `Σm_ν` constraint
imposed by retained cosmology content + Lane 4 4D Dirac-only
retention (Cycle 8), and names the additional Lane-4 retentions
that would unlock a numerical `Σm_ν` prediction.
**Lane:** 4 — Neutrino quantitative closure (route 4F)
**Loop:** `neutrino-quantitative-20260428`

---

## 0. Setup

Cycles 2-8 of this loop produced the **Dirac Global Lift on the
Current Axiom Set** theorem
(`NEUTRINO_DIRAC_GLOBAL_LIFT_CURRENT_AXIOM_SET_THEOREM_NOTE_2026-04-28.md`).
This pins the framework's neutrino sector as Dirac on the current
axiom set. The remaining Lane-4 closure work shifts to:

- 4A absolute mass scale `m_lightest`
- 4E Dirac mass mechanism without seesaw (smallness without
  suppression)
- **4F Σm_ν cosmological constraint (this cycle)**
- 4G internal consistency check with retained `δ_CP` and `θ_23`
- 4B/C splittings (arithmetic from 4A/4E)

This cycle (4F) maps the **structural coupling** between Lane 4's
mass spectrum and Lane 5's retained cosmology surface. It is a
bridge audit, not a closure cycle.

The hubble-h0 work is now **integrated upstream** as of
`a8dd7918 cosmology: land Hubble structural lock lane` and
`52b18fa4 Add Lane 5 Hubble two-gate dependency firewall`. So Lane 5's
retained surface is fully available as input to Lane 4's 4F.

## 1. Retained Lane 5 cosmology surface

The integrated retentions:

| Identity | Authority | Role |
|---|---|---|
| `Λ = 3 / R_Λ²` (spectral-gap) | `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` | Λ structural identity |
| `w_Λ = -1` (DE EOS) | `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` | DE EOS |
| `H_inf = c / R_Λ` | `COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` | scale identification |
| `Ω_Λ = (H_inf/H_0)²` (matter-bridge) | `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` | matter-bridge |
| Single-ratio inverse reconstruction | `COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md` | inverse certificates |
| Hubble Tension Structural Lock | `HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md` | late-time `H_0(z)` constancy |
| Cosmology Open-Number Reduction | `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md` | exactly 2 open nos `(H_0, L)` |
| Matter-radiation equality `1 + z_mr = Ω_m / Ω_r` | `MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md` | structural identity |
| `N_eff = 3 + 0.046 = 3.046` | `N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md` | active-neutrino + thermal |
| `R_base = 31/9` | `R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md` | exact `Ω_DM / Ω_b` base |

Open numbers (per Lane-5 closure-pathway no-go): `H_0` and `L`.

## 2. The `Σm_ν` cosmology coupling

Cosmologically, neutrinos contribute to two density components:

- **Radiation-like at high z:** for `z >> z_nr,i` (where
  `z_nr,i = m_i c² / (3.151 k T_CMB) - 1` for species `i`),
  neutrinos are relativistic and contribute to `Ω_r` via the retained
  `N_eff = 3.046`.
- **Matter-like at low z:** for `z << z_nr,i`, neutrinos are
  non-relativistic and contribute to `Ω_m` via the standard
  cosmological identity

```text
Ω_ν h² = Σm_ν / (93.14 eV)                                       (1)
```

with `h = H_0 / (100 km/s/Mpc)` and `Σm_ν = m_1 + m_2 + m_3`.

The transition redshift for the heaviest species (heaviest `m_i`):

```text
z_nr ~ m_heaviest / (3.151 k T_CMB) - 1                          (2)
       ~ m_heaviest / (5.28 × 10⁻⁴ eV) - 1.
```

For `m_heaviest ~ 0.05 eV` (atmospheric splitting scale),
`z_nr ~ 95`. So neutrinos are non-relativistic for essentially all
late-time observation epochs.

## 3. Constraints from retained content

### 3.1 `N_eff = 3.046` retained

The retained `N_eff` is the **relativistic** count, defined at
`z >> z_nr,i`. With `Cycles 2-8 4D Dirac retention`, the three
active species are Dirac neutrinos. The standard thermal correction
`+0.046` is the post-decoupling `e⁺e⁻` annihilation correction,
identical for Dirac and Majorana species (this is already implicit
in the retained `N_eff` derivation).

So the retained `N_eff` is consistent with 4D Dirac retention. **No
new constraint** from this direction.

### 3.2 Matter-bridge + open-number reduction → `Ω_m` and `Ω_r`

Per the open-number reduction theorem
(`COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`), every
late-time bounded cosmology row is an exact function of `(H_0, L)`
with `R = Ω_r,0` admitted from `T_CMB` + retained `N_eff`. The
matter density follows by flatness:

```text
Ω_m,0 = 1 - L - R                                               (3)
```

With observational `R ~ 9.2 × 10⁻⁵` and observational `L ~ 0.685`,
`Ω_m,0 ~ 0.315`.

### 3.3 `Σm_ν` enters `Ω_m` decomposition

`Ω_m,0` decomposes as:

```text
Ω_m,0 = Ω_b + Ω_DM + Ω_ν                                        (4)
```

with `Ω_ν` from (1). The retained `R_base = 31/9 = Ω_DM,base / Ω_b`
plus the bounded Sommerfeld correction give

```text
Ω_DM / Ω_b ≈ 5.4                                                (5)
```

(per `OMEGA_LAMBDA_DERIVATION_NOTE.md`).

So:

```text
Ω_m,0 = Ω_b + 5.4 Ω_b + Σm_ν / (93.14 eV h²)
      = 6.4 Ω_b + Σm_ν / (93.14 eV h²)                          (6)
```

For observational `Ω_m,0 ~ 0.315` and `Ω_b ~ 0.0493`:

```text
Σm_ν / (93.14 eV h²) ~ 0.315 - 6.4 × 0.0493 = 0.315 - 0.316
                     ~ -0.001                                   (7)
```

i.e., observationally consistent with `Σm_ν ≈ 0` or sub-eV. With
`h ~ 0.674`, this gives `Σm_ν / (42.3 eV) ≈ 0`, hence
`Σm_ν << 0.05 eV` (tighter than the empirical Planck+BAO bound
`Σm_ν < 0.12 eV`).

### 3.4 Structural upper bound from retained content

Even without observational `Ω_m,0`, the retained `R_base = 31/9` plus
the matter-bridge identity gives a structural relationship:

```text
Ω_b + Ω_DM + Ω_ν = 1 - L - R                                    (8)
                 = 1 - (H_inf/H_0)² - R                          (9)
```

Substituting `Ω_DM = R_base × S_corr × Ω_b` (with `S_corr` the
bounded Sommerfeld correction):

```text
Ω_b (1 + R_base × S_corr) + Σm_ν / (93.14 eV h²)
   = 1 - (H_inf/H_0)² - R                                      (10)
```

Equation (10) is the structural `Σm_ν` coupling. Three retained
identities enter:

- `R_base = 31/9` (exact)
- `(H_inf/H_0)²` matter-bridge
- `R` admitted via `T_CMB` + retained `N_eff`

Plus the bounded `S_corr` Sommerfeld correction and the bounded /
external `Ω_b`.

**Structural conclusion:** `Σm_ν` is constrained by the retained
cosmology surface plus retained `R_base`, modulo the bounded
Sommerfeld correction and external `Ω_b`. Closing `Σm_ν` numerically
requires retaining `Ω_b` and `S_corr`.

## 4. Structural `Σm_ν` upper bound (no neutrino-mass content needed)

Even with `Σm_ν` undetermined, equation (10) implies a one-sided
constraint. Using flatness + retained `R_base`:

- if `Σm_ν > 0`, then `Ω_b (1 + R_base × S_corr) < 1 - L - R`;
- equivalently, `Ω_b < (1 - L - R) / (1 + R_base × S_corr)`.

For `R_base × S_corr ≈ 5.4`, `1 - L - R ≈ 0.315`:

```text
Ω_b < 0.315 / 6.4 ≈ 0.049                                      (11)
```

This is **independent of `Σm_ν`**; it's a retained-content upper bound
on `Ω_b`. With observational `Ω_b ≈ 0.0493`, the framework's retained
content places `Ω_b` near the upper bound, leaving little room for
`Σm_ν` if `R_base × S_corr` is taken at face value.

Conversely, if `Ω_b` were independently retained at sub-percent
precision, `Σm_ν` would be constrained to:

```text
Σm_ν < (0.315 - 6.4 Ω_b,retained) × 93.14 h² eV                 (12)
```

For any plausible `Ω_b,retained ~ 0.049 ± 0.001`, the structural
upper bound is `Σm_ν < 0.06 - 0.6 eV`, depending on the precision
of `Ω_b,retained` and `S_corr`.

## 5. What this cycle closes and does not close

**Closes (claim-state movement):**

- Structural mapping of the `Σm_ν` coupling between Lane 4 and
  Lane 5: equation (10) gives the explicit retained-content
  constraint.
- Identification of the Lane-4-side retentions needed for
  numerical `Σm_ν`: the 4D Dirac retention (already landed) is
  sufficient on the Lane-4 side; the remaining work is **Ω_b
  retention via the bounded cascade** (with `eta` retired) +
  **`S_corr` retention** (bounded Sommerfeld → retained-with-budget).
- Demonstration that retained content already places a structural
  upper bound on `Σm_ν` (within the bounded `Ω_b` and `S_corr`
  surfaces).

**Does not close:**

- A numerical `Σm_ν` prediction. That requires retiring `eta`
  (DM-leptogenesis lane open), retiring `α_GUT` for `S_corr`
  (gauge-coupling unification lane open), or otherwise retaining
  `Ω_b`.
- The Lane-4-side mass spectrum `(m_1, m_2, m_3)`. That requires
  4A absolute scale + 4E mass mechanism + 4B/C splittings.
- An empirical falsifier. The structural upper bound is
  observationally tight but not falsifying.

## 6. Bridge to Lane 5 closure

The 4F bridge is bidirectional:

- **Lane 5 → Lane 4:** retained cosmology surface (matter-bridge,
  open-number reduction, retained `N_eff`) + bounded cascade gives
  a structural upper bound on `Σm_ν` (equations 10-11).
- **Lane 4 → Lane 5:** retained 4D Dirac global lift (Cycle 8)
  consistent with retained `N_eff` (no new species at thermal
  abundances). 4A retained `m_lightest` would give `Σm_ν` and
  feed back into Ω_m decomposition.

Neither direction closes Lane 5 itself (which gates on `(C1)` Planck
Clifford coframe + `(C2)` DM `Z_3` doublet-block per the integrated
two-gate firewall) or Lane 4 itself (which gates on 4A absolute
scale).

## 7. Cross-references

- Cycle 8 manuscript-grade theorem:
  `NEUTRINO_DIRAC_GLOBAL_LIFT_CURRENT_AXIOM_SET_THEOREM_NOTE_2026-04-28.md`.
- Hubble retained surface:
  `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`,
  `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`,
  `HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md`.
- Bounded cascade:
  `OMEGA_LAMBDA_DERIVATION_NOTE.md`,
  `R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md`.
- Retained cosmology identities:
  `MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`,
  `N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md`.
- Lane file:
  `docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md` §3F.
- Loop pack:
  `.claude/science/physics-loops/neutrino-quantitative-20260428/`.

## 8. Boundary

This is a structural bridge audit, not a theorem. It does not
retain any new content, does not predict `Σm_ν` numerically, and
does not close any other Lane-4 sub-target. It maps the structural
couplings between Lane 4 and Lane 5 and identifies the path forward
for 4F closure (Ω_b retention via the DM-leptogenesis lane).

A runner is not authored: the bridge is editorial / structural.
