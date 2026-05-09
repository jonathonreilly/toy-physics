# Complete n/N_color^2 Structural Family from CKM Retained Inputs: Koide-Bridge Support

**Date:** 2026-04-25

**Status:** exact CKM-side support corollary on proposed_retained `main` inputs, plus
explicit cross-sector SUPPORT commentary. This is not a retained Koide theorem
and not a retained cross-sector identification.
**Primary runner:** `scripts/frontier_ckm_n9_structural_family_koide_bridge.py`


This note packages an explicit nine-member CKM support family

```text
F_n = n / N_color^2 = n/9,  n = 1,...,9,
```

using only retained CKM inputs:

- `A^2 = N_pair/N_color = 2/3`
- `rho = 1/N_quark = 1/6`
- `eta^2 = (N_quark - 1)/N_quark^2 = 5/36`
- `N_pair = 2`, `N_color = 3`, `N_quark = N_pair*N_color = 6`

The support value is not that arbitrary rational arithmetic can name `n/9`.
The value is that the retained CKM surface supplies a compact set of named
expressions whose exact Fraction values cover the complete `n/9` ladder and
exhibit a structural numerator reading for each member.

## Statement

On the retained CKM atlas + Wolfenstein structural surface:

```text
(F1)  1/9  =  A^2 rho

(F2)  2/9  =  N_pair / N_color^2
             =  A^2(1 - A^2)
             =  2 rho A^2
             =  A^2 / N_color
             =  (1/N_color)(1 - 1/N_color)

(F3)  3/9  =  1/3 = 1 - A^2 = 1/N_color

(F4)  4/9  =  A^4 = N_pair^2 / N_color^2

(F5)  5/9  =  (N_quark - 1) / N_color^2
             =  (1 - A^2)(1 + A^2)
             =  1 - A^4
             =  eta^2 N_pair^2

(F6)  6/9  =  2/3 = A^2 = N_pair/N_color = N_quark/N_color^2

(F7)  7/9  =  1 - F2 = (N_color^2 - N_pair)/N_color^2

(F8)  8/9  =  1 - F1 = (N_color^2 - 1)/N_color^2

(F9)  9/9  =  1 = N_color^2/N_color^2

(G1)  F1 + F2 + ... + F9 = 45/9 = 5 = N_quark - 1

(G2)  All F_n have universal denominator N_color^2 = 9

(G3)  Numerator ladder:
      1, N_pair, N_color, N_pair^2, N_quark - 1,
      N_quark, N_quark + 1, N_color^2 - 1, N_color^2
```

The new nontrivial member is `F5 = 5/9`, because it has two algebraically
distinct retained-input paths:

```text
F5a = (1 - A^2)(1 + A^2) = 1 - A^4 = 5/9
F5b = eta^2 N_pair^2 = ((N_quark - 1)/N_quark^2) N_pair^2 = 5/9
```

## Retained Inputs

| Input | Authority on `main` |
| --- | --- |
| `(W2)` `A^2 = N_pair/N_color = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/N_quark = 1/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `eta^2 = (N_quark - 1)/N_quark^2 = 5/36` | same |
| `N_quark = N_pair*N_color = 6`, `N_pair = 2`, `N_color = 3` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |
| CKM-side `2/9` support readouts | [`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md) |

No PDG observable enters as a derivation input. No Koide support target,
bare-coupling ratio, dimension-color quadratic, or cross-sector bridge is used
as a derivation input. The cross-sector reading is commentary only.

## Derivation

### F1 through F4

`F1` follows directly:

```text
A^2 rho = (2/3)(1/6) = 1/9.
```

`F2` is the accepted CKM-side Bernoulli support readout:

```text
A^2(1 - A^2) = (2/3)(1/3) = 2/9.
```

The same accepted support surface also gives the equivalent CKM readouts
`2 rho A^2`, `A^2/N_color`, and `(1/N_color)(1 - 1/N_color)`.

`F3` is the W2 complement:

```text
1 - A^2 = 1 - 2/3 = 1/3 = 3/9.
```

`F4` is the W2 square:

```text
A^4 = (2/3)^2 = 4/9.
```

### F5: two paths to 5/9

Path F5a uses W2 alone:

```text
(1 - A^2)(1 + A^2)
  = (1/3)(5/3)
  = 5/9.
```

Equivalently, this is `1 - A^4 = 1 - 4/9 = 5/9`.

Path F5b uses retained `eta^2` and `N_pair`:

```text
eta^2 N_pair^2
  = ((N_quark - 1)/N_quark^2) N_pair^2
  = (5/36) * 4
  = 5/9.
```

Using `N_quark = N_pair*N_color`, the same expression is

```text
eta^2 N_pair^2
  = ((N_quark - 1)/(N_pair^2 N_color^2)) N_pair^2
  = (N_quark - 1)/N_color^2.
```

### F6 through F9

`F6` is W2 itself:

```text
A^2 = 2/3 = 6/9.
```

`F7` and `F8` are complements of F2 and F1:

```text
F7 = 1 - F2 = 1 - 2/9 = 7/9.
F8 = 1 - F1 = 1 - 1/9 = 8/9.
```

`F9` is the unit:

```text
F9 = 1 = 9/9.
```

### G1: sum identity

```text
F1 + F2 + ... + F9
  = (1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9)/9
  = 45/9
  = 5
  = N_quark - 1.
```

### G3: structural numerator ladder

The numerator values have the following retained-count readings:

| n | Structural numerator |
| -: | --- |
| 1 | `1` |
| 2 | `N_pair` |
| 3 | `N_color` |
| 4 | `N_pair^2` |
| 5 | `N_quark - 1` |
| 6 | `N_quark` |
| 7 | `N_quark + 1 = N_color^2 - N_pair` |
| 8 | `N_color^2 - 1` |
| 9 | `N_color^2` |

These readings are structural bookkeeping consequences of the retained counts
`N_pair=2`, `N_color=3`, `N_quark=6`; they are not introduced as new axioms.

## Cross-Sector Reading

This note does not derive Koide. The only cross-sector reading is conditional:

```text
If a separate Koide-side derivation produces ratios n/N_gen^2,
then the separately retained numeric equality N_gen = N_color = 3 lets this
CKM support family supply matching n/9 target-class expressions.
```

The Koide-side requirement remains open outside this note. The CKM-side family
is useful because it makes the target class explicit and exact; it does not
close charged-lepton Koide or any structural Koide mechanism
beyond the retained numeric equality `N_gen=N_color=3`.

## What This Packages

- `(F1)` through `(F9)`: every `n/9` for `n=1,...,9` has an explicit retained
  CKM expression.
- `(F5)`: two distinct retained-input paths to `5/9`.
- `(G1)`: the exact sum identity `F1 + ... + F9 = N_quark - 1 = 5`.
- `(G2)`: the universal denominator observation `N_color^2 = 9`.
- `(G3)`: a structural numerator ladder built from retained counts.

## What This Does Not Claim

- It does not close `A^2` deeper than retained W2.
- It does not close charged-lepton Koide or any specific Koide `n/9`.
- It does not prove that the Koide sector produces a complete `n/9` family.
- It does not derive or use the separately retained numeric equality
  `N_gen=N_color=3` as an input to its CKM-side arithmetic.
- It does not use cross-sector support notes as derivation inputs.
- It does not add a physical observable prediction; this is CKM-side algebraic
  support and package bookkeeping.

## Reproduction

```bash
python3 scripts/frontier_ckm_n9_structural_family_koide_bridge.py
```

Expected result:

```text
TOTAL: PASS=35, FAIL=0
```

The runner uses Python's `fractions.Fraction` for exact-rational arithmetic.

## Cross-References

- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `(W2)` `A^2 = N_pair/N_color`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `rho = 1/N_quark` and `eta^2 = (N_quark - 1)/N_quark^2`.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- retained `N_pair = 2`, `N_color = 3`, `N_quark = N_pair*N_color = 6`.
- [`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md)
  -- accepted CKM-side `2/9` support readouts.
