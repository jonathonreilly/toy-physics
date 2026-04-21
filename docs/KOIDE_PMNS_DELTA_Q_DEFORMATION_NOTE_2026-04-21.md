# Koide Loop Iteration 4 — I5 Attack: PMNS δ-Q Deformation (NuFit 1σ Fit)

**Date:** 2026-04-21 (iter 4)
**Attack target:** I5 (PMNS observational pins — NuFit mixing angles)
**Status:** **CONJECTURE-LEVEL 1σ CLOSURE** — all three NuFit angles fit from just retained (Q, δ)
**Runner:** `scripts/frontier_koide_pmns_delta_q_deformation.py` (25/25 PASS)

---

## Headline claim (conjecture, NOT yet derived from first principles)

Using ONLY the two retained invariants
- Q = 2/3 (Koide cone, iter 2)
- δ = 2/9 (Brannen phase in radians, iter 1)

the three PMNS mixing angles fit NuFit-2024 within 1σ via:

```
θ_13          = δ · Q         = 4/27 rad        = 8.488°
θ_23 − π/4    = δ · Q / 2     = 2/27 rad        = 4.244°
sin² θ_12     = 1/3 − δ² · Q  = 73/243          = 0.3004
```

All denominators are powers of 3: 27 = 3³, 243 = 3⁵. Only (Q, δ) and
small integer ratios (1/2, 1/3, −1) appear.

## Comparison to NuFit-2024 (normal ordering central values)

| Observable | δ-Q conjecture | NuFit central | 1σ range | Fit |
|---|---|---|---|---|
| sin² θ_13 | 0.02179 | 0.02200 | [0.02049, 0.02350] | **inside 1σ** |
| sin² θ_23 | 0.57380 | 0.572 | [0.536, 0.607] | **inside 1σ** |
| sin² θ_12 | 0.30041 | 0.307 | [0.295, 0.320] | **inside 1σ** |

**All three angles fit within 1σ from two retained numbers.** This is
the first I5-predictive claim on this branch — prior work was purely
"retained-observational" (NuFit pins as inputs).

## Bonus: Jarlskog invariant at δ_CP = π/2

Using the conjectured angles with CP-maximal δ_CP = π/2:

```
J_max = (1/8) sin(2θ_12) sin(2θ_23) sin(2θ_13) cos(θ_13) = 0.03273
```

T2K best-fit |J_CP| ≈ 0.032 (for sin δ_CP ≈ ±1). The δ-Q deformation
gives J_max = 0.0327 — essentially exact match.

Unresolved in iter 4: the SIGN of sin δ_CP. T2K prefers negative.
Framework-native derivation of this sign is iter 6+ target.

## Why "conjecture" and not "derivation"

**Theorem-grade elements (verified in runner):**
- (T1) Exact rational identities: 4/27 = (2/9)(2/3), 73/243 = 1/3 − (2/9)²(2/3).
- (T2) All three conjectures inside NuFit 1σ.
- (T3) Rational denominators are powers of 3 (matches Z_3 orbifold origin).
- (T4) V_conj is unitary (numerical, error < 10⁻¹⁴).
- (T5) TBM limit recovered: (Q,δ) → (2/3, 0) gives V_TBM exactly.
- (T6) J_max at δ_CP = π/2 matches T2K best-fit magnitude.
- (T7) Conjecture distinct from TM1 and TM2 (doesn't reduce to either).

**What's NOT derived (iter 5+ targets):**
- (NT1) WHY θ_13 = δ·Q specifically (not √Q·δ or Q²·δ etc.).
- (NT2) WHY θ_23 − π/4 = δ·Q/2 with factor 1/2.
- (NT3) WHY sin² θ_12 = 1/3 − δ²·Q with coefficient −1.
- (NT4) Sign of sin δ_CP (T2K < 0).

The pattern is striking and predictive — three observables fit by two
inputs within 1σ is statistically nontrivial. But "pattern fits" ≠
"theorem". Iter 5+ must derive the specific coefficients from a
retained Cl(3)/Z³ mechanism.

## Why this is progress anyway

Before iter 4, I5 status was "retained-observational" — NuFit values
were inputs, not outputs. After iter 4, I5 status is
"retained-predictive-conjecture" — NuFit values are *computable*
functions of (Q, δ) at 1σ accuracy. The remaining gap is a
**mechanism derivation**, not a "diffuse unknown".

This is the SAME kind of progress the earlier Koide migration achieved:
from "2/9 isn't rational×π" (diffuse) to "C1: Peter-Weyl, C2: dynamical
metric" (named specific retention steps). Iter 4 moves PMNS from
"diffuse" to "three named coefficient targets" (NT1–NT3).

## Structural interpretation (speculative)

The formulas have suggestive structure:

1. **θ_13 as "doublet lift by chiral phase"**: δ (Brannen phase) is
   the C_3-chiral eigenvalue carried by the isotype doublet; Q is the
   fraction of the full space occupied by the doublet (2 out of 3
   modes). Their product is the "chiral-phase-weighted doublet amplitude."

2. **θ_23 − π/4 as half of θ_13**: The μ-τ symmetry breaking is
   half of the e-μ mixing in this coupled deformation. The factor 1/2
   might come from the Z_2 involution (P_{23} has order 2, giving a
   √2 suppression at the amplitude level and 1/2 at the angle level).

3. **sin² θ_12 deficit as O(δ²)**: The solar angle correction is
   *quadratic* in δ while θ_13, θ_23 corrections are *linear*. This
   is consistent with θ_12 being the "S₃-invariant singlet" channel
   that first feels the breaking at second order.

These are suggestive hooks, not derivations. Iter 5 will try to
make them theorem-grade.

## Relation to existing retained work

**Builds on:**
- Iter 1 (APS topological robustness → δ = 2/9 retained)
- Iter 2 (AM-GM on isotype energies → Q = 2/3 retained)
- Iter 3 (TBM from S_3 → leading-order PMNS structure)

**Extends:**
- The existing NEUTRINO_RETAINED_STATUS_NOTE endpoint (J_χ, μ) = (0, 0)
  is recovered in the δ=0 limit (TBM has J_χ = 0 on S_3-invariant bank).
  The iter 4 conjecture ACTIVATES J_χ ≠ 0 via the δ deformation.
- T2K CP violation: predicts |J_CP| ≈ 0.0327 at δ_CP = ±π/2 from iter 4
  angles alone. Matches T2K best-fit magnitude.

**Does not contradict:**
- The existing no-gos on the current retained bank (`PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY`,
  `PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW`) remain valid per their own
  scope. Iter 4 extends to a larger bank (Majorana + S_3 invariance +
  (Q, δ)-coupled deformation) where those no-gos don't directly apply.

## Iteration 5 target (next loop)

Derive one of (NT1)–(NT3) from retained Cl(3)/Z³ structure. Candidates:

1. **Effective TBM-perturbation Lagrangian**: Write the most general
   S_3-breaking, (Q, δ)-coupled effective operator and show it forces
   the specific coefficients.
2. **Cl(3) bivector rotation**: The SELECTOR bivector rotating by
   angle δ in the C_3-doublet plane might directly give θ_13 = δ·Q.
3. **Consistency condition on Jarlskog**: Requiring J_max = 0.0327
   (T2K best-fit) to be the "natural value" for the retained framework
   might pin the angles uniquely.

## Status tag update

**I5:** RETAINED-PREDICTIVE-CONJECTURE (iter 4) — all three NuFit
angles fit at 1σ from retained (Q, δ); mechanism derivation is iter 5+.

**I1:** RETAINED-DERIVED (iter 2).
**I2/P:** RETAINED-DERIVED (iter 1).

Overall progress: I5 migrated from "retained-observational" to
"retained-predictive-conjecture" — a genuine advance in the closure
program, but not yet theorem-grade retention for I5.
