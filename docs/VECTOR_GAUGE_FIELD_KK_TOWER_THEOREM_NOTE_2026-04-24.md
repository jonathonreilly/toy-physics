# Vector Gauge-Field KK Tower on Retained S³ Theorem

**Date:** 2026-04-24
**Status:** **retained standalone structural-identity theorem** on `main`. Companion to [`GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md`](GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md), which packages the **spin-2** TT graviton tower on retained S³. The present theorem packages the **spin-1** vector gauge-field KK tower on the same retained surface, with explicit eigenvalues, ratios, and connection to retained `Λ = 3/R²`. This is the natural sibling to the spin-2 tower; both come from the Lichnerowicz / Hodge-Laplace spectrum on round S³ but with different spin-curvature shifts.
**Primary runner:** `scripts/frontier_vector_gauge_field_kk_tower.py`

---

## 0. Statement

**Theorem (vector gauge-field KK tower).** On the retained S³ + spectral-gap cosmology surface ([`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)), every gauge-field species (U(1)_em, SU(2)_L, SU(3)_color, U(1)_{B−L} extension if gauged) inherits a Kaluza–Klein tower of transverse vector modes from the round-S³ spectrum, with masses

```text
(V1)   m_l²  =  [ l(l+2) − 1 ] · ℏ² / (c² R²)         for l = 1, 2, 3, …
```

The tower starts at `l = 1` (in contrast to the graviton tower's `l ≥ 2`), giving a lowest-mode mass

```text
m_1²  =  2 · ℏ² / (c² R²)  =  (2/3) · Λ · ℏ² / c²       (with retained Λ = 3/R²)
```

and inter-mode ratios

```text
(V2)   (m_l / m_k)²  =  [ l(l+2) − 1 ] / [ k(k+2) − 1 ]
```

are pure rationals.

For massless gauge fields (photon, gluon) on the retained S³ slice:
- The l = 0 (constant) mode is gauge-equivalent to zero — the standard SM **massless photon / massless gluon zero mode**.
- The l ≥ 1 modes form a tower of ultralight massive copies with masses set by the cosmological scale (`m_1 ~ 10⁻³³ eV` at observed `R ~ R_Λ`).

For massive gauge fields (W, Z, after Higgs mechanism), KK contributions are negligible compared to electroweak masses (`m_W ~ 80 GeV ≫ √2/R ~ 10⁻³³ eV`), so the KK tower is effectively `m_l ≈ m_W` to all observable precision.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| Retained `S³` spatial topology | [`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md), [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md) |
| Retained `Λ = 3/R²` spectral-gap identity | [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) |
| Retained graviton spectral tower | [`GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md`](GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md) |
| Retained native SU(2)_L | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) |
| Retained graph-first SU(3) | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| Retained U(1)_Y commutant | [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) |
| Hodge–Laplace transverse vector spectrum on round S³ | textbook (Higuchi 1987, Allen & Jacobson 1986) |

## 2. Background: vector spectrum on S³

The Hodge–Laplace operator acting on transverse divergence-free vector fields on round S^d has eigenvalues `λ_l = [l(l+d−1) − 1] / R²` for `l = 1, 2, …`. On `S³` (`d = 3`):

```text
λ_l(transverse vector)  =  [ l(l+2) − 1 ] / R².
```

The "−1" is the spin-1 curvature-coupling shift (analog of the spin-2 Lichnerowicz "−2"). Compare with:

| Spin | Tower eigenvalue (× R²) | Lowest l |
|------|------------------------|----------|
| Spin-0 (scalar) | `l(l+2)` | l = 0 |
| Spin-1 (vector) | `l(l+2) − 1` | l = 1 |
| Spin-2 (TT graviton) | `l(l+2) − 2` | l = 2 |

The pattern: `λ_l × R² = l(l+2) − s²` where `s` is approximately the spin (more precisely, related to the spin via the Casimir of the SO(4) tangent group). This unifies the scalar / vector / tensor towers on S³.

Standard KK identification: each transverse vector eigenmode contributes a 4D vector field with rest-mass `m_l² c²/ℏ² = λ_l`.

## 3. Derivation

### 3.1 (V1) Tower mass identity

Applying the standard Hodge–Laplace transverse vector spectrum on round S³ of radius `R`:

```text
m_l²  =  ℏ² · λ_l / c²
       =  ℏ² · [l(l+2) − 1] / (c² R²)        for l = 1, 2, 3, …                    (V1)
```

With retained `Λ = 3/R²`:

```text
m_l²  =  [l(l+2) − 1] / 3  ·  ℏ² Λ / c².
```

For `l = 1`:

```text
m_1²  =  (1·3 − 1) / 3  ·  ℏ² Λ / c²  =  (2/3) ℏ² Λ / c²
       =  2 ℏ² / (c² R²).
```

### 3.2 (V2) Inter-mode rational ratios

Direct from (V1):

```text
(m_l / m_k)²  =  [l(l+2) − 1] / [k(k+2) − 1]                                       (V2)
```

is rational for every integer pair (l, k). Spectrum-normalised ratios (m_l / m_1)² = [l(l+2) − 1] / 2:

| l | l(l+2) − 1 | (m_l / m_1)² | (m_l / m_1) |
|---|------------|---------------|--------------|
| 1 | 2 | 1 | 1 |
| 2 | 7 | 7/2 | √(7/2) ≈ 1.871 |
| 3 | 14 | 7 | √7 ≈ 2.646 |
| 4 | 23 | 23/2 | √(23/2) ≈ 3.391 |
| 5 | 34 | 17 | √17 ≈ 4.123 |

### 3.3 Comparison with graviton tower

The graviton tower (T1-T3) has eigenvalues `λ_l^TT × R² = l(l+2) − 2` starting at `l = 2`. Compared to vector tower `λ_l^V × R² = l(l+2) − 1` starting at `l = 1`:

| l | spin-1 (V): l(l+2) − 1 | spin-2 (T): l(l+2) − 2 |
|---|---------------------------|---------------------------|
| 1 | 2 | (no transverse-traceless mode) |
| 2 | 7 | 6 |
| 3 | 14 | 13 |
| 4 | 23 | 22 |
| 5 | 34 | 33 |
| 6 | 47 | 46 |

The two towers differ by `Δ(l) = (l(l+2)−1) − (l(l+2)−2) = +1` at every common l. The vector tower is one curvature-shift unit above the spin-2 tower.

Particular ratio: at `l = 2` (lowest spin-2 mode = graviton):

```text
m_2^V / m_2^TT  =  √(7/6) ≈ 1.080
```

So at `l = 2`, the vector mode is ~8% heavier than the graviton mode.

## 4. Numerical evaluation

Using `R = c/H_0 ≈ 1.373 × 10²⁶ m` (Hubble radius, matching the retained graviton-mass numerical convention):

```text
ℏ c / R  ≈  1.4375 × 10⁻³³ eV  (mass-energy prefactor)
```

| l | m_l (eV) | ratio m_l / m_1 |
|---|---|---|
| 1 (lowest vector) | √2 × 1.44e-33 ≈ 2.03 × 10⁻³³ | 1.000 |
| 2 | √7 × 1.44e-33 ≈ 3.80 × 10⁻³³ | √(7/2) ≈ 1.871 |
| 3 | √14 × 1.44e-33 ≈ 5.38 × 10⁻³³ | √7 ≈ 2.646 |
| 4 | √23 × 1.44e-33 ≈ 6.89 × 10⁻³³ | √(23/2) ≈ 3.391 |

**Comparison with l=2 graviton:** m_2^TT (graviton) ≈ 3.52 × 10⁻³³ eV, vs lowest spin-1 m_1^V ≈ 2.03 × 10⁻³³ eV. Ratio m_g/m_1^V = √6/√2 = √3 ≈ 1.732.

## 5. Physical content and observability

### 5.1 Massless gauge field zero mode

For unbroken gauge symmetries (electromagnetism U(1)_em, color SU(3)), the **l = 0 constant mode** is gauge-equivalent to zero and contributes the standard SM **massless photon and gluons**. The KK tower starts at `l = 1`.

### 5.2 KK tower for photon and gluon

The tower for the photon and gluons lies at:
- m_1 ≈ 2.03 × 10⁻³³ eV (lowest)
- m_2 ≈ 3.80 × 10⁻³³ eV
- m_3 ≈ 5.38 × 10⁻³³ eV
- ...

These ultralight massive vector modes are well below any current observational sensitivity. Strongest model-independent constraints on photon mass: Lakes (2003) `m_γ < 10⁻¹⁸ eV`. Framework prediction `m_1^γ ~ 10⁻³³ eV` is 15 orders of magnitude below.

### 5.3 KK tower for W and Z bosons

For the broken SU(2)_L × U(1)_Y → U(1)_em, W and Z get masses from the Higgs mechanism: `m_W ≈ 80.4 GeV`, `m_Z ≈ 91.2 GeV`. KK additions:

```text
m_W,l²  =  m_W² + [l(l+2) − 1] ℏ² / (c² R²)
        ≈  m_W²  (Higgs mass dominates by 60+ orders of magnitude)
```

The KK shift is `~10⁻³³ eV` per mode, completely negligible compared to `m_W = 80 GeV`. So W and Z KK towers are `m_W,l ≈ m_W` for all l.

### 5.4 Non-observability and falsifiability

The framework predicts:
- **Photon and gluon** KK tower at `m ~ 10⁻³³ eV` (far below any direct detection).
- **W/Z** KK tower indistinguishable from the standard W/Z (KK shifts negligible).

Since the KK mass scale is set by `1/R ~ H_0 ~ 10⁻³³ eV`, the tower is "frozen" at the cosmological scale and not directly observable in particle physics. The structural prediction is the **existence** of the tower (forced by retained S³ topology), not the specific mass values.

**Falsifiability:**
- A confirmed photon mass above `~10⁻¹⁸ eV` (current bound) at >5σ would be inconsistent with the framework's massless zero mode (unless attributed to BSM mechanisms).
- The lowest KK photon mode at `~10⁻³³ eV` is invisible to any conceivable terrestrial experiment.
- Cosmological signatures (e.g., gauge boson dark matter from the KK tower being thermally produced) would test the framework.

## 6. Combined retained spin tower

Combined with my retained graviton tower theorem, the framework predicts the following spin tower on retained S³:

| Spin | Lowest l | (Mass × R / ℏ)² | Lowest mass at R = c/H_0 |
|------|----------|---------------------|---------------------------|
| 0 (scalar) | 0 | 0 | 0 (zero mode) |
| 0 (scalar, l=1) | 1 | 3 | √3 × 1.44e-33 ≈ 2.49 × 10⁻³³ eV |
| 1 (vector) | 1 | 2 | √2 × 1.44e-33 ≈ 2.03 × 10⁻³³ eV |
| 2 (TT graviton) | 2 | 6 | √6 × 1.44e-33 ≈ 3.52 × 10⁻³³ eV |

The "spin-curvature shift" pattern `l(l+2) − s_curv` with `s_curv = 0, 1, 2` for `s = 0, 1, 2` is a structural fingerprint of the round-S³ spectral structure.

## 7. Scope and boundary

**Claims:**

- (V1) `m_l² = [l(l+2) − 1] ℏ²/(c²R²)` for `l ≥ 1` on retained S³.
- (V2) Ratios `(m_l/m_k)² ∈ ℚ`.
- Connection to retained `Λ = 3/R²` via `m_1² = (2/3) Λℏ²/c²`.
- Combined with graviton T1-T3, covers spin-0, spin-1, spin-2 towers on S³.

**Does NOT claim:**

- Any beyond-SM gauge-field species (the framework retains only SM gauge group).
- Direct observational evidence for the KK tower (masses too small).
- A native-axiom derivation of `R` (cosmology-scale identification, separately bounded).
- 4D-effective-theory interpretation of the KK modes as physically distinct vector bosons (depends on quantization scheme).
- Mass for photon or gluon at finite scale (the "zero mode" at l = 0 is gauge-equivalent to zero, giving massless SM zero modes).

## 8. Falsifiability

- Photon mass detection above `~10⁻¹⁸ eV` (current Lakes 2003 bound) inconsistent with retained massless zero mode.
- Multi-mode photon signatures inconsistent with KK tower would falsify the retained S³ topology.
- Cosmological photon-mass-from-S³ signature: dark photon abundance = `m_1` × (KK production rate × cosmic time). Within current cosmological bounds.

Currently no experimental sensitivity to this prediction.

## 9. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_vector_gauge_field_kk_tower.py
```

Expected: all checks pass.

The runner:

1. Computes vector KK eigenvalues `λ_l = l(l+2) − 1` for `l = 1, ..., 20`.
2. Verifies (V1) `m_l² = [l(l+2)−1] ℏ²/(c²R²)`.
3. Verifies (V2) rational ratios `(m_l/m_k)²`.
4. Confirms the spin-curvature shift pattern: scalar (0), vector (1), graviton (2).
5. Computes numerical mass values at observed `R ~ R_Λ`.
6. Compares lowest mode `m_1` to graviton lowest `m_2` (factor √(2/6) = 1/√3 lighter).
7. Compares to current photon mass bounds.

## 10. Cross-references

- [`GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md`](GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md) — sibling spin-2 tower
- [`GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) — single-mode graviton retained
- [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) — `Λ = 3/R²`
- [`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md) — retained S³ topology
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md), [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained gauge structure
- Allen & Jacobson 1986, Higuchi 1987 — TT vector and tensor harmonics on dS / S³
- Lakes 1998, Phys. Rev. Lett. 80, 1826 — photon mass bound `m_γ < 10⁻¹⁸ eV`
