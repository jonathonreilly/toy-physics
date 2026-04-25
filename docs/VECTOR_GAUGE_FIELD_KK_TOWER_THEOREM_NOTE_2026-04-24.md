# Vector Gauge-Field Compactness Spectral Tower on Retained S^3

**Date:** 2026-04-24

**Status:** **retained structural-identity extension theorem** on `main`.
Packages the transverse spin-1 / gauge-connection compactness spectrum on the
same retained round `S^3` surface used by the spectral-gap cosmology and
graviton compactness towers.

**Script:** `scripts/frontier_vector_gauge_field_kk_tower.py`

**Upstream authorities (all retained/admitted on `main`):**
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md),
[`GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md`](GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md),
[`GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md),
[`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md),
[`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md)

---

## 0. Scope

This note packages the **structural compactness spectrum** for transverse
vector one-forms on the retained round `S^3` slice:

```text
lambda_l^V = [l(l+2) - 1] / R^2,        l = 1, 2, 3, ...
```

Applying the same compact-slice mass bookkeeping used in the graviton
compactness theorem gives:

```text
m_l^2 = [l(l+2) - 1] hbar^2 / (c^2 R^2).        (V1)
```

The retained content is the eigenvalue tower and the pure-rational ratio
surface.  This note does **not** promote a claim that the higher compactness
modes are detected 4D particle states, and it does not introduce any new gauge
species.

## 1. Theorem

For any retained/admitted gauge connection treated as a transverse one-form on
the retained round `S^3_R` compact slice:

1. **Vector compactness tower**

   ```text
   m_l^2 = [l(l+2) - 1] hbar^2 / (c^2 R^2),       l >= 1.       (V1)
   ```

2. **Pure-rational squared-mass ratios**

   ```text
   (m_l/m_k)^2 = [l(l+2) - 1] / [k(k+2) - 1] in Q.              (V2)
   ```

3. **Lambda coefficient form**

   Using the retained `Lambda = 3/R^2` identity:

   ```text
   m_l^2 = [l(l+2) - 1] hbar^2 Lambda / (3 c^2).
   ```

   The lowest vector compactness mode is therefore

   ```text
   m_1^2 = 2 hbar^2 / (c^2 R^2)
         = (2/3) hbar^2 Lambda / c^2.
   ```

## 2. Derivation

The standard transverse one-form spectrum on a round three-sphere is

```text
lambda_l^V R^2 = l(l+2) - 1,        l >= 1.
```

The compact-slice mass identification used in the retained graviton tower is
applied mode-by-mode:

```text
m_l^2 c^2 / hbar^2 = lambda_l^V.
```

Substituting the spectrum gives (V1).  Dividing (V1) at levels `l` and `k`
gives (V2).  Substituting the retained `Lambda = 3/R^2` identity gives the
Lambda coefficient form.  No observational value of `R` enters this derivation.

## 3. Relation to the Retained Spin Towers

On the retained round `S^3` slice, the scalar, vector, and TT spin-2 spectra
share a simple curvature-shift pattern:

| carrier | compactness eigenvalue numerator | lowest level | status |
|---|---:|---:|---|
| scalar | `l(l+2)` | `l = 0` zero compactness mode; `l = 1` first non-zero mode | retained scalar tower |
| vector transverse one-form | `l(l+2) - 1` | `l = 1` | this theorem |
| spin-2 transverse-traceless | `l(l+2) - 2` | `l = 2` | retained graviton tower |

This is a bookkeeping identity for these three spectra on the round `S^3`
carrier.  It is not a universal spin formula beyond this listed context.

The lowest spin-1 compactness mass-squared is one third of the lowest retained
spin-2 compactness mass-squared:

```text
m_1,V^2 / m_2,TT^2 = 2/6 = 1/3.
```

At the common level `l = 2`, the vector numerator is `7` and the TT numerator
is `6`, so:

```text
m_2,V / m_2,TT = sqrt(7/6).
```

## 4. Numerical Companion Values

If the bounded numerical convention `R = c/H_0` used by the graviton
compactness-mass companion is inserted, the lowest vector compactness levels
are:

| `l` | `lambda_l^V R^2` | `m_l` (eV) | `m_l/m_1` |
|---:|---:|---:|---:|
| 1 | 2 | `2.03e-33` | 1 |
| 2 | 7 | `3.80e-33` | `sqrt(7/2)` |
| 3 | 14 | `5.38e-33` | `sqrt(7)` |
| 4 | 23 | `6.90e-33` | `sqrt(23/2)` |
| 5 | 34 | `8.37e-33` | `sqrt(17)` |

These numerical masses are **bounded companion values**, not new retained
observables.  The retained theorem is the structural tower and its rational
ratios.

## 5. Physical Boundary

This theorem keeps the same boundary discipline as the graviton compactness
tower:

- It packages the compact `S^3` mode spectrum for gauge connections; it does
  not assert direct observation of higher compactness modes.
- The photon and gluon zero-mode gauge sectors remain massless in the usual
  gauge sense; this theorem concerns the transverse compactness tower
  beginning at `l = 1`.
- Electroweak `W/Z` masses are dominated by the Higgs mechanism.  Any
  cosmological compactness shift at this scale is negligible relative to the
  retained electroweak masses.
- The theorem applies to retained/admitted gauge connections only.  It does
  not claim that optional sectors such as `U(1)_{B-L}` are gauged.
- A full 4D-effective particle interpretation of the tower is bounded, not
  promoted.

## 6. What This Adds

Before this note, the public retained surface explicitly carried the
cosmological spectral gap, the graviton compactness-mass identity, and the
spin-2 TT compactness tower.  This note adds the parallel spin-1 structural
tower:

```text
m_l^2 = [l(l+2) - 1] hbar^2 / (c^2 R^2),      l >= 1.
```

The entire spin-1 tower is pinned by the same open scale `R` as the retained
`Lambda` and TT compactness tower.  No new numerical calibration is introduced.

## 7. Reproduction

```bash
python3 scripts/frontier_vector_gauge_field_kk_tower.py
```

Expected: `PASSED: 46/46`.
