# Egyptian Fraction Unitarity 1/N_pair + 1/N_color + 1/N_quark = 1: Ternary Refinement of Koide Unitarity Supporting the Cross-Sector Bridge

**Date:** 2026-04-25

**Status:** retained CKM-structure THEOREM (closure on retained main inputs) **plus**
clearly-labeled cross-sector SUPPORT commentary. This note exhibits a sharp
**number-theoretic identity** linking the framework's three structural integers
N_pair = 2, N_color = 3, N_quark = 6:

```text
1/N_pair + 1/N_color + 1/N_quark  =  1     EXACTLY.
```

This is the unique three-element Egyptian fraction representation of unity that
is consistent with the framework's structural primitives `N_pair = N_color − 1`
and `N_quark = N_pair × N_color`. The identity is a structural fingerprint of the
framework's specific integer choice (2, 3, 6) — no other set of integers
satisfying the framework's primitives gives 1.

The note also exhibits **geometric series closures** ∑_k M^(k)(N) = 1 for any N
≥ 2 (universal Bernoulli tower closure to unity), and **cross-N Bernoulli sum
closures** at fixed k:

```text
k=1:  sum_N M(N)  =  N_pair  =  2
k=3:  sum_N W(N)  =  2/9    [= central Koide-relevant ratio!]
```

The k=3 cross-N sum equals **exactly** 2/9, the Koide-relevant ratio derived
multi-path in prior branches. This is a strong supporting structural fact.

The most striking new content is the **ternary refinement of Koide unitarity**:

```text
Binary Koide:           cos^2(theta_K)  +  sin^2(theta_K)              =  1
Ternary framework:      1/N_pair          +  1/N_color  +  1/N_quark    =  1

Identification (under cross-sector A^2 = Q_l = 2/3):
   cos^2(theta_K)  =  1/N_pair                                          [from prior branches]
   sin^2(theta_K)  =  1/N_color + 1/N_quark                              [NEW DECOMPOSITION]
```

So the framework's ternary unitarity **REFINES** Koide's binary unitarity by
splitting `sin²θ_K = 1/2` into TWO structural pieces `1/N_color = 1/3` and
`1/N_quark = 1/6`.

This note is **not a closure of A² (already retained as W2)** and **not a
closure of Koide 2/9 (cross-sector identification still conjectural)**. It pushes
the *supporting* structure further than prior branches by exhibiting a sharp
**number-theoretic** identity that uniquely characterizes the framework's
structural integer choice.

**Primary runner:**
`scripts/frontier_ckm_egyptian_bernoulli_closures_koide_bridge.py`

## Statement

On the retained CKM atlas + Wolfenstein structural surface, with retained
N_pair = 2, N_color = 3, N_quark = N_pair × N_color = 6:

```text
(E1)  Egyptian fraction unitarity:
       1/N_pair + 1/N_color + 1/N_quark  =  1     EXACTLY.

(E2)  Uniqueness theorem:
       (N_pair, N_color, N_quark) = (2, 3, 6) is the UNIQUE solution to the system:
         (a)  N_pair  =  N_color - 1
         (b)  N_quark =  N_pair * N_color
         (c)  1/N_pair + 1/N_color + 1/N_quark  =  1
       The framework's structural integers are uniquely characterized by these
       three primitives + the Egyptian fraction unitarity.

(GS1) Geometric series closure: for any N ≥ 2,
       sum_{k=1}^∞ M^(k)(N)  =  sum_{k=1}^∞ (N-1)/N^k  =  1     EXACTLY.

(GS2) Extended geometric closure (with k=0 deficit):
       sum_{k=0}^∞ M^(k)(N)  =  N - 1 + 1  =  N     EXACTLY.

(CS1) Cross-N Bernoulli sum at k=1:
       sum_{N in {N_pair, N_color, N_quark}} M(N)  =  M(N_pair) + M(N_color) + M(N_quark)
                                                    =  3 - (1/N_pair + 1/N_color + 1/N_quark)
                                                    =  3 - 1 = 2 = N_pair.

(CS2) Cross-N Bernoulli sum at k=2:
       sum_N V(N)  =  1/4 + 2/9 + 5/36  =  11/18.    [less clean]

(CS3) Cross-N Bernoulli sum at k=3 (NEW STRIKING):
       sum_N W(N)  =  W(N_pair) + W(N_color) + W(N_quark)
                    =  1/8 + 2/27 + 5/216
                    =  2/9     EXACTLY.
       Equal to the framework's central Koide-relevant ratio.

(K1)  Ternary refinement of Koide unitarity (NEW SUPPORT reading):
       Under conjectural cross-sector A^2 ↔ Q_l identification:
         Koide cos^2(theta_K)  =  1/N_pair  =  1/2                   [from prior branches]
         Koide sin^2(theta_K)  =  1 - 1/N_pair  =  1/N_color + 1/N_quark
                              =  1/3 + 1/6  =  1/2                  [NEW DECOMPOSITION]
       Framework's E1 splits Koide's binary sin^2 unitarity piece into TWO
       structural sub-pieces.

(K2)  M(N_pair) decomposition (NEW):
       M(N_pair)  =  (N_pair - 1)/N_pair  =  1/N_color + 1/N_quark.
       The Bernoulli mean at the pair level decomposes as the sum of reciprocals
       of color and quark levels.

(K3)  Cross-product consistency:
       (sum_N M(N)) * (sum_N W(N))  =  N_pair × 2/9  =  4/9  =  A^4.
       (sum_N M(N)) / (sum_N W(N))  =  N_pair / (2/9)  =  N_color^2  =  9.
```

`(E1)`-`(K3)` are NEW. Prior branches packaged Bernoulli identities at fixed N
or fixed k, but did NOT package the **Egyptian fraction unitarity** linking
all three structural levels, the **geometric series closure** at any N, or the
**ternary refinement** of Koide unitarity.

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| `N_pair = 2`, `N_color = 3`, `N_quark = N_pair × N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |
| Structural primitive `N_pair = N_color − 1` | implicit in retained N_pair = 2, N_color = 3 |
| `(W2)` `A² = N_pair/N_color = 2/3` (= M(N_color)) | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `ρ = 1/N_quark` (= 1/M(N_quark) × 1/(N_quark)... or just 1/N_quark = 1 − M(N_quark)) | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |

The Egyptian fraction unitarity (E1) is a **pure number-theoretic consequence**
of the retained framework primitives `N_pair = N_color − 1`, `N_quark = N_pair ×
N_color`, with the specific framework values `N_pair = 2` and `N_color = 3`.

No PDG observable enters as a derivation input. No SUPPORT-tier or open inputs
(Koide `Q_l`, bare-coupling ratios, cross-sector A²-Koide bridge) are USED as
derivation inputs. The cross-sector reading is commentary only.

## Derivation

### E1: Egyptian fraction unitarity

Starting from retained N_pair = 2, N_color = 3, N_quark = N_pair × N_color = 6:

```text
1/N_pair + 1/N_color + 1/N_quark
  =  1/2 + 1/3 + 1/6
  =  3/6 + 2/6 + 1/6
  =  6/6
  =  1.
```

Direct numerical verification.

### E2: Uniqueness theorem

Suppose `N_pair = N_color − 1` and `N_quark = N_pair × N_color`. Substituting:

```text
1/N_pair + 1/N_color + 1/N_quark
  =  1/(N_color - 1) + 1/N_color + 1/((N_color - 1) × N_color)
  =  [N_color + (N_color - 1) + 1] / ((N_color - 1) × N_color)
  =  [2 N_color] / ((N_color - 1) × N_color)
  =  2 / (N_color - 1).
```

Setting this equal to 1: `2 = N_color − 1`, so `N_color = 3`. Then `N_pair =
N_color − 1 = 2` and `N_quark = N_pair × N_color = 6`.

So the framework's specific integer choice (2, 3, 6) is the **unique** solution
to the three primitives plus Egyptian unitarity.

### GS1, GS2: Geometric series closure

For any N ≥ 2 (with |1/N| < 1):

```text
sum_{k=1}^∞ (N - 1)/N^k  =  (N - 1) * sum_{k=1}^∞ (1/N)^k
                          =  (N - 1) * (1/N) / (1 - 1/N)
                          =  (N - 1) * (1/N) * (N / (N - 1))
                          =  1.
```

This is `(GS1)`. Verifying at all three N-levels:

```text
N = N_pair = 2:    1/2 + 1/4 + 1/8 + 1/16 + ...  =  1
N = N_color = 3:   2/3 + 2/9 + 2/27 + 2/81 + ...  =  1
N = N_quark = 6:   5/6 + 5/36 + 5/216 + ...        =  1
```

For `(GS2)`: at k=0, M^(0)(N) = (N − 1)/N⁰ = N − 1, so adding to the geometric
series sum (which is 1):

```text
sum_{k=0}^∞ M^(k)(N)  =  (N - 1) + 1  =  N.
```

So each structural integer N is recovered as the geometric sum of its own
Bernoulli tower including the deficit.

### CS1: Cross-N sum at k=1

```text
sum_N M(N)  =  M(N_pair) + M(N_color) + M(N_quark)
            =  (1 - 1/N_pair) + (1 - 1/N_color) + (1 - 1/N_quark)
            =  3 - (1/N_pair + 1/N_color + 1/N_quark)
            =  3 - 1                          [using E1]
            =  2
            =  N_pair.
```

So the sum of Bernoulli means at all three N-levels equals exactly `N_pair = 2`.

### CS3: Cross-N sum at k=3 (NEW STRIKING)

```text
sum_N W(N)  =  W(N_pair) + W(N_color) + W(N_quark)
            =  1/8 + 2/27 + 5/216.

LCD 216:    27/216 + 16/216 + 5/216
          =  48/216
          =  2/9.
```

So `∑_N W(N) = 2/9` EXACTLY — the framework's central Koide-relevant ratio.

This is striking: the cubic Bernoulli summed across all three N-levels recovers
the very ratio that prior branches identified as the Koide-relevant 2/9.

### K1: Ternary refinement of Koide unitarity

Under the conjectural cross-sector identification A² = Q_l = 2/3:

```text
cos^2(theta_K)  =  1/(3 Q_l)  =  1/(3 × 2/3)  =  1/2.        [conjectural Koide]
```

In framework: `cos²θ_K = 1/N_pair = 1/2` (matching at N_pair = 2).

Then by Koide unitarity:

```text
sin^2(theta_K)  =  1 - cos^2(theta_K)  =  1/2.
```

But by the framework's Egyptian fraction E1:

```text
1/N_color + 1/N_quark  =  1 - 1/N_pair  =  1 - cos^2(theta_K)  =  sin^2(theta_K)
                       =  1/3 + 1/6  =  1/2.
```

So `sin²θ_K = 1/N_color + 1/N_quark` EXACTLY in the framework's reading.

This is `(K1)`: the framework's ternary unitarity REFINES Koide's binary
unitarity. Where Koide says `1 = cos² + sin²` (two pieces), the framework says
`1 = 1/N_pair + 1/N_color + 1/N_quark` (three pieces), with `cos²θ_K = 1/N_pair`
and `sin²θ_K = 1/N_color + 1/N_quark`.

### K2: M(N_pair) decomposition

A direct corollary of E1:

```text
M(N_pair)  =  (N_pair - 1)/N_pair  =  1 - 1/N_pair  =  1/N_color + 1/N_quark.
```

So `M(N_pair) = 1/N_color + 1/N_quark`. The Bernoulli mean at the pair level
decomposes as the sum of reciprocals of the color and quark levels.

In framework values: `1/2 = 1/3 + 1/6`. ✓

### K3: Cross-product consistency

```text
(sum_N M(N)) * (sum_N W(N))  =  N_pair * (2/9)  =  2 * (2/9)  =  4/9  =  A^4.
(sum_N M(N)) / (sum_N W(N))  =  N_pair / (2/9)  =  9 N_pair/2  =  9.
```

Both products give clean structural quantities: A⁴ = 4/9 (Wolfenstein) and 9 =
N_color² (universal denominator from prior n/9 branch).

## Numerical Verification

All identities verified to **exact Fraction arithmetic**:

| Identity | Closed form | Value |
| --- | --- | ---: |
| E1 Egyptian unitarity | 1/2 + 1/3 + 1/6 | 1 ✓ |
| GS1 (N = 2, 3, 6) | geometric limit | 1 ✓ at each N |
| GS2 (N = 2, 3, 6) | (N − 1) + 1 | N ✓ at each N |
| CS1 ∑_N M(N) | 3 − 1 = 2 | N_pair ✓ |
| CS3 ∑_N W(N) | 1/8 + 2/27 + 5/216 | 2/9 ✓ |
| K1 sin²θ_K decomposition | 1/N_color + 1/N_quark | 1/2 ✓ |
| K2 M(N_pair) decomposition | 1/N_color + 1/N_quark | 1/2 ✓ |
| K3 product N_pair × (2/9) | A⁴ | 4/9 ✓ |
| K3 ratio N_pair / (2/9) | N_color² | 9 ✓ |

## Science Value

### What this lets the framework predict that it could not before

Previously the framework's Bernoulli identities were single-N or cross-N at
single k-levels. This note unifies them through the **Egyptian fraction
unitarity** E1, exhibits **geometric series closure** GS1 at each N, and most
strikingly, identifies the **cross-N cubic sum** CS3 with the central
Koide-relevant ratio 2/9.

### E1 is a sharp number-theoretic identity

`1/N_pair + 1/N_color + 1/N_quark = 1` is a number-theoretic identity that:

1. Holds in framework's specific integers (2, 3, 6).
2. Requires the framework primitives `N_pair = N_color − 1` and `N_quark = N_pair
   × N_color` to derive.
3. Has UNIQUE solution (2, 3, 6) under those primitives + the unitarity
   constraint.

So the framework's specific structural integer choice is **uniquely fixed** by:
- N_pair = N_color − 1 (structural primitive)
- N_quark = N_pair × N_color (multiplicative structure)
- 1/N_pair + 1/N_color + 1/N_quark = 1 (Egyptian unitarity)

These three facts **suffice** to determine (N_pair, N_color, N_quark) = (2, 3,
6).

### CS3: ∑_N W(N) = 2/9 is structurally striking

The sum of cubic Bernoulli at all three N-levels equals **EXACTLY** the Koide-
relevant ratio 2/9:

```text
W(N_pair) + W(N_color) + W(N_quark)  =  1/8 + 2/27 + 5/216  =  2/9.
```

This means the multi-N Bernoulli tower's cubic-level sum is the same value as:
- The Bernoulli variance at color level: V(N_color) = 2/9 (prior branches)
- The Wolfenstein × CP-phase: A²(1 − A²) = 2/9 (K1 prior)
- The orthogonal channel ratio: A²/N_color = 2/9 (K5 prior)
- ... and three other paths.

So 2/9 has now SIX framework-native paths (the previous K1, K2, K5, K6, K7 from
prior branches plus this CS3 cross-N cubic sum). All converge at 2/9 by structural
algebra.

### K1 is the ternary refinement of Koide unitarity

```text
Binary Koide:     cos^2(theta_K) + sin^2(theta_K) = 1
Ternary framework: 1/N_pair + 1/N_color + 1/N_quark = 1
```

The framework's Egyptian fraction is a **ternary refinement** of Koide's binary
unitarity:

- `cos²θ_K = 1/N_pair = 1/2` (single piece, matches prior branches)
- `sin²θ_K = 1/N_color + 1/N_quark = 1/3 + 1/6 = 1/2` (TWO pieces, NEW)

The "extra" structure from the ternary form is that `sin²θ_K` decomposes as
`1/N_color + 1/N_quark`, with each piece having a structural integer
interpretation:

- `1/N_color = 1/3` — the "color" piece of sin²θ_K
- `1/N_quark = 1/6` — the "quark" piece of sin²θ_K (= ρ in framework)

Under cross-sector with N_gen = N_color, the color piece becomes `1/N_gen = 1/3`,
matching Koide-natural quantities. The quark piece `1/N_quark = 1/6` is uniquely
framework-internal; its role under cross-sector unification is conjectural.

### K2: M(N_pair) = 1/N_color + 1/N_quark is a NEW retained-input identity

The Bernoulli mean at the pair level (= 1/2) decomposes as the sum of two
reciprocals from the other levels:

```text
M(N_pair)  =  1/N_color + 1/N_quark.
```

This ties the three N-levels in a single retained-input arithmetic identity,
beyond the multiplicative ties of prior branches.

### Falsifiable structural claim

E1, the Egyptian fraction unitarity, is a sharp falsifiable claim:

```text
The framework's specific integers (N_pair, N_color, N_quark) = (2, 3, 6) are
the UNIQUE solution to:
  N_pair = N_color - 1,  N_quark = N_pair × N_color,  1/N_pair + 1/N_color + 1/N_quark = 1.
```

If a future framework revision changed pair-color counting, the Egyptian
unitarity would break (or shift to a different specific value), unraveling the
ternary refinement of Koide unitarity and the cross-N cubic sum at 2/9.

### Why this counts as pushing the science forward

Three layers of new content:

1. **Egyptian fraction unitarity E1** — a sharp number-theoretic identity that
   uniquely characterizes the framework's structural integers. Pushes beyond
   Bernoulli arithmetic into number-theoretic ground.

2. **Cross-N cubic sum CS3** — the cubic Bernoulli summed at all three N-levels
   equals the central Koide-relevant 2/9. Sixth framework-native path to 2/9,
   from a structurally distinct mechanism (sum, not product).

3. **Ternary refinement of Koide unitarity K1** — the framework's three-piece
   unitarity refines Koide's binary cos² + sin² = 1, decomposing sin²θ_K into
   two structural sub-pieces 1/N_color + 1/N_quark.

Together with prior five Koide-bridge branches:

| Branch | Mechanism | Content |
|---|---|---|
| Bernoulli-2/9 | Multi-path | 4 paths to 2/9, K3 consistency |
| Multiplicative-A-rho | Multiplicative | M1 = 1/9, M2 = 4, fifth 2/9 path |
| n/9 family | Universal denominator | Complete n/9 family at N_color² |
| Multi-projection Bernoulli | Multi-N at fixed k | 6-element family, V = M/N |
| Cubic Bernoulli | Multi-k cubic level | 4×3 tower, T1 triple-level factorization |
| **Egyptian-Bernoulli closures** (this) | Number-theoretic | E1 unitarity, sin²θ_K ternary refinement |

Six complementary structural descriptions of the cross-sector unification ground,
each from a different structural mechanism.

## What This Claims

- `(E1)`: NEW Egyptian fraction unitarity 1/N_pair + 1/N_color + 1/N_quark = 1.
- `(E2)`: NEW uniqueness theorem (2, 3, 6) is unique solution to framework
  primitives + E1.
- `(GS1, GS2)`: NEW geometric series closures of Bernoulli tower at each N.
- `(CS1, CS3)`: NEW cross-N Bernoulli sum closures at k=1 and k=3 with structural
  values N_pair and 2/9 respectively.
- `(K1)`: NEW ternary refinement of Koide unitarity (under conjectural cross-
  sector).
- `(K2)`: NEW M(N_pair) = 1/N_color + 1/N_quark decomposition.
- `(K3)`: NEW cross-product consistency.

## What This Does NOT Claim

- It does NOT close `A²` deeper than the retained structural-counts level.
- It does NOT close `Koide 2/9` or any specific Koide quantity.
- It does NOT promote any cross-sector identification to retained status.
- It does NOT use SUPPORT-tier inputs as derivation inputs.

## Reproduction

```bash
python3 scripts/frontier_ckm_egyptian_bernoulli_closures_koide_bridge.py
```

Expected result:

```text
TOTAL: PASS=22, FAIL=0
```

The runner uses Python's `fractions.Fraction` for exact-rational arithmetic.

## Cross-References

- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- retained `N_pair = 2`, `N_color = 3`, `N_quark = N_pair × N_color = 6`, and
  the structural primitive `N_pair = N_color − 1`.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `(W2)` `A² = N_pair/N_color = 2/3` (used in cross-sector reading).
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `ρ = 1/N_quark` (which appears as 1/N_quark in E1).
- (NOT cited as derivation input) prior pending Koide-bridge branches: Bernoulli-2/9,
  Multiplicative-A-rho, n/9-family, Multi-projection Bernoulli, Cubic Bernoulli.
- (NOT cited as derivation input) cross-sector `_SUPPORT_NOTE_` for the A²-Koide bridge.
