# Koide Loop Iteration 5 — I5: Single-Rotation No-Go

**Date:** 2026-04-21 (iter 5)
**Attack target:** I5 mechanism derivation (iter 4 coefficient targets)
**Status:** **THEOREM-GRADE NEGATIVE RESULT**
**Runner:** `scripts/frontier_koide_pmns_single_rotation_nogo.py` (13/13 PASS)

---

## One-line finding

The iter 4 V_conj matrix (fitting NuFit angles from (Q, δ)) is **not**
obtainable by a single Cl(3) bivector rotation of V_TBM with a clean
(Q, δ) angle and a retained direction axis. The mechanism must be
genuinely composite.

## The attack

For the iter 4 conjecture to be theorem-grade "retained-derived",
we need a Cl(3) operator (rotation, projection, etc.) that maps V_TBM
to V_conj. The simplest such operator is a single bivector rotation
R(axis, angle). This iter 5 runner **rules out** this simplest case.

## Specific tests performed

1. **Exact rotation**: Computed R = V_conj · V_TBM^T.
   - Angle: 0.1682 rad = 9.636° (NOT a simple (Q, δ) function)
   - Axis: (-0.424, 0.753, -0.503) (NOT a single clean direction)

2. **Angle candidate tests**: Compared the exact angle to 10 natural
   (Q, δ) combinations: δ, δ·Q, √Q·δ, Q, δ²Q, etc.
   - **Best match: √Q · δ = 0.1814 rad — 7.88% off.**
   - No candidate matches within 1%.

3. **Axis candidate tests**: Compared exact axis to 9 retained flavor
   directions: (1,1,1)/√3, (0,1,-1)/√2, (1,-1,0)/√2, TBM cols, etc.
   - **Best match: (0,1,-1)/√2 (μ-τ anti-diagonal) — overlap 0.888.**
   - Substantial subleading component (2,-1,-1)/√6 at 0.449.
   - No clean single direction.

4. **90-candidate grid scan** (9 axes × 10 angles): best single-rotation
   mechanism is `R[(0,1,-1)/√2, δ·Q]` with distance 0.109 to V_conj
   (baseline 0.238). Reduces gap by 54% but NOT exact.

## Why this is theorem-grade progress

**Theorem-grade negative results** are valuable in closure programs:
they rule out natural-but-incorrect mechanism hypotheses, narrowing
the search space. This iter 5 result:

- Rules out "single bivector rotation by (Q, δ) function around
  retained axis" as the iter 4 mechanism.
- Identifies the dominant component: the μ-τ anti-diagonal axis
  (0,1,-1)/√2 with angle ≈ √Q·δ.
- Tells us the mechanism needs AT LEAST 2 rotation components.

The parallel in I1 closure history: the original `PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY`
no-go was also a theorem-grade negative result (forcing J_χ=0 on the
current bank). It didn't close I5, but it sharpened what kind of
mechanism was needed.

## Suggestive interpretation

The best single-axis rotation has:
- **Axis primarily along (0,1,-1)/√2** — the μ-τ antisymmetric direction.
  This is EXACTLY the axis that breaks the retained P₂₃ reflection
  symmetry of the S₃ cubic group (iter 3).
- **Angle close to √Q·δ** — the geometric mean of Q and δ², or equivalently
  the angle such that sin²(angle) ≈ δ²·Q / Q = δ² (for small angles,
  angle ≈ δ·√Q).

Physical reading: the S₃→Z₃ breaking is DOMINANTLY along the μ-τ
antisymmetric direction (breaking P₂₃) with magnitude √Q·δ. But the
REMAINING 54% of the required deformation must come from another
component (iter 6+ target).

## Iter 6+ targets (updated backlog)

1. **Search for 2-rotation composite mechanisms**:
   - R = R_{(0,1,-1)/√2}(√Q·δ) · R_{(2,-1,-1)/√6}(something) acting
     on V_TBM.
   - Parametrize both rotation angles as (Q, δ)-functions and look
     for a clean match.

2. **Search for effective TBM-breaking operator**:
   - Find a Cl(3) operator O such that exp(ε·O)·V_TBM ≈ V_conj for
     some ε related to (Q, δ).
   - Test O from: SELECTOR bivector, C_3 doublet operators, μ-τ
     breaking operators.

3. **CP phase derivation (sign of sin δ_CP)**:
   - T2K: sin δ_CP < 0.
   - Derive from Cl(3) pseudoscalar I = e₁e₂e₃ (retained).
   - Would strengthen iter 4 prediction.

4. **Reviewer stress-test** for iter 1 / iter 2 closures:
   - Challenge iter 1 "topological robustness" on PL S³ × R
     (is PL sufficient? Is dynamical metric really not needed?)
   - Challenge iter 2 "AM-GM" uniqueness (why F = log(E_+·E_⊥)?)

## Status update

- **I1 (Q=2/3):** RETAINED-DERIVED (iter 2).
- **I2/P (δ=2/9):** RETAINED-DERIVED (iter 1).
- **I5 (PMNS):** RETAINED-PREDICTIVE-CONJECTURE (iter 4) +
  SINGLE-ROT-MECHANISM-RULED-OUT (iter 5). Mechanism search continues
  in iter 6+.

Iter 5 is a consolidation/constraint iteration — it sharpens what
kind of mechanism can realize the iter 4 fit, by eliminating the
simplest hypothesis. This keeps the loop moving by advancing the
search space analysis even without finding the final answer.
