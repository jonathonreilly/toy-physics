# Consecutive Primes and S3 Representation Structure from CKM Counts: Koide-Bridge Support

**Date:** 2026-04-25

**Status:** exact CKM-side support corollary plus conditional cross-sector
commentary. This is not a retained charged-lepton Koide theorem, not a
derivation of `N_gen = N_color`, and not a derivation of `Q_l = 2/3`.

The retained CKM structural counts

```text
N_pair = 2,   N_color = 3,   N_quark = N_pair N_color = 6
```

sit on several elementary number-theory and representation-theory identities:
`(2,3)` is the unique pair of consecutive positive primes, `|S_3|=6`, the
conjugacy-class sizes of `S_3` are `{1,2,3}`, and the standard representation
of `S_3` has dimension `2 = N_pair`. This packet records those identities as a
CKM-side support card for the open Koide bridge.

**Primary runner:** `scripts/frontier_ckm_consecutive_primes_s3_koide_bridge.py`

## Statement

On the retained CKM structural-count surface:

```text
(P1)  N_pair = 2 and N_color = 3 are prime.
(P2)  (N_pair, N_color) = (2,3) is the unique consecutive positive-prime pair.

(D1)  d(N_pair) = d(N_color) = N_pair = 2.
(D2)  d(N_quark) = N_pair^2 = 4.
(D3)  Div(N_quark) = {1, N_pair, N_color, N_quark}.

(G1)  |S_{N_color}| = |S_3| = 3! = N_quark = 6.
(G2)  The conjugacy-class sizes of S_3 are {1, N_pair, N_color}.
(G3)  The S_3 class equation is 1 + N_pair + N_color = N_quark.
(G4)  The S_3 irrep dimensions (1,1,N_pair) obey
      1^2 + 1^2 + N_pair^2 = N_quark.

(R1)  dim(std rep S_{N_color}) = N_color - 1 = N_pair.
(R2)  dim(perm rep S_{N_color}) = 1 + N_pair = N_color.

(F1)  (N_pair, N_color, N_quark - 1) = (F_3, F_4, F_5) = (2,3,5).
(F2)  N_pair + N_color = N_quark - 1.

(C1)  binom(N_color, 2) = 3.
(C2)  With N_pair = 2, binom(N_color, 2) = N_color.

(U1)  The five constraints
        N_pair and N_color prime,
        N_pair and N_color consecutive,
        N_pair + N_color = N_quark - 1,
        1 + N_pair + N_color = N_quark,
        1 + 1 + N_pair^2 = N_quark
      have the unique positive-integer solution (2,3,6) in the audited range.
```

The useful new interpretation is `(R1)`: the retained primitive
`N_pair = N_color - 1` can be read as the dimension formula for the standard
representation of the symmetric group on `N_color` letters.

## Retained Inputs

| Input | Authority on `main` |
| --- | --- |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |
| Prior CKM-side Koide target-class support | [`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md), [`CKM_N9_STRUCTURAL_FAMILY_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_N9_STRUCTURAL_FAMILY_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md), [`CKM_CUBIC_BERNOULLI_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_CUBIC_BERNOULLI_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md), [`CKM_EGYPTIAN_BERNOULLI_CLOSURES_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_EGYPTIAN_BERNOULLI_CLOSURES_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md) |

Only the retained CKM structural counts are derivation inputs for this packet.
The cross-sector Koide reading is commentary only.

## Derivation

### Consecutive Primes and Divisors

`2` and `3` are prime and differ by one. If `p > 2` is prime, then `p` is odd,
so `p+1` is even and composite. Therefore `(2,3)` is the unique consecutive
positive-prime pair.

The divisor identities follow immediately:

```text
d(2) = 2,
d(3) = 2,
d(6) = 4,
Div(6) = {1,2,3,6}.
```

### Symmetric Group S3

For `N_color = 3`,

```text
|S_{N_color}| = |S_3| = 3! = 6 = N_quark.
```

The conjugacy classes of `S_3` have cycle types:

```text
identity        size 1
3-cycles        size 2 = N_pair
transpositions  size 3 = N_color
```

Hence the class equation is

```text
1 + N_pair + N_color = 6 = N_quark.
```

The irreducible representation dimensions of `S_3` are `1,1,2`, giving

```text
1^2 + 1^2 + N_pair^2 = 1 + 1 + 4 = 6 = N_quark.
```

### Standard Representation

The permutation representation of `S_n` on `n` letters decomposes as

```text
permutation = trivial + standard.
```

Therefore the standard representation has dimension `n-1`. For `n=N_color=3`,

```text
dim(std rep S_{N_color}) = N_color - 1 = 2 = N_pair.
```

This is an interpretation of the retained pair/color count relation, not a new
derivation of the retained counts.

### Fibonacci and Mixing-Angle Count

The adjacent Fibonacci values `(F_3,F_4,F_5)=(2,3,5)` match

```text
(N_pair, N_color, N_quark - 1) = (2,3,5),
```

so `N_pair + N_color = N_quark - 1`.

The generic angle count of a real `N_color x N_color` mixing matrix is

```text
binom(N_color,2) = 3.
```

Since `N_pair = 2`, this also reads

```text
binom(N_color,2) = N_color N_pair / 2 = N_color.
```

### Combined Uniqueness

The runner exhaustively audits positive integer pairs in the stated finite
window and finds only `(N_pair,N_color,N_quark)=(2,3,6)` satisfying all five
constraints `(U1)`.

## Conditional Koide Reading

The charged-lepton Koide formula is symmetric under permutations of the lepton
mass eigenvalues. If a separate retained cross-sector theorem later identifies
`N_gen = N_color = 3`, then the Koide permutation group would be the same
abstract `S_3` group used in this support card, and the natural three-dimensional
permutation representation would decompose as `1 + 2`.

That is useful target-class bookkeeping. It is not a proof of `N_gen=N_color`,
not a proof of charged-lepton Koide, and not a proof of any Koide readout.

## What This Does Not Claim

- It does not close charged-lepton Koide or promote `Q_l = 2/3`.
- It does not derive `N_gen = N_color`.
- It does not derive `A^2 = 2/3` below the retained W2/counting surface.
- It does not prove a PMNS theorem; PMNS references are conditional
  cross-sector commentary.
- It does not use support-tier Koide premises as derivation inputs.

## Verification

Expected result:

```text
python3 scripts/frontier_ckm_consecutive_primes_s3_koide_bridge.py
TOTAL: PASS=27, FAIL=0
```

The runner uses exact integer arithmetic and enumerates `S_3` conjugacy classes
directly.
