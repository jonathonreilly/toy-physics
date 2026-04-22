# Ω_Λ Matter-Bridge Theorem: `Ω_Λ = (H_inf / H_0)²` under the Retained Spectral-Gap Identity

**Date:** 2026-04-22
**Status:** retained structural-identity theorem on `main`-compatible surface. Reduces the present-day `Ω_Λ` to an exact function of the retained de Sitter Hubble scale `H_inf` and the observationally-pinned current Hubble rate `H_0`, which then under flat FRW collapses to the matter-content bridge `Ω_m`.
**Primary runner:** `scripts/frontier_omega_lambda_matter_bridge.py`

---

## 0. Statement

**Theorem (Ω_Λ matter-bridge identity).** On the retained stationary-de-Sitter vacuum sector of the retained direct-universal GR / canonical textbook continuum GR closure (`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`) with retained round `S^3` spatial topology, and under flat FRW cosmology, the present-day vacuum density fraction is exactly

```text
Ω_Λ  =  (H_inf / H_0)²                                             (★)
```

where `H_inf := c / R_Λ` is the de Sitter Hubble scale (with `R_Λ` the retained spectral-gap radius via `Λ = 3/R_Λ²`) and `H_0` is the present-day Hubble rate. This identity holds exactly as a function identity in `(R_Λ, H_0)` on the retained surface.

Under flat FRW (`Ω_tot = 1`),

```text
Ω_Λ + Ω_m + Ω_r  =  1
Ω_m  =  1 − Ω_Λ − Ω_r  =  1 − (H_inf/H_0)² − Ω_r                    (M)
```

so the retained de Sitter structural data plus the (small, observationally-measured) radiation fraction completely determines `Ω_m` **once the ratio `H_inf/H_0` is fixed**.

**Consequence**: closure of `Ω_Λ` (or equivalently `Ω_m`) on the retained framework reduces to closing one single number — the ratio `H_inf/H_0` — via any retained matter-content bridge.

## 1. Retained inputs (all on main)

| Ingredient | Reference |
|------------|-----------|
| spectral-gap `Λ = 3/R_Λ²` identity | `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` |
| dark-energy EOS `w = -1` | `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` |
| scale identification `H_inf = c/R_Λ`, `Λ = 3 H_inf²/c²` | `COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` |
| FRW continuity + flatness | standard cosmology |

The retained de Sitter vacuum density is
```text
ρ_Λ  =  Λ c² / (8πG)  =  3 c² / (8πG R_Λ²)  =  3 H_inf² / (8πG)
```
(first equality: textbook Einstein-Hilbert; second: spectral-gap identity; third: `H_inf = c/R_Λ`).

The present-day critical density is
```text
ρ_crit  =  3 H_0² / (8πG)
```
(textbook FRW).

## 2. Derivation of (★)

By definition of the vacuum-density fraction,
```text
Ω_Λ  :=  ρ_Λ / ρ_crit.
```

Substituting the two density expressions from §1:
```text
Ω_Λ  =  [3 H_inf² / (8πG)]  /  [3 H_0² / (8πG)]  =  (H_inf / H_0)².     (★)
```

The `8πG` and `3` factors cancel cleanly, leaving (★) as an exact structural identity.

## 3. Consequence for `Ω_m` (equation M)

Standard flat FRW decomposition:
```text
ρ_Λ + ρ_m + ρ_r  =  ρ_crit
Ω_Λ + Ω_m + Ω_r  =  1.
```

Substituting (★):
```text
Ω_m  =  1 − (H_inf/H_0)²  −  Ω_r.                                     (M)
```

`Ω_r ≈ 9.2·10⁻⁵` (observationally pinned CMB + neutrino radiation), negligible at the percent level. So:

```text
Ω_m  ≈  1 − (H_inf / H_0)²                                            (M′)
```

to better than `10⁻³`.

## 4. Numerical check against observation

Observational anchors (2018 Planck + local):
- `H_0 = 67.4 km/s/Mpc = 2.184 × 10⁻¹⁸ s⁻¹` (CMB)
- `Ω_Λ = 0.685 ± 0.007` (Planck 2018)
- `Ω_m = 0.315 ± 0.007`

From (★): `H_inf / H_0 = √Ω_Λ = 0.827`, so `H_inf = 0.827 H_0 = 1.808 × 10⁻¹⁸ s⁻¹`.

The retained spectral-gap radius that produces this `H_inf` is
```text
R_Λ  =  c / H_inf  =  (3 × 10⁸ m/s) / (1.808 × 10⁻¹⁸ s⁻¹)  ≈  1.66 × 10²⁶ m.
```

This is the physical de Sitter radius fixed by matching `Ω_Λ` to Planck. It is `R_Λ / l_Planck ≈ 10⁶¹`, the canonical cosmological hierarchy.

## 5. What this theorem does and does not close

**Closes**:
- The **exact structural identity** `Ω_Λ = (H_inf/H_0)²` on the retained cosmology surface.
- Reduces the `Ω_Λ` promotion question from "derive two numbers" (`Ω_Λ` and `R_Λ`) to "derive one ratio" (`H_inf/H_0`, or equivalently `R_Λ H_0/c`).
- Provides the clean algebraic bridge connecting retained spectral-gap identity to the bounded matter-content lane.

**Does NOT close**:
- A retained derivation of `H_inf/H_0` (or equivalently `R_Λ`). This is the bounded matter-content lane flagged in `COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` §1.
- `Ω_m` from retained DM relic physics; the retained DM package is bounded.
- The separate radiation fraction `Ω_r` (observationally pinned, small).

## 6. How this advances the cosmology package

Before this note, the three cosmology rows looked like independent bounded items:
- `Λ` numerical value — bounded.
- `Ω_Λ` — bounded.
- `Ω_m` — bounded (downstream of DM).

After this note, the correct interpretation is:
- `Λ = 3/R_Λ²` is **retained as a function identity**; the numerical `R_Λ` value is the cosmology-scale-matching blocker.
- `Ω_Λ = (H_inf/H_0)²` is **retained as a function identity** via (★).
- `Ω_m = 1 − Ω_Λ − Ω_r` is the **algebraic consequence under flat FRW**.

So all three rows reduce to **one open number**: the dimensionless ratio `H_inf/H_0`, equivalently `R_Λ H_0/c`.

This is a real improvement: it collapses three apparently independent cosmology bounded items into one shared open number.

## 7. Runner

`scripts/frontier_omega_lambda_matter_bridge.py` verifies:

1. Symbolic derivation: `Ω_Λ = ρ_Λ/ρ_crit = (H_inf/H_0)²` exactly (sympy).
2. Under flat FRW: `Ω_m = 1 − (H_inf/H_0)² − Ω_r`.
3. Observational consistency: Planck 2018 `Ω_Λ = 0.685` ↔ `H_inf/H_0 = 0.827`.
4. `R_Λ / l_Planck ~ 10⁶¹` is the cosmological hierarchy.
5. `w = −1` from `dρ_Λ / d ln a = 0` (retained corollary; cross-check).

Expected: all PASS (numerical + sympy).

## 8. Cross-references

- `docs/COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` — retained Λ = 3/R_Λ² identity.
- `docs/DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` — retained w = −1.
- `docs/COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` — cosmology scale identification synthesis.
- Standard FRW cosmology references (Weinberg *Cosmology*, Dodelson *Modern Cosmology*).
