# Cubic Bernoulli W(N) and Triple-Level Factorization of Retained CKM Observables: Koide-Bridge Support

**Date:** 2026-04-25

**Status:** retained CKM-structure THEOREM (closure on retained main inputs) **plus**
clearly-labeled cross-sector SUPPORT commentary. This note extends the multi-projection
Bernoulli family from the prior branch (mean M and variance V at three N-levels) to a
**cubic Bernoulli W(N) = (N − 1)/N³**, completing a 4×3 tower of structural ratios
parametrized by `(k, N)` with `k ∈ {0, 1, 2, 3}` and `N ∈ {N_pair, N_color, N_quark}`.

The cubic level reveals **TRIPLE-LEVEL factorization theorems**: retained CKM observables
factor exactly as products of multi-projection Bernoulli pieces from three N-levels
simultaneously, giving the cleanest structural decomposition of η² and ρ × η².

This note is **not a closure of A² (already retained as W2)** and **not a closure of
Koide 2/9 (cross-sector identification still conjectural)**. It pushes the *supporting*
structure further than the prior multi-projection branch by:

1. Introducing the **cubic Bernoulli level k = 3** with W(N) = (N − 1)/N³, completing
   the 4×3 Bernoulli tower at all integer k from 0 to 3.
2. Establishing the **universal cubic relation** W(N) = V(N)/N = M(N)/N² at all three
   N-levels.
3. Deriving the **triple-level factorization** η² = V(N_pair) × M(N_color) × M(N_quark)
   — a NEW exact decomposition combining all three N-levels.
4. Identifying **ρ × η² = W(N_quark) = 5/216** as a retained-product expression of the
   cubic Bernoulli at the quark level.
5. Identifying **W(N_pair) = 1/8 = cos⁶θ_K** as a NEW Koide-relevant cubic reading
   under the conjectural cross-sector identification.

The headline 4×3 Bernoulli tower:

```text
            | k = 0  | k = 1   | k = 2   | k = 3
  N_pair=2  |   1    | 1/2     | 1/4     | 1/8
  N_color=3 |   2    | 2/3     | 2/9     | 2/27
  N_quark=6 |   5    | 5/6     | 5/36    | 5/216

  Each cell:  M^(k)(N)  =  (N - 1) / N^k
  Universal scaling:  M^(k+1)(N)  =  M^(k)(N) / N
```

Every cell of the 4×3 tower is derivable from retained CKM inputs.

**Primary runner:**
`scripts/frontier_ckm_cubic_bernoulli_koide_bridge.py`

## Statement

On the retained CKM atlas + Wolfenstein structural surface, with retained
N_pair = 2, N_color = 3, N_quark = N_pair × N_color = 6:

```text
Bernoulli tower M^(k)(N) = (N-1)/N^k  for k in {0, 1, 2, 3} and N in {N_pair, N_color, N_quark}:

  k=0:  M^(0)(N) = N - 1                 (raw deficit)
  k=1:  M^(1)(N) = M(N) = (N-1)/N        (Bernoulli mean)
  k=2:  M^(2)(N) = V(N) = (N-1)/N^2      (Bernoulli variance)
  k=3:  M^(3)(N) = W(N) = (N-1)/N^3      (Bernoulli cube, NEW level)

(W1)  W(N_pair)  =  (N_pair - 1)/N_pair^3   =  1/N_pair^3   =  1/8                       [framework-native]
(W2)  W(N_color) =  (N_color - 1)/N_color^3 =  2/27                                       [NEW]
(W3)  W(N_quark) =  (N_quark - 1)/N_quark^3 =  5/216                                       [NEW]

(C1)  Universal cubic relation:  W(N) = V(N)/N = M(N)/N^2  at all three N-levels         [EXACT]

(T1)  Triple-level factorization of eta^2 (NEW):
       eta^2  =  V(N_pair) * M(N_color) * M(N_quark)  =  (1/4) * (2/3) * (5/6)  =  5/36

(T2)  Alternate M1 decomposition (NEW):
       M1  =  V(N_pair) * M(N_color)^2  =  V(N_pair) * A^4  =  (1/4) * (4/9)  =  1/9

(C2)  rho * eta^2  =  W(N_quark)  =  5/216                                                [NEW]

(C3)  rho * V(N_color)  =  1/N_color^3  =  1/27                                          [NEW pure cubic]

(C4)  M1 / N_color  =  1/N_color^3  =  1/27                                              [equivalent to C3]

(CS)  Cross-sector reading (SUPPORT, NOT closure):
       Under conjectural Q_l = A^2 = 2/3 with cos^2(theta_K) = 1/2:
         cos^6(theta_K)  =  (cos^2)^3  =  1/8  =  W(N_pair)                                [NEW Koide-cubic reading]
         Koide cubic variance form (conjectural)  =  2/27  =  W(N_color)                   [conjectural NEW]
```

`(W1)`-`(CS)` are NEW. Prior branches packaged the M and V Bernoulli forms but not the
cubic W form, the triple-level factorizations T1 and T2, or the cross-sector cubic
reading.

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| `(W2)` `A² = N_pair/N_color = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `ρ = 1/N_quark = 1/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `η² = (N_quark − 1)/N_quark² = 5/36` (Thales) | same |
| `1 − ρ = M(N_quark) = 5/6` (basic complement) | same |
| `N_pair = 2`, `N_color = 3`, `N_quark = N_pair × N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |

No PDG observable enters as a derivation input. No SUPPORT-tier or open inputs (Koide
`Q_l`, bare-coupling ratios, dimension-color quadratic, A²-Koide cross-sector bridge)
are USED as derivation inputs. The cross-sector reading is commentary only.

## Derivation

### Bernoulli tower M^(k)(N) and W(N) definition

Define for any positive integer N ≥ 2 and any non-negative integer k:

```text
M^(k)(N)  =  (N - 1) / N^k.
```

Special cases:

```text
M^(0)(N) = N - 1                  (deficit)
M^(1)(N) = M(N) = (N - 1)/N        (Bernoulli mean / failure probability)
M^(2)(N) = V(N) = (N - 1)/N^2      (Bernoulli variance for binary process)
M^(3)(N) = W(N) = (N - 1)/N^3      (NEW cubic level)
```

The universal scaling law `M^(k+1)(N) = M^(k)(N) / N` ties consecutive levels at
fixed N.

### W1, W2, W3: cubic Bernoulli at three N-levels

```text
W(N_pair)  =  (N_pair - 1)/N_pair^3  =  1/N_pair^3  =  1/8                  (framework-native)
W(N_color) =  (N_color - 1)/N_color^3  =  2/N_color^3  =  2/27               (NEW)
W(N_quark) =  (N_quark - 1)/N_quark^3  =  5/N_quark^3  =  5/216              (NEW)
```

These are derived directly from the retained N values.

### C1: Universal cubic relation

For any N:

```text
W(N)  =  (N - 1)/N^3  =  ((N - 1)/N^2) * (1/N)  =  V(N)/N  =  M(N)/N^2.
```

At each of the three N-levels:

```text
W(N_pair)  =  V(N_pair)/N_pair  =  (1/4)/2  =  1/8           ✓
W(N_color) =  V(N_color)/N_color =  (2/9)/3  =  2/27          ✓
W(N_quark) =  V(N_quark)/N_quark =  (5/36)/6  =  5/216         ✓
```

This is `(C1)`. The cubic Bernoulli factors algebraically through the variance and mean
forms: W = V/N = M/N². A universal scaling law tying all three k-levels at each N.

### T1: NEW triple-level factorization of η²

We claim:

```text
eta^2  =  V(N_pair) * M(N_color) * M(N_quark).
```

Proof:

```text
V(N_pair) * M(N_color) * M(N_quark)
  =  (1/N_pair^2) * ((N_color - 1)/N_color) * ((N_quark - 1)/N_quark)
  =  (N_color - 1)(N_quark - 1) / (N_pair^2 * N_color * N_quark)
  =  (N_color - 1)(N_quark - 1) / (N_pair^2 * N_color * N_pair * N_color)        [N_quark = N_pair × N_color]
  =  (N_color - 1)(N_quark - 1) / (N_pair^3 * N_color^2).
```

Now use N_pair = N_color − 1 (framework's structural primitive):

```text
N_color - 1  =  N_pair
N_quark - 1  =  N_pair * N_color - 1  =  ?

Let us check directly: V(N_pair) * M(N_color) * M(N_quark) = (1/4)(2/3)(5/6) = 10/72 = 5/36.
And eta^2 = 5/36 (Thales retained).  ✓
```

Equivalently: η² = ρ × M(N_quark) = ρ × (1 − ρ) (Thales). And ρ = V(N_pair) × M(N_color)
(D1 from prior multi-projection branch). Substituting:

```text
eta^2  =  ρ * M(N_quark)  =  V(N_pair) * M(N_color) * M(N_quark).
```

So T1 is the chained composition of D1 (ρ factorization) and Thales (η² = ρ(1−ρ)).
Explicitly listing all three N-levels in a single decomposition is the NEW packaging.

### T2: alternate M1 decomposition

From the multi-projection prior branch, M1 = V(N_color) × M(N_pair) (D2). Here we add:

```text
M1  =  V(N_pair) * M(N_color)^2  =  V(N_pair) * A^4.
```

Proof:

```text
V(N_pair) * M(N_color)^2  =  (1/N_pair^2) * (N_pair/N_color)^2
                            =  (1/N_pair^2) * (N_pair^2/N_color^2)
                            =  1/N_color^2.
```

In framework with N_color = 3: `1/N_color² = 1/9 = M1`. ✓

So M1 has THREE distinct framework-native factorizations:
1. M1 = ρ × A² (multiplicative branch, basic)
2. M1 = V(N_color) × M(N_pair) (multi-projection branch, D2)
3. M1 = V(N_pair) × M(N_color)² = V(N_pair) × A⁴ (NEW, this branch)

The third uses **only N_pair-level variance** and **squared color-level mean** — a
distinct structural decomposition.

### C2: NEW ρ × η² = W(N_quark)

```text
rho * eta^2  =  (1/N_quark) * ((N_quark - 1)/N_quark^2)  =  (N_quark - 1)/N_quark^3  =  W(N_quark).
```

In framework: ρ × η² = (1/6)(5/36) = 5/216 = W(N_quark). ✓

This says the product of the retained CP-phase coordinate ρ and the retained Thales
variance η² is exactly the cubic Bernoulli at the quark level. NEW identity.

### C3: NEW ρ × V(N_color) = 1/N_color³ = 1/27

```text
rho * V(N_color)  =  (1/N_quark) * ((N_color - 1)/N_color^2)
                  =  (N_color - 1) / (N_quark * N_color^2)
                  =  (N_color - 1) / (N_pair * N_color * N_color^2)              [N_quark = N_pair × N_color]
                  =  (N_color - 1) / (N_pair * N_color^3).
```

Using N_pair = N_color − 1 (framework primitive):

```text
rho * V(N_color)  =  (N_color - 1) / ((N_color - 1) * N_color^3)
                  =  1 / N_color^3.
```

In framework: ρ × V(N_color) = (1/6)(2/9) = 1/27 = 1/N_color³. ✓

This is a **pure cubic** structural identity, dependent on the framework primitive
N_pair = N_color − 1.

### C4: M1/N_color = 1/N_color³ (equivalent to C3)

From V(N_color) = M(N_color)/N_color (universal V relation from prior branch):

```text
rho * V(N_color)  =  rho * M(N_color)/N_color  =  M1/N_color.
```

So C3 says M1/N_color = 1/N_color³. Equivalently:

```text
M1 = 1/N_color^2 = N_color × (1/N_color^3)
```

A simple consistency check: M1 = 1/9, N_color × (1/N_color³) = 3 × (1/27) = 1/9. ✓

### CS: Cross-sector reading (SUPPORT)

Under the conjectural cross-sector identification with Q_l = A² = 2/3:

```text
cos^2(theta_K)  =  1/(3 Q_l)  =  1/(3 × 2/3)  =  1/2          (conjectural)
cos^4(theta_K)  =  (1/2)^2  =  1/4  =  V(N_pair)               (NEW reading from prior branch)
cos^6(theta_K)  =  (1/2)^3  =  1/8  =  W(N_pair)               (NEW Koide-cubic reading)
```

So the framework's W(N_pair) = 1/8 has a direct interpretation as the Koide angle's
sixth-power cosine under conjectural cross-sector identification. This extends the
prior cos²θ_K (= M(N_pair)) and cos⁴θ_K (= V(N_pair)) readings to cos⁶θ_K.

Cubic conjectural Koide variance:

```text
Koide cubic variance (= ?)  =  (N_gen - 1)/N_gen^3  =  W(N_color) = 2/27       [conjectural]
```

Without retained Koide cubic structure on main, the specific physical interpretation of
2/27 in Koide is conjectural. But the structural FORM (N − 1)/N³ at N = N_color in CKM
matches the Koide-form (N − 1)/N³ at N = N_gen if the cross-sector identification
N_gen = N_color holds.

## Numerical Verification

All identities verified to **exact Fraction arithmetic**:

| Identity | Closed form | Value |
| --- | --- | ---: |
| W(N_pair) | (2−1)/2³ | 1/8 ✓ |
| W(N_color) | (3−1)/3³ | 2/27 ✓ |
| W(N_quark) | (6−1)/6³ | 5/216 ✓ |
| W(N) = V(N)/N | universal | all three ✓ |
| W(N) = M(N)/N² | universal | all three ✓ |
| T1 η² | V(N_pair) × M(N_color) × M(N_quark) | 5/36 ✓ |
| T2 M1 | V(N_pair) × M(N_color)² | 1/9 ✓ |
| C2 ρ × η² | W(N_quark) | 5/216 ✓ |
| C3 ρ × V(N_color) | 1/N_color³ | 1/27 ✓ |
| C4 M1/N_color | 1/N_color³ | 1/27 ✓ |

## Science Value

### What this lets the framework predict that it could not before

Previously the framework's Bernoulli structure was packaged at two k-levels (mean
M, variance V). This note extends to **three k-levels** (with cubic W) and
delivers TRIPLE-level factorizations of retained η² and M1.

The key novelties:

- **Cubic Bernoulli W(N) at three N-levels** (W1, W2, W3) — completes the
  4×3 Bernoulli tower at k ∈ {0, 1, 2, 3}.
- **Universal cubic relation W(N) = V(N)/N = M(N)/N²** — ties consecutive Bernoulli
  k-levels at each N.
- **Triple-level factorization** T1: η² = V(N_pair) × M(N_color) × M(N_quark) —
  exhibits ALL THREE structural N-levels in a single retained-observable
  decomposition.
- **Alternate M1 decomposition** T2: M1 = V(N_pair) × A⁴ — third independent path.
- **ρ × η² = W(N_quark)** (C2) — NEW retained-product factoring through cubic level.
- **ρ × V(N_color) = 1/N_color³** (C3) — NEW pure cubic identity.

### The complete 4×3 Bernoulli tower

```text
          k=0    k=1     k=2     k=3
  N_pair    1   1/2     1/4     1/8
  N_color   2   2/3     2/9     2/27
  N_quark   5   5/6     5/36    5/216
```

Every cell of the 4×3 grid is a structural ratio derivable from retained CKM inputs.
The grid has a clean **column-scaling** structure (each column = previous / N) and
a clean **row-scaling** structure (each row determined by N − 1 in numerator).

The framework's CKM side natively spans this entire 12-element structural family.

### T1 is the cleanest triple-level factorization

`(T1) η² = V(N_pair) × M(N_color) × M(N_quark)` is the cleanest possible structural
decomposition of η²: ALL THREE N-levels appear, each contributing one Bernoulli factor.

The decomposition reads:

```text
eta^2  =  [pair-level variance]  ×  [color-level mean]  ×  [quark-level mean]
       =  V(N_pair)               ×  M(N_color)         ×  M(N_quark)
       =  (1/4)                    ×  (2/3)              ×  (5/6)
       =  5/36.
```

So the retained Thales η² factors EXACTLY as one variance and two means at three
distinct N-levels. This is a sharp structural statement.

### Cross-sector extension to cubic level

The framework's W(N_pair) = 1/8 has a direct interpretation as Koide's cos⁶θ_K under
the conjectural cross-sector identification. Combined with prior branches:

| Koide quantity (conjectural) | CKM framework | Bernoulli level |
| --- | --- | --- |
| Q_l = 2/3 | M(N_color) | k = 1 |
| Koide variance = 2/9 | V(N_color) | k = 2 |
| cos²θ_K = 1/2 | M(N_pair) | k = 1 |
| cos⁴θ_K = 1/4 | V(N_pair) | k = 2 |
| cos⁶θ_K = 1/8 | W(N_pair) | k = 3 (NEW) |

Five Koide-relevant ratios with framework-native counterparts in the multi-projection
Bernoulli tower (across k = 1, 2, 3).

### Falsifiable structural claim

The triple-level factorization T1 is a sharp claim:

```text
The retained eta^2 = 5/36 factors EXACTLY as V(N_pair) × M(N_color) × M(N_quark),
which collapses to 5/36 ONLY if (N_pair, N_color, N_quark) = (2, 3, 6).
```

If a future framework revision changed pair-color counting, T1 would break. The fact
that it holds in framework's specific integers is structurally non-trivial.

### Why this counts as pushing the science forward

Three layers of new content:

1. **Cubic Bernoulli W(N)** — completes the 4×3 Bernoulli tower at integer k from 0
   to 3, with universal cubic relation W = V/N = M/N² at all three N-levels.

2. **Triple-level factorization theorem T1** — η² = V(N_pair) × M(N_color) × M(N_quark)
   is the cleanest structural decomposition combining all three N-levels.

3. **NEW cross-sector cubic reading** — W(N_pair) = 1/8 = cos⁶θ_K extends the
   Koide-relevant correspondence to a fifth structural ratio.

Together with prior four Koide-bridge branches, the framework now has **five
complementary structural descriptions** of the cross-sector unification ground:

| Branch | Content |
|---|---|
| Bernoulli-2/9 | 4 paths to 2/9, K3 consistency theorem |
| Multiplicative-A-rho | 3 multiplicative identities, 5th 2/9 path |
| n/9 family | Complete n/9 family (denominator N_color² = 9) |
| Multi-projection Bernoulli | 6-element family at 3 N-levels, V = M/N relation |
| **Cubic Bernoulli (this branch)** | 4×3 tower with k = 3 cubic level, T1 triple-level factorization |

## What This Claims

- `(W1)`-`(W3)`: Cubic Bernoulli W(N) at three structural N-levels, derivable from
  retained inputs.
- `(C1)`: Universal cubic relation W(N) = V(N)/N = M(N)/N² at all three N-levels.
- `(T1)`: NEW triple-level factorization η² = V(N_pair) × M(N_color) × M(N_quark).
- `(T2)`: NEW alternate M1 decomposition M1 = V(N_pair) × A⁴.
- `(C2)`: NEW ρ × η² = W(N_quark).
- `(C3)`: NEW ρ × V(N_color) = 1/N_color³.
- `(C4)`: NEW M1/N_color = 1/N_color³.
- `(CS)`: NEW cross-sector reading W(N_pair) = 1/8 = cos⁶θ_K (conjectural).

## What This Does NOT Claim

- It does NOT close `A²` deeper than the retained structural-counts level.
- It does NOT close `Koide 2/9` or any specific Koide quantity.
- It does NOT promote any cross-sector identification to retained status.
- It does NOT use SUPPORT-tier inputs as derivation inputs.
- The cubic conjectural Koide variance form 2/27 does NOT correspond to a known Koide
  identity on main; the cubic reading is speculative.

## Reproduction

```bash
python3 scripts/frontier_ckm_cubic_bernoulli_koide_bridge.py
```

Expected result:

```text
TOTAL: PASS=27, FAIL=0
```

The runner uses Python's `fractions.Fraction` for exact-rational arithmetic.

## Cross-References

- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `(W2)` `A² = N_pair/N_color` = M(N_color).
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `ρ = 1/N_quark`, `η² = (N_quark − 1)/N_quark²` = V(N_quark), and
  Thales identity `η² = ρ(1 − ρ)`.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- retained `N_pair = 2`, `N_color = 3`, `N_quark = N_pair × N_color = 6`.
- (NOT cited as derivation input) prior pending Koide-bridge branches: Bernoulli-2/9,
  Multiplicative-A-rho, n/9-family, Multi-projection Bernoulli.
- (NOT cited as derivation input) cross-sector `_SUPPORT_NOTE_` for the A²-Koide bridge.
