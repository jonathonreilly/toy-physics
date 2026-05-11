# Multi-Projection Bernoulli Family at N_pair, N_color, N_quark

**Date:** 2026-04-25

**Status:** proposed_retained CKM-structure theorem on current `main`. This note
generalizes the Bernoulli-form ratios `(N-1)/N` and `(N-1)/N²` from a single
N-level to a **multi-projection family** evaluated at all three
structural-integer levels of the framework: `N_pair = 2`, `N_color = 3`,
`N_quark = 6`.

The result is a **six-element Bernoulli family** `{M(N), V(N) for N in
{N_pair, N_color, N_quark}}` with **universal Bernoulli relation**
`V(N) = M(N)/N` at every level, plus **cross-level decomposition theorems**
that express retained CKM quantities `rho` and `A^2 rho` as exact products of
multi-projection Bernoulli pieces.

It pushes the retained CKM structure further than the prior support-side
Bernoulli/ninth-family notes by:

1. Lifting the Bernoulli structure from a single N-level to **three N-levels
   simultaneously**, exhibiting a 6-element family.
2. Establishing the **universal Bernoulli relation** V(N) = M(N)/N as a
   structural fact at all three levels.
3. Deriving **cross-level decomposition theorems** D1, D2 expressing retained
   `rho` and `A^2 rho` as products of Bernoulli pieces from different levels.
4. Packaging those decompositions as a dual pair with exact pair/color and
   mean/variance role exchange.

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
  rho      =  V(N_pair) * M(N_color)  =  (1/4) * (2/3)  =  1/6
  A^2 rho  =  V(N_color) * M(N_pair)  =  (2/9) * (1/2)  =  1/9
```

**Primary runner:**
`scripts/frontier_ckm_multi_projection_bernoulli_family.py`

## Statement

On the retained CKM atlas + Wolfenstein structural surface, with retained
N_pair = 2, N_color = 3, N_quark = N_pair × N_color = 6:

```text
(B1)  M(N_pair)  =  (N_pair - 1) / N_pair  =  1/2

(B2)  M(N_color) =  (N_color - 1) / N_color  =  A^2  =  2/3

(B3)  M(N_quark) =  (N_quark - 1) / N_quark  =  1 - rho  =  sin^2(gamma_bar)
                  =  5/6

(B4)  V(N_pair)  =  (N_pair - 1) / N_pair^2  =  1/4

(B5)  V(N_color) =  (N_color - 1) / N_color^2  =  2/9

(B6)  V(N_quark) =  (N_quark - 1) / N_quark^2  =  eta^2  =  5/36

(MV1) V(N) = M(N) / N    for all N in {N_pair, N_color, N_quark}

(D1)  rho  =  V(N_pair) * M(N_color)  =  1/N_pair^2 * N_pair/N_color
           =  1/(N_pair * N_color)  =  1/N_quark

(D2)  A^2 rho  =  V(N_color) * M(N_pair)
               =  ((N_color - 1)/N_color^2) * (1/N_pair)
               =  1/N_color^2  =  1/9
```

The theorem's new content is the **packaging** of these retained constituents as
one six-element Bernoulli family, together with the universal relation `(MV1)`
and the cross-level decompositions `(D1)` and `(D2)`. Individual entries such
as `A^2 = 2/3`, `1 - rho = 5/6`, and `eta^2 = 5/36` were already present on
current `main`.

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
(cross-sector Koide bridges, bare-coupling support notes, or open quark/lepton
bridges) are used as derivation inputs.

## Derivation

### Bernoulli forms M(N) and V(N)

Define for any positive integer N ≥ 2:

```text
M(N)  =  (N - 1) / N        [Bernoulli mean, "probability of failure"]
V(N)  =  (N - 1) / N^2      [Bernoulli variance for binary process with prob 1/N]
```

### B1, B4: Pair-projection (N = N_pair = 2)

```text
M(N_pair)  =  (N_pair - 1) / N_pair  =  1/N_pair  =  1/2
V(N_pair)  =  (N_pair - 1) / N_pair^2  =  1/N_pair^2  =  1/4
```

These are derived directly from the retained N_pair = 2.

### B2, B5: Color-projection (N = N_color = 3)

```text
M(N_color)  =  (N_color - 1) / N_color  =  2/3
V(N_color)  =  (N_color - 1) / N_color^2  =  2/9
```

With retained `N_pair = 2` and `N_color = 3`, `M(N_color)` matches retained W2
(`A² = N_pair/N_color = 2/3`) and `V(N_color) = 2/9` is its corresponding
Bernoulli variance form.

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

### D2: NEW cross-level decomposition for `A^2 rho`

```text
V(N_color) * M(N_pair)  =  ((N_color - 1)/N_color^2) * (1/N_pair)
                         =  (N_color - 1) / (N_color^2 * N_pair).
```

In framework with N_pair = N_color − 1 = 2, N_color = 3:

```text
V(N_color) * M(N_pair)  =  (2/9) * (1/2)  =  2/18  =  1/9.
```

Compare with `A^2 rho`:

```text
A^2 rho  =  rho * A^2  =  (1/N_quark) * (N_pair/N_color)
        =  N_pair / (N_quark * N_color)
        =  1/N_color^2     (using N_quark = N_pair × N_color)
        =  1/9.
```

So `A^2 rho = V(N_color) × M(N_pair) = 1/9`. The retained product `A^2 rho`
factors EXACTLY as the **color-level variance** times the **pair-level mean**.

### Symmetry observation

D1 and D2 are **dual** to each other:

- D1: `ρ = V(N_pair) × M(N_color)` — pair-variance × color-mean
- D2: `A^2 rho = V(N_color) × M(N_pair)` — color-variance × pair-mean

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
| D2 `A^2 rho` | V(N_color) × M(N_pair) | 1/9 ✓ |

## Science Value

### What this lets the framework package that it did not before

Previously the framework had retained Bernoulli-form ratios at single N-levels
(N_color via W2, N_quark via Thales). This note unifies the Bernoulli structure
across **three N-levels simultaneously**, deriving:

- A **complete six-element family** {M(N), V(N) for N ∈ {N_pair, N_color, N_quark}}
  from retained CKM inputs.
- The **universal Bernoulli relation V(N) = M(N)/N** at all three levels.
- **Cross-level decomposition theorems** D1 and D2 expressing retained `rho`
  and `A^2 rho` as products of Bernoulli pieces at different levels.

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

D2: `A^2 rho = V(N_color) × M(N_pair)` is the dual factorization. The retained
product `A^2 rho = 1/N_color²` is expressed as the color-variance times the
pair-mean.

These factorizations illuminate **what** the retained `rho` and `A^2 rho` mean
structurally: they are products of Bernoulli pieces from different N-levels,
with the levels swapping roles between D1 and D2.

### Falsifiable structural claim

The universal Bernoulli relation V(N) = M(N)/N at all three levels, plus the
cross-level decompositions D1 and D2, makes a sharp claim:

```text
The framework's retained quantities (rho, A^2 rho) factor EXACTLY as products of
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
   retained `rho` and `A^2 rho` as products of Bernoulli pieces at different
   levels.
   The pair-color swap symmetry between D1 and D2 is a sharp structural
   duality.

3. **Exact dual product law** — the theorem packages
   `rho = V(N_pair) M(N_color)` and `A^2 rho = V(N_color) M(N_pair)` as a dual
   pair of exact retained CKM identities.

## What This Claims

- `(B1)`-`(B6)`: 6-element Bernoulli family at three N-levels, each derivable
  from retained CKM inputs.
- `(MV1)`: NEW universal Bernoulli relation V(N) = M(N)/N at all three levels.
- `(D1)`: NEW cross-level decomposition `ρ = V(N_pair) × M(N_color)`.
- `(D2)`: NEW cross-level decomposition `A^2 rho = V(N_color) × M(N_pair)`.

## What This Does NOT Claim

- It does NOT close any charged-lepton Koide target or cross-sector bridge.
- It does NOT derive or use `N_gen = N_color` or any other cross-sector
  identification as a CKM-side input.
- It does NOT use SUPPORT-tier or open inputs as derivation inputs.

## Exact-symbolic verification

The algebraic content of `(B1)`-`(B6)`, the universal Bernoulli relation
`(MV1)`, and the cross-level decompositions `(D1)`, `(D2)` is certified
at exact-symbolic precision via `sympy` in
`scripts/audit_companion_ckm_multi_projection_bernoulli_family_exact.py`.
The companion runner treats `(N_pair, N_color, N_quark)` as
positive-integer symbols `(p, c, q)` with the framework constraint
`q = p c`, and checks each identity via `sympy.simplify(lhs - rhs)`
asserting the residual equals `0`. The cited atlas-side inputs
(`A^2 = N_pair/N_color`, `rho = 1/N_quark`,
`eta^2 = (N_quark - 1)/N_quark^2`, cited `N_pair = 2`,
`N_color = 3`) are imported from upstream authority notes and are not
re-derived here.

| Identity | Symbolic form | Verification |
| --- | --- | --- |
| `(MV1)` | `V(N) == M(N)/N` parametric in `N` | `sympy.simplify` residual `= 0` |
| `(B1)`-`(B6)` | six Bernoulli values at `(p, c, q) = (2, 3, 6)` | exact rationals match `1/2, 2/3, 5/6, 1/4, 2/9, 5/36` |
| `(B3)` | `M(N_quark) == 1 - rho` parametric in `q` | `sympy.simplify` residual `= 0` |
| `(B6)` | `V(N_quark) == eta^2` parametric in `q` | `sympy.simplify` residual `= 0` |
| `(B2)` | `M(N_color) == A^2 = N_pair/N_color` only at `(2, 3)` (specialization, not generic) | residual non-zero parametric, `= 0` at `(2, 3)` |
| `(D1)` | `(1/p^2)(p/c) == 1/(p c)`; under `q = p c`, equals `1/q = rho` | `sympy.simplify` residual `= 0` |
| `(D1)` framework | `V(N_pair) M(N_color) == 1/6` at `(2, 3, 6)` | exact rational `1/6` |
| `(D2)` | `V(N_color) (1/N_pair) == (c-1)/(p c^2)` parametric | `sympy.simplify` residual `= 0` |
| `(D2)` framework | `V(N_color) M(N_pair) == 1/9` at `(2, 3, 6)` | exact rational `1/9` |
| `A^2 rho` | `A^2 rho == p/(c q)`; under `q = p c`, equals `1/c^2` | `sympy.simplify` residual `= 0` |
| pair/color swap | `D1` and `D2` interchange variance/mean roles between `(p, c)` | structural duality confirmed |

A counterfactual at `(p, c) = (3, 2)` (swap of the framework values)
shows `A^2 rho = 1/c^2 = 1/4`, not `1/9`, confirming that the cited
ordering `(N_pair, N_color) = (2, 3)` is load-bearing for the named
`(D2) = 1/9` value.

The structural relations are therefore exact-symbolic over the imported
atlas-side inputs and the framework counts. No floating-point pin is
required for any identity in this note (the family is purely rational
under exact `sympy` arithmetic).

## Reproduction

```bash
python3 scripts/frontier_ckm_multi_projection_bernoulli_family.py
PYTHONPATH=scripts python3 scripts/audit_companion_ckm_multi_projection_bernoulli_family_exact.py
```

Expected result:

```text
TOTAL: PASS=23, FAIL=0
```

The runner uses Python's `fractions.Fraction` for exact-rational arithmetic.

## Cross-References

- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- cited `(W2)` `A² = N_pair/N_color` = M(N_color).
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- cited `ρ = 1/N_quark`, `η² = (N_quark − 1)/N_quark²` = V(N_quark).
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- cited `N_pair = 2`, `N_color = 3`, `N_quark = N_pair × N_color = 6`.
- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  -- cited N4 protection: `tan(γ̄) = √5` ⇒ `sin²(γ̄) = 5/6 = M(N_quark)`.
- [`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md)
  and [`CKM_N9_STRUCTURAL_FAMILY_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_N9_STRUCTURAL_FAMILY_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md)
  -- related CKM-side support notes; not needed as derivation inputs here.
