# Electron Mass: Framework Blockage Analysis

**Date:** 2026-04-19
**Branch:** `frontier/hydrogen-helium-review`
**Script:** `scripts/electron_mass_from_axioms.py`
**Status:** NOT DERIVED — precise blockage located

---

## Summary

The Cl(3)/Z³ framework cannot derive m_e on the current surface. This note
precisely locates the blockage at two independent problems:

1. **No mechanism selects the Koide angle θ_ℓ.** The fundamental reason is
   that the Koide parameterization is a circle in complex space on which
   ALL magnitude-based observables (log|det|, power-law variational
   principles) are FLAT. This is an analytically exact obstruction.

2. **No clean formula for the lepton mass scale m_τ.** No integer-power
   combination of derived quantities {v, α_s(v), α_LM, g₂(v)} reproduces m_τ.

---

## What the framework provides

| Ingredient | Status | Notes |
|------------|--------|-------|
| Three generations | DERIVED | Z³ lattice → C₃[111] irreducible orbit |
| Koide Q = 2/3 automatic | STRUCTURAL | a₀ = √3 is θ-independent (exact) |
| C₃[111] phase spacing 2π/3 | DERIVED | from Z³ translation symmetry |
| Koide family parameterized by θ | ACCOMMODATED | second-order Clifford return |

---

## The analytic obstruction (new result)

The Koide family is parameterized by:

```
√m_k = A (1 + √2 cos(θ + 2πk/3))   k=0,1,2
A = √(M/6),  M = m_e + m_μ + m_τ
```

The DFT character decomposition on the C₃[111] orbit gives:

```
a₀ = (1/√3) Σ v_k                where v_k = 1 + √2 cos(θ + 2πk/3)
z  = (1/√3) Σ v_k ω^k            where ω = e^{2πi/3}
```

**Analytic computation:**

For a₀:
```
Σ v_k = 3 + √2 Σ cos(θ + 2πk/3) = 3 + √2 × 0 = 3
→ a₀ = √3  [independent of θ, exactly]
```

For z:
```
Σ v_k ω^k = Σ ω^k + √2 Σ cos(θ+2πk/3) ω^k
          = 0 + √2 × (3/2) e^{-iθ}        [by Fourier identity]
→ z = (√6/2) e^{-iθ}
→ |z| = √6/2 ≈ 1.2247  [independent of θ, exactly]
```

**Consequence:** Both character components a₀ and |z| are θ-independent.
Any observable of the form:

```
S[θ] = f(a₀, |z|) = f(√3, √6/2)  [constant on the Koide family]
```

The only θ-dependence enters through the **phase** of z: arg(z) = −θ.
Therefore only a **phase-sensitive** observable can select θ_ℓ.

---

## What would break the obstruction

Phase sensitivity requires one of:

1. **An observable that distinguishes the complex phase of z.** This means
   the observable contains a term like Im(z) or arg(z) — a CP-odd or
   species-ordering-sensitive contribution.

2. **A non-C₃-symmetric perturbation.** If the three generations are not
   perfectly symmetric under C₃[111] (e.g., they have different staircase
   thresholds), the character decomposition above changes. A small
   breaking of C₃ symmetry at the staircase level would introduce θ-dependence.

3. **The Ward identity analog for leptons (most tractable path):** The top
   quark mass comes from a Ward identity y_t(M_Pl) = g_latt/√6 that runs
   down to y_t(v) ≈ 1. If a charged-lepton Ward identity
   y_τ(M_Pl) = g_latt^τ/√N_τ exists, it would set the mass scale M
   (via m_τ = y_τ v/√2) and potentially break the C₃ symmetry via the
   flavor structure of g_latt^τ. The specific value N_τ and the identification
   of g_latt^τ are open.

---

## Mass scale problem

No integer-power formula for m_τ from derived framework quantities:

| Formula | Value | m_τ target | Dev |
|---------|-------|-----------|-----|
| v × α_s² | 2.629 GeV | 1.777 GeV | +48% |
| v × α_LM² | 2.025 GeV | 1.777 GeV | +14% |
| v × α_s^(2.17) | 1.777 GeV | 1.777 GeV | 0% (by fit, not clean) |

The best-fit exponent 2.17 is not a clean integer or simple fraction. The
lepton Yukawa y_τ = √2 m_τ/v = 0.0102 has no identified framework origin.

**Interesting near-miss:** v × α_LM² = 2.025 GeV is 14% above m_τ. This is
the closest simple formula and could be the leading term of a series:
m_τ ≈ v × α_LM² × (1 − correction), but the correction (~0.14) is not derivable.

---

## Numerical fingerprint of the blockage

From `scripts/electron_mass_from_axioms.py`:

```
Clifford asymmetry (τ,μ): w₁ = (√m_τ − √m_μ)/(√m_τ + √m_μ) = 0.6079
Clifford asymmetry (μ,e): w₂ = (√m_μ − √m_e)/(√m_μ + √m_e) = 0.8700
Ratio w₁/w₂ = 0.6988

C₃[111] equal-asymmetry prediction: w₁/w₂ = 1.000
Observed discrepancy: 30%
```

The ratio w₁/w₂ = 0.6988 measures the breaking of the equal-asymmetry
prediction of the symmetric C₃[111] orbit. Any mechanism that derives θ_ℓ
must reproduce this specific ratio. It is the numerical target for Primitive C.

---

## Connection to absolute H/He energies

The atomic energy prediction requires:

```
E₁(H) = − ½ m_e c² α_EM²
```

With α_EM derived to 0.21% (see `ALPHA_EM_DERIVATION_NOTE.md`), the
remaining factor is m_e. The framework predicts:

```
E₁(H) / m_e = − α_EM²/2 = − (1/137.036)²/2 = − 2.66 × 10⁻⁵
```

This is fully derivable. The conversion to eV requires m_e in eV, which
is not yet derived. The two-gap structure is:

| Gap | Status |
|-----|--------|
| α_EM (was 27%) | CLOSED: 0.21% accuracy (taste staircase) |
| m_e | OPEN: Primitive C + lepton mass scale both needed |

Closing the m_e gap would complete the framework's prediction of absolute
atomic energies in eV. Given the analytic obstruction identified here,
this requires genuinely new machinery beyond current framework primitives.

---

## Authority

- `scripts/electron_mass_from_axioms.py` — four-approach numerical exploration
- `docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` — canonical lepton review
- `docs/ALPHA_EM_DERIVATION_NOTE.md` — α_EM derivation (complementary gap)
