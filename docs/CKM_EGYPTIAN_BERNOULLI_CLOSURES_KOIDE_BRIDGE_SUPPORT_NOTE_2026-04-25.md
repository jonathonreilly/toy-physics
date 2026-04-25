# Egyptian Fraction and Bernoulli Sum Identities from CKM Retained Inputs: Koide-Bridge Support

**Date:** 2026-04-25

**Status:** exact CKM-side support corollary plus conditional cross-sector
commentary. This is not a retained charged-lepton Koide theorem, not a
derivation of `cos^2(theta_K)`, and not a retained `N_gen = N_color` bridge.

The useful retained-input content is number-theoretic. With the CKM structural
counts

```text
N_pair = 2,   N_color = 3,   N_quark = N_pair N_color = 6,
```

the framework integers satisfy the exact Egyptian fraction identity

```text
1/N_pair + 1/N_color + 1/N_quark = 1/2 + 1/3 + 1/6 = 1.
```

This note packages that identity, its uniqueness under the retained pair/color
primitives, exact Bernoulli-series sum rules, and the resulting CKM-side
`2/9` sum mechanism. The Koide reading is included only as target-class
bookkeeping: if a separate cross-sector theorem later supplies the charged
lepton identifications, the CKM-side arithmetic already supplies the matching
decomposition.

**Primary runner:** `scripts/frontier_ckm_egyptian_bernoulli_closures_koide_bridge.py`

## Statement

Let

```text
M^(k)(N) := (N - 1)/N^k,   M(N) := M^(1)(N),   V(N) := M^(2)(N),   W(N) := M^(3)(N).
```

On the retained CKM structural-count surface:

```text
(E1)  1/N_pair + 1/N_color + 1/N_quark = 1.

(E2)  The system
        N_pair = N_color - 1,
        N_quark = N_pair N_color,
        1/N_pair + 1/N_color + 1/N_quark = 1
      has the unique positive-integer solution
        (N_pair, N_color, N_quark) = (2, 3, 6).

(GS1) For every N >= 2,
        sum_{k>=1} M^(k)(N) = 1.

(GS2) For every N >= 2,
        sum_{k>=0} M^(k)(N) = N.

(CS1) sum_{N in {2,3,6}} M(N) = 2 = N_pair.

(CS2) sum_{N in {2,3,6}} V(N) = 11/18.

(CS3) sum_{N in {2,3,6}} W(N) = 2/9.

(K2)  M(N_pair) = 1/N_color + 1/N_quark.

(K3)  (sum_N M(N))(sum_N W(N)) = A^4 = 4/9,
      (sum_N M(N))/(sum_N W(N)) = N_color^2 = 9.
```

The new `2/9` mechanism is `(CS3)`: the cubic Bernoulli terms summed across
the pair/color/quark levels give `2/9` exactly. This is CKM-side arithmetic
only; it does not close charged-lepton Koide.

## Retained Inputs

| Input | Authority on `main` |
| --- | --- |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |
| `A^2 = N_pair/N_color = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/N_quark`, `eta^2 = 5/36` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Prior CKM-side Koide target-class support | [`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md), [`CKM_N9_STRUCTURAL_FAMILY_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_N9_STRUCTURAL_FAMILY_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md), [`CKM_CUBIC_BERNOULLI_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_CUBIC_BERNOULLI_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md) |

The conditional cross-sector comparison to charged-lepton Koide is aligned with
the existing support lane [`CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md),
but that support lane is not used as a derivation input here.

## Derivation

### E1: Egyptian Fraction Identity

```text
1/N_pair + 1/N_color + 1/N_quark
  = 1/2 + 1/3 + 1/6
  = 3/6 + 2/6 + 1/6
  = 1.
```

### E2: Uniqueness

Assume `N_pair = N_color - 1` and `N_quark = N_pair N_color`. Then

```text
1/N_pair + 1/N_color + 1/N_quark
  = 1/(N_color - 1) + 1/N_color + 1/((N_color - 1)N_color)
  = 2/(N_color - 1).
```

Setting the Egyptian sum equal to `1` gives `N_color = 3`, hence `N_pair = 2`
and `N_quark = 6`. The runner also exhaustively audits the positive-integer
search window used by this packet.

### GS1 and GS2: Exact Bernoulli Series

For `N >= 2`,

```text
sum_{k>=1} (N - 1)/N^k
  = (N - 1)(1/N)/(1 - 1/N)
  = 1.
```

Including the `k=0` term gives

```text
sum_{k>=0} M^(k)(N) = (N - 1) + 1 = N.
```

These are exact geometric-series identities. The runner checks the closed forms
directly, not numerical partial sums.

### Cross-Level Sums

At fixed `k=1`:

```text
sum_N M(N)
  = (1/2) + (2/3) + (5/6)
  = 2
  = N_pair.
```

At fixed `k=2`:

```text
sum_N V(N)
  = (1/4) + (2/9) + (5/36)
  = 11/18.
```

At fixed `k=3`:

```text
sum_N W(N)
  = (1/8) + (2/27) + (5/216)
  = 27/216 + 16/216 + 5/216
  = 48/216
  = 2/9.
```

This is the new sum-route appearance of the CKM-side `2/9` target-class ratio.

### K2 and K3

The Egyptian identity immediately gives

```text
M(N_pair) = 1 - 1/N_pair = 1/N_color + 1/N_quark.
```

Using `sum_N M(N) = 2` and `sum_N W(N) = 2/9`,

```text
(sum_N M(N))(sum_N W(N)) = 2 * (2/9) = 4/9 = A^4,
(sum_N M(N))/(sum_N W(N)) = 2 / (2/9) = 9 = N_color^2.
```

## Conditional Koide Reading

If a separate retained cross-sector theorem later identifies the charged-lepton
Koide angle with the pair-count target

```text
cos^2(theta_K) = 1/N_pair = 1/2,
```

then `(E1)` supplies the target-class decomposition

```text
sin^2(theta_K) = 1 - 1/N_pair = 1/N_color + 1/N_quark = 1/3 + 1/6.
```

That is useful bookkeeping, but it is not a proof of `cos^2(theta_K)`, not a
proof of charged-lepton Koide, and not a proof of `N_gen = N_color`.

## What This Does Not Claim

- It does not close charged-lepton Koide or promote `Q_l = 2/3`.
- It does not derive `cos^2(theta_K) = 1/2`.
- It does not derive or promote `N_gen = N_color`.
- It does not derive `A^2 = 2/3` below the already-retained W2 surface.
- It does not use Koide, PDG data, or support-tier cross-sector premises as
  derivation inputs.

## Verification

The runner audits all exact identities using `fractions.Fraction` arithmetic and
does not count the conditional Koide reading as a proof check.

Expected result:

```text
python3 scripts/frontier_ckm_egyptian_bernoulli_closures_koide_bridge.py
TOTAL: PASS=21, FAIL=0
```
