# DM Neutrino `Z_3`-Circulant Mass-Basis No-Go

**Date:** 2026-04-15  
**Status:** exact no-go theorem on the physical leptogenesis tensor for the
entire exact `Z_3`-covariant circulant bridge class  
**Script:** `scripts/frontier_dm_neutrino_z3_circulant_mass_basis_nogo.py`

## Question

Suppose the invented phase-lift family is promoted to exact source transfer.

Then the local bridge lands on the exact `Z_3`-covariant circulant family

`K = d I + r (chi S + chi^* S^2)`

with `chi` a true `Z_3` character.

Does that already close the physical leptogenesis CP kernel in the basis where
the right-handed Majorana mass matrix is diagonal?

## Bottom line

No.

Every exact `Z_3`-covariant circulant kernel is diagonalized by the Fourier
matrix `U_Z3` with a **real** diagonal spectrum.

And on the current denominator stack, the right-handed Majorana matrix in that
same `Z_3` basis is

`M_R = [[A,0,0],[0,eps,B],[0,B,eps]]`,

so its remaining diagonalization is only a **real orthogonal rotation** inside
the doublet block.

Therefore the kernel in the heavy-neutrino mass basis stays real symmetric.
Hence

`Im[(K_mass)_{1j}^2] = 0`

for all `j`.

So the entire exact `Z_3`-covariant circulant bridge class, including the
full-source branch `chi = omega`, is still a no-go for the physical standard
leptogenesis tensor on the current stack.

## Why this matters

This is harsher than the old blocker wording.

The branch can no longer honestly say:

- "if we just derive `lambda = 1`, the odd-slot problem closes"

It now has to say:

- exact character transfer does close `lambda`
- but the whole exact circulant family still dies in the heavy-neutrino mass
  basis

So the odd-circulant family is at best a local structural guide. It is not the
final physical leptogenesis texture.

## The actual remaining object

The missing object is now stricter:

- not a free `lambda`
- not an exact `Z_3`-covariant circulant bridge

It must be a **non-circulant**, right-sensitive, CP-carrying bridge that
survives as a genuinely complex off-diagonal object after moving to the
heavy-neutrino mass basis.

That is much closer in spirit to the CKM tensor-slot mechanism than to a pure
character lift.

## What this closes

This closes the whole exact circulant rescue class for physical leptogenesis CP
on the current denominator stack.

## Command

```bash
python3 scripts/frontier_dm_neutrino_z3_circulant_mass_basis_nogo.py
```
