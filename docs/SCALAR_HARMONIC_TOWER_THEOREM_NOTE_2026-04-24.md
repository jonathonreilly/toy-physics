# Scalar Harmonic Compactness Spectral Tower on Retained S^3

**Date:** 2026-04-24

**Status:** **proposed_retained structural-identity extension theorem** on `main`.
Packages the scalar Laplace-Beltrami compactness spectrum on the same retained
round `S^3` surface used by the spectral-gap cosmology, vector compactness,
and graviton compactness towers.

**Script:** `scripts/frontier_scalar_harmonic_tower.py`

**Upstream authorities (all retained/admitted on `main`):**
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md),
[`VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE_2026-04-24.md`](VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE_2026-04-24.md),
[`GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md`](GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md),
[`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md),
[`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md)

---

## 0. Scope

This note packages the **structural compactness spectrum** for scalar
harmonics on the retained round `S^3_R` slice:

```text
lambda_l^S = l(l+2) / R^2,        l = 0, 1, 2, ...
```

Applying the same compact-slice mass bookkeeping used in the vector and
graviton compactness towers gives:

```text
m_l^2 = l(l+2) hbar^2 / (c^2 R^2).        (S1)
```

The retained content is the eigenvalue tower, the pure-rational ratio surface,
and the exact lowest non-zero coefficient relative to the retained
`Lambda = 3/R^2` identity. This note does **not** claim that the retained
Standard Model contains a fundamental massless scalar, and it does not promote
the compactness modes as detected 4D particle states.

## 1. Theorem

For any retained/admitted scalar carrier treated on the retained round
`S^3_R` compact slice:

1. **Scalar compactness tower**

   ```text
   m_l^2 = l(l+2) hbar^2 / (c^2 R^2),       l >= 0.       (S1)
   ```

   The `l = 0` compactness mode has zero compactness mass contribution.

2. **Pure-rational squared-mass ratios**

   ```text
   (m_l/m_k)^2 = l(l+2) / [k(k+2)] in Q,     l,k >= 1.    (S2)
   ```

3. **Lambda coefficient form**

   Using the retained `Lambda = 3/R^2` identity:

   ```text
   m_l^2 = [l(l+2)/3] hbar^2 Lambda / c^2.
   ```

   The lowest non-zero scalar compactness mode is therefore

   ```text
   m_1^2 = hbar^2 Lambda / c^2.                             (S3)
   ```

## 2. Derivation

The standard scalar Laplace-Beltrami spectrum on a round three-sphere is

```text
lambda_l^S R^2 = l(l+2),        l >= 0.
```

The compact-slice mass identification used in the retained vector and graviton
towers is applied mode-by-mode:

```text
m_l^2 c^2 / hbar^2 = lambda_l^S.
```

Substituting the spectrum gives (S1). Dividing (S1) at levels `l` and `k`
gives (S2). Substituting the retained `Lambda = 3/R^2` identity gives the
Lambda coefficient form. At `l = 1`, `l(l+2) = 3`, so the coefficient is
exactly one and (S3) follows.

No observational value of `R` enters this derivation.

## 3. Relation to the Retained Spin Towers

On the retained round `S^3` slice, the scalar, transverse vector one-form, and
TT spin-2 spectra share a simple curvature-shift bookkeeping pattern:

| carrier | compactness eigenvalue numerator | lowest level | status |
|---|---:|---:|---|
| scalar | `l(l+2)` | `l = 0` zero compactness mode; `l = 1` first non-zero mode | this theorem |
| vector transverse one-form | `l(l+2) - 1` | `l = 1` | retained vector tower |
| spin-2 transverse-traceless | `l(l+2) - 2` | `l = 2` | retained graviton tower |

This is a bookkeeping identity for these three spectra on the round `S^3`
carrier. It is not a universal spin formula beyond this listed context.

Relative to `Lambda`, the lowest non-zero compactness coefficients are:

```text
scalar l=1:        m_1^2 = 1     * hbar^2 Lambda / c^2
vector l=1:        m_1^2 = 2/3   * hbar^2 Lambda / c^2
TT spin-2 l=2:     m_2^2 = 2     * hbar^2 Lambda / c^2
```

## 4. Numerical Companion Values

If the bounded numerical convention `R = c/H_0` used by the graviton
compactness-mass companion is inserted, the lowest scalar compactness levels
are:

| `l` | `lambda_l^S R^2` | `m_l` (eV) | `m_l/m_1` |
|---:|---:|---:|---:|
| 0 | 0 | `0` | n/a |
| 1 | 3 | `2.49e-33` | 1 |
| 2 | 8 | `4.06e-33` | `sqrt(8/3)` |
| 3 | 15 | `5.57e-33` | `sqrt(5)` |
| 4 | 24 | `7.04e-33` | `sqrt(8)` |
| 5 | 35 | `8.50e-33` | `sqrt(35/3)` |

These numerical masses are **bounded companion values**, not new retained
observables. The retained theorem is the structural tower and its rational
ratios.

## 5. Physical Boundary

This theorem keeps the same boundary discipline as the vector and graviton
compactness towers:

- It packages the compact `S^3` scalar harmonic spectrum; it does not assert
  the existence of any specific scalar species.
- The Standard Model Higgs is not a massless retained scalar. Its electroweak
  mass dominates any cosmological compactness correction by many orders of
  magnitude.
- A full 4D-effective particle interpretation of the compactness modes is
  bounded, not promoted.
- The numerical value of each mass remains pinned by the same open/conditioned
  radius `R` as the retained `Lambda` and existing compactness towers.

## 6. What This Adds

Before this note, the public retained surface explicitly carried the scalar
spectral gap through `Lambda = 3/R^2`, the spin-1 compactness tower, and the
spin-2 TT compactness tower. This note adds the parallel spin-0 structural
tower:

```text
m_l^2 = l(l+2) hbar^2 / (c^2 R^2),      l >= 0.
```

The first non-zero scalar mode gives the exact identity

```text
m_1^2 = hbar^2 Lambda / c^2.
```

No new numerical calibration is introduced.

## 7. Reproduction

```bash
python3 scripts/frontier_scalar_harmonic_tower.py
```

Expected: `PASSED: 51/51`.
