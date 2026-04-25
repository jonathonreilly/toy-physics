# Bernoulli-Variance 2/9 Identities in CKM: Support for the Cross-Sector Koide Bridge

**Date:** 2026-04-25

**Status:** exact CKM-structure support corollary on retained main inputs,
plus explicit cross-sector SUPPORT commentary. The CKM section derives the
rational identity `2/9` through four algebraically distinct CKM readouts using
only retained inputs from `main`. The support section reads these CKM identities
as structural parallels to the conjectural Koide variance ratio
`(N_gen - 1)/N_gen² = 2/9`, supporting (without closing) the cross-sector
unification programme.

This note is **not a closure of A² (already retained as W2)** and **not a closure of
Koide 2/9 (lepton-sector, conditional on cross-sector bridge)**. It pushes the
*supporting* structure: it shows that `2/9` is **multiply-determined** in the CKM
sector from retained inputs, with consistency conditions tied directly to the
retained integer counts `(N_pair, N_color) = (2, 3)`.

The headline framework-native identities, all from retained inputs:

```text
(K1)   A^2 * (1 - A^2)             =  2/9   [Bernoulli variance of Wolfenstein A^2]

(K2)   2 * rho * A^2                =  2/9   [apex coupling × pair-prob × 2]

(K5)   A^2 / N_color                =  2/9   [Wolfenstein A^2 normalized by colors]

(K6)   (1/N_color)(1 - 1/N_color)  =  2/9   [color-projected Bernoulli]
```

All four equal `2/9 = N_pair / N_color² = (N_color − 1)/N_color²` exactly after
substituting the retained framework counts `N_pair = 2`, `N_color = 3`.

**Consistency Corollary (NEW K3):**

```text
For positive integer pair/color counts:

K1 = K2 = K5 = K6 = 2/9   <==>   N_pair = 2 AND N_color = 3.
```

The convergence of all four CKM readouts to the same value `2/9` is therefore
equivalent to the framework's retained pair-color counts. This converts the
seemingly arbitrary numerical coincidence `2/9` into a **structural consistency
test** of the framework's integer bookkeeping.

**Cross-sector reading (SUPPORT, conditional):**

If the Koide variance ratio is structurally `(N_gen − 1)/N_gen² = 2/9` with
`N_gen = 3 = N_color`, then the framework's CKM identity `K6` and the lepton-
sector Koide variance share the same structural form `(N − 1)/N²` with
`N = N_color = N_gen = 3`. Promotion of the cross-sector identification
`N_color = N_gen` to retained status would still require a separate theorem;
this note supplies only the CKM-side exact algebra.

**Primary runner:**
`scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py`

## Statement

On the retained CKM atlas + Wolfenstein structural surface (where `(W2)`
`A² = N_pair/N_color`, `ρ = 1/N_quark`, and `N_quark = N_pair × N_color` hold
from the magnitudes counts theorem):

```text
(K1)  A^2 * (1 - A^2)  =  N_pair * (N_color - N_pair) / N_color^2     [EXACT, from W2]

      In framework where N_pair = N_color - 1 = 2, this collapses to:
      A^2 * (1 - A^2)  =  (N_color - 1) / N_color^2  =  2/9.

(K2)  2 * rho * A^2  =  2 * (1/N_quark) * (N_pair/N_color)
                     =  2 * N_pair / (N_quark * N_color)
                     =  2 * N_pair / (N_pair * N_color^2)        [N_quark = N_pair × N_color]
                     =  2 / N_color^2
                     =  2/9        [EXACT, from W2 and CP-phase rho identity]

(K3)  CONSISTENCY over positive integer pair/color counts:
      K1 = K2 = K5 = K6 = 2/9
      <==>  N_pair = 2 AND N_color = 3.

      The four-fold convergence of CKM-native 2/9 readouts is therefore
      equivalent to the retained framework pair-color counts.

(K5)  A^2 / N_color  =  N_pair / N_color^2  =  2/9                    [EXACT]

(K6)  rho_color * (1 - rho_color)
        where rho_color = 1/N_color
        =  (N_color - 1) / N_color^2
        =  2/9                                                         [EXACT, color-projected Bernoulli]
```

The numerical relation `N_pair = N_color − 1` follows from the retained counts
`N_pair = 2`, `N_color = 3` in the framework's CKM magnitudes structural counts
theorem. This note does not introduce it as an additional axiom.

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| `(W2)` `A² = N_pair/N_color = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `ρ = 1/6 = 1/N_quark`, `η² = 5/36 = (N_quark − 1)/N_quark²` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `N_quark = N_pair × N_color = 6`, `N_pair = 2`, `N_color = 3` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |
| Numerical relation `N_pair = N_color − 1` | direct consequence of retained N_pair = 2, N_color = 3 (same authority) |

No PDG observable enters as a derivation input. No SUPPORT-tier or open
inputs (Koide `Q_l`, bare-coupling ratios, dimension-color quadratic, A²-
Koide cross-sector bridge) are USED as inputs to the K1, K2, K3, K5, K6
derivations. The cross-sector READING in the support commentary is clearly
labeled.

## Derivation

### K1: Bernoulli variance of A²

From retained `(W2)`:

```text
A^2  =  N_pair / N_color.
1 - A^2  =  (N_color - N_pair) / N_color.
A^2 (1 - A^2)  =  N_pair (N_color - N_pair) / N_color^2.
```

In the framework where N_pair = N_color − 1 = 2:

```text
A^2 (1 - A^2)  =  (N_color - 1) * 1 / N_color^2  =  (N_color - 1) / N_color^2
              =  2/9.
```

This is the Bernoulli variance of a binary process with success probability A² —
"variance of the Wolfenstein A² parameter as a probability". Its specific value
`2/9` is fully determined by the structural integers N_pair, N_color.

### K2: apex coupling identity

From retained CP-phase: `ρ = 1/N_quark = 1/6`. From retained `(W2)`:
`A² = N_pair/N_color = 2/3`. Then

```text
2 * rho * A^2  =  2 * (1/N_quark) * (N_pair/N_color)
              =  2 * N_pair / (N_quark * N_color)
              =  2 * N_pair / (N_pair * N_color * N_color)        [using N_quark = N_pair * N_color]
              =  2 / N_color^2.
```

In the framework with N_color = 3:

```text
2 * rho * A^2  =  2 / 9.
```

### K3: consistency identity (NEW structural test)

Let `p = N_pair` and `c = N_color` be positive integers. The four readouts are:

```text
K1 = p(c - p)/c²
K2 = 2/c²
K5 = p/c²
K6 = (c - 1)/c².
```

If all four readouts equal `2/9`, then in particular `K6 = 2/9`:

```text
(c - 1)/c² = 2/9
=> 2c² - 9c + 9 = 0
=> c = 3 or c = 3/2.
```

Since `c` is a positive integer, `c = 3`. Then `K5 = 2/9` gives
`p/c² = 2/9`, hence `p = 2`. Conversely, `p = 2`, `c = 3` immediately gives
`K1 = K2 = K5 = K6 = 2/9`.

Thus, over positive integer pair/color counts:

```text
K1 = K2 = K5 = K6 = 2/9   <==>   N_pair = 2 AND N_color = 3.
```

The framework satisfies the right-hand side by retained CKM count authority.
The convergence is therefore a **consistency test** of the retained integer
structure, not an additional closure primitive.

### K5: A² normalized by N_color

```text
A^2 / N_color  =  (N_pair / N_color) / N_color  =  N_pair / N_color^2.
```

With N_pair = 2 and N_color = 3:

```text
A^2 / N_color  =  2 / 9.
```

### K6: color-projected Bernoulli variance

Define `ρ_color = 1/N_color = 1/3`. Then

```text
rho_color (1 - rho_color)  =  (1/N_color) * ((N_color - 1)/N_color)
                            =  (N_color - 1) / N_color^2
                            =  2 / 9   for N_color = 3.
```

This is the Bernoulli variance of a uniform process with N_color outcomes
(probability 1/N_color per outcome), restricted to "one specific outcome" vs
"any other". The CKM CP-phase structural identity `η² = (N_quark − 1)/N_quark²`
has the same functional form `(N − 1)/N²` but with `N = N_quark = 6` instead of
`N = N_color = 3`. Replacing `N_quark → N_color` in the CP-phase variance gives
exactly K6.

### Convergence

All four readouts (K1, K2, K5, K6) yield `2/9` exactly under the retained
framework inputs, with K3 articulating that this convergence is equivalent to
the retained pair-color counts `(N_pair, N_color) = (2, 3)`.

## Numerical Verification

All identities verified to **exact Fraction arithmetic** (no floating-point):

| Path | Closed-form expression | Value |
| --- | --- | ---: |
| K1 | `A² (1 - A²)` from `A² = 2/3` | `2/3 × 1/3 = 2/9` ✓ |
| K2 | `2 ρ A² = 2 × 1/6 × 2/3` | `2/9` ✓ |
| K5 | `A² / N_color = (2/3) / 3` | `2/9` ✓ |
| K6 | `(1/N_color)(1 - 1/N_color) = 1/3 × 2/3` | `2/9` ✓ |

All four readouts produce the **identical Fraction** `2/9` when computed via Python's
exact-rational `fractions.Fraction` arithmetic.

## Science Value

### What this lets the framework predict that it could not before

This note records **four algebraically distinct CKM-native readouts of `2/9`**,
all derived from retained CKM inputs only:

1. K1 Bernoulli variance of `A²`.
2. K2 apex coupling `2ρA²`.
3. K5 normalized `A²/N_color`.
4. K6 color-projected Bernoulli variance.

The convergence of all four readouts to `2/9` is structurally non-trivial:
by K3, over positive integer pair/color counts it is equivalent to
`(N_pair, N_color) = (2, 3)`. Alternative structural counts would generally
break at least one of the four readouts.

### The K3 consistency identity is the structural anchor

```text
K1 = K2 = K5 = K6 = 2/9   <==>   N_pair = 2 AND N_color = 3.
```

The retained framework satisfies this because both `N_pair = 2` and `N_color = 3`
are explicitly retained in the magnitudes counts theorem, and `N_pair = N_color − 1`
follows by direct numerical identity. K3 articulates the converse: any CKM
framework where K1, K2, K5, K6 all give `2/9` MUST have `(N_pair, N_color) = (2, 3)`.

This converts the CKM-side appearance of `2/9` from a coincidence into a
structural consistency consequence of the retained pair-color counts.

### Cross-sector reading (SUPPORT, not retained closure)

The conjectural Koide variance ratio `(N_gen − 1)/N_gen² = 2/9` with
`N_gen = 3` has the **identical structural form** as K6's color-Bernoulli
readout `(N_color − 1)/N_color² = 2/9` with `N_color = 3`. Under the cross-sector
identification `N_gen = N_color = 3` (which is in the framework only as
support context), the Koide variance ratio has the same closed form as the CKM
color-projected Bernoulli readout K6.

This does not by itself close Koide 2/9. It only says that once a separate
retained theorem identifies `N_gen = N_color`, the CKM-side Bernoulli algebra
needed for the shared `(N - 1)/N²` value is already exact.

### What this does NOT close

- **A² is already retained at structural-counts level (W2)**. This note does
  NOT provide a deeper derivation of A² from below the structural counts
  (e.g., from CL3 lattice/algebraic foundations). Closing A² "deeper than
  W2" remains an open problem in the framework.
- **Koide 2/9 is not closed by this note alone**. The cross-sector
  identification `N_gen = N_color` is a structural conjecture, currently a
  `_SUPPORT_NOTE_`. Promoting it to retained closure requires a separate
  derivation of the lepton-sector counting `N_gen = 3` from CL3 first
  principles, OR an explicit algebraic identification of `N_gen` with
  `N_color` in the lepton mixing / Koide mass structure.
- This note does NOT use the existing `CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md` as INPUT; the K1-K6 derivations stand on retained
  CKM inputs alone. The cross-sector reading is **commentary**, not derivation.

### Falsifiable structural claim

The K3 consistency identity is a sharp claim:

```text
The framework's positive integer pair/color counts MUST satisfy
N_pair = 2 and N_color = 3 in order for K1 through K6 to all equal 2/9.
```

If a future framework revision modified the pair-color counting (e.g.,
`N_pair = 3` or `N_color = 4`), one or more of K1-K6 would no longer give
`2/9`, breaking the convergence. The CKM-side claim that K1-K6 all give
`2/9` is therefore equivalent to the retained pair-color count
`(N_pair, N_color) = (2, 3)`.

### Why this counts as pushing the science forward

Three layers of new content beyond retained `(W2)`:

1. **Four algebraically distinct CKM-native readouts of 2/9** (K1, K2,
   K5, K6) from retained inputs alone.

2. **Structural consistency corollary K3** linking the four-fold convergence
   to the retained pair-color counts `(N_pair, N_color) = (2, 3)`.

3. **Explicit cross-sector reading** (clearly labeled as SUPPORT, not
   closure): the K6 color-Bernoulli form `(N_color − 1)/N_color²` is identical to the
   conjectured Koide variance `(N_gen − 1)/N_gen²` with `N_gen = N_color`;
   this isolates, but does not close, the cross-sector identification.

This **pushes the supporting science forward**: it doesn't close A² or Koide
2/9, but it exhibits `2/9` as a CKM-native multiply-determined structural
constant, and articulates exactly what additional input (cross-sector
N_gen = N_color identification) would be needed for Koide 2/9 closure.

## What This Claims

- `(K1)`: NEW algebraic identity `A² (1 − A²) = N_pair (N_color − N_pair)/N_color²
  = 2/9` in CKM, EXACT from retained `(W2)`.
- `(K2)`: NEW algebraic identity `2ρA² = 2/N_color² = 2/9` in CKM, EXACT from
  retained `(W2)` and `ρ = 1/N_quark`.
- `(K3)`: NEW structural consistency identity over positive integer pair/color
  counts: K1 = K2 = K5 = K6 = 2/9 ⟺ `N_pair = 2` AND `N_color = 3`.
- `(K5)`: NEW algebraic identity `A²/N_color = N_pair/N_color² = 2/9` in CKM,
  EXACT from retained `(W2)`.
- `(K6)`: NEW algebraic identity `(1/N_color)(1 − 1/N_color) = (N_color − 1)/N_color²
  = 2/9` from retained `N_color = 3`.

## What This Does NOT Claim

- It does NOT close `A²` deeper than the retained structural-counts level
  (W2 still required).
- It does NOT close `Koide 2/9`. The cross-sector reading is explicitly
  conditional on the `N_gen = N_color` identification (a `_SUPPORT_NOTE_`,
  not retained closure).
- It does NOT use the existing cross-sector `_SUPPORT_NOTE_` as derivation
  input. K1-K6 stand on retained CKM inputs alone.
- It does NOT promote the cross-sector A²-Koide bridge to retained status.
- It does NOT prove or use a retained `N_gen = N_color` theorem.
- It does NOT modify any retained CKM atlas, Wolfenstein, CP-phase, NLO-
  protected-γ̄, magnitudes structural counts, or Brannen-Koide CH-three-gap
  theorem.

## Reproduction

```bash
python3 scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py
```

Expected result:

```text
TOTAL: PASS=31, FAIL=0
```

The runner uses Python's `fractions.Fraction` for exact-rational arithmetic
(no floating-point comparisons). All upstream authorities are retained on
`main`.

## Cross-References

- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `(W2)` `A² = N_pair/N_color` used in K1, K2, K5.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `ρ = 1/N_quark` used in K2; retained `η² = (N_quark − 1)/N_quark²`
  noted as having the SAME functional form as K6 but with N=N_quark instead
  of N=N_color.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- retained `N_pair = 2`, `N_color = 3`, `N_quark = N_pair × N_color = 6`,
  with `N_pair = N_color − 1` as a direct numerical consequence of those counts.
- (NOT cited as derivation input) the `_SUPPORT_NOTE_` for the cross-sector
  A²-Koide bridge, which is the conditional path to Koide 2/9 closure that
  this note articulates but does not close.
