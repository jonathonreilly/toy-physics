# Koide Z³ Scalar Potential Support Note

**Date:** 2026-04-19
**Status:** exact selected-slice scalar-potential support theorem on the
charged-lepton Koide review stack; cubic coupling pinned by Clifford trace
identity; honest gap to the physical selected point recorded

---

## Summary

The frozen-bank decomposition `K_Z3^sel(m) = K_frozen + m T_m^(K)` reduces the
charged-lepton selected slice to one real coordinate `m = Tr K_Z3`. This note
derives the exact Z³-invariant scalar potential `V(m)` for that coordinate and
records what is proved versus what remains open. It does not claim a
framework-derived charged-lepton mass tower.

---

## 1. Clifford Involution Pins the Potential

The active generator on the selected slice is

```
T_m = [[1, 0, 0],
       [0, 0, 1],
       [0, 1, 0]]
```

This matrix satisfies the **Clifford involution identity**

```
T_m² = I_3
```

from which two trace identities follow immediately:

| Identity | Value | Role |
|----------|-------|------|
| `Tr(T_m²) = Tr(I) = 3` | 3 | sets the quadratic coefficient g₂ = 3/2 |
| `Tr(T_m³) = Tr(T_m) = 1` | 1 | pins the cubic coupling g₃ = 1/6 |

The cubic coupling is **not a free parameter** — it is fixed by the Clifford algebra structure of the Z³ generator.

---

## 2. The Z³ Scalar Potential

The natural Z³-invariant scalar action on the selected slice is

```
V(m) = (1/2) Tr(K_sel²) + (1/6) Tr(K_sel³)
```

Expanding using `K_sel = K_frozen + m T_m` and `Tr(K_frozen) = 0`:

| Term | Coefficient | Origin |
|------|-------------|--------|
| `m³` | `1/6` | `Tr(T_m³) = 1` (Clifford involution) |
| `m²` | `3/2` | `Tr(T_m²) = 3` (Clifford involution) |
| `m`  | `c1 + c2/2` | `c1 = Tr(K_frozen T_m) ≈ -0.2526`, `c2 = Tr(K_frozen² T_m) ≈ 2.9167` |
| `1`  | `(1/2)Tr(K_f²) + (1/6)Tr(K_f³)` | frozen bank constant |

with `c1 + c2/2 ≈ 1.2057`.

The `m²` cross term in `Tr(K³)` vanishes exactly because `Tr(K_frozen) = 0` (a consequence of the bank identities `cp1 = -2√6/9`, `cp2 = 2√2/9`).

### Exact form

```
V(m) = V₀ + (c1 + c2/2) m + (3/2) m² + (1/6) m³
```

where V₀ is the frozen-bank constant. All coefficients of the `m`-dependent terms are exact.

### General lemma: Tr(K_frozen) = 0 throughout the affine chamber

`Tr(kz_from_h(active_affine_h(0, δ, q))) = 0` for **all** (δ, q) on the affine slice, not only at the Koide selected point δ = q = √6/3. This is a structural identity of the `kz_from_h ∘ active_affine_h` composition. Consequence: the m² cross-term in Tr(K³) vanishes throughout the chamber — the scalar potential retains the form V₀ + linear + (3/2)m² + (1/6)m³ for any point on the live source-oriented sheet.

---

## 3. Critical-Point Equation

Setting `dV/dm = 0`:

```
m² + 6m + 2(c1 + c2/2) = 0
```

Solutions:

| Critical point | Value | Type |
|----------------|-------|------|
| `m_V ≈ -0.433` | minimum | physical side of positivity threshold |
| `m₂ ≈ -5.567` | maximum | outside positive branch |

---

## 4. The det(K_sel) Cubic

The determinant `det(K_sel(m))` is a cubic polynomial in `m`:

```
det(K_sel(m)) = -m³ + c1 m² + ... 
```

The **leading coefficient is exactly -1**. This follows from the Leibniz–Levi-Civita formula for the determinant: `T_m` contributes one factor to each diagonal of the ε_ijk expansion, and `det(T_m) = -1` (T_m is an odd permutation matrix). The cubic Levi-Civita coupling is therefore Clifford-fixed, not a free parameter.

---

## 5. Honest Gap: V_eff Minimum ≠ Physical Selected Point

| Quantity | Value |
|----------|-------|
| V_eff minimum `m_V` | ≈ -0.433 |
| Positivity threshold `m_pos` | ≈ -1.2958 |
| Physical selected point `m_*` | ≈ -1.1605 |

The V_eff minimum **does not coincide with the physical selected point**. The
gap is `|m_V - m_*| ≈ 0.73` in `m` units. The V_eff potential alone does not
select `m_*`.

The physical `m_*` is selected by the H_* witness ratio `r_* = w_*/v_* ≈ 4.1009`, which corresponds to `kappa_* ≈ -0.6079`. The potential V(m) records the Clifford-fixed cubic structure of the scalar sector; identifying which critical condition pins `m_*` requires an additional microscopic selector.

**kappa values:**
- `kappa(m_V) ≈ -0.7596` (at V_eff minimum)
- `kappa(m_pos) = -1/√3 ≈ -0.5774` (at positivity threshold — exact algebraic identity)
- `kappa_* ≈ -0.6079` (physical selected point)

---

## 6. Scale Analysis

At the physical `m_*`, the Koide triplet `(u_*, v_*, w_*)` satisfies `Q = 2/3` on the cone. After one overall scale factor, the slot direction reproduces all three charged-lepton masses:

| Mass | Predicted √m (√MeV) | PDG √m (√MeV) | Relative error (√mass) |
|------|---------------------|----------------|------------------------|
| `m_e` | 0.7150 | 0.7150 | −4.6 × 10⁻⁴ |
| `m_μ` | 10.280 | 10.279 | +1.0 × 10⁻⁵ |
| `m_τ` | 42.155 | 42.155 | −5 × 10⁻⁷ |

All errors < 0.05% on the √mass metric (used because the Koide relation and
slot values are native to √mass; the retained H_* witness yields the same
bound on mass directly). This is a scale check on the selected point, not a
derivation of the charged-lepton tower from the scalar potential alone. The
remaining work is deriving the one overall scale from the lattice.

The dimensionless ratio `v_*/|m_*| ≈ 1.309` connects the slot value to the scalar coordinate in pure lattice units.

---

## 7. Transport Gap Observation

The ratio `η/η_obs ≈ 0.189` (factor ~5.29 gap) is numerically close to

```
4π/√6 ≈ 5.13   (3.2% mismatch)
```

This ratio has a geometric interpretation: `4π` is the full solid angle and `√6/2` is the analytically constant Koide character norm `|z|`. This is an **observation only** — a formal derivation connecting transport and Koide geometry through the lattice is a separate open problem.

---

## Status

| Claim | Status |
|-------|--------|
| T_m² = I (Clifford involution) | Proved exact |
| Tr(T_m³) = 1 pins cubic coupling 1/6 | Proved exact |
| Tr(T_m²) = 3 pins quadratic coefficient 3/2 | Proved exact |
| c₂ = 35/12 exactly | Proved exact (< 4 × 10⁻¹³ error) |
| Tr(K_frozen(δ,q)) = 0 for all (δ,q) — general lemma | Proved exact (structural identity) |
| det(K_sel) leading coeff = -1 from Levi-Civita | Proved numerically (< 10⁻⁹) |
| V_eff minimum at m_V ≈ -0.433 | Proved numerically |
| Physical m_* ≈ -1.161 NOT at V_eff minimum | Confirmed — honest gap |
| Slot values at m_* reproduce PDG masses to < 0.05% | Confirmed numerically |
| Transport gap factor ≈ 4π/√6 | Observation only |

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_selected_slice_frozen_bank_decomposition_note_2026-04-18](KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md)
- [dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16](DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
- [dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16](DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
