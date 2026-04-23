# Neutrino Absolute Mass Sum Σm_ν Prediction

**Date:** 2026-04-22
**Status:** Derived Σm_ν range from retained chain, with two scope surfaces. Testable against cosmological bounds.
**Primary runner:** `scripts/frontier_neutrino_mass_sum_prediction.py`

## 0. Prediction

**Framework prediction**: `Σm_ν ∈ [0.059, 0.102] eV`, comfortably below the current cosmological bound `Σm_ν < 0.12 eV` (Planck 2018 TTTEEE + lowE + BAO, 95% CL).

The range endpoints correspond to two scope surfaces:

- **Pure retained chain (A)**: `Σm_ν ≈ 0.102 eV = 85% of current bound`.
- **Observable-corrected (B, uses Δm²_21_obs once)**: `Σm_ν ≈ 0.065 eV = 54% of current bound`.

Both use the retained Majorana staircase with `k_A = 7`, `k_B = 8`, `ε/B = α_LM/2`.

## 1. Derivation chain (retained)

From `NEUTRINO_MASS_DERIVED_NOTE.md`:

- `A = M_Pl · α_LM^7`
- `B = M_Pl · α_LM^8`
- `ε/B = α_LM/2` (retained residual-sharing)
- `M_1 = B(1 − α_LM/2)`, `M_2 = B(1 + α_LM/2)`, `M_3 = A`
- `y_ν^eff = g_weak²/64` (retained local Dirac theorem)
- Permutation σ: `m_1 = y²v²/M_3`, `m_2 = y²v²/M_2`, `m_3 = y²v²/M_1`

Numerical retained values (verified by the runner):

```text
M_1 ≈ 5.34 × 10^10 GeV
M_2 ≈ 5.85 × 10^10 GeV
M_3 ≈ 6.16 × 10^11 GeV

m_1 ≈  4.37 meV       (lightest; from M_3)
m_2 ≈ 45.9  meV       (middle)
m_3 ≈ 50.4  meV       (heaviest; atmospheric — retained to +3.5% of NuFit)

Σm_ν(A) ≈ m_1 + m_2 + m_3 ≈ 100.7 meV  (pure diagonal)
```

## 2. Pure diagonal (A) — inherits solar-gap over-prediction

On the pure diagonal benchmark:

```text
Δm²_21 = m_2² − m_1² ≈ (45.9)² − (4.37)² ≈ 2089 meV² = 2.09 × 10⁻³ eV²
```

vs observed `Δm²_21 = 7.41 × 10⁻⁵ eV²`. The predicted value is `28×` too large — the well-documented solar-gap open lane (requires off-diagonal `M_R` texture; not derived from retained core).

Therefore Part (A) is the pure retained prediction, but it does NOT close the solar gap.

## 3. Observable-corrected (B) — uses Δm²_21_obs once

Strategy: trust the retained `m_1` (from `M_3 = A`, which is well-separated from `M_1, M_2` and not affected by the texture mixing in the near-degenerate doublet) and the retained `m_3` (atmospheric, retained to 3.5%). Replace the retained `m_2` (which inherits the solar gap) by

```text
m_2_corrected = √(m_1² + Δm²_21_obs) ≈ 9.71 meV
```

Giving:

```text
m_1 ≈  4.37 meV      (retained)
m_2 ≈  9.71 meV      (corrected by observed Δm²_21)
m_3 ≈ 50.4  meV      (retained)

Σm_ν(B) ≈ 64.5 meV
```

This prediction uses **one** observational input (`Δm²_21`) as a bridge over the open solar gap; the rest remains retained.

## 4. Baseline comparison

For reference, the **absolute minimum Σm_ν** under normal ordering (NO) with lightest neutrino = 0:

```text
Σm_ν(NO, m_1 = 0)_min = √Δm²_21_obs + √Δm²_31_obs
                      ≈ 8.61 + 50.0 meV
                      ≈ 58.6 meV
```

So Part (B) = 64.5 meV is 6 meV above the NO minimum — consistent with a non-zero `m_1 ≈ 4 meV`.

## 5. Comparison with cosmological bounds

| Surface | Σm_ν (meV) | Planck 2018 bound (meV) | Fraction of bound |
|---------|-----------|------------------------|-------------------|
| Part (A) pure retained | 100.7 | 120 | 84% |
| Part (B) corrected | 64.5 | 120 | 54% |
| NO minimum (lightest = 0) | 58.6 | 120 | 49% |

Both (A) and (B) are testable against tightening future cosmological bounds:

- DESI 2024 BAO + Planck: `Σm_ν < 0.072 eV` (reported by DESI combination) — Part (A) = 0.101 eV **would exceed** this tighter bound; Part (B) = 0.0645 eV is below it.
- CMB-S4 + Euclid (2030s): projected `Σm_ν < 0.03-0.04 eV` — both (A) and (B) would be **in tension** with this.

So the framework's Σm_ν prediction is **falsifiable** by near-future cosmological surveys. A DESI-level tightening would distinguish Part (A) from Part (B), giving scientific leverage on the solar-gap open lane.

## 6. What this note does and does not close

**Does**:
- Derive a concrete numerical prediction for Σm_ν on two retained-scope surfaces.
- Identify Part (B) as the robust framework prediction against M_R texture corrections (since `m_1` and `m_3` live on well-separated Majorana scales).
- Provide a falsifiable cosmological-observable prediction.

**Does NOT**:
- Close the solar-gap open lane (Δm²_21 still over-predicted by 28× on the diagonal benchmark).
- Derive `Δm²_21` from retained M_R off-diagonal texture (that remains the open lane).
- Promote the neutrino-mass lane from bounded to retained (that requires the M_R texture derivation).

## 7. Runner

`scripts/frontier_neutrino_mass_sum_prediction.py` verifies:

1. Majorana heavy spectrum `(M_1, M_2, M_3)` from retained staircase.
2. Diagonal light-neutrino masses `(m_1, m_2, m_3) = (4.37, 45.9, 50.4) meV`.
3. Retained `m_3` matches atmospheric within 5%.
4. Part (A) `Σm_ν ≈ 0.101 eV` (diagonal).
5. Diagonal `Δm²_21` over-prediction = 28× vs observed.
6. Part (B) `Σm_ν ≈ 0.065 eV` (corrected via observed `Δm²_21`).
7. Both predictions below Planck 2018 bound; scope discipline noted.
8. NO-minimum baseline `≈ 0.059 eV` for comparison.

Expected: 9/9 PASS.

## 8. Cross-references

- `docs/NEUTRINO_MASS_DERIVED_NOTE.md` — retained neutrino mass derivation chain.
- `docs/DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md` — atmospheric-scale theorem.
- `docs/NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md` — k_B − k_A = 1.
- `docs/NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE.md` — ε/B = α_LM/2.
- Planck 2018 collaboration, *Planck 2018 results. VI. Cosmological parameters*, A&A 641 (2020) A6.
