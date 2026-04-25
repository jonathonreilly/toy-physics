# FRW Late-Time Kinematic Reduction Theorem

**Date:** 2026-04-24
**Status:** retained/admitted-surface structural identity theorem on `main`.
Extends the retained Ω_Λ matter-bridge theorem
(`OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`) by showing that
**four additional late-time FRW kinematic observables** (deceleration
parameter `q_0`, acceleration-onset redshift `z_*`, matter-Λ equality redshift
`z_{mΛ}`, asymptotic Hubble rate `H_∞`) are structural functions of the
**same single open number `H_inf / H_0`** once the retained `w=-1` surface,
flat FRW, and the standard matter/radiation equations of state are accepted.
This is not a point prediction for the numerical value of any of those
observables.
**Primary runner:** `scripts/frontier_cosmology_frw_kinematic_reduction.py`

---

## 0. Statement

**Theorem (FRW late-time kinematic reduction).** On the retained cosmology
surface
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
+ [`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
+ flat FRW + standard pressureless matter and radiation
(`w_m = 0`, `w_r = 1/3`, `w_Λ = −1`), the following structural identities
hold:

```text
(K1)  q_0       =  (1/2) (1 + Ω_r,0 − 3 Ω_Λ,0)                    [deceleration parameter today]
(K2)  2 Ω_Λ,0 a_*^4 − Ω_m,0 a_* − 2 Ω_r,0 = 0                   [exact deceleration→acceleration onset]
      z_*       =  1/a_* − 1
      z_*       ≈  (2 Ω_Λ,0 / Ω_m,0)^(1/3) − 1   [Ω_r,0 → 0]
(K3)  z_{mΛ}    =  (Ω_Λ,0 / Ω_m,0)^(1/3) − 1                       [matter–Λ equality redshift]
(K4)  a(t → ∞) ∝ exp(H_∞ t),   H_∞ ≡ c / R_Λ                      [asymptotic de Sitter attractor]
(K5)  H(t) ≥ H_∞   for all t ≥ 0 with non-negative matter + radiation content
```

Combined with the retained matter-bridge identity `Ω_Λ,0 = (H_inf/H_0)²` and the algebraic consequence `Ω_m,0 = 1 − Ω_Λ,0 − Ω_r,0`, every quantity in (K1)–(K5) is a closed-form function of the **single open number** `H_inf / H_0` (equivalently `R_Λ H_0 / c`).

## 1. Retained/admitted inputs

| Ingredient | Reference |
|------------|-----------|
| spectral-gap `Λ = 3 / R_Λ²` | `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` |
| dark-energy EOS `w_Λ = −1` exactly | `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` |
| `Ω_Λ,0 = (H_inf/H_0)²` identity | `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` |
| flatness `Ω_tot = 1` | S³ topology / inflation (same basis) |
| standard FRW continuity + Friedmann | admitted continuum-cosmology layer |
| matter `w_m = 0`, radiation `w_r = 1/3` | standard late-time equation-of-state |

No measured cosmological value enters the algebraic derivations below after
this retained/admitted surface is accepted. Numerical comparators are used only
after the identities are derived.

## 2. Derivation of (K1) — deceleration parameter today

The deceleration parameter is `q ≡ −ä a / ȧ²`. Using the Friedmann acceleration equation `ä/a = −(4πG/3)(ρ + 3p)` and `H² = 8πG ρ_tot / 3`:

```text
q  =  (4πG/3)(ρ + 3p) / ((8πG/3) ρ_tot)
   =  (1/2)(1 + 3 p_tot/ρ_tot)
   =  (1/2)(1 + 3 w_eff)
```

With three non-interacting fluids (matter, radiation, Λ) and flat FRW (Σ Ω_i = 1):

```text
w_eff  =  (w_m Ω_m + w_r Ω_r + w_Λ Ω_Λ) / Σ Ω_i
       =  0·Ω_m + (1/3)·Ω_r + (−1)·Ω_Λ
       =  Ω_r/3 − Ω_Λ
```

Substituting at `t = t_0`:

```text
q_0  =  (1/2)(1 + Ω_r,0 − 3 Ω_Λ,0).                                (K1)
```

At late times, `Ω_r,0 ≈ 9.2 × 10⁻⁵` is negligible at percent level:

```text
q_0  ≈  (1/2)(1 − 3 Ω_Λ,0)                                         (K1′)
```

to better than `10⁻³`. The sign of `q_0` changes at `Ω_Λ,0 = 1/3` exactly (neglecting Ω_r).

## 3. Derivation of (K2) — acceleration onset redshift

Each component scales as `ρ_i(a) = ρ_{i,0} · a^{−3(1 + w_i)}`, so

```text
ρ_m(a)  =  ρ_{m,0} / a³
ρ_r(a)  =  ρ_{r,0} / a⁴
ρ_Λ(a)  =  ρ_{Λ,0}              (constant)
```

Setting `q(a_*) = 0` with matter, radiation, and Λ gives

```text
0  =  Ω_m(a_*) + 2 Ω_r(a_*) − 2 Ω_Λ(a_*).
```

The common `H(a)²/H_0²` denominator cancels, so the exact acceleration-onset
scale factor is the unique positive root of

```text
Ω_m,0 / a_*³ + 2 Ω_r,0 / a_*⁴ = 2 Ω_Λ,0

equivalently

2 Ω_Λ,0 a_*⁴ − Ω_m,0 a_* − 2 Ω_r,0 = 0.                         (K2)
```

In the late-time matter+Λ approximation `Ω_r,0 → 0`, this reduces to

```text
a_*³  =  Ω_m,0 / (2 Ω_Λ,0)
1 + z_*  ≡  1/a_*  =  (2 Ω_Λ,0 / Ω_m,0)^(1/3).                     (K2′)
```

For the listed comparator density values the radiation correction to `z_*` is
below `10⁻³`, well below the quoted observational precision.

## 4. Derivation of (K3) — matter–Λ equality redshift

The matter-Λ equality condition is `ρ_m(a_{mΛ}) = ρ_Λ(a_{mΛ})`:

```text
ρ_{m,0} / a_{mΛ}³  =  ρ_{Λ,0}
a_{mΛ}³  =  Ω_{m,0} / Ω_{Λ,0}
1 + z_{mΛ}  =  (Ω_{Λ,0} / Ω_{m,0})^(1/3).                          (K3)
```

**Comparison with the late-time form of (K2).** Since
`2^(1/3) ≈ 1.26 > 1`, we have

```text
1 + z_*  =  2^(1/3) · (1 + z_{mΛ})
```

i.e. the universe begins to accelerate **before** ρ_Λ overtakes ρ_m. The
late-time gap is a factor of `2^(1/3) ≈ 1.26` in `(1 + z)`. With radiation
retained exactly, this factor receives the negligible K2 quartic correction.

## 5. Derivation of (K4), (K5) — asymptotic de Sitter attractor + Hubble lower bound

From the Friedmann equation and late-time scaling:

```text
H²(a)  =  H_0² [Ω_{r,0}/a⁴ + Ω_{m,0}/a³ + Ω_{Λ,0}]
      →  H_0² Ω_{Λ,0}                                (as a → ∞)
      =  H_inf²                                      (using Ω_Λ = (H_inf/H_0)²)
```

so `H(t) → H_inf = c / R_Λ` asymptotically (K4), and the FRW equation integrates to `a(t) ∝ exp(H_inf t)` in the late-time limit.

For every `a` (hence every `t`), radiation and matter densities are non-negative, so

```text
H²(a)  =  H_0² [Ω_{r,0}/a⁴ + Ω_{m,0}/a³ + Ω_{Λ,0}]  ≥  H_0² Ω_{Λ,0}  =  H_inf²
⇒  H(a)  ≥  H_inf   for all a ≥ 0.                                (K5)
```

In particular `H_0 ≥ H_inf`, equivalently `Ω_{Λ,0} ≤ 1` (trivially consistent with flatness).

## 6. Structural consequence: full late-time kinematic reduction

Combining the retained matter-bridge identity `Ω_{Λ,0} = (H_inf/H_0)²` with (K1)–(K5):

```text
Ω_{Λ,0}   =  (H_inf/H_0)²                    [retained matter-bridge]
Ω_{m,0}   =  1 − (H_inf/H_0)² − Ω_{r,0}     [flatness]
q_0       =  (1/2)(1 + Ω_{r,0} − 3 (H_inf/H_0)²)
z_*       =  [2 (H_inf/H_0)² / (1 − (H_inf/H_0)² − Ω_{r,0})]^(1/3) − 1
z_{mΛ}    =  [(H_inf/H_0)² / (1 − (H_inf/H_0)² − Ω_{r,0})]^(1/3) − 1
```

The displayed `z_*` expression is the late-time closed form. The exact
radiation-retaining expression is the positive root of the K2 quartic with
`Ω_Λ,0 = (H_inf/H_0)^2` and
`Ω_m,0 = 1 − (H_inf/H_0)^2 − Ω_r,0`.

**Six late-time FRW kinematic observables** (Ω_Λ, Ω_m, q_0, z_*, z_{mΛ}, H_∞) all reduce to the **same single open number** `H_inf/H_0`. This strengthens the matter-bridge theorem's reduction from "three cosmology rows in one number" to "six cosmology observables in one number".

## 7. Numerical checks against listed comparators (post-derivation)

Listed comparator values (Planck 2018 + SN/cosmology summaries):

| Input | Value | Source |
|-------|-------|--------|
| H_inf/H_0 = √Ω_Λ,0 | 0.8276 | √0.685 |
| Ω_{Λ,0} | 0.685 | Planck 2018 |
| Ω_{m,0} | 0.315 | Planck 2018 |
| Ω_{r,0} | 9.2 × 10⁻⁵ | CMB + Nν |

Framework outputs from K-identities after substituting the listed comparator
`H_inf/H_0 = sqrt(Ω_Λ,0)`:

| Observable | Framework value after inserting comparator `Ω_Λ,0` | Comparator | Source |
|------------|-----------|----------|--------|
| q_0 | **−0.528** | −0.55 ± 0.05 | Type Ia SN (Union3, DES-Y5, 2024) |
| z_* (accel. onset, exact radiation) | **0.632** | 0.67 ± 0.10 | SN Ia compilations |
| z_{mΛ} | **0.296** | ~0.30 ± 0.05 | derived from Planck cosmology |
| z_* − z_{mΛ} | **0.336** | ~0.37 | both SN Ia + Planck consistent |

The `q_0` and `z_*` rows are independent late-time kinematic checks once a
common `Ω_Λ,0` comparator is inserted. The `z_{mΛ}` row is primarily a
consistency check because it is derived from the same density parameters.
The framework does **not** predict the specific values of `Ω_Λ,0` or
`H_inf/H_0`, but it does predict that `q_0`, `z_*`, and `z_{mΛ}` must be
**correlated** via the K-identities.

## 8. Falsifiability

The K-identities hold as **joint** identities. A measurement of any one combination (e.g. q_0) that is inconsistent with another (e.g. z_* under the same Ω_Λ) falsifies the retained w = −1 + flat FRW surface.

Specific falsification channels:

- **DESI / Euclid**: tightening BAO + SN constraints on `(Ω_Λ, q_0)` pair. A > 3σ inconsistency with `q_0 = (1/2)(1 − 3Ω_Λ)` falsifies w = −1 or flat FRW.
- **SNIa precision at z ~ 0.6**: if `z_*` is confidently inconsistent with the retained Ω_m, Ω_Λ reconstruction via K2.
- **Any w(z) measurement confirming `w ≠ −1`** with high significance → falsifies the w = −1 corollary, hence the entire K-package.
- **Any evidence of non-flatness** at a level incompatible with the accepted
  flat-FRW input breaks the reduction surface.

This is a **joint-identity** falsification target, not a single-parameter fit.

## 9. What this theorem does and does not close

**Closes (new):**

- The structural identities K1–K5 for late-time FRW kinematics on the
  retained/admitted `w = −1` + flat-FRW surface.
- The explicit reduction of `q_0, z_*, z_{mΛ}, H_∞` to the **same** single open number `H_inf/H_0` already carrying `Ω_Λ` and `Ω_m`.
- The asymptotic de Sitter attractor statement `a(t) ∝ exp(H_inf t)` as t → ∞.
- The Hubble-rate lower bound `H(t) ≥ H_inf` for all t ≥ 0.

**Does NOT close:**

- A retained derivation of `H_inf/H_0` (equivalently `R_Λ H_0/c`). This is the single open matter-bridge number, unchanged by this note.
- The numerical value of `Ω_{Λ,0}` or `Ω_{m,0}`. They remain bounded.
- The matter composition (η, Ω_b, R, α_GUT). The separate cosmology cascade (`COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md`) is not altered.

## 10. Relationship to existing cosmology rows

Before this note, the retained matter-bridge theorem reduced three cosmology rows (Λ, Ω_Λ, Ω_m) to one open number. After this note:

| Row | Status before | Status after |
|-----|---------------|--------------|
| Λ = 3/R² | retained identity | unchanged |
| w = −1 | retained corollary | unchanged |
| Ω_Λ = (H_inf/H_0)² | retained identity | unchanged |
| Ω_m = 1 − Ω_Λ − Ω_r | algebraic under flatness | unchanged |
| **q_0** | (not packaged) | **retained K1 identity** |
| **z_*** | (not packaged) | **retained K2 identity** |
| **z_{mΛ}** | (not packaged) | **retained K3 identity** |
| **H_∞ / de Sitter attractor** | (not packaged) | **retained K4–K5 identities** |

The cosmology matter-bridge open item — one open number `H_inf/H_0` — now carries **six** structural observables, not three. This is a reduction of the apparent multiplicity of open cosmology rows, matching the same principle as the original matter-bridge theorem.

## 11. Safe-claim boundary

**Can claim**

- K1–K5 are exact structural identities on the retained/admitted surface, with
  K2 represented by its exact radiation-retaining quartic.
- The deceleration-to-acceleration transition is the positive root of the K2
  quartic; in the late-time radiation-negligible limit this is equivalent to
  `Ω_Λ(a_*) = 1/3`.
- The late-time gap between `z_*` and `z_{mΛ}` is exactly
  `2^(1/3) ≈ 1.26` in `(1+z)`, a pure structural consequence.
- The framework predicts a joint `(q_0, z_*, z_{mΛ})` relationship; the listed
  comparator values are consistent once the comparator `Ω_Λ` is inserted.

**Cannot claim**

- A point prediction for q_0, z_*, or z_{mΛ} at retained/admitted-surface level; each depends on the still-open `H_inf/H_0`.
- Closure of the matter-bridge open number itself.
- Anything beyond late-time (matter + Λ) FRW kinematics.

The early-time matter-radiation equality identity is packaged separately in
`MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`.
It is not a late-time `H_inf/H_0` reduction; its numerical readout is instead
conditioned on `Omega_m,0` and observational `Omega_r,0`.

## 12. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_cosmology_frw_kinematic_reduction.py
```

Expected: all checks pass.

## 13. Cross-references

- `docs/COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` — `Λ = 3/R²`
- `docs/DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` — `w = −1` retained
- `docs/OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` — `Ω_Λ = (H_inf/H_0)²`
- `docs/MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md` — early-time matter-radiation equality identity
- `docs/COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` — open `H_inf/H_0` lane
- `docs/COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md` — Phase-5 cascade (not altered here)
- Weinberg, *Cosmology*, ch. 1 — standard FRW kinematics
