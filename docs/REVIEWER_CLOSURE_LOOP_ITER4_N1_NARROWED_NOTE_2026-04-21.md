# Reviewer-Closure Loop Iter 4: N1 (δ·q_+ = Q_Koide) Structurally Narrowed

**Date:** 2026-04-21
**Branch:** `evening-4-21`
**Status:** **Narrowed, not closed.** The retained Atlas theorems alone
do NOT force `δ · q_+ = 2/3`; the missing piece is pinpointed as a
"SELECTOR-quadrature" identity on the `(T_Δ, T_Q)` active directions.
Iter 4 provides the structural clarification needed to close N1 via
a targeted retained identity.
**Runner:** `scripts/frontier_reviewer_closure_iter4_n1_delta_qplus_derivation.py`
— 8/8 PASS.

---

## User-directed item N1

> Derive `δ · q_+ = Q_Koide = 2/3` from first principles.
> afternoon-4-21-proposal observes it numerically but does not derive it.

## Iter 4 method

Use retained Atlas theorems on main and attempt a symbolic derivation:

- **(a)** active-affine point-selection boundary (chart `H = H_base + m·T_M + δ·T_Δ + q_+·T_Q`)
- **(b)** Z_3 doublet-block point-selection theorem (retained K-block formulas)
- **(c)** carrier normal-form theorem (retained σ sin(2v) = 8/9, δ + ρ = √(8/3))

Express `δ · q_+` symbolically via the retained K-block formulas and
ask whether it simplifies to `2/3` under (a)+(b)+(c).

## Results

### Path 1 — derive from existing retained theorems: **RULED OUT**

- The retained K-block formulas give `q_+ = 2√2/9 − (K_11 + K_22)/2`
  and `δ = (Im K_12 + 4√2/3)/√3`. These are **inversions**, not
  constraints — they tell us how to read off `(δ, q_+)` from the
  K-entries, not what their product equals.
- The carrier normal-form theorem gives two constraints on `(σ, v)`
  and links `q_+` to `σ cos(2v)`. But `δ` lives on the free 1-real
  direction `δ + ρ = √(8/3)`, and no retained theorem in (a)-(c)
  forces a specific value of `δ`.
- Therefore `δ · q_+` is **not forced** to `2/3` by the currently
  retained Atlas stack.

### Path 2 — specific missing retained identity: **PINPOINTED**

The exact additional identity needed is

```
  δ · q_+  =  SELECTOR²  =  Q_Koide  =  2/3
```

equivalently (in carrier variables):

```
  δ  =  2 / (3 q_+)  =  2 / (√8/9 − σ cos(2v))
```

This is a **SELECTOR-quadrature** pairing between the CP-odd active
direction `T_Δ` and the even-carrier active direction `T_Q`: their
product is fixed to the retained SELECTOR² constant. In the retained
framework's vocabulary this is a **reciprocity** relation between
the two active chart generators.

### Path 3 — primitive retained identity: **tentative current state**

If a retained SELECTOR-quadrature origin cannot be identified, the
identity itself is primitive (taken as an axiom of the PMNS-chart
closure). Currently:
- Observational saturation < 0.2% at the PDG-pinned chamber point.
- Under exact imposition, predicts PMNS angles within 1σ NO (afternoon-
  4-21-proposal iter 5).
- Bridge B (iter 3) gives a precedent: arg(b) = δ_B holds as a
  retained identity with a framework-structural origin (ambient APS
  on Z_3 orbifold). An analogous origin for `δ·q_+ = SELECTOR²`
  would parallel Bridge B.

## What iter 4 achieves

1. **Rules out** derivability from currently-retained Atlas theorems
   (Path 1).
2. **Pinpoints** the specific missing retained identity: SELECTOR-
   quadrature reciprocity between `T_Δ` and `T_Q`.
3. **Connects to Gate 2 A-BCC item**: if A-BCC is derived from
   Cl(3)/Z³, it may come with a δ·q_+ constraint as corollary —
   closing both the reviewer's A-BCC item AND N1 simultaneously.
4. **Sets up iter 5**: N2 (derive det(H) = E2) has analogous
   structure and may share the same missing retained piece.

## N1 status

- **Narrowed**: the specific missing retained piece is named.
- **Not closed**: a retained SELECTOR-quadrature identity on
  `(T_Δ, T_Q)` is required.
- **Broader DM/PMNS gate remains OPEN pending this + N2 + N3**.

## Iter 5 plan (queued)

Attack N2: derive `det(H) = E2 = √8/3` from first principles.

Specifically: expand `det(H(m, δ, q_+))` as a polynomial in retained
H_base + chart generators. Check whether under the N1 SELECTOR-
quadrature conjecture `δ · q_+ = SELECTOR²` and the retained
carrier/K-block identities, `det(H) = E2` becomes a consequence, a
separate primitive, or an incompatibility.

If N1 and N2 collapse to the same missing retained piece, that's
important structural progress. If they're independent, iter 6 on N3
(uniqueness) will address both numerically via the full closure
system.
