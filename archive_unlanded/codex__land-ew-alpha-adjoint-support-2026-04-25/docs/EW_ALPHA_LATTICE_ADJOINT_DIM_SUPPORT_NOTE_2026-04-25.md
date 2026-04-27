# EW Alpha Lattice Adjoint-Dimension Support Note

Date: 2026-04-25

Status: exact EW lattice-scale support corollary on the retained
EW-normalization package. This note does not promote a new retained theorem,
does not change the retained `M_Z` electroweak matching lane, and does not
claim a direct low-energy observable.

Primary verifier:

```bash
python3 scripts/frontier_ew_alpha_lattice_adjoint_dim_support.py
```

## Claim

On the same bare electroweak bookkeeping used by the retained EW normalization
lane, the retained values

```text
g_2^2 = 1/(d + 1) = 1/4,
g_Y^2 = 1/(d + 2) = 1/5,
d = 3,
N_color = 3
```

give the exact lattice-surface electromagnetic combination

```text
e_lattice^2 = g_2^2 g_Y^2 / (g_2^2 + g_Y^2) = 1/9 = 1/N_color^2.
```

If the retained leading `R_conn = (N_color^2 - 1)/N_color^2 = 8/9` color
projection factor is read on the same lattice-scale support surface, the
corresponding support value is

```text
alpha_EW,Rconn(lattice)
  = (1/R_conn) e_lattice^2/(4 pi)
  = 1 / (4 pi (N_color^2 - 1))
  = 1 / (4 pi dim(adj SU(N_color)))
  = 1/(32 pi).
```

The useful science is the compact support identity:

```text
4 pi alpha_EW,Rconn(lattice) dim(adj SU(3)) = 1.
```

## Authority Boundary

This card uses existing retained/package facts but remains support-only.

1. `YT_EW_COLOR_PROJECTION_THEOREM.md` carries the retained EW normalization
   lane, including the bare `g_2^2 = 1/4`, `g_Y^2 = 1/5` bookkeeping and the
   leading `R_conn = 8/9` color-projection correction.
2. `MINIMAL_AXIOMS_2026-04-11.md` carries the accepted `Z^3` spatial
   substrate, hence `d = 3`.
3. `CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md` packages
   the retained structural counts `N_pair = 2`, `N_color = 3`,
   `N_quark = 6` on the CKM atlas surface.
4. `FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`
   already records the sibling support identities
   `e_lattice^2 = 1/9`, `alpha_em(bare) = 1/(36 pi)`, and
   `alpha_3(bare)/alpha_em(bare) = 9`.

Therefore this note is a same-surface algebraic support corollary. It should
be cited with the retained EW lane, not as an independent retained observable.

## Derivation

The electroweak mixing relation on the bare support surface is

```text
1/e_lattice^2 = 1/g_2^2 + 1/g_Y^2.
```

Equivalently,

```text
e_lattice^2
  = g_2^2 g_Y^2 / (g_2^2 + g_Y^2)
  = (1/4)(1/5) / (1/4 + 1/5)
  = (1/20) / (9/20)
  = 1/9.
```

With `N_color = 3`, this is

```text
e_lattice^2 = 1/N_color^2.
```

The bare support alpha value is

```text
alpha_em,bare = e_lattice^2/(4 pi) = 1/(36 pi).
```

The retained leading color-projection factor is

```text
R_conn = (N_color^2 - 1)/N_color^2 = 8/9.
```

Applying that same support-side correction gives

```text
alpha_EW,Rconn(lattice)
  = alpha_em,bare / R_conn
  = (1/(4 pi N_color^2)) (N_color^2/(N_color^2 - 1))
  = 1/(4 pi (N_color^2 - 1)).
```

Since `dim(adj SU(N)) = N^2 - 1`, the framework value is

```text
alpha_EW,Rconn(lattice)
  = 1/(4 pi dim(adj SU(N_color)))
  = 1/(4 pi * 8)
  = 1/(32 pi).
```

## What This Does Not Claim

- It does not replace the retained `YT_EW_COLOR_PROJECTION_THEOREM.md`
  prediction path for `sin^2(theta_W)`, `1/alpha_EM`, `g_1(v)`, or `g_2(v)`.
- It does not assert that `1/(32 pi)` is the observed `alpha_EM(M_Z)`.
- It does not remove the `O(1/N_color^4)` caveat attached to the retained
  leading `R_conn` analysis.
- It does not derive `d = 3`, `N_color = 3`, or `R_conn = 8/9`; those are
  inherited package inputs.
- It does not use the inconsistent alternative route
  `g_2^2 cos^2(theta_W) = (1/4)(5/9) = 5/36`; that expression is not equal
  to `1/9` and is not part of this support card.

## Comparator Role

Numerically,

```text
alpha_EW,Rconn(lattice) = 1/(32 pi) = 0.009947...
alpha_EM(M_Z)           = 1/127.9   = 0.007819...
```

The ratio is about `1.27`. This is not a failure of the support identity: the
support identity sits at the lattice bookkeeping surface, while the retained
EW lane supplies the running/projection bridge to the `M_Z` comparator.

## Summary

The landed support content is:

```text
(S1) e_lattice^2 = 1/N_color^2 = 1/9.

(S2) alpha_em,bare = 1/(4 pi N_color^2) = 1/(36 pi).

(S3) alpha_EW,Rconn(lattice)
     = 1/(4 pi (N_color^2 - 1))
     = 1/(4 pi dim(adj SU(N_color)))
     = 1/(32 pi).
```

This is worth keeping because it exposes the existing EW normalization and
`R_conn` support package in a compact adjoint-dimension form, while preserving
the correct status boundary.
