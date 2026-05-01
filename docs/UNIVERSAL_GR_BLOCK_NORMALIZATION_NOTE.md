# Universal GR Block Normalization Note

**Status:** support - structural or confirmatory support note
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** direct universal block split only  
**Ownership:** universal block normalization / sign only

## Verdict

Sign conventions, spectral normalization, and invariant ratios inside the
shift/shear blocks are not enough to finish direct universal localization.

The strongest exact statement supported by the current universal stack is
only orbit-normalization:

`Pi_A1` is canonical, the `E \oplus T1` complement is not.

After the canonical `A1` split, the complement remains an `SO(3)` orbit
bundle. Normalizing the shift/shear blocks can fix scale, sign, and a block
ratio, but it does not canonically choose a complement section.

## Exact block split

The universal `3+1` polarization basis already splits into:

- `Pi_A1`: lapse + spatial trace;
- `Pi_shift`: the three shift components;
- `Pi_shear`: the five traceless/shear components.

The invariant core is exact:

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

That projector commutes with the valid spatial rotations on the current
atlas. The complement does not.

## What normalization can do

Within the direct universal complement, the following quantities are exact
orbit invariants:

- the shift block norm;
- the shear block norm;
- their ratio `rho = ||shift|| / ||shear||` when both blocks are nonzero;
- sign conventions on a chosen anchor component.

So block normalization can produce a canonical-looking *scale* convention.
It can also remove a discrete `Z_2` sign choice on the chosen anchor. It
cannot remove the connected complement orbit.

## What normalization cannot do

The current atlas does **not** provide a canonical section of the
complement bundle.

More precisely:

1. the normalized shift block still rotates inside its `SO(3)` orbit;
2. the normalized shear block still rotates inside its `SO(3)` orbit;
3. the invariant ratio `rho` is preserved by valid frame changes;
4. none of those facts choose a preferred complement axis;
5. therefore no canonical `Pi_curv` follows from block normalization alone.

The direct universal route is therefore orbit-canonical, not
section-canonical.

## Time does not rescue the split

This note does not introduce the phase-lift `lambda` family. The direct
universal route already bypasses that ambiguity.

The remaining ambiguity here is different:

- the `A1` core is fixed;
- the `E \oplus T1` complement is still an `SO(3)` orbit bundle;
- no current invariant in the atlas distinguishes one complement section
  from another.

The time-lift factor is already frame-independent on the direct universal
route, so it does not break the complement orbit.

## Strongest exact normalization theorem

The strongest exact theorem currently supported is:

> Block normalization canonically fixes the invariant `A1` core and the
> scalar shift/shear block ratios, but it does not canonically section the
> `E \oplus T1` complement. The exact residual ambiguity is the connected
> `SO(3)` orbit on the complement.

Equivalently:

> sign conventions, spectral normalization, and invariant ratios are enough
> to normalize the complement orbit, but not enough to finish direct
> universal localization.

## Honest status

The current direct universal route is:

- exact at the scalar observable level;
- exact at the `3+1` kinematic lift level;
- exact at the symmetric quotient-kernel level;
- exact at the invariant `A1` projector level;
- exact at the block-normalized orbit level;
- still blocked at the canonical complement-frame level.

So the exact remaining ambiguity is:

`SO(3)`

on the direct universal complement.
