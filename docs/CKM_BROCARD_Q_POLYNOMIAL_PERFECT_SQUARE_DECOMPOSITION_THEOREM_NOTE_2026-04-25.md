# Brocard / Q Polynomial Perfect-Square Decomposition

**Date:** 2026-04-25

**Status:** proposed_retained CKM-structure corollary on the proposed_promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives the
**EXACT algebraic decomposition** of the polynomial pair
`(P(α_s), Q(α_s))` — the two fundamental quartic polynomials of the
retained NLO Wolfenstein protected-γ̄ surface — into **two distinct
scalar-multiple square-channel linear combinations**, each tied to a specific
physical observable channel (Jarlskog vs Perimeter).

The headline closed forms:

```text
(D2)  Q(alpha_s) - P(alpha_s)  =  N_pair^6 (N_quark - 1) (N_pair^2 - alpha_s)^2
                                 =  320 (4 - alpha_s)^2.

      Scalar-multiple square channel in (4 - alpha_s); proportional to Wolfenstein
      eta_bar (and hence to Jarlskog J_bar).

(D3)  P(alpha_s) + 3 Q(alpha_s)  =  N_pair^2 (alpha_s^2 - 4 alpha_s + 96)^2
                                  =  4 (48 perim_sq)^2
                                  =  N_pair^8 N_quark^2 perim_sq^2.

      Scalar-multiple square channel in (alpha_s^2 - 4 alpha_s + 96) = 48 perim_sq;
      proportional to perimeter-squared of the unitarity triangle.
```

So **the (P, Q) algebraic module decomposes into two scalar-multiple square
channels**:
- **Jarlskog channel** `Q − P = N_pair^10 N_quark^2 · η̄²`
  (proportional to `J̄²` in the normalized Wolfenstein plane),
- **Perimeter channel** `P + 3Q = N_pair^8 N_quark^2 · perim_sq²`.

Together they span the (P, Q) module:
```text
P  =  ((P + 3Q) − 3(Q − P))/4  =  (perimeter-channel − 3 Jarlskog-channel)/4,
Q  =  ((P + 3Q) + (Q − P))/4   =  (perimeter-channel + Jarlskog-channel)/4.
```

Throughout this note, "perfect-square channel" means a scalar multiple of
one square polynomial in `alpha_s`. With the displayed structural prefactors,
each channel is a literal square over the corresponding real quadratic
coefficient field; over `Q[alpha_s]` the line classification is the
classification of scalar-multiple square channels.

**Primary runner:**
`scripts/frontier_ckm_brocard_q_polynomial_perfect_square_decomposition.py`

## Statement

The retained NLO Wolfenstein protected-γ̄ surface admits two
fundamental quartic polynomials of `α_s`:

```text
P(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2  -  240 (4 - alpha_s)^2
            =  alpha_s^4 - 8 alpha_s^3 - 32 alpha_s^2 + 1152 alpha_s + 5376.

Q(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2  +  80 (4 - alpha_s)^2
            =  alpha_s^4 - 8 alpha_s^3 + 288 alpha_s^2 - 1408 alpha_s + 10496.
```

`P` is the **Brocard polynomial** (universal equilateral excess; emerged
through 9+ closed-form theorems on the retained surface). `Q` is the
**Brocard-points denominator polynomial** (Q-P sibling theorem from the
Brocard-points branch).

```text
(D1) The pair (P, Q) generates a 2-dimensional Q-module within the ring
     of polynomials in alpha_s. A general linear combination decomposes as

       alpha P + beta Q  =  (alpha + beta) (alpha_s^2 - 4 alpha_s + 96)^2
                            + (-240 alpha + 80 beta) (4 - alpha_s)^2.

(D2) NEW scalar-multiple square decomposition (1) -- Jarlskog channel:
       Q(alpha_s) - P(alpha_s)  =  N_pair^6 (N_quark - 1) (N_pair^2 - alpha_s)^2
                                  =  320 (4 - alpha_s)^2.

     This is a scalar-multiple square in (N_pair^2 - alpha_s) = (4 - alpha_s),
     with structural-integer scaling N_pair^6 (N_quark - 1) = 64 * 5 = 320.

(D3) NEW scalar-multiple square decomposition (2) -- Perimeter channel:
       P(alpha_s) + 3 Q(alpha_s)  =  N_pair^2 (alpha_s^2 - 4 alpha_s + 96)^2
                                   =  4 (alpha_s^2 - 4 alpha_s + 96)^2.

     This is a scalar-multiple square in (alpha_s^2 - 4 alpha_s + 96) = 48 perim_sq,
     with structural-integer scaling N_pair^2 = 4. Equivalently:
       P + 3Q  =  N_pair^8 N_quark^2 perim_sq^2  =  9216 perim_sq^2.

(D4) Two scalar-multiple square subspaces of the (P, Q) module:
       Line A: {(alpha, 3 alpha) : alpha in Q}  ->  P + 3Q channel,
       Line B: {(alpha, -alpha) : alpha in Q}  ->  Q - P channel.

     ALL other linear combinations alpha P + beta Q (with (alpha, beta)
     not on either line) have BOTH (alpha_s^2 - 4 alpha_s + 96)^2 and
     (4 - alpha_s)^2 components, and are therefore NOT single-square channels
     in alpha_s.

     The two lines are independent in the (alpha, beta) parameter space,
     so the scalar-multiple square-channel subset = (Line A) union (Line B), a
     1-dimensional union of two 1-D affine subspaces (modulo origin).

(D5) Physical interpretation -- Jarlskog vs Perimeter channels:
       Q - P  =  N_pair^10 N_quark^2 eta_bar^2,
       P + 3Q  =  N_pair^8 N_quark^2 perim_sq^2.

     where:
       eta_bar  =  sqrt(5) (4 - alpha_s)/24  =  Jarlskog J_bar in the
                   Wolfenstein-normalized unitarity plane (J_bar = eta_bar),
       perim_sq  =  (alpha_s^2 - 4 alpha_s + 96)/48  =  a^2 + b^2 + c^2
                    of the unitarity triangle (sum of squared sides).

(D6) Cross-channel identity (NEW):
       (P + 3Q)(Q - P)  =  N_pair^8 (N_quark - 1) (alpha_s^2 - 4 alpha_s + 96)^2 (4 - alpha_s)^2
                         =  1280 (alpha_s^2 - 4 alpha_s + 96)^2 (4 - alpha_s)^2.

     The product of the two square channels is itself a scalar-multiple
     square (squared-cross-product), with structural integer 1280 = N_pair^8 (N_quark - 1).

(D7) The (P, Q) module is fully scalar-multiple-square-decomposable on the
     retained surface:
       P  =  ((P + 3Q) - 3(Q - P)) / 4,
       Q  =  ((P + 3Q) + (Q - P)) / 4.

     The two scalar-multiple square channels span the module under linear
     combination over Q.
```

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `(rho_bar, eta_bar)` apex coordinates | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note
is load-bearing. The Brocard polynomial `P(α_s)` and the Q-polynomial
`Q(α_s)` are independently re-derived here from the retained
`(rho_bar, eta_bar)` and the classical Brocard / Brocard-points
constructions.

## Derivation

### General linear combination

For any rationals `α, β`, the linear combination `α P + β Q` is

```text
alpha P + beta Q  =  alpha [(alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2]
                     + beta [(alpha_s^2 - 4 alpha_s + 96)^2 + 80 (4 - alpha_s)^2]

                  =  (alpha + beta) (alpha_s^2 - 4 alpha_s + 96)^2
                     + (-240 alpha + 80 beta) (4 - alpha_s)^2.
```

For this to be a **single-square channel** in `α_s`, exactly one of the two
components must remain:

- **Line A**: `−240 α + 80 β = 0 ⟺ β = 3α`. Combination becomes
  `(α + 3α)(α_s² − 4α_s + 96)² = 4α (α_s² − 4α_s + 96)²`.
- **Line B**: `α + β = 0 ⟺ β = −α`. Combination becomes
  `(−240α + 80(−α))(4 − α_s)² = −320α (4 − α_s)²`.

These are the only two scalar-multiple square subspaces. Every other `(α, β)`
gives a combination with both square components, which is not itself a
single-square channel. The runner verifies this generically by coefficient
comparison against an arbitrary quadratic square, not only by testing one
off-line example.

### D2: Q − P scalar-multiple square channel (Jarlskog channel)

Setting `α = −1, β = 1` in Line B:

```text
Q - P  =  -(-240 + 80) (4 - alpha_s)^2  =  320 (4 - alpha_s)^2.
```

In structural integers: `320 = 64 · 5 = N_pair⁶ (N_quark − 1)`. So:

```text
Q - P  =  N_pair^6 (N_quark - 1) (4 - alpha_s)^2  =  N_pair^6 (N_quark - 1) (N_pair^2 - alpha_s)^2.
```

### D3: P + 3Q scalar-multiple square channel (Perimeter channel)

Setting `α = 1, β = 3` in Line A:

```text
P + 3Q  =  4 (alpha_s^2 - 4 alpha_s + 96)^2.
```

In structural integers: `4 = N_pair²`, and using
`α_s² − 4α_s + 96 = 48 perim_sq`:

```text
P + 3Q  =  N_pair^2 (48 perim_sq)^2
        =  N_pair^2 * 2304 perim_sq^2
        =  N_pair^10 N_color^2 perim_sq^2
```

Because `N_pair² × 2304 = 4 × 2304 = 9216 = (N_pair⁴ N_quark)² = N_pair⁸ N_quark²`,

So:

```text
P + 3Q  =  N_pair^8 N_quark^2 perim_sq^2  =  (N_pair^4 N_quark perim_sq)^2.
```

This is a perfect square equal to `(N_pair⁴ N_quark × perim_sq)²` —
clean structural-integer form.

### D5: physical interpretation

The two scalar-multiple square channels are tied to **physical CKM observables**:

- **Jarlskog channel** `Q − P`: proportional to `(4 − α_s)²` and hence to
  `η̄² = 5(4 − α_s)²/576`. So `Q − P = 320(4−α_s)² = 320 × 576/5 × η̄² = 36864 η̄²`.
  In structural integers: `36864 = N_pair^10 N_quark² = 1024 × 36`. So:

  ```text
  Q - P  =  N_pair^10 N_quark^2 eta_bar^2.
  ```

  Since `J̄ = η̄` in the Wolfenstein-normalized unitarity plane (the
  Jarlskog invariant equals twice the area of the unitarity triangle,
  which equals `η̄` after unit-base normalization), this is exactly
  proportional to `J̄²`:

  ```text
  Q - P  =  N_pair^10 N_quark^2 J_bar^2.
  ```

- **Perimeter channel** `P + 3Q`: proportional to `(α_s² − 4α_s + 96)²`
  and hence to `(48 perim_sq)²`. So:

  ```text
  P + 3Q  =  N_pair^8 N_quark^2 perim_sq^2.
  ```

These are the two **physical observable channels** of the (P, Q)
module on the retained surface.

### D6: cross-channel identity

```text
(P + 3Q)(Q - P)  =  4 (alpha_s^2 - 4 alpha_s + 96)^2 × 320 (4 - alpha_s)^2
                  =  1280 (alpha_s^2 - 4 alpha_s + 96)^2 (4 - alpha_s)^2.
```

`1280 = 4 × 320 = N_pair² × N_pair⁶ (N_quark − 1) = N_pair⁸ (N_quark − 1)`.
So:

```text
(P + 3Q)(Q - P)  =  N_pair^8 (N_quark - 1) (alpha_s^2 - 4 alpha_s + 96)^2 (4 - alpha_s)^2.
```

This is a perfect square of `√(1280) (α_s² − 4α_s + 96)(4 − α_s) =
N_pair⁴ √(N_quark − 1) (α_s² − 4α_s + 96)(4 − α_s)`, since
`√(N_pair⁸) = N_pair⁴`.

In physical terms: the cross-channel product `(P + 3Q)(Q − P) ∝ perim_sq² · η̄² = perim_sq² · J̄²`,
i.e. proportional to the product of the **perimeter-squared and the
Jarlskog-squared** of the unitarity triangle.

### D7: module decomposition

From `Line A: P + 3Q = X` (perimeter channel) and `Line B: Q − P = Y` (Jarlskog channel),
solving for `(P, Q)`:

```text
P + 3Q  =  X,
Q - P  =  Y.

Adding the two: P + 3Q + Q - P = X + Y => 4Q = X + Y => Q = (X + Y)/4.
Subtracting: (P + 3Q) - 3(Q - P) = X - 3Y => P + 3Q - 3Q + 3P = X - 3Y => 4P = X - 3Y => P = (X - 3Y)/4.
```

So:

```text
P  =  ((P + 3Q) - 3(Q - P)) / 4  =  (perimeter channel - 3 * Jarlskog channel) / 4,
Q  =  ((P + 3Q) + (Q - P)) / 4   =  (perimeter channel + Jarlskog channel) / 4.
```

This is the **inverse decomposition**. The two scalar-multiple square channels
`(X, Y) = (P + 3Q, Q − P)` form a complete basis for the (P, Q)
module, with `(P, Q)` recovered by linear combinations of `(X, Y)`.

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| D2 Q − P | `320 (4 − α_s)² = N_pair⁶ (N_quark − 1) (N_pair² − α_s)²` | sympy `simplify(diff) == 0` |
| D2 struct | `320 = N_pair⁶ (N_quark − 1)` | exact integer |
| D3 P + 3Q | `4 (α_s² − 4α_s + 96)² = N_pair² (α_s² − 4α_s + 96)²` | sympy `simplify(diff) == 0` |
| D4 Line A | `P + 3Q proportional to (α_s² − 4α_s + 96)²` | sympy exact |
| D4 Line B | `Q − P proportional to (4 − α_s)²` | sympy exact |
| D4 generic classification | coefficient comparison against an arbitrary quadratic square forces `β = 3α` or `β = −α` | sympy exact |
| D5 Jarlskog | `Q − P = 36864 η̄² = N_pair^10 N_quark² η̄²` | sympy `simplify(diff) == 0` |
| D5 Perimeter | `P + 3Q = 9216 perim_sq² = N_pair⁸ N_quark² perim_sq²` | sympy `simplify(diff) == 0` |
| D6 cross | `(P + 3Q)(Q − P) = 1280 (α_s²−4α_s+96)² (4−α_s)²` | sympy `simplify(diff) == 0` |
| D6 sqrt | `sqrt = N_pair⁴ √(N_quark−1) (α_s²−4α_s+96)(4−α_s)` | sympy `simplify(diff) == 0` |
| D7 inverse P | `P = ((P+3Q) − 3(Q−P))/4` | sympy exact |
| D7 inverse Q | `Q = ((P+3Q) + (Q−P))/4` | sympy exact |

## Science Value

### What this lets the framework state cleanly

Previously, the framework had retained the Brocard polynomial `P(α_s)`
as the universal equilateral-excess polynomial across **9 distinct
companion theorems** (Brocard angle, Symmedian/Brocard circle,
Steiner-Marden, Weitzenbock, Pedoe, Brocard points, Napoleon,
nine-point pencil, Vieta structural integers). The Q-polynomial
`Q(α_s)` was retained from the Brocard-points branch. The pair `(P, Q)`
was treated as a 2-dimensional algebraic system, but the **internal
structure of linear combinations** had not been characterized.

This note delivers:

1. **NEW scalar-multiple square decomposition** of the (P, Q) module into two
   distinct channels, each with structural-integer scaling:
   - Jarlskog channel `Q − P = N_pair^10 N_quark² η̄²`,
   - Perimeter channel `P + 3Q = N_pair⁸ N_quark² perim_sq²`.

2. **NEW characterization of scalar-multiple square channels**: the
   set of `(α, β)` such that `αP + βQ` is a scalar multiple of one
   square polynomial consists of exactly two lines `(Line A: β = 3α)`
   and `(Line B: β = −α)`. All other `(α, β)` give mixed-channel
   combinations.

3. **NEW physical interpretation**: the two scalar-multiple square channels
   correspond to two specific physical observables — Jarlskog squared
   and perimeter-squared — and their structural-integer scalings are
   exact powers of `N_pair, N_quark`.

4. **NEW cross-channel identity**: the product of the two channels is
   itself a scalar-multiple square of `N_pair⁴ √(N_quark − 1) (α_s² − 4α_s + 96)(4 − α_s)`.

5. **NEW module decomposition**: `P` and `Q` are recovered as linear
   combinations of the two scalar-multiple square channels:
   `P = (perimeter − 3·Jarlskog)/4`, `Q = (perimeter + Jarlskog)/4`.

### Why this counts as pushing the science forward

The Brocard polynomial `P(α_s)` and Q-polynomial `Q(α_s)` are the
**two fundamental quartic polynomials** of the retained NLO Wolfenstein
protected-γ̄ surface. This note shows that the algebraic structure of
the (P, Q) pair has a **canonical scalar-multiple square decomposition** into
two channels, each tied to a specific physical observable:

- The **Jarlskog channel** `Q − P` is purely a scalar-multiple square in
  `(4 − α_s)`, proportional to `J̄²`. This decouples the
  CP-violation magnitude from the rest.
- The **Perimeter channel** `P + 3Q` is purely a scalar-multiple square in
  `(α_s² − 4α_s + 96)`, proportional to `perim_sq²`. This decouples
  the triangle-shape magnitude from the rest.

The fact that the (P, Q) module decomposes **exactly** into these two
scalar-multiple square channels — with structural-integer scaling factors —
is a strong algebraic statement about the retained surface. It says:
the protected-γ̄ structure forces a clean separation of the algebraic
content into "CP-violation magnitude" and "perimeter magnitude"
components, with no mixed terms when expressed in the right linear basis.

This is the **algebraic skeleton of the (P, Q) system** on the retained
surface, complementing the Vieta structural-integer expansion of `P`
itself (companion theorem). Together they give the complete algebraic
characterization of the Brocard-polynomial / Q-polynomial pair.

### Falsifiable structural claim

The closure (D2-D7) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
forces:
  Q - P  =  N_pair^6 (N_quark - 1) (N_pair^2 - alpha_s)^2  (Jarlskog channel),
  P + 3Q  =  N_pair^8 N_quark^2 perim_sq^2                  (Perimeter channel).

  The set of scalar-multiple square-channel linear combinations alpha P + beta Q is
  exactly the union of two lines (beta = 3 alpha) and (beta = -alpha).
```

Any framework revision moving `(rho_bar, eta_bar)` off the retained
protected-γ̄ surface would break the square-channel structure of both
combinations simultaneously, since the algebraic identity
`P = (alpha_s^2 - 4 alpha_s + 96)^2 - 240(4 - alpha_s)^2` and the
analogous one for Q are tied to the retained `tan(γ̄) = √5`.

## What This Claims

- `(D2)`: NEW retained scalar-multiple square decomposition
  `Q − P = N_pair⁶ (N_quark − 1) (N_pair² − α_s)²`.
- `(D3)`: NEW retained scalar-multiple square decomposition
  `P + 3Q = N_pair² (α_s² − 4α_s + 96)²`.
- `(D4)`: NEW retained characterization of the two scalar-multiple square
  subspaces of the (P, Q) module.
- `(D5)`: NEW retained physical interpretation: Jarlskog channel
  `Q − P = N_pair^10 N_quark² η̄²`; Perimeter channel
  `P + 3Q = N_pair⁸ N_quark² perim_sq²`.
- `(D6)`: NEW retained cross-channel identity
  `(P + 3Q)(Q − P) = N_pair⁸ (N_quark − 1) (α_s² − 4α_s + 96)² (4 − α_s)²`.
- `(D7)`: NEW retained module decomposition: `P = (Perimeter − 3 Jarlskog)/4`,
  `Q = (Perimeter + Jarlskog)/4`.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs.
- Does **not** depend on any α_s-running pipeline.
- Does **not** make a direct CKM-observable claim about the (P, Q) pair;
  the scalar-multiple square channels are derived algebraic structures of the
  Brocard polynomial and the Q-polynomial.

## Reproduction

```bash
python3 scripts/frontier_ckm_brocard_q_polynomial_perfect_square_decomposition.py
```

Expected:

```text
TOTAL: PASS=28, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs (`N_pair`, `N_color`, `N_quark`).
- Computes `P, Q` symbolically and verifies all six identities (D2-D7)
  by `simplify(diff) == 0` via sympy.
- Checks that off-line linear combinations are NOT single-square channels.
- Verifies the cross-channel identity and the module decomposition
  inverse relations.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.

**Companion barred-triangle closed forms (cited for context, not
load-bearing here):**

The Brocard polynomial `P(α_s)` and Q-polynomial `Q(α_s)` appear in
9+ companion closed-form theorems (Brocard angle, Symmedian/Brocard
circle, Steiner-Marden, Weitzenbock, Pedoe, Brocard points,
Napoleon, nine-point pencil, Vieta structural integers, Orthic
triangle). This note provides the scalar-multiple square decomposition of
the (P, Q) module that completes the algebraic characterization.

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch.
- Any candidates-tier theorem.
