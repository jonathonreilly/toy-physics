# arXiv Abstract Draft — Lepton Koide and PMNS from Cl(3)/Z³ Retained Structure

**Date:** 2026-04-21 (iter 27)
**Type:** Concise reviewer-digestible abstract + key results

---

## Title (proposed)

**"Koide Relation Q = 2/3 and Brannen Phase δ = 2/9 from Cl(3)/Z³ Axioms:
 A Retained-Derivation Program"**

## Abstract (draft)

We present a retained-derivation framework in which the charged-lepton
Koide relation Q = 2/3 and the Brannen phase δ = 2/9 rad emerge as
forced consequences of Cl(3) on a Z³ lattice with cubic S₃ symmetry.

**Two independent closures**:

1. **Q = 2/3 via AM-GM on isotype Frobenius energies** (32+24+35 = 91
   executable PASS checks across dedicated runners).  The Koide
   functional F = log(E_+·E_⊥) with E_+ = (tr M)²/3 (scalar projection)
   and E_⊥ = Tr(M²) − E_+ (traceless projection) reaches its unique
   constrained maximum at E_+ = E_⊥, forcing κ = a²/|b|² = 2 and
   Q = (1 + 2/κ)/d = 2/3 at d = 3.

2. **δ = 2/9 rad via APS equivariant η-invariant** (41+34+21+33 = 129
   PASS checks).  The Atiyah-Bott-Segal-Singer fixed-point formula on
   the Z₃ orbifold C_3[111]\Z³ with tangent weights (1, 2) gives
   η = (1/3)[1/((ζ−1)(ζ²−1)) + 1/((ζ²−1)(ζ−1))] = 2/9 exactly via the
   core identity (ζ−1)(ζ²−1) = 3.

**Combined retained identity**: **Q = p · δ = 3·δ**, where p = 3 is the
Z₃ orbifold order (= number of generations d).  Derivation:
Q = 2/d = 2/p and δ = 2/p², so Q/δ = p at p = d = 3.

**PMNS structure** (partial, conjectural at mechanism level):
- V_TBM is the forced leading-order mixing matrix (S_3 simultaneous
  eigenbasis).
- Iter 4-style (Q, δ) deformation fits all three NuFit-2024 mixing angles
  within 1σ via:
  - θ₁₃ = δ·Q = 4/27 rad = 8.488°
  - θ₂₃ − π/4 = δ·Q/2 = 2/27 rad
  - sin²θ₁₂ = 1/3 − δ²·Q = 73/243 = 0.3004
- Two sum rules unify these:
  - **SR1 (exact)**: θ₁₃ = 2·(θ₂₃ − π/4)
  - **SR2 (leading, conservation law)**:
     Q · sin²θ₁₂ + sin²θ₁₃ = δ
- SR2 is a conservation law under iter 4 deformation, anchored at the
  retained Q = 3·δ identity at the TBM limit.
- Iter 4 is UNIQUE within NuFit 1σ among simple (Q, δ)-algebraic
  expressions for θ₁₃ (uniqueness-by-elimination).

**Robust observational validation**:
- NuFit 5.0-5.3 (2020-2024): all three angles within 1σ for every release.
- T2K |J_CP|: matches iter 4 J_max = 0.0327 at δ_CP = ±π/2.

**Open directions** (honest):
- I5 mechanism: the product structure θ₁₃ = δ·Q specifically (rather
  than, say, θ₁₃ = δ²·Q) is not yet derived from retained axioms.
  Shown to be unique among simple alternatives by data, but full
  mechanism derivation remains open.
- δ_CP sign: identified as a Z_2 orientation choice in the Cl(3)
  pseudoscalar; T2K's preferred sin δ_CP < 0 selects one of two
  orientations, but retained orientation derivation open.
- Quark sector: Q_u ≈ 0.849, Q_d ≈ 0.732 do not equal lepton Q = 2/3.
  The Cabibbo angle θ_C ≈ δ numerically (2% gap) is an intriguing but
  undeirived coincidence.  Quark-sector retention is separate.

## Key Numerical Claims (for reviewer table)

| Observable | Predicted | NuFit-2024 Central | Gap |
|---|---|---|---|
| Q (Koide) | 2/3 | 0.666±ε_PDG | Input (retained-forced) |
| δ (Brannen) | 2/9 rad | — | Retained-forced |
| θ₁₃ | 4/27 rad = 8.488° | 8.573° | 1σ |
| θ₂₃ − π/4 | 2/27 rad = 4.244° | 4.2° | 0.1σ |
| sin²θ₁₂ | 73/243 = 0.3004 | 0.307 | 0.5σ |
| J_max (δ_CP = ±π/2) | 0.0327 | T2K \|J\| ≈ 0.033 | 0.1σ |

## Methodology Summary

- **Executable verification**: 423+ PASS checks across 22 dedicated
  frontier runners on `evening-4-20` branch (iter 1-26).
- **Block-by-block forcing**: each building block of I1 and I2/P
  closures verified retained-forced (iter 9 for I1, iter 10 for I2/P).
- **Reviewer stress-test**: 9 enumerated objections for I1/I2 addressed
  (iter 6).
- **Honest self-correction**: iter 12 revised iter 11's basis-confusion
  error; iter 24 downgraded iter 22's "retained-derived at numerical
  level" language to "retained-rewritten given iter 4 conjecture".
- **Uniqueness-by-elimination**: iter 25 showed iter 4's θ_13 = δ·Q is
  the unique simple (Q, δ)-expression matching NuFit within 1σ.

## Bottom line

**Retained-forced closures**: lepton Koide Q = 2/3, Brannen phase
δ = 2/9, and their retained arithmetic identity Q = 3·δ.

**Observationally robust**: PMNS mixing angles in the (Q, δ)-deformation
ansatz fit NuFit 1σ across 2020-2024 data.

**Structurally elegant**: two sum rules (SR1, SR2) unify PMNS
predictions into a conservation-law-preserving 1-parameter trajectory.

**Open mechanism**: full Cl(3)/Z³ derivation of the iter 4 θ_13 = δ·Q
product structure remains a target for future work, with specific
operator form M_SR2 = diag(0, Q, 1) identified in mass basis (iter 19).

---

## Suggested next steps (for paper development)

1. **Convert runners → figures**: tabulate iter 1-26 PASS checks,
   include block-by-block forcing tables for I1 and I2/P.
2. **Editorial pass**: tighten prose, add bibliography
   (Koide 1981, Brannen, Harrison-Perkins-Scott 2002, APS 1975,
   Atiyah-Bott 1967, NuFit 2024, T2K 2024).
3. **Numerical precision**: verify central values + error bars from
   latest NuFit release.
4. **Scope note**: explicitly limit to lepton sector; flag quark
   parallel as separate retention problem.
5. **Discussion section**: honestly state open directions (mechanism
   derivation for product structure, δ_CP sign, quark sector).

---

## Branch artifact census (iter 1-26)

| Category | Count |
|---|---|
| Dedicated frontier runners | 22 |
| Companion notes | 22+ |
| Master status notes | 3 (V1, V2, V3) |
| Publication outline | 1 (iter 20) |
| **This abstract draft** | 1 (iter 27) |
| Total executable PASS checks | 423+ |
| Commits on evening-4-20 | 27 (iter 1-27) + pre-loop |

## Ready for promotion to main?

Subjectively assessed:

**Yes, main-landable** (with minor editorial cleanup):
- I1 closure chain (iter 2, 9, 6)
- I2/P closure chain (iter 1, 10, 6)
- Q = 3·δ retained identity (iter 21)
- V_TBM leading-order PMNS (iter 3)
- Observational robustness of (Q, δ)-ansatz (iter 13)

**Published-draft-ready but not main-landable yet**:
- iter 4 (Q, δ)-deformation as conjecture (iter 4)
- Sum rules (iter 18)
- iter 4 uniqueness among simple forms (iter 25)
- Honest-caveat state (iter 24)

**Open questions** (not closure):
- I5 mechanism derivation
- δ_CP sign
- Quark sector

User can choose to consolidate the "main-landable" portion now or
continue loop for more mechanism work.
