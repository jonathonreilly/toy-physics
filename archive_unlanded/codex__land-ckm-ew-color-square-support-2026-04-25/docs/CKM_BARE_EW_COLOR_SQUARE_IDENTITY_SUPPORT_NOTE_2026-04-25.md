# Bare EW / CKM Color-Square Support Note

**Date:** 2026-04-25

**Status:** exact algebraic support corollary on the retained EW-normalization
and CKM structural-count surfaces. This note is not a new retained closure
theorem and it does not derive `d = 3` or `N_color = 3` from scratch.

**Primary verifier:** `scripts/frontier_ckm_bare_ew_color_square_support.py`

## Claim

On the current retained package surface, the bare EW inverse-coupling sum and
the CKM color count obey

```text
1/g_2^2 + 1/g_Y^2 = N_color^2 = 9.
```

The calculation uses only already-retained inputs:

- `YT_EW_COLOR_PROJECTION_THEOREM.md`: bare lattice couplings
  `g_3^2 = 1`, `g_2^2 = 1/(d+1) = 1/4`, and
  `g_Y^2 = 1/(d+2) = 1/5`;
- `MINIMAL_AXIOMS_2026-04-11.md`: the package substrate is `Z^3`, so `d=3`;
- `CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`:
  `N_pair = 2`, `N_color = 3`, and `N_quark = 6`;
- `WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`:
  `A^2 = N_pair/N_color = 2/3`, used only for the optional weak-angle
  cross-read.

Therefore

```text
1/g_2^2 + 1/g_Y^2 = 4 + 5 = 9 = 3^2 = N_color^2.
```

## Boundary

This support note records a sharp same-surface identity. It does not upgrade
the bare `alpha_3/alpha_em = 2d+3 = 9` card into a direct low-energy
observable, and it does not turn the identity into an independent derivation of
the spatial substrate.

The correct logical direction is:

```text
retained d=3, retained bare EW couplings, retained N_color=3
  -> exact color-square identity.
```

The reverse direction is only a conditional selector statement:

```text
if one promotes 1/g_2^2 + 1/g_Y^2 = N_color^2
and also imposes N_color=d, then 2d+3=d^2 has the unique non-negative
solution d=3.
```

That conditional uniqueness lemma is useful bookkeeping, but it is not a new
minimal-stack derivation of `d=3`.

## Exact Identities

With the retained values above:

```text
(S1)  1/g_2^2 + 1/g_Y^2
      = (d+1) + (d+2)
      = 2d + 3
      = 9
      = N_color^2.

(S2)  (1/g_2^2)(1/g_Y^2)
      = (d+1)(d+2)
      = 20
      = N_pair^2 (N_quark - 1).

(S3)  1/g_2^2 and 1/g_Y^2 are the roots of
      x^2 - N_color^2 x + N_pair^2(N_quark - 1) = 0,
      namely x^2 - 9x + 20 = (x-4)(x-5).

(S4)  N_color^4 - 4 N_pair^2(N_quark - 1)
      = 81 - 80
      = 1.

(S5)  1/g_2^2 + 1/g_Y^2 - 1/g_3^2
      = 9 - 1
      = 8
      = dim(adj SU(N_color)).

(S6)  N_pair^2 + (N_quark - 1)
      = 4 + 5
      = 9
      = N_color^2.
```

The weak-angle cross-read is the same identity in normalized form:

```text
sin^2(theta_W)_bare = g_Y^2 / (g_2^2 + g_Y^2)
                    = 4/9
                    = N_pair^2 / N_color^2
                    = A^4,

cos^2(theta_W)_bare = g_2^2 / (g_2^2 + g_Y^2)
                    = 5/9
                    = (N_quark - 1) / N_color^2.
```

This is a lattice-scale bookkeeping identity. The retained low-energy
electroweak comparison remains the separate EW-normalization/running lane.

## Conditional Selector Lemma

For a generalized bookkeeping variable `d`, the retained EW form gives

```text
1/g_2^2 + 1/g_Y^2 = 2d+3.
```

If an additional selector requires this to equal `N_color^2`, and if one also
sets `N_color=d`, then

```text
2d + 3 = d^2
d^2 - 2d - 3 = 0
(d - 3)(d + 1) = 0.
```

The only non-negative solution is `d=3`.

This lemma is why the identity is scientifically useful: it exposes a compact
dimension/color compatibility condition. But the selector premise is not
derived in this note.

## Relation To Existing Support

`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`
already records the same bare EW sum as

```text
alpha_3(bare)/alpha_em(bare)
  = g_3^2 (1/g_2^2 + 1/g_Y^2)
  = 2d+3
  = 9.
```

This note adds the CKM structural-count cross-read:

```text
2d+3 = N_color^2,
(d+1)(d+2) = N_pair^2(N_quark-1),
N_pair^2 + (N_quark-1) = N_color^2.
```

So the new value is not another low-energy prediction. It is the exact
EW/CKM integer packaging of an already visible bare-coupling support surface.

## What This Claims

- The exact color-square identity `1/g_2^2 + 1/g_Y^2 = N_color^2` at the
  current retained lattice-scale values.
- The exact product, quadratic, unit-discriminant, adjoint-dimension, and
  normalized weak-angle forms above.
- The conditional selector lemma: if the color-square relation is promoted as
  a generalized `d=N_color` compatibility condition, it selects `d=3`.

## What This Does Not Claim

- It does not derive the retained EW bare couplings independently of
  `YT_EW_COLOR_PROJECTION_THEOREM.md`.
- It does not derive the CKM structural counts independently of the CKM atlas.
- It does not derive `d=3` or `N_color=3` as a new minimal-stack theorem.
- It does not cite or rely on support-tier `Cl(3) -> SM` embedding notes.
- It does not claim the bare `sin^2(theta_W)=4/9` is the observed low-energy
  value.

## Reproduction

```bash
python3 scripts/frontier_ckm_bare_ew_color_square_support.py
```

Expected result:

```text
TOTAL: PASS=32, FAIL=0
```

## Cross-References

- [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
- [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md)
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
- [`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`](FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md)
