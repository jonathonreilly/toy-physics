# Koide Positive-Parent Axis Obstruction Note

**Date:** 2026-04-18
**Status:** exact obstruction note on the candidate `√m` lane, now sharpened by
the companion full-lattice Schur-inheritance result
**Runner:** `scripts/frontier_koide_positive_parent_axis_obstruction.py`

## Safe statement

Suppose one tries to realize the charged-lepton masses through a positive
`C_3[111]`-covariant parent operator `M` on the retained `hw=1` triplet, with
principal square root `Y = M^(1/2)` carrying the Koide amplitudes.

On the current retained charged-lepton surface, this route is **not yet a
physical closure**, because:

1. any positive `C_3`-covariant parent is circulant and therefore diagonalized by
   the Fourier/character basis;
2. the retained charged-lepton readout requires masses to be the **diagonal
   entries in the axis basis** (`U_e = I_3`);
3. the only matrices that are both circulant and axis-diagonal are scalar
   multiples of `I_3`.

Therefore any **nondegenerate** positive `C_3[111]` parent necessarily lives in
the forbidden eigenvalue channel on the current retained surface.

This note is the smallest-carrier version of the obstruction. The companion
[KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md](./KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md)
shows that the same obstruction survives any larger full-carrier completion as
long as the reduction back to the charged-lepton lane is the standard
`C_3`-equivariant Schur/effective-operator map. So the real hypothesis is not
"bare `hw=1` only"; it is "same reduction class + same axis readout."

## Proof

Write a general Hermitian circulant as
```
M = a·I + b·C + b̄·C².
```
In the axis basis this has the form
```
M = [[a,    b̄,  b ],
     [b,    a,   b̄],
     [b̄,   b,   a ]].
```
If `M` is axis-diagonal, the off-diagonal entries must vanish:
```
b = 0.
```
Then
```
M = a I.
```
So

> `M` circulant and axis-diagonal  ⟺  `M` is a scalar multiple of `I`.

Hence no nontrivial charged-lepton hierarchy can arise from a positive
`C_3`-covariant parent while keeping the current axis-diagonal readout.

## Fourier-basis form

Conversely, for any positive eigenvalue triple `(m_1, m_2, m_3)`, the unique
positive `C_3`-covariant parent with those eigenvalues is
```
M = F · diag(m_1, m_2, m_3) · F^†,
```
where `F` is the `C_3` Fourier matrix.

This matrix is always Hermitian and `C_3`-covariant. But unless
`m_1 = m_2 = m_3`, it has nonzero axis-basis off-diagonal entries. So the
positive-parent route automatically enters the eigenvalue channel.

## Relation to existing charged-lepton authorities

This obstruction matches the existing April 17 higher-order theorem:

- the eigenvalue channel can show a near-match to the observed `√m` direction;
- but the retained charged-lepton readout excludes that channel because
  `U_e = I_3`;
- physical masses are the axis-basis diagonal entries, not eigenvalues of a
  non-diagonal operator.

So the new `√m` amplitude principle does sharpen `P1`, but it also shows that
the positive-parent route alone is insufficient on the current retained surface.
And the full-lattice Schur-inheritance theorem shows that merely enlarging the
carrier without changing the reduction/readout class is still insufficient.

## Consequence for the science stack

The open problem is sharper than before:

- not “why `√m`?” in the abstract;
- not even only “which positive parent `M`?”;
- but
  **which new retained readout/basis primitive lets a nontrivial positive
  `C_3[111]` parent become physical despite the current `U_e = I_3` axis
  readout?**

More carefully, one now needs at least one of:

- a new readout primitive,
- a new non-Schur or non-`C_3`-equivariant reduction from the larger physical
  carrier,
- a charged-lepton carrier not reducible to an isolated `T_1` target,
- or a controlled charged-lepton-specific breaking of strict `C_3[111]`
  covariance.

This means the `P1` lane is now tightly coupled to the already-known
eigenvalue-channel obstruction.

## What this does not claim

- It does **not** prove that no future retained extension can realize the
  positive-parent route.
- It does **not** rule out a new readout primitive or a controlled breaking of
  the current axis-diagonal `U_e = I_3` readout.
- It does **not** alter the present retained charged-lepton verdict, which
  remains the bounded April 17 package.
