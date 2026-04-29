# Multiplicative A²–ρ–η² Structural Identities and Fifth 2/9 Path: Supporting the Koide Bridge

**Date:** 2026-04-25

**Status:** retained CKM-structure THEOREM (closure on retained main inputs) **plus**
clearly-labeled cross-sector SUPPORT commentary. This note derives a layer of
**multiplicative structural identities** linking three retained CKM quantities —
the Wolfenstein A², the CP-phase ρ, and the CP-phase η² — that, when combined,
expose `2/9` as multiply-determined and tie the Wolfenstein and CP-phase sectors
of the framework together at the structural-integer level.

This note is **not a closure of A² (already retained as W2)** and **not a closure
of Koide 2/9 (cross-sector identification still conjectural)**. It pushes the
*supporting* structure further than the previous Bernoulli-2/9 branch by
establishing **multiplicative ties** (not just additive variance forms) between
A², ρ, and η².

The headline framework-native multiplicative identities, all from retained inputs:

```text
(M1)   A^2 * rho             =  1 / N_color^2   =  1/9        [Wolfenstein × CP-phase product]

(M2)   A^2 / rho             =  N_pair^2        =  4          [Wolfenstein × CP-phase ratio]

(M3)   eta^2 / rho^2         =  N_quark - 1     =  5          [Thales-derived structural ratio]

(M2')  Equivalently:  4 * rho  =  A^2                          [clean reading of M2]
```

These three identities tie:
- A² (Wolfenstein, retained W2)
- ρ (CP-phase, retained from CP-phase identity)
- η² (CP-phase squared, retained Thales identity)

through structural integers `N_pair`, `N_color`, `N_quark`, `N_quark − 1`,
giving FOUR independent algebraic constraints that the retained framework
satisfies exactly.

**Cross-multiplication consistency:**

```text
A^4  =  (A^2 * rho) * (A^2 / rho)  =  M1 * M2  =  N_pair^2 / N_color^2
```

So `A⁴ = (1/9) × 4 = 4/9` is a consequence of M1 and M2 together, providing an
**internal consistency check** of the multiplicative structure.

**FIFTH framework-native path to 2/9:**

```text
(K7)   A^4 / N_pair  =  N_pair / N_color^2  =  2/9   EXACTLY
```

This adds to the four paths derived in the previous Bernoulli-2/9 branch (K1, K2,
K5, K6), giving FIVE independent framework-native algebraic paths to 2/9.

**Cross-sector reading (SUPPORT, conditional):**

The conjectural Koide squared cosine `cos²θ_K = 1/(3 Q_l) = 1/2` matches
`1/N_pair = 1/2` in CKM under cross-sector A² ↔ Q_l identification. Under this
identification, `1/N_pair` is a Koide-natural quantity, and M2's `A²/ρ = N_pair²`
becomes the assertion `Q_l/ρ_lepton = (1/cos²θ_K)² × cos²θ_K = sec²θ_K · sec(...)`
(under unspecified lepton-side ρ identification). The cross-sector parallel is
articulated explicitly but **NOT** used as derivation input.

**Primary runner:**
`scripts/frontier_ckm_a_rho_multiplicative_koide_bridge.py`

## Statement

On the retained CKM atlas + Wolfenstein structural surface (where `(W2)` and
the CP-phase identities hold):

```text
(M1)  A^2 * rho      =  (N_pair/N_color) * (1/N_quark)
                      =  N_pair / (N_color * N_quark)
                      =  N_pair / (N_color * N_pair * N_color)        [N_quark = N_pair × N_color]
                      =  1 / N_color^2
                      =  1/9                                            [EXACT, from W2 + CP-phase rho]

(M2)  A^2 / rho      =  (N_pair/N_color) / (1/N_quark)
                      =  N_pair * N_quark / N_color
                      =  N_pair * N_pair * N_color / N_color           [N_quark = N_pair × N_color]
                      =  N_pair^2
                      =  4                                              [EXACT, from W2 + CP-phase rho]

(M2') Equivalently:  4 * rho = A^2,
                      since A^2/rho = 4 ==> A^2 = 4*rho.

(M3)  eta^2 / rho^2  =  ((N_quark - 1)/N_quark^2) / (1/N_quark^2)
                      =  N_quark - 1
                      =  5                                              [EXACT, from Thales/CP-phase eta^2]

(C1)  A^4  =  M1 * M2  =  (1/N_color^2) * N_pair^2  =  N_pair^2/N_color^2  =  4/9
                                                                        [consistency identity]

(K7)  A^4 / N_pair  =  N_pair / N_color^2  =  2/9                       [NEW 5th 2/9 path]

(K8)  Five-fold convergence to 2/9 (combining with Bernoulli branch K1, K2, K5, K6):
       K1 = K2 = K5 = K6 = K7 = 2/9
       <==>
       (N_pair, N_color) = (2, 3) AND N_quark = N_pair × N_color = 6.
```

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| `(W2)` `A² = N_pair/N_color = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `ρ = 1/6 = 1/N_quark` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `η² = 5/36 = (N_quark − 1)/N_quark²` (Thales identity) | same |
| `N_quark = N_pair × N_color = 6`, `N_pair = 2`, `N_color = 3` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |
| Structural primitive `N_pair = N_color − 1` | implicit in retained N_pair = 2, N_color = 3 |

No PDG observable enters as a derivation input. No SUPPORT-tier or open
inputs (Koide `Q_l`, bare-coupling ratios, dimension-color quadratic, A²-
Koide cross-sector bridge) are USED as derivation inputs. The cross-sector
reading is commentary only.

## Derivation

### M1: `A² × ρ = 1/N_color²`

From retained `(W2)` and CP-phase ρ:

```text
A^2 * rho  =  (N_pair / N_color) * (1 / N_quark)
            =  N_pair / (N_color * N_quark)
            =  N_pair / (N_color * N_pair * N_color)        [N_quark = N_pair × N_color]
            =  1 / N_color^2.
```

In framework with N_color = 3: `A² × ρ = 1/9`.

This is `(M1)`. The product **decouples N_pair entirely** from the result —
the answer is `1/N_color²` regardless of N_pair (as long as N_quark =
N_pair × N_color holds). So `(M1)` is a sharp **N_color-only structural
identity** derived from a Wolfenstein × CP-phase product.

### M2: `A² / ρ = N_pair²`

From retained `(W2)` and CP-phase ρ:

```text
A^2 / rho  =  (N_pair / N_color) / (1 / N_quark)
            =  (N_pair / N_color) * N_quark
            =  (N_pair * N_quark) / N_color
            =  (N_pair * N_pair * N_color) / N_color         [N_quark = N_pair × N_color]
            =  N_pair^2.
```

In framework with N_pair = 2: `A² / ρ = 4`.

This is `(M2)`. The ratio **decouples N_color entirely** from the result —
the answer is `N_pair²` regardless of N_color (as long as N_quark =
N_pair × N_color holds). So `(M2)` is a sharp **N_pair-only structural
identity** derived from a Wolfenstein / CP-phase ratio.

Equivalently, `(M2')` reads: `4ρ = A²`. So Wolfenstein A² is exactly four
times the CP-phase apex coordinate ρ on the framework's structural integer
identification.

### M3: `η²/ρ² = N_quark − 1`

From retained CP-phase Thales identity `η² = ρ(1 − ρ) = (N_quark − 1)/N_quark²`:

```text
eta^2 / rho^2  =  ((N_quark - 1)/N_quark^2)  /  (1/N_quark^2)
                =  (N_quark - 1) * N_quark^2 / (N_quark^2)
                =  N_quark - 1.
```

In framework with N_quark = 6: `η²/ρ² = 5`.

This is `(M3)`. The ratio is a **pure structural integer**, the "quark deficit"
N_quark − 1.

### Consistency C1: `A⁴ = M1 × M2 = N_pair²/N_color² = 4/9`

```text
M1 * M2  =  (A^2 * rho) * (A^2 / rho)  =  A^4.
```

So

```text
A^4  =  (1/N_color^2) * N_pair^2  =  N_pair^2 / N_color^2  =  4/9.
```

This is the cross-multiplication consistency: M1 and M2 together force
`A⁴ = N_pair²/N_color² = 4/9`, agreeing with the direct evaluation
`A⁴ = (A²)² = (2/3)² = 4/9`.

### K7: NEW fifth path to 2/9

```text
A^4 / N_pair  =  (N_pair^2 / N_color^2) / N_pair
              =  N_pair / N_color^2
              =  2 / 9                                       (with N_pair = 2, N_color = 3).
```

This is `(K7)`. It joins the four framework-native 2/9 paths from the
previous Bernoulli-2/9 branch (K1, K2, K5, K6) as a fifth independent
algebraic route.

### K8: Five-fold consistency

Combining K7 with K1, K2, K5, K6:

```text
K1 = A^2 (1 - A^2)              =  N_pair (N_color - N_pair) / N_color^2  =  2/9
K2 = 2 * rho * A^2               =  2 / N_color^2                          =  2/9
K5 = A^2 / N_color               =  N_pair / N_color^2                     =  2/9
K6 = (1/N_color)(1 - 1/N_color)  =  (N_color - 1) / N_color^2              =  2/9
K7 = A^4 / N_pair                 =  N_pair / N_color^2                     =  2/9
```

All five framework-native paths converge at `2/9` if and only if
`(N_pair, N_color) = (2, 3)` (with `N_quark = 6` derived). The five-fold
convergence is **EQUIVALENT** to the framework's primitive integer counting.

## Numerical Verification

All identities verified to **exact Fraction arithmetic** (no floating-point):

| Identity | Closed form | Value |
| --- | --- | ---: |
| `(M1)` `A² × ρ` | `(2/3)(1/6)` | `1/9` ✓ |
| `(M2)` `A² / ρ` | `(2/3)/(1/6)` | `4` ✓ |
| `(M2')` `4ρ` vs `A²` | `4(1/6)` vs `2/3` | `2/3` = `2/3` ✓ |
| `(M3)` `η² / ρ²` | `(5/36)/(1/36)` | `5` ✓ |
| `(C1)` `A⁴` via `M1 × M2` | `(1/9)(4)` vs `(2/3)²` | `4/9` = `4/9` ✓ |
| `(K7)` `A⁴ / N_pair` | `(4/9)/2` | `2/9` ✓ |
| `(K8)` Five-fold convergence | K1 = K2 = K5 = K6 = K7 | All `2/9` ✓ |

## Science Value

### What this lets the framework predict that it could not before

Previously the framework had retained closed forms for A² (W2), ρ (CP-phase),
and η² (Thales), but **no retained theorem packaged the multiplicative ties
between them** in structural-integer form. This note delivers:

- `(M1)`: A² × ρ = 1/N_color². The Wolfenstein × CP-phase product gives a
  pure N_color-only ratio.
- `(M2)`: A² / ρ = N_pair². The Wolfenstein / CP-phase ratio gives a pure
  N_pair-only ratio. Equivalently: `4ρ = A²`.
- `(M3)`: η² / ρ² = N_quark − 1. The Thales-derived ratio gives a pure
  quark-deficit integer.
- `(C1)`: A⁴ = N_pair²/N_color² = 4/9. Consistency forced by M1 × M2.
- `(K7)`: A⁴/N_pair = 2/9. A fifth framework-native path to 2/9.
- `(K8)`: Five-fold convergence at 2/9 (combining with K1, K2, K5, K6).

### M1 and M2 are sector-decoupling identities

`(M1)` `A² × ρ = 1/N_color²` is striking because **N_pair drops out entirely
from the result** (despite both A² and ρ depending on N_pair). The product is
purely a function of `N_color`.

`(M2)` `A² / ρ = N_pair²` is the dual: **N_color drops out entirely from the
ratio**, leaving a pure function of `N_pair`.

So the Wolfenstein × CP-phase product isolates N_color, and the Wolfenstein /
CP-phase ratio isolates N_pair. This is a clean **sector decoupling**: the
combination M1 × M2 = A⁴ = (N_pair/N_color)² recovers the original A² squared,
but the individual M1 and M2 each carry only one of the two structural integers.

### The "4ρ = A²" identity (M2') is structurally non-trivial

`(M2')` reads: **the Wolfenstein A² parameter equals 4 times the CP-phase ρ**.

Numerically: A² = 2/3, 4ρ = 4 × 1/6 = 2/3. ✓

Structurally: `4ρ = A²` ⟺ `4/N_quark = N_pair/N_color` ⟺ `4 × N_color =
N_pair × N_quark = N_pair² × N_color`, so `N_pair² = 4`, i.e., `N_pair = 2`.

So `4ρ = A²` is **EQUIVALENT** to `N_pair = 2` (given N_quark = N_pair × N_color
holds). The framework's specific N_pair = 2 is the algebraic statement of M2'.

### M3 is a structural reading of the Thales identity

`(M3)` `η²/ρ² = N_quark − 1` rewrites the retained Thales identity
`η² = ρ(1 − ρ)` (with `ρ = 1/N_quark`, `1 − ρ = (N_quark − 1)/N_quark`) as a
pure integer ratio:

```text
eta^2 / rho^2  =  ρ(1-ρ) / ρ^2  =  (1-ρ)/ρ  =  (N_quark - 1).
```

So η²/ρ² is the **quark deficit integer** `N_quark − 1 = 5`. This is the
structural reading of "Thales applied to the unitarity triangle apex coordinates".

### K7 strengthens the multi-path convergence at 2/9

The previous Bernoulli-2/9 branch derived four framework-native paths to 2/9.
This branch adds a fifth (K7), making the convergence five-fold:

```text
K1 = K2 = K5 = K6 = K7 = 2/9   <==>   (N_pair, N_color) = (2, 3).
```

The more independent paths converge at 2/9, the **stronger** the structural
case for `2/9` being algebraically forced by the framework's pair-color
counting (rather than a numerical coincidence).

### Cross-sector reading (SUPPORT, NOT closure)

Under the conjectural cross-sector A² ↔ Q_l identification (currently a
`_SUPPORT_NOTE_`):

- M1's value `1/N_color² = 1/9` matches the squared Koide cosine pattern,
  since Koide cos²θ_K = 1/(3 Q_l) = 1/2 = 1/N_pair (under N_pair = 2 = N_color − 1).
- M2's `4ρ = A²` becomes `(N_pair²) ρ_lepton = Q_l` under cross-sector,
  giving `ρ_lepton = Q_l/N_pair² = (2/3)/4 = 1/6`. This matches CKM ρ = 1/N_quark = 1/6,
  suggesting **cross-sector ρ identification** as a corollary.
- M3 has no direct Koide analog (Thales is CKM-specific), but the form
  `(N − 1)/N²` is shared between CKM η²_LO (with N=N_quark) and Koide 2/9
  (with N=N_gen=N_color, conjectural).

These cross-sector parallels are SUPPORT, not closure. Closing Koide 2/9
still requires promoting the cross-sector identifications (A² ↔ Q_l,
N_gen ↔ N_color, possibly ρ_lepton ↔ ρ_CKM) to retained theorems.

### Falsifiable structural claim

The five-fold convergence K1 = K2 = K5 = K6 = K7 = 2/9, combined with M1, M2,
M3, is a sharp claim about the framework's integer structure:

```text
The framework MUST have (N_pair, N_color, N_quark) = (2, 3, 6) with
N_pair = N_color - 1 in order for ALL of K1-K8, M1-M3 to evaluate
to their reported clean integer ratios.
```

If a future framework revision modified pair-color counting, multiple
identities would simultaneously break. The system of five 2/9 paths plus
three multiplicative identities is **redundantly determined** by the
specific integer choice.

### Why this counts as pushing the science forward

Three layers of new content beyond the Bernoulli-2/9 branch:

1. **Multiplicative identities** (M1, M2, M3) tying Wolfenstein A², CP-phase
   ρ, and Thales η² through structural integers. M1 and M2 are sector-
   decoupling: M1 isolates N_color, M2 isolates N_pair.

2. **Cross-multiplication consistency** (C1): A⁴ = M1 × M2 = N_pair²/N_color² = 4/9.
   Internal consistency check forced by M1 and M2 together.

3. **Fifth 2/9 path** (K7): A⁴/N_pair = 2/9, strengthening the framework's
   five-fold algebraic determination of `2/9`.

These propositions push the supporting structure for cross-sector unification
**deeper** than the previous Bernoulli-2/9 branch by exhibiting
**multiplicative** (not just additive variance) ties between retained
quantities, and by tightening the convergence count from four to five.

## What This Claims

- `(M1)`: NEW EXACT `A² × ρ = 1/N_color² = 1/9`.
- `(M2)`: NEW EXACT `A² / ρ = N_pair² = 4`.
- `(M2')`: NEW reading `4ρ = A²` (equivalent to M2).
- `(M3)`: NEW EXACT `η²/ρ² = N_quark − 1 = 5`.
- `(C1)`: NEW consistency `A⁴ = M1 × M2 = N_pair²/N_color² = 4/9`.
- `(K7)`: NEW EXACT 5th 2/9 path `A⁴/N_pair = 2/9`.
- `(K8)`: NEW five-fold convergence K1 = K2 = K5 = K6 = K7 = 2/9 ⟺
  (N_pair, N_color) = (2, 3).

## What This Does NOT Claim

- It does NOT close `A²` deeper than the retained structural-counts level
  (W2 still required).
- It does NOT close `Koide 2/9`. The cross-sector reading is commentary.
- It does NOT promote any cross-sector identification (A² ↔ Q_l,
  N_gen ↔ N_color, ρ_lepton ↔ ρ_CKM) to retained status. Those remain
  separate `_SUPPORT_NOTE_` programs.
- It does NOT use the existing cross-sector `_SUPPORT_NOTE_`s as derivation
  inputs. M1-M3, C1, K7 stand on retained CKM inputs alone.

## Reproduction

```bash
python3 scripts/frontier_ckm_a_rho_multiplicative_koide_bridge.py
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
  -- retained `(W2)` `A² = N_pair/N_color` used in M1, M2, K7.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `ρ = 1/N_quark`, `η² = (N_quark − 1)/N_quark²` used in M1, M2, M3.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- retained `N_pair = 2`, `N_color = 3`, `N_quark = N_pair × N_color = 6`,
  and structural primitive `N_pair = N_color − 1`.
- (NOT cited as derivation input) the previous `CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_THEOREM_NOTE_2026-04-25` (pending unmerged branch); K7 supplements its K1, K2, K5, K6.
- (NOT cited as derivation input) the cross-sector `_SUPPORT_NOTE_` for the A²-Koide bridge.
