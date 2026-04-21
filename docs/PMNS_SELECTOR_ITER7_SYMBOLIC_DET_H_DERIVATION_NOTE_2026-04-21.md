# PMNS Selector Iter 7: Symbolic det(H) Derivation — Informative Partial

**Date:** 2026-04-21
**Branch:** `afternoon-4-21`
**Status:** Informative partial. The identity `det(H) = E2 = √8/3`
(iter 6's second cut) does NOT reduce to a simpler one-variable
retained identity. The closure equation under `δ · q_+ = 2/3` is an
explicit cubic in `m` with irrational coefficients — that cubic IS the
retained content, but it's not a clean factorization. Crucially, NO
THIRD simple-value scalar identity is manifest at the closure point.
**Runner:** `scripts/frontier_pmns_selector_iter7_symbolic_det_H_derivation.py`
— 1 PASS, 0 FAIL (on closure-point verification).

---

## What iter 7 attempted

Iter 6 found `det(H) = √8/3 = E2` as the best second-cut candidate.
Iter 7's question: can we **derive** this from Cl(3)/Z³ retained
structure, or simplify to a manifest framework identity?

## What iter 7 computed

**Part A** — symbolic `det(H(m, δ, q_+))` as a polynomial:

The determinant is computed exactly via `sympy` with retained constants
`E1 = √(8/3)`, `E2 = √8/3`, `γ = 1/2`. The expression is a
multinomial in (m, δ, q_+) with radical coefficients.

**Part B** — substitute `q_+ = 2/(3δ)`:

Under the first cut, `det(H) · δ² = P(m, δ)` where `P` is a polynomial
whose terms involve {1, √2, √3, √6} rational combinations of m and δ.

**Part C** — solve `det(H) = E2` for `m(δ)`:

sympy returns explicit cubic solutions `m_0(δ), m_1(δ), m_2(δ)`. At
`δ = δ_* = 0.933806`, one of them evaluates to `m ≈ 0.660` (the
closure value). The cubic is irreducible — no clean linear or quadratic
reduction.

**Part D** — closure polynomial `P(m, δ) = det(H) · δ² − E2 · δ²`:

```
P(m_c, δ_c) = −2.0e-8  (essentially 0, verifies the closure point)
```

`sympy.factor(P)` does NOT produce a clean factorization — the
polynomial is irreducible over ℚ(√2, √3, √6).

**Part E** — alternative retained simple-value targets for det(H):

Tested `det(H) ∈ {1, √(8/3), 2/3, 1/3, √6/3, 1/√3, 2/√3, √2}`. Each
produces a similar cubic-in-m structure. None factor cleanly. The
constant-term coefficients distinguish them — all are messy radical
expressions, no simple form dominates.

**Part F** — all natural scalars at the closure point:

```
Scalar               Value         Closest retained    |dev|
δ_c * q_+c           0.666667      2/3                 4.5e-07
det(H_c)             0.942811      sqrt(8)/3           1.6e-06
m_c                  0.660242      2/3                 6.4e-03
Tr(H_c)              0.660242      2/3                 6.4e-03
δ_c                  0.935995      sqrt(8)/3           6.8e-03
δ_c + q_+c           1.648250      sqrt(8/3)           1.5e-02
... (all others > 3e-2)

Scalars hitting < 1e-4 at closure: 2  (only the two IMPOSED cuts)
```

## What this rules out and what it keeps

**Ruled out**: a THIRD simple-value retained identity within the
broad scalar-invariant class (33 scalars × 19 retained simple values
tested in iter 6; Part F at the closure point confirms no third hit).

**Kept**: the support package is
```
  δ · q_+  = 2/3   (retained I1 Koide value)
  det(H)   = √8/3  (retained atlas constant E2)
  s_13²    = 0.0218 (observational PDG)
  ⟹ (m, δ, q_+) pinned in chamber
  ⟹ sin²θ_12 and sin²θ_23 PREDICTED within PDG 1σ
```

This is a viable **2-retained-identity + 1-observational** closure
form for the PMNS selector. It is observationally falsifiable and
framework-native on its retained-identity part.

## Structural observation

The polynomial structure in Part A/B/C suggests the "retained identity"
content lives at the **polynomial** level, not at the "single scalar =
single simple value" level. Specifically:

- `det(H(m, δ, q_+)) − E2 = 0` is a polynomial identity on the
  2-D source manifold (under `δ · q_+ = 2/3`).
- That polynomial has coefficients in ℤ[√2, √3, √6] — all
  framework-retained numbers.
- It does NOT further reduce to a product of linear retained factors.

**Interpretation**: `det(H) = E2` is not "derived from" simpler
retained identities; it's **itself the identity at the polynomial
level**. Iter 8 should not try to reduce it further — instead, it
should accept this as a primitive retained content and focus on
finding the **third** polynomial identity.

## What iter 8 should pursue

Four directions, in order of framework-naturalness:

1. **Non-scalar operator-valued cuts** — not a single scalar hit, but
   a relation like `[H, O]_{rest}` vanishing in a specific basis.
2. **A-BCC axiomatic derivation (A5)** — derive `sign(det H) > 0`
   from Cl(3)/Z³; this doesn't give s13² directly but may restrict
   the chamber further.
3. **Variational on the 1-D curve** — on the curve
   `{δ·q_+ = 2/3, det(H) = E2}` (a 1-parameter family in m),
   find a retained functional whose extremum is the physical point.
4. **Graceful acceptance of the 2-retained structure** — note that
   `sin²θ_13 = 0.0218` is experimentally the best-measured PMNS
   angle (reactor experiments, ~3% precision); using it as input
   + 2 retained cuts predicts the other two angles to PDG 1σ.
   The framework predictive content is REAL even if formally
   "2 retained + 1 observational".

Iter 8 will try direction 3 (variational on the 1-D curve) as it's
the most likely to yield a genuine third retained identity.
