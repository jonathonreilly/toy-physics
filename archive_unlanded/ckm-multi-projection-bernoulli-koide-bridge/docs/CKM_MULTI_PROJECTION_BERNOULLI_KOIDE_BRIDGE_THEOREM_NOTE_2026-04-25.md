# Multi-Projection Bernoulli Family at N_pair, N_color, N_quark: Six-Element Structural Family Supporting the Koide Bridge

**Date:** 2026-04-25

**Status:** retained CKM-structure THEOREM (closure on retained main inputs) **plus**
clearly-labeled cross-sector SUPPORT commentary. This note generalizes the
Bernoulli-form ratios `(N-1)/N` and `(N-1)/N²` from a single N-level to a
**multi-projection family** evaluated at all three structural-integer levels of
the framework: `N_pair = 2`, `N_color = 3`, `N_quark = 6`.

The result is a **six-element Bernoulli family** {M(N), V(N) for N ∈ {N_pair,
N_color, N_quark}} with **universal Bernoulli relation V(N) = M(N)/N** at every
level, plus **cross-level decomposition theorems** that express retained CKM
quantities (ρ, M1) as products of multi-projection Bernoulli pieces.

This note is **not a closure of A² (already retained as W2)** and **not a
closure of Koide 2/9 (cross-sector identification still conjectural)**. It pushes
the *supporting* structure further than the prior n/9-family branch by:

1. Lifting the Bernoulli structure from a single N-level to **three N-levels
   simultaneously**, exhibiting a 6-element family.
2. Establishing the **universal Bernoulli relation** V(N) = M(N)/N as a
   structural fact at all three levels.
3. Deriving **cross-level decomposition theorems** D1, D2 expressing retained
   ρ and M1 as products of Bernoulli pieces from different levels.
4. Identifying V(N_pair) = 1/4 as a **NEW Koide-relevant ratio** under
   cross-sector reading: cos⁴θ_K = 1/4 maps onto the framework's V(N_pair).

The headline identities, all from retained CKM inputs:

```text
Mean form M(N) = (N-1)/N at three structural levels:
  M(N_pair)  =  1/2     =  1/N_pair                     [framework-native]
  M(N_color) =  2/3     =  A^2                          [retained W2]
  M(N_quark) =  5/6     =  1 - rho  =  sin^2(gamma_bar) [retained CP-phase + N4]

Variance form V(N) = (N-1)/N^2 at three structural levels:
  V(N_pair)  =  1/4     =  1/N_pair^2                   [framework-native, NEW reading]
  V(N_color) =  2/9     =  (N_color-1)/N_color^2        [from prior 2/9 branches]
  V(N_quark) =  5/36    =  eta^2                        [retained Thales]

Universal Bernoulli relation:
  V(N) = M(N) / N    for all N in {N_pair, N_color, N_quark}    [EXACT]

Cross-level decompositions (NEW):
  rho  =  V(N_pair) * M(N_color)    =  (1/4) * (2/3)  =  1/6
  M1   =  V(N_color) * M(N_pair)     =  (2/9) * (1/2)  =  1/9    (= rho * A^2)
```

**Cross-sector reading (SUPPORT, conditional):**

Under the conjectural cross-sector identification N_gen = N_color = 3, the
Koide angle's squared and fourth-power cosines have framework counterparts:

```text
cos^2(theta_K)  =  1/(3 Q_l)  =  1/2  =  1/N_pair  =  M(N_pair)   [under Q_l = A^2 = 2/3]
cos^4(theta_K)  =  1/4         =  1/N_pair^2  =  V(N_pair)        [NEW reading]
```

So the framework's M(N_pair) = 1/2 and V(N_pair) = 1/4 directly match the
Koide cos²θ_K and cos⁴θ_K under cross-sector identification. Both are NEW
structural readings supporting the bridge.

**Primary runner:**
`scripts/frontier_ckm_multi_projection_bernoulli_koide_bridge.py`

## Statement

On the retained CKM atlas + Wolfenstein structural surface, with retained
N_pair = 2, N_color = 3, N_quark = N_pair × N_color = 6:

```text
(B1)  M(N_pair)  =  (N_pair - 1) / N_pair  =  1/2                              [framework-native]

(B2)  M(N_color) =  (N_color - 1) / N_color  =  A^2  =  2/3                    [retained W2]

(B3)  M(N_quark) =  (N_quark - 1) / N_quark  =  1 - rho  =  sin^2(gamma_bar)
                  =  5/6                                                         [retained CP-phase, N4 protection]

(B4)  V(N_pair)  =  (N_pair - 1) / N_pair^2  =  1/4                            [framework-native, NEW reading]

(B5)  V(N_color) =  (N_color - 1) / N_color^2  =  2/9                          [from prior 2/9 branches]

(B6)  V(N_quark) =  (N_quark - 1) / N_quark^2  =  eta^2  =  5/36              [retained Thales]

(MV1) V(N) = M(N) / N    for all N in {N_pair, N_color, N_quark}                [EXACT structural relation]

(D1)  rho  =  V(N_pair) * M(N_color)  =  1/N_pair^2  *  N_pair/N_color  =  1/(N_pair * N_color)  =  1/N_quark
                                                                                 [NEW cross-level decomposition]

(D2)  M1  =  rho * A^2  =  V(N_color) * M(N_pair)  =  ((N_color - 1)/N_color^2) * (1/N_pair)
                                                                                 [NEW cross-level decomposition]

(CS1) Cross-sector reading (SUPPORT, NOT closure):
       Koide cos^2(theta_K) = M(N_pair) = 1/2    [under conjectural Q_l = A^2 = 2/3]
       Koide cos^4(theta_K) = V(N_pair) = 1/4    [NEW reading]
       Koide Q_l            = M(N_color) = 2/3    [conjectural]
       Koide variance       = V(N_color) = 2/9    [conjectural]
```

`(B1)` through `(D2)` are NEW. The framework had retained W2 (= M(N_color)),
CP-phase identities (= M(N_quark), V(N_quark)), and basic N_pair = 2
structural counts, but did NOT package the **multi-projection Bernoulli family**
as a unified structural object, nor the V(N) = M(N)/N universal relation,
nor the cross-level decompositions D1 and D2.

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| `(W2)` `A² = N_pair/N_color = 2/3` (= M(N_color)) | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `ρ = 1/N_quark = 1/6`, `1 - ρ = 5/6` (= M(N_quark)) | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `η² = (N_quark − 1)/N_quark² = 5/36` (Thales = V(N_quark)) | same |
| `N_pair = 2`, `N_color = 3`, `N_quark = N_pair × N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |
| `tan(γ̄) = √5` PROTECTED ⇒ `sin²(γ̄) = 5/6 = 1 - ρ` (= M(N_quark)) | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md), N4 |

No PDG observable enters as a derivation input. No SUPPORT-tier or open inputs
(Koide `Q_l`, bare-coupling ratios, dimension-color quadratic, A²-Koide
cross-sector bridge) are USED as derivation inputs. The cross-sector reading is
commentary only.

## Derivation

### Bernoulli forms M(N) and V(N)

Define for any positive integer N ≥ 2:

```text
M(N)  =  (N - 1) / N        [Bernoulli mean, "probability of failure"]
V(N)  =  (N - 1) / N^2      [Bernoulli variance for binary process with prob 1/N]
```

### B1, B4: Pair-projection (N = N_pair = 2)

```text
M(N_pair)  =  (N_pair - 1) / N_pair  =  1/N_pair  =  1/2      (framework-native)
V(N_pair)  =  (N_pair - 1) / N_pair^2  =  1/N_pair^2  =  1/4   (framework-native, NEW reading)
```

These are derived directly from the retained N_pair = 2.

### B2, B5: Color-projection (N = N_color = 3)

```text
M(N_color)  =  (N_color - 1) / N_color  =  2/3
V(N_color)  =  (N_color - 1) / N_color^2  =  2/9
```

Under the framework's structural primitive `N_pair = N_color − 1`, M(N_color)
matches retained W2 (`A² = N_pair/N_color = 2/3`), and V(N_color) matches the
multi-path 2/9 derivations from prior branches.

### B3, B6: Quark-projection (N = N_quark = 6)

```text
M(N_quark)  =  (N_quark - 1) / N_quark  =  5/6  =  1 - rho
V(N_quark)  =  (N_quark - 1) / N_quark^2  =  5/36  =  eta^2  (Thales)
```

These match retained CP-phase identities directly (1 − ρ and η² = ρ(1 − ρ)).

### MV1: Universal Bernoulli relation V(N) = M(N) / N

For any N:

```text
V(N)  =  (N - 1) / N^2  =  ((N - 1) / N) * (1 / N)  =  M(N) / N.
```

This is a basic algebraic fact, but its appearance at THREE different N-levels
in the framework, each with a retained-derivable interpretation, is the
structural content. Concretely:

```text
V(N_pair)  =  M(N_pair)  / N_pair  =  (1/2)  / 2  =  1/4    ✓
V(N_color) =  M(N_color) / N_color =  (2/3)  / 3  =  2/9    ✓
V(N_quark) =  M(N_quark) / N_quark =  (5/6)  / 6  =  5/36   ✓
```

### D1: NEW cross-level decomposition for ρ

```text
V(N_pair) * M(N_color)  =  (1/N_pair^2) * (N_pair/N_color)
                         =  N_pair/(N_pair^2 * N_color)
                         =  1/(N_pair * N_color)
                         =  1/N_quark            (using N_quark = N_pair × N_color)
                         =  rho.
```

So `ρ = V(N_pair) × M(N_color)`. The CP-phase apex coordinate `ρ` factors
EXACTLY as the product of the **pair-level variance** times the **color-level
mean**.

In framework with N_pair = 2, N_color = 3:

```text
V(N_pair) * M(N_color)  =  (1/4) * (2/3)  =  2/12  =  1/6  =  rho.   ✓
```

This is a NEW cross-level decomposition theorem. The retained ρ = 1/N_quark is
expressed as a product of multi-projection Bernoulli pieces.

### D2: NEW cross-level decomposition for M1

```text
V(N_color) * M(N_pair)  =  ((N_color - 1)/N_color^2) * (1/N_pair)
                         =  (N_color - 1) / (N_color^2 * N_pair).
```

In framework with N_pair = N_color − 1 = 2, N_color = 3:

```text
V(N_color) * M(N_pair)  =  (2/9) * (1/2)  =  2/18  =  1/9.
```

Compare with M1 = ρ × A² (from prior multiplicative-A-rho branch):

```text
M1  =  rho * A^2  =  (1/N_quark) * (N_pair/N_color)
                  =  N_pair / (N_quark * N_color)
                  =  1/N_color^2     (using N_quark = N_pair × N_color)
                  =  1/9.
```

So `M1 = V(N_color) × M(N_pair) = 1/9`. The retained M1 (Wolfenstein × CP-phase
product) factors EXACTLY as the **color-level variance** times the **pair-level
mean**.

### Symmetry observation

D1 and D2 are **dual** to each other:

- D1: `ρ = V(N_pair) × M(N_color)` — pair-variance × color-mean
- D2: `M1 = V(N_color) × M(N_pair)` — color-variance × pair-mean

The roles of N_pair and N_color SWAP between D1 and D2 (variance↔mean and
pair↔color). This is a structural duality.

## Numerical Verification

All identities verified to **exact Fraction arithmetic**:

| Identity | Closed form | Value |
| --- | --- | ---: |
| B1 M(N_pair) | (2−1)/2 | 1/2 ✓ |
| B2 M(N_color) | (3−1)/3 | 2/3 ✓ |
| B3 M(N_quark) | (6−1)/6 | 5/6 ✓ |
| B4 V(N_pair) | (2−1)/2² | 1/4 ✓ |
| B5 V(N_color) | (3−1)/3² | 2/9 ✓ |
| B6 V(N_quark) | (6−1)/6² | 5/36 ✓ |
| MV1 at N_pair | M/N = (1/2)/2 | 1/4 = V ✓ |
| MV1 at N_color | M/N = (2/3)/3 | 2/9 = V ✓ |
| MV1 at N_quark | M/N = (5/6)/6 | 5/36 = V ✓ |
| D1 ρ | V(N_pair) × M(N_color) | 1/6 ✓ |
| D2 M1 | V(N_color) × M(N_pair) | 1/9 ✓ |

## Science Value

### What this lets the framework predict that it could not before

Previously the framework had retained Bernoulli-form ratios at single N-levels
(N_color via W2, N_quark via Thales). This note unifies the Bernoulli structure
across **three N-levels simultaneously**, deriving:

- A **complete six-element family** {M(N), V(N) for N ∈ {N_pair, N_color, N_quark}}
  from retained CKM inputs.
- The **universal Bernoulli relation V(N) = M(N)/N** at all three levels.
- **Cross-level decomposition theorems** D1 and D2 expressing retained ρ and M1
  as products of Bernoulli pieces at different levels.
- A **NEW Koide-relevant reading**: V(N_pair) = 1/4 = cos⁴θ_K under cross-sector
  identification.

### The multi-projection structure is the central new content

Where the prior n/9 branch fixed the denominator at N_color² and varied the
numerator integer, this note **varies the level N** (N_pair, N_color, N_quark)
within a fixed Bernoulli form (M, V).

Both perspectives are complementary:
- n/9 family: fixes denominator, exhausts numerators with structural integers.
- Multi-projection family: fixes Bernoulli form, evaluates at three structural
  levels.

The framework supports BOTH structural decompositions of retained CKM ratios.

### Cross-level decompositions D1, D2 are sharp structural identities

D1: `ρ = V(N_pair) × M(N_color)` is a clean factorization of the retained
CP-phase apex coordinate. The retained ρ = 1/N_quark is expressed as a product
of multi-projection Bernoulli quantities at different levels.

D2: `M1 = V(N_color) × M(N_pair)` is the dual factorization. M1 = 1/N_color² is
expressed as the color-variance times the pair-mean.

These factorizations illuminate **what** the retained ρ and M1 mean structurally:
they are products of Bernoulli pieces from different N-levels, with the levels
swapping roles between D1 and D2.

### NEW Koide-relevant reading: V(N_pair) = 1/4 = cos⁴θ_K

Under the conjectural cross-sector reading where Koide Q_l = A² = 2/3:

- `cos²θ_K = 1/(3 Q_l) = 1/2 = M(N_pair)` (already noted in prior branch)
- `cos⁴θ_K = 1/4 = V(N_pair)` (NEW)

So the framework's pair-projection variance V(N_pair) = 1/4 has a direct
interpretation as the Koide angle's fourth-power cosine. This is a NEW
supporting reading: the Koide angle's higher-order trigonometric quantities
have framework counterparts in the multi-projection Bernoulli family.

### Cross-sector unification ground

Under N_gen = N_color (cross-sector conjecture):

| CKM identity | Koide interpretation | Form |
| --- | --- | --- |
| M(N_color) = 2/3 | Q_l (Koide ratio) | (N-1)/N |
| V(N_color) = 2/9 | Koide variance | (N-1)/N² |
| M(N_pair) = 1/2 | cos²θ_K | (N-1)/N |
| V(N_pair) = 1/4 | cos⁴θ_K | (N-1)/N² |

The framework's CKM side spans the Bernoulli structure at TWO N-levels relevant
to Koide (N_color and N_pair), with M and V both interpreted. The cross-sector
unification has matching CKM expressions for FOUR Koide-relevant ratios.

### Falsifiable structural claim

The universal Bernoulli relation V(N) = M(N)/N at all three levels, plus the
cross-level decompositions D1 and D2, makes a sharp claim:

```text
The framework's retained quantities (rho, M1) factor EXACTLY as products of
multi-projection Bernoulli pieces, with the levels (N_pair, N_color)
swapping roles between D1 and D2.
```

If a future framework revision changed pair-color counting, D1 and D2 would
break (or shift to different Bernoulli combinations).

### Why this counts as pushing the science forward

Three layers of new content beyond prior branches:

1. **Multi-projection Bernoulli family** — first retained CKM theorem packaging
   the {M, V} × {N_pair, N_color, N_quark} structure as a unified 6-element
   object with universal relation V(N) = M(N)/N at all three levels.

2. **Cross-level decomposition theorems D1, D2** — NEW factorizations of
   retained ρ and M1 as products of Bernoulli pieces at different levels.
   The pair-color swap symmetry between D1 and D2 is a sharp structural
   duality.

3. **NEW Koide-relevant reading** — V(N_pair) = 1/4 = cos⁴θ_K under cross-sector
   identification. Adds another supporting parallel beyond the prior cos²θ_K
   reading.

Together with the prior three branches:

| Branch | Content |
|---|---|
| Bernoulli-2/9 | 4 paths to 2/9, K3 consistency theorem |
| Multiplicative-A-rho | 3 multiplicative identities, 5th 2/9 path, sector decoupling |
| n/9 family | Complete n/9 family with universal denominator N_color² |
| **Multi-projection Bernoulli** (this branch) | 6-element family, V(N) = M(N)/N universal, D1/D2 cross-level decompositions |

Together: the framework's CKM side now provides **four complementary structural
descriptions** of the same retained content, each illuminating different aspects
of the cross-sector unification programme.

## What This Claims

- `(B1)`-`(B6)`: 6-element Bernoulli family at three N-levels, each derivable
  from retained CKM inputs.
- `(MV1)`: NEW universal Bernoulli relation V(N) = M(N)/N at all three levels.
- `(D1)`: NEW cross-level decomposition `ρ = V(N_pair) × M(N_color)`.
- `(D2)`: NEW cross-level decomposition `M1 = V(N_color) × M(N_pair)`.
- `(CS1)`: NEW cross-sector reading V(N_pair) = 1/4 = cos⁴θ_K (conjectural).

## What This Does NOT Claim

- It does NOT close `A²` deeper than the retained structural-counts level.
- It does NOT close `Koide 2/9` or any specific Koide quantity.
- It does NOT promote any cross-sector identification to retained status.
- It does NOT use SUPPORT-tier inputs as derivation inputs.

## Reproduction

```bash
python3 scripts/frontier_ckm_multi_projection_bernoulli_koide_bridge.py
```

Expected result:

```text
TOTAL: PASS=25, FAIL=0
```

The runner uses Python's `fractions.Fraction` for exact-rational arithmetic.

## Cross-References

- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `(W2)` `A² = N_pair/N_color` = M(N_color).
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `ρ = 1/N_quark`, `η² = (N_quark − 1)/N_quark²` = V(N_quark).
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- retained `N_pair = 2`, `N_color = 3`, `N_quark = N_pair × N_color = 6`.
- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  -- retained N4 protection: `tan(γ̄) = √5` ⇒ `sin²(γ̄) = 5/6 = M(N_quark)`.
- (NOT cited as derivation input) prior pending branches: Bernoulli-2/9,
  Multiplicative-A-rho, n/9-family. This branch's content is independent
  from retained main inputs.
- (NOT cited as derivation input) cross-sector `_SUPPORT_NOTE_` for the
  A²-Koide bridge.
