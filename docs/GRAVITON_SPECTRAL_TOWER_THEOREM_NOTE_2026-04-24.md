# Graviton TT Compactness Spectral Tower on Retained S³

**Date:** 2026-04-24

**Status:** **retained structural-identity extension theorem** on `main`.
Extends the retained graviton-mass theorem
([`GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md))
from the lowest Lichnerowicz TT mode (`l = 2`) to the full transverse-traceless
compactness eigenvalue tower on the retained `S³` spatial topology.  The
retained content is the eigenvalue/mass-ratio/Higuchi-margin structure, not a
claim that each higher `l` is a detected or independently established
Fierz-Pauli particle species.

**Script:** `scripts/frontier_graviton_spectral_tower.py`

**Upstream authorities (all retained on `main`):**
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md),
[`GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md),
[`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md),
[`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md)

---

## 0. Scope

The retained graviton-mass identity theorem promotes only the **lowest**
Lichnerowicz TT eigenvalue on `S³` (`λ_2^TT = 6/R²`) to a structural identity
`m_g² = 2ℏ²Λ/c²`. The **higher** Lichnerowicz TT eigenvalues sit implicitly in
the same retained surface but are not explicitly packaged.

This note packages that implicit tower as its own retained structural identity theorem, consisting of three closed-form components:

1. **(T1) Tower compactness-mass identity.** The structural spin-2 TT compactness masses are
   ```text
   m_l² = [l(l+2) − 2] · ℏ² / (c² R²),   l = 2, 3, 4, ...    (T1)
   ```
   with `l = 2` reproducing the retained graviton-mass identity.

2. **(T2) Pure-rational ratio identities.** Every mass ratio in the tower is a pure rational number:
   ```text
   (m_l / m_k)²  =  [l(l+2) − 2] / [k(k+2) − 2]                (T2)
   ```
   In particular, the spectrum-normalised ratios (m_l / m_2)² = [l(l+2) − 2] / 6 are rationals for every l ≥ 2.

3. **(T3) Uniform Higuchi stability.** Every mode in the tower strictly satisfies the Higuchi non-ghost bound `m² > 2Λ/3`, with explicit margin
   ```text
   m_l² / (2Λ/3) = [l(l+2) − 2] / 2  ≥  3    (T3)
   ```
   The lower bound `3` is saturated only at the lowest mode `l = 2`; higher modes have progressively larger margins that grow as `l²/2 + O(l)`.

The whole tower is thus pinned by the **same** single open number `R` as the
retained `Λ` and `m_g` rows. This is a spectral compactness statement on the
retained compact slice. The separate physical interpretation of those
compactness masses as 4D-effective massive spin-2 particles remains no stronger
than in the single-mode graviton-mass theorem.

## 1. Retained inputs (all on main)

| Ingredient | Reference |
|------------|-----------|
| `Λ = 3/R²` spectral-gap identity | [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) |
| `m_g² = 2ℏ²Λ/c² = 6ℏ²/(c²R²)` graviton-mass identity | [`GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) |
| retained `S³` spatial topology (round, radius `R > 0`) | [`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md), [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md) |
| Lichnerowicz TT spectrum on `S³`: `λ_l^TT = [l(l+2) − 2]/R²`, `l ≥ 2` | standard spin-2 perturbation theory on Einstein manifolds; Higuchi 1987, Deser & Nepomechie 1984, Gibbons & Hawking 1993; explicitly quoted in [`GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) Leg A |
| KK-style compactness-mass identification `m_l² c²/ℏ² = λ_l^TT` per harmonic | classical KK-style identification on compact spatial slice; explicitly used in [`GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) mass-identification leg |

No observational cosmological value enters the derivations below.

## 2. Derivation

### 2.1 Tower mass identity (T1)

The retained theorem's Leg A gives the full Lichnerowicz TT eigenvalue at each `l ≥ 2`:

```text
λ_l^TT  =  [l(l + 2) − 2] / R²
```

The retained theorem's mass-identification leg applies per mode, so

```text
m_l²  =  ℏ² λ_l^TT / c²  =  [l(l + 2) − 2] · ℏ² / (c² R²).                (T1)
```

Substituting `Λ = 3/R²` (retained):

```text
m_l²  =  [l(l + 2) − 2] / 3 · ℏ²Λ / c².                                    (T1')
```

For `l = 2`: `l(l+2) − 2 = 6`, giving `m_2² = 2 ℏ²Λ/c² = 6ℏ²/(c²R²)`, reproducing the retained graviton-mass identity exactly. ∎

### 2.2 Pure-rational ratio identities (T2)

Direct from (T1):

```text
(m_l / m_k)²  =  λ_l^TT / λ_k^TT  =  [l(l + 2) − 2] / [k(k + 2) − 2]      (T2)
```

The numerator and denominator are integers for integer `l, k`, so every ratio is a rational number. In particular the spectrum-normalised ratios are

```text
(m_l / m_2)²  =  [l(l + 2) − 2] / 6
```

with the first few values: `(m_3/m_2)² = 13/6`, `(m_4/m_2)² = 22/6 = 11/3`, `(m_5/m_2)² = 33/6 = 11/2`, `(m_6/m_2)² = 46/6 = 23/3`. ∎

### 2.3 Uniform Higuchi stability (T3)

The Higuchi (1987) non-ghost bound for a massive spin-2 field on a de Sitter background with cosmological constant Λ is

```text
m²  >  2 Λ / 3     (non-ghost criterion)
```

with saturation `m² = 2Λ/3` giving the partially-massless (null-norm) case. At each mode `l`:

```text
m_l² / (2 Λ / 3)  =  ([l(l+2) − 2] ℏ²/(c²R²)) / (2 · 3/R² · ℏ²/(3c²))
                  =  [l(l+2) − 2] / 2
```

For `l = 2`: `[l(l+2) − 2]/2 = 6/2 = 3`, reproducing the retained Higuchi-factor-3 corollary.

For `l ≥ 2`: the function `f(l) = [l(l+2) − 2]/2 = (l² + 2l − 2)/2` is strictly increasing in `l ≥ 2`, giving

```text
m_l² / (2Λ/3)  ≥  3    with equality iff l = 2.                            (T3)
```

Every tower mode satisfies the Higuchi bound strictly. The lowest tower margin is 3 (at `l = 2`), and the margin grows as `l²/2 + O(l)` for higher modes. ∎

## 3. Numerical values on the retained surface

Using `R = c/H_0 ≈ 1.373 × 10²⁶ m` (Hubble radius today), matching the numerical convention of [`GRAVITON_MASS_DERIVED_NOTE.md`](GRAVITON_MASS_DERIVED_NOTE.md); this pin is **bounded, not native-axiom**.

| `l` | `λ_l^TT · R²` | `m_l` (eV) | ratio `m_l/m_2` | Higuchi margin `m_l²/(2Λ/3)` |
|-----|---------------|------------|----------------|-------------------------------|
| 2 (graviton) | 6 | 3.52 × 10⁻³³ | 1.000 | 3 |
| 3 | 13 | 5.18 × 10⁻³³ | √(13/6) ≈ 1.472 | 13/2 |
| 4 | 22 | 6.74 × 10⁻³³ | √(22/6) ≈ 1.915 | 11 |
| 5 | 33 | 8.26 × 10⁻³³ | √(33/6) ≈ 2.345 | 33/2 |
| 6 | 46 | 9.75 × 10⁻³³ | √(46/6) ≈ 2.769 | 23 |
| 7 | 61 | 1.12 × 10⁻³² | √(61/6) ≈ 3.189 | 61/2 |
| 8 | 78 | 1.27 × 10⁻³² | √(78/6) ≈ 3.606 | 39 |

The **ratios** (column 4) and **Higuchi margins** (column 5) are structural — they depend only on `l` and not on `R`. The **numerical masses** (column 3) are bounded, conditional on the cosmology-scale identification fixing the S³ radius `R`.

## 4. Observational status

**No tower mode is currently observable.** The lightest compactness mode
(`l = 2`, the graviton row already packaged on `main`) is at
`m_g ≈ 3.5 × 10⁻³³ eV`, below current detector sensitivity by roughly
`10¹⁰` against the strongest model-independent bound quoted in the companion
note. Higher-`l` compactness modes are heavier by at most `√(l²/6)` at fixed
`l`; this is still `~10⁻³² eV` at `l = 10`, far below observation.

**The ratio identities (T2) are in principle falsifiable** only after the
compactness modes have a validated physical readout. A future observation of
two or more spin-2 compactness modes with a ratio inconsistent with
`√([l(l+2)−2]/[k(k+2)−2])` for every integer pair `(l, k)` would falsify the
retained `S³` + spectral-gap structure.

**The Higuchi margin (T3) is a self-consistency constraint** on the retained theory. It cannot be falsified by cosmology-scale observation alone because it is not a numerical prediction; it is a structural stability statement. An experimental detection of a ghost spin-2 mode, or of a spin-2 mass exactly at the Higuchi boundary, would falsify the identification — but the retained structure strictly forbids this.

## 5. What this theorem does and does not close

**Retains / packages exactly (new):**

- The full tower identity `m_l² = [l(l+2) − 2] · ℏ²/(c²R²)` for every `l ≥ 2`, as a structural extension of the retained graviton-mass identity.
- The pure-rational ratio identities `(m_l/m_k)² ∈ ℚ` for every integer pair `(l, k)`.
- The uniform Higuchi stability statement `m_l²/(2Λ/3) ≥ 3` with strict equality only at the lowest mode.
- The reduction: the whole infinite tower of spin-2 TT compactness masses is pinned by the **same** single open number `R` that carries `Λ` and `m_g`.

**Does NOT close:**

- The numerical value of `R` / `R_Λ`: unchanged from the matter-bridge open lane.
- The 4D-effective-theory interpretation of these compactness masses as physical Fierz-Pauli masses — inherits the same vDVZ caveat as the retained single-mode `m_g` theorem.
- The claim that higher `l` modes are separately observable particle states.
- The Vainshtein-screening / solar-system consistency argument — unchanged.
- Detectability: none of the tower modes are within current reach.

## 6. Dual-status architecture

Directly parallels the graviton-mass single-mode theorem and [`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md), [`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md):

- **retained structural tower (this note):**
  `m_l² = [l(l+2) − 2] · ℏ²/(c²R²)` and its ratio + Higuchi consequences, on the retained de Sitter + `S³` surface.
- **bounded quantitative continuation (unchanged):**
  each `m_l` has a bounded numerical value conditional on the cosmology-scale identification; the lightest `m_2 ≈ 3.52 × 10⁻³³ eV` is already captured in [`GRAVITON_MASS_DERIVED_NOTE.md`](GRAVITON_MASS_DERIVED_NOTE.md).

## 7. Package reduction summary

| Observable | Status before | Status after |
|-----------|---------------|--------------|
| Λ = 3/R² | retained identity | unchanged |
| m_g² = 2ℏ²Λ/c² (l = 2) | retained identity | unchanged |
| **m_l² = [l(l+2)−2]·ℏ²/(c²R²), l ≥ 2** | (not packaged) | **retained identity (T1)** |
| **(m_l/m_k)² ∈ ℚ** | (not packaged) | **retained identity (T2)** |
| **m_l²/(2Λ/3) ≥ 3 for all l ≥ 2** | (not packaged) | **retained identity (T3)** |
| numerical `m_l` values | bounded | unchanged (one per mode) |

Before: one identity (graviton `l = 2` only), one open number (`R`).
After: one identity per mode `l`, still one open number (`R`).

The retained cosmology package now carries structurally the **entire** Lichnerowicz TT spin-2 spectrum on the compact slice, not just its lowest member.

## 8. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_graviton_spectral_tower.py
```

Expected: `PASS=89, FAIL=0`.

## 9. Cross-references

- `docs/COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` — `Λ = 3/R²`
- `docs/GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` — single-mode `m_g² = 2ℏ²Λ/c²`
- `docs/GRAVITON_MASS_DERIVED_NOTE.md` — bounded numerical `m_g` companion
- `docs/S3_GENERAL_R_DERIVATION_NOTE.md`, `docs/S3_CAP_UNIQUENESS_NOTE.md` — `S³` topology
- Higuchi 1987 "Forbidden mass range for spin-2 field theory in de Sitter spacetime" — `m² > 2Λ/3` non-ghost condition
- Deser & Nepomechie 1984, Gibbons & Hawking 1993 — TT spectrum on constant-curvature spaces
