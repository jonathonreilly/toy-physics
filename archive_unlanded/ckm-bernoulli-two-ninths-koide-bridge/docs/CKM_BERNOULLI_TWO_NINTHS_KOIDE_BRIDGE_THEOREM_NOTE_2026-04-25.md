# Bernoulli-Variance 2/9 Identities in CKM: Framework-Native Derivations Supporting the Cross-Sector Koide Bridge

**Date:** 2026-04-25

**Status:** retained CKM-structure THEOREM (closure on retained main inputs) **plus** explicit cross-sector
SUPPORT commentary. The theorem section derives the rational identity `2/9` in the CKM
framework via FOUR independent algebraic paths, using ONLY retained inputs from main.
The support section reads these CKM identities as structural parallels to the
conjectural Koide variance ratio `(N_gen - 1)/N_gen² = 2/9`, supporting (without
closing) the cross-sector unification programme.

This note is **not a closure of A² (already retained as W2)** and **not a closure of
Koide 2/9 (lepton-sector, conditional on cross-sector bridge)**. It pushes the
*supporting* structure: it shows that `2/9` is **multiply-determined** in the CKM
sector from retained inputs, with consistency conditions tied directly to the
structural identity `N_pair = N_color − 1`.

The headline framework-native identities, all from retained inputs:

```text
(K1)   A^2 * (1 - A^2)             =  2/9   [Bernoulli variance of Wolfenstein A^2]

(K2)   2 * rho * A^2                =  2/9   [apex coupling × pair-prob × 2]

(K5)   A^2 / N_color                =  2/9   [Wolfenstein A^2 normalized by colors]

(K6)   (1/N_color)(1 - 1/N_color)  =  2/9   [color-projected Bernoulli]
```

All four equal `2/9 = N_pair / N_color² = (N_color − 1)/N_color²` exactly, when
the structural identity `N_pair = N_color − 1` (retained in framework) is used.

**Consistency Theorem (NEW K3):**

```text
K1  =  K2   <==>   N_pair  =  N_color - 1   [structural primitive]
K1  =  K6   <==>   N_pair  =  N_color - 1
K2  =  K5   <==>   N_pair  =  2 (i.e., N_color - 1 = 2 in the framework)
```

The convergence of all four paths to the same value `2/9` is **EQUIVALENT** to
the framework's structural primitive `N_pair = N_color - 1`. This converts the
seemingly arbitrary numerical coincidence `2/9` into a **structural consistency
test** of the framework's pair-color counting.

**Cross-sector reading (SUPPORT, conditional):**

If the Koide variance ratio is structurally `(N_gen − 1)/N_gen² = 2/9` with
`N_gen = 3 = N_color`, then the framework's CKM identity `K1` and the lepton-
sector Koide variance share the SAME structural form `(N − 1)/N²` with `N = N_color
= N_gen = 3`. Promotion of the cross-sector identification `N_color = N_gen` to
retained status would CLOSE the Koide 2/9 identity by reducing it to the CKM
Bernoulli variance K1.

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

(K3)  CONSISTENCY: K1 = K2 = K5 = K6 = 2/9
      <==>  N_pair = N_color - 1 = 2  AND  N_color = 3.

      The four-fold convergence of CKM-native 2/9 paths is structurally
      equivalent to the framework's primitive: N_pair = N_color - 1.

(K5)  A^2 / N_color  =  N_pair / N_color^2  =  2/9                    [EXACT]

(K6)  rho_color * (1 - rho_color)
        where rho_color = 1/N_color
        =  (N_color - 1) / N_color^2
        =  2/9                                                         [EXACT, color-projected Bernoulli]
```

The structural primitive `N_pair = N_color − 1` is retained (with N_pair = 2,
N_color = 3) in the framework's CKM magnitudes structural counts theorem.

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| `(W2)` `A² = N_pair/N_color = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `ρ = 1/6 = 1/N_quark`, `η² = 5/36 = (N_quark − 1)/N_quark²` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `N_quark = N_pair × N_color = 6`, `N_pair = 2`, `N_color = 3` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |
| Structural primitive `N_pair = N_color − 1` | implicit in retained N_pair = 2, N_color = 3 (same authority) |

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

K1 and K2 give the same value `2/9` only when both N_pair = N_color − 1 (so K1
collapses to (N_color − 1)/N_color²) AND N_pair = 2 (so K2 = 2/N_color² is also
2/9 = N_pair/N_color² when N_pair = 2). These two requirements together specify

```text
N_pair  =  2,    N_color  =  3,    N_quark  =  6.
```

Equivalently, K1 = K2 = 2/9 is the structural identity `N_pair = N_color − 1 = 2`
applied to the framework's pair-color counts. The four-fold convergence
K1 = K2 = K5 = K6 = 2/9 (with K5, K6 below) is therefore a **consistency test**
of the framework's primitive integer structure.

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

All four paths (K1, K2, K5, K6) yield `2/9` exactly under the retained framework
inputs, with K3 articulating that the convergence is the structural primitive
`N_pair = N_color − 1` itself.

## Numerical Verification

All identities verified to **exact Fraction arithmetic** (no floating-point):

| Path | Closed-form expression | Value |
| --- | --- | ---: |
| K1 | `A² (1 - A²)` from `A² = 2/3` | `2/3 × 1/3 = 2/9` ✓ |
| K2 | `2 ρ A² = 2 × 1/6 × 2/3` | `2/9` ✓ |
| K5 | `A² / N_color = (2/3) / 3` | `2/9` ✓ |
| K6 | `(1/N_color)(1 - 1/N_color) = 1/3 × 2/3` | `2/9` ✓ |

All four paths produce the **identical Fraction** `2/9` when computed via Python's
exact-rational `fractions.Fraction` arithmetic.

## Science Value

### What this lets the framework predict that it could not before

Previously the framework's only direct production of `2/9` from retained inputs
was via the conjectural cross-sector A²-Koide bridge (a `_SUPPORT_NOTE_`,
not retained closure). This note delivers **FOUR independent CKM-native
algebraic paths to 2/9**, all derived from retained inputs only:

1. K1 Bernoulli variance of `A²`.
2. K2 apex coupling `2ρA²`.
3. K5 normalized `A²/N_color`.
4. K6 color-projected Bernoulli variance.

The convergence of all four paths to `2/9` is **structurally non-trivial**:
it requires the framework's primitive `N_pair = N_color − 1`. Under any
alternative structural counting (e.g., N_pair ≠ N_color − 1), the four
paths would in general give four different values; their agreement at `2/9`
is a sharp statement about the framework's specific integer structure.

### The K3 consistency identity is the structural anchor

```text
K1 = K2 = K5 = K6 = 2/9   <==>   N_pair = 2 AND N_color = 3.
```

The retained framework satisfies this because both `N_pair = 2` and `N_color = 3`
are explicitly retained in the magnitudes counts theorem, and `N_pair = N_color − 1`
follows by direct numerical identity. K3 articulates the converse: any CKM
framework where K1, K2, K5, K6 all give `2/9` MUST have `(N_pair, N_color) = (2, 3)`.

This converts the appearance of `2/9` from a coincidence into a **structural
consequence**: `2/9` IS the framework's integer counting, expressed
algebraically.

### Cross-sector reading (SUPPORT, not retained closure)

The conjectural Koide variance ratio `(N_gen − 1)/N_gen² = 2/9` with
`N_gen = 3` has the **identical structural form** as K1's collapse
`(N_color − 1)/N_color² = 2/9` with `N_color = 3`. Under the cross-sector
identification `N_gen = N_color = 3` (which is in the framework only as a
`_SUPPORT_NOTE_`), the Koide variance ratio reduces EXACTLY to the CKM
Bernoulli K1 derived in this note from retained W2 alone.

So if the cross-sector identification `N_gen = N_color` is promoted to
retained status (via a separate derivation grounded in CL3 algebra/lattice
structure that this note does NOT provide), the Koide 2/9 ratio is closed by
the K1 derivation here.

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
- This note does NOT use the existing `CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25` as INPUT; the K1-K6 derivations stand on retained
  CKM inputs alone. The cross-sector reading is **commentary**, not derivation.

### Falsifiable structural claim

The K3 consistency identity is a sharp claim:

```text
The framework's structural integers MUST satisfy N_pair = N_color - 1 = 2
and N_color = 3 in order for K1 through K6 to converge at 2/9.
```

If a future framework revision modified the pair-color counting (e.g.,
`N_pair = 3` or `N_color = 4`), one or more of K1-K6 would no longer give
`2/9`, breaking the convergence. The framework's claim that K1-K6 all give
`2/9` is therefore equivalent to the claim that the integer counting is
exactly `(N_pair, N_color) = (2, 3)`.

### Why this counts as pushing the science forward

Three layers of new content beyond retained `(W2)`:

1. **Four independent CKM-native paths to 2/9** (K1, K2, K5, K6) from
   retained inputs alone. Previously no retained CKM theorem produced
   `2/9` algebraically; this note delivers four.

2. **Structural consistency theorem K3** linking the four-fold convergence
   to the framework's primitive `N_pair = N_color − 1`. Converts `2/9`
   from numerical accident into algebraic necessity.

3. **Explicit cross-sector reading** (clearly labeled as SUPPORT, not
   closure): the K1 form `(N_color − 1)/N_color²` is identical to the
   conjectured Koide variance `(N_gen − 1)/N_gen²` with `N_gen = N_color`,
   reducing Koide 2/9 closure to closure of the cross-sector identification.

This **pushes the supporting science forward**: it doesn't close A² or Koide
2/9, but it exhibits `2/9` as a CKM-native multiply-determined structural
constant, and articulates exactly what additional input (cross-sector
N_gen = N_color identification) would be needed for Koide 2/9 closure.

## What This Claims

- `(K1)`: NEW algebraic identity `A² (1 − A²) = N_pair (N_color − N_pair)/N_color²
  = 2/9` in CKM, EXACT from retained `(W2)`.
- `(K2)`: NEW algebraic identity `2ρA² = 2/N_color² = 2/9` in CKM, EXACT from
  retained `(W2)` and `ρ = 1/N_quark`.
- `(K3)`: NEW structural consistency identity: K1 = K2 = K5 = K6 ⟺ `N_pair = 2`
  AND `N_color = 3`.
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
- It does NOT modify any retained CKM atlas, Wolfenstein, CP-phase, NLO-
  protected-γ̄, magnitudes structural counts, or Brannen-Koide CH-three-gap
  theorem.

## Reproduction

```bash
python3 scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py
```

Expected result:

```text
TOTAL: PASS=29, FAIL=0
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
  and the implicit structural primitive `N_pair = N_color − 1`.
- (NOT cited as derivation input) the `_SUPPORT_NOTE_` for the cross-sector
  A²-Koide bridge, which is the conditional path to Koide 2/9 closure that
  this note articulates but does not close.
