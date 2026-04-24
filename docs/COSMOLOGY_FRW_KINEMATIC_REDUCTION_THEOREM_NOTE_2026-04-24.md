# FRW Late-Time Kinematic Reduction Theorem

**Date:** 2026-04-24
**Status:** retained structural-identity theorem on `main`. Extends the retained Ω_Λ matter-bridge theorem (`OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`) by showing that **four additional late-time FRW kinematic observables** (deceleration parameter `q_0`, acceleration-onset redshift `z_*`, matter-Λ equality redshift `z_{mΛ}`, asymptotic Hubble rate `H_∞`) are structural functions of the **same single open number `H_inf / H_0`**.
**Primary runner:** `scripts/frontier_cosmology_frw_kinematic_reduction.py`

---

## 0. Statement

**Theorem (FRW late-time kinematic reduction).** On the retained cosmology surface
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) + [`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md) + flat FRW + standard (pressureless matter, radiation `w_r = 1/3`, `w_Λ = −1`), the following structural identities hold:

```text
(K1)  q_0       =  (1/2) (1 + Ω_r,0 − 3 Ω_Λ,0)                    [deceleration parameter today]
(K2)  z_*       =  (2 Ω_Λ,0 / Ω_m,0)^(1/3) − 1   [Ω_r,0 ≈ 0]       [deceleration→acceleration onset]
(K3)  z_{mΛ}    =  (Ω_Λ,0 / Ω_m,0)^(1/3) − 1                       [matter–Λ equality redshift]
(K4)  a(t → ∞) ∝ exp(H_∞ t),   H_∞ ≡ c / R_Λ                      [asymptotic de Sitter attractor]
(K5)  H(t) ≥ H_∞   for all t ≥ 0 with non-negative matter + radiation content
```

Combined with the retained matter-bridge identity `Ω_Λ,0 = (H_inf/H_0)²` and the algebraic consequence `Ω_m,0 = 1 − Ω_Λ,0 − Ω_r,0`, every quantity in (K1)–(K5) is a closed-form function of the **single open number** `H_inf / H_0` (equivalently `R_Λ H_0 / c`).

## 1. Retained inputs (all on main)

| Ingredient | Reference |
|------------|-----------|
| spectral-gap `Λ = 3 / R_Λ²` | `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` |
| dark-energy EOS `w_Λ = −1` exactly | `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` |
| `Ω_Λ,0 = (H_inf/H_0)²` identity | `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` |
| flatness `Ω_tot = 1` | S³ topology / inflation (same basis) |
| standard FRW continuity + Friedmann | textbook cosmology |
| matter `w_m = 0`, radiation `w_r = 1/3` | standard equation-of-state |

No observed cosmological value enters the derivations below. Numerical comparators are used only after the identities are derived.

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

Setting `q(a_*) = 0` (neglecting Ω_r):

```text
0  =  1 + Ω_r(a_*) − 3 Ω_Λ(a_*)  ≈  1 − 3 Ω_Λ(a_*)
Ω_Λ(a_*)  =  1/3.
```

With `Ω_Λ(a)/Ω_m(a) = (ρ_Λ,0 · a³) / (ρ_m,0 · 1) · (1 / (H_0² / H(a)²))` cancelling the common `H(a)²/H_0²` factor:

```text
Ω_Λ(a_*) / Ω_m(a_*)  =  (a_*³ ρ_Λ,0) / ρ_m,0  =  2
```

using `Ω_Λ(a_*) = 1/3` and `Ω_m(a_*) + Ω_Λ(a_*) = 1` (late times):

```text
a_*³  =  Ω_m,0 / (2 Ω_Λ,0)
1 + z_*  ≡  1/a_*  =  (2 Ω_Λ,0 / Ω_m,0)^(1/3).                     (K2)
```

## 4. Derivation of (K3) — matter–Λ equality redshift

The matter-Λ equality condition is `ρ_m(a_{mΛ}) = ρ_Λ(a_{mΛ})`:

```text
ρ_{m,0} / a_{mΛ}³  =  ρ_{Λ,0}
a_{mΛ}³  =  Ω_{m,0} / Ω_{Λ,0}
1 + z_{mΛ}  =  (Ω_{Λ,0} / Ω_{m,0})^(1/3).                          (K3)
```

**Comparison with (K2).** Since `2^(1/3) ≈ 1.26 > 1`, we have

```text
1 + z_*  =  2^(1/3) · (1 + z_{mΛ})
```

i.e. the universe begins to accelerate **before** ρ_Λ overtakes ρ_m. The gap is a factor of `2^(1/3) ≈ 1.26` in `(1 + z)`.

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

**Six late-time FRW kinematic observables** (Ω_Λ, Ω_m, q_0, z_*, z_{mΛ}, H_∞) all reduce to the **same single open number** `H_inf/H_0`. This strengthens the matter-bridge theorem's reduction from "three cosmology rows in one number" to "six cosmology observables in one number".

## 7. Numerical checks against observation (post-derivation)

Observational values (Planck 2018 + cosmological comparators):

| Input | Value | Source |
|-------|-------|--------|
| H_inf/H_0 = √Ω_Λ,0 | 0.8276 | √0.685 |
| Ω_{Λ,0} | 0.685 | Planck 2018 |
| Ω_{m,0} | 0.315 | Planck 2018 |
| Ω_{r,0} | 9.2 × 10⁻⁵ | CMB + Nν |

Framework outputs from K-identities:

| Observable | Framework | Observed | Source |
|------------|-----------|----------|--------|
| q_0 | **−0.528** | −0.55 ± 0.05 | Type Ia SN (Union3, DES-Y5, 2024) |
| z_* (accel. onset) | **0.632** | 0.67 ± 0.10 | SN Ia compilations |
| z_{mΛ} | **0.296** | ~0.30 ± 0.05 | derived from Planck cosmology |
| z_* − z_{mΛ} | **0.336** | ~0.37 | both SN Ia + Planck consistent |
| z_* / z_{mΛ} | **2.135** | ~2.23 | structural prediction |

Agreement at 1σ across all four observables on the retained w = −1 surface. The framework does **not** predict the specific values of Ω_Λ,0 or H_inf/H_0, but it does predict that q_0, z_*, z_{mΛ} must be **correlated** via the K-identities.

## 8. Falsifiability

The K-identities hold as **joint** identities. A measurement of any one combination (e.g. q_0) that is inconsistent with another (e.g. z_* under the same Ω_Λ) falsifies the retained w = −1 + flat FRW surface.

Specific falsification channels:

- **DESI / Euclid**: tightening BAO + SN constraints on `(Ω_Λ, q_0)` pair. A > 3σ inconsistency with `q_0 = (1/2)(1 − 3Ω_Λ)` falsifies w = −1 or flat FRW.
- **SNIa precision at z ~ 0.6**: if `z_*` is confidently inconsistent with the retained Ω_m, Ω_Λ reconstruction via K2.
- **Any w(z) measurement confirming `w ≠ −1`** with high significance → falsifies the w = −1 corollary, hence the entire K-package.
- **Any evidence of non-flatness** (|Ω_k| > 0.002) breaks the flatness input; this is already constrained by Planck.

This is a **joint-identity** falsification target, not a single-parameter fit.

## 9. What this theorem does and does not close

**Closes (new):**

- The structural identities K1–K5 for late-time FRW kinematics on the retained w = −1 + flat FRW surface.
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

- K1–K5 are exact structural identities on the retained surface.
- The deceleration-to-acceleration transition occurs precisely at `Ω_Λ = 1/3` under w = −1 + flat FRW + matter (neglecting Ω_r at late times), this is algebraically exact.
- The gap between `z_*` and `z_{mΛ}` is exactly `2^(1/3) ≈ 1.26` in `(1+z)`, a pure structural consequence.
- The framework predicts a joint (q_0, z_*, z_{mΛ}) relationship matching observation at 1σ under the retained cosmology surface + observed Ω_Λ.

**Cannot claim**

- A point prediction for q_0, z_*, or z_{mΛ} at native axiom level; each depends on the still-open `H_inf/H_0`.
- Closure of the matter-bridge open number itself.
- Anything beyond late-time (matter + Λ) FRW kinematics.

## 12. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_cosmology_frw_kinematic_reduction.py
```

Expected: all checks pass.

## 13. Cross-references

- `docs/COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` — `Λ = 3/R²`
- `docs/DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` — `w = −1` retained
- `docs/OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` — `Ω_Λ = (H_inf/H_0)²`
- `docs/COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` — open `H_inf/H_0` lane
- `docs/COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md` — Phase-5 cascade (not altered here)
- Weinberg, *Cosmology*, ch. 1 — standard FRW kinematics
