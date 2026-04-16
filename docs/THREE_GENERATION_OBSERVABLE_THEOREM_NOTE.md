# Three-Generation Observable Theorem Note

**Date:** 2026-04-15
**Status:** exact support theorem on the retained three-generation / flavor surface
**Script:** `scripts/frontier_three_generation_observable_theorem.py`
**Authority role:** theorem-facing support note showing that the retained
`hw=1` triplet cannot be collapsed below three sectors without destroying the
current observable flavor package

## Safe statement

On the current package surface, the three retained `hw=1` sectors are not
merely present and unrootable. They are exact observable sectors of the
Hamiltonian:

- the exact lattice translation algebra separates `X1`, `X2`, `X3` by three
  distinct joint characters
- any translation-compatible `3 -> 2` quotient can only delete one whole
  sector; it cannot identify two sectors while preserving the observable
  algebra
- any two-generation flavor package has vanishing CP-odd Jarlskog invariant
  `J = 0`
- the promoted CKM package on the retained surface has `J > 0`

Therefore no consistent reduction / rooting / projection to fewer than three
sectors preserves the current observable flavor structure.

## Role in the package

This note is not the original three-generation claim surface. That remains
[THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md).

Its narrower job is to close the exact scientific point:

> why the retained triplet sectors are physically distinct sectors of the
> observable theory rather than removable label copies.

The package now has two complementary no-collapse layers:

1. **Algebraic / full-space no-rooting**
   [frontier_generation_rooting_undefined.py](./../scripts/frontier_generation_rooting_undefined.py)
   proves that Cl(3)-preserving taste removal is not a legal operation on the
   full `C^8` taste surface.
2. **Observable / retained-sector no-collapse**
   [frontier_three_generation_observable_theorem.py](./../scripts/frontier_three_generation_observable_theorem.py)
   proves that even on the retained `hw=1` physical sector, any collapse below
   three sectors destroys the observable flavor package.

## Input surface

This theorem uses only current retained package ingredients:

1. the exact `hw=1` triplet on the physical `Z^3` surface
2. the physical-lattice boundary isolated in
   [GENERATION_AXIOM_BOUNDARY_NOTE.md](./GENERATION_AXIOM_BOUNDARY_NOTE.md)
3. the promoted CKM closure package in
   [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)

No observed quark masses, fitted generation labels, or new continuum flavor
assumptions are introduced here.

## Assumptions and dependency boundary

This note is exact **on a stated retained package surface**. Its assumptions
should be read narrowly:

1. **Physical-lattice reading.**
   The `hw=1` triplet is retained as physical sector structure on the same
   physical-lattice surface used throughout the current matter package.
2. **Admissible collapse maps.**
   A putative reduction to fewer than three sectors is called admissible only
   if it is a linear surjection

   `Q : H_hw=1 -> H_red`

   that intertwines the exact retained translation algebra:

   `Q T_mu = T'_mu Q`, for `mu in {x,y,z}`,

   for some quotient representation `T'_mu` on `H_red`.
3. **Flavor witness surface.**
   The contradiction to two sectors uses the already promoted CKM package as
   the retained flavor witness. This note does **not** re-derive that package;
   it uses only the exact retained fact that the package gives `J > 0`.

So the theorem is:

- exact as a no-collapse theorem on the retained observable surface
- dependent on the promoted CKM package only through the witness statement
  `J > 0`
- not a standalone replacement for the CKM closure note or the physical-lattice
  boundary note

## Theorem statement

> **Three-Generation Observable No-Collapse Theorem.**
> On the retained `hw=1` sector `H_hw=1 = span{X1, X2, X3}`, the exact lattice
> translations act by three distinct joint characters
>
> - `X1 : (-1, +1, +1)`
> - `X2 : (+1, -1, +1)`
> - `X3 : (+1, +1, -1)`.
>
> Hence the retained translation commutant on `H_hw=1` has dimension `3` and
> is exhausted by the three sector projectors. In particular, the translation
> observable algebra has exact rank-1 projectors onto the three sectors. Any
> translation-compatible quotient from `H_hw=1` to a
> two-dimensional quotient space must have a one-dimensional invariant kernel,
> and the only such invariant lines are `span(X1)`, `span(X2)`, `span(X3)`.
> Therefore a legal `3 -> 2` quotient can only delete one whole sector; it
> cannot identify two sectors while preserving the observable algebra.
>
> But every two-generation flavor package has `J = 0`, whereas the promoted
> CKM package on the retained surface has `J > 0`.
>
> Therefore no consistent reduction / rooting / projection to fewer than three
> sectors preserves the current observable flavor package.

## Proof skeleton

### 1. Exact translation characters

On the retained `hw=1` basis, the three elementary translations act as:

- `T_x = diag(-1, +1, +1)`
- `T_y = diag(+1, -1, +1)`
- `T_z = diag(+1, +1, -1)`.

So the three sectors are already separated by exact Hamiltonian observables.

### 2. Exact sector projectors

For a sign triple `(s_x, s_y, s_z)`, the joint projector is

`P(s) = ((I + s_x T_x)/2) ((I + s_y T_y)/2) ((I + s_z T_z)/2)`.

Only three sign triples give nonzero projectors, and they are exactly the
rank-1 projectors onto `X1`, `X2`, `X3`.

Equivalently, the commutant of `{T_x, T_y, T_z}` inside `End(H_hw=1)` has
dimension `3` and is spanned by those three rank-1 projectors. There are no
off-diagonal inter-sector intertwiners inside the exact retained translation
algebra.

### 3. Quotient classification

Any translation-compatible quotient must have translation-invariant kernel.
Because the only common translation eigenlines are the three sector lines,
every legal `3 -> 2` quotient can only delete one sector. Identification
kernels such as `X1 - X2` are not translation-invariant and therefore do not
define legal observable quotients.

This is the exact place where the admissibility definition matters: the theorem
does not classify arbitrary nonlinear or non-observable identifications. It
classifies reductions that preserve the exact retained translation algebra of
the physical sector.

### 4. Two-generation CP witness vanishes

For a generic `U(2)` matrix,

`U_11 U_22 U_12* U_21* = -cos^2(theta) sin^2(theta) in R`,

so the CP-odd plaquette invariant has zero imaginary part. Therefore every
two-generation flavor package has `J = 0`.

### 5. Retained CKM witness is nonzero

The promoted CKM package on the retained surface gives

- `|V_us| = 0.227269`
- `|V_cb| = 0.042174`
- `|V_ub| = 0.003913`
- `delta = 65.905 deg`
- `J = 3.331e-5 > 0`.

So deleting one full sector leaves a two-generation quotient that cannot carry
the retained flavor witness.

## What this closes

This closes the exact point that remained implicit in the earlier
three-generation discussion:

- the retained triplet sectors are not just structural placeholders
- they are the minimal physical sector count required by the current
  observable flavor package

So the package no longer relies only on:

- "rooting is undefined on the full taste space"

It now also has:

- "observable flavor closure fails immediately if the sector count is reduced
  below three."

## What this does not close

This note does **not** claim:

- a full `1+1+1` first-principles mass hierarchy
- a standalone purely spatial chirality theorem
- a complete neutrino-generation closure

Those remain separate tasks.

It also does **not** claim a theorem about arbitrary sector-relabeling maps
outside the retained observable-algebra surface. The theorem is specifically
about admissible observable-preserving reductions.

## Paper-safe wording

> On the retained physical-lattice surface, the three `hw=1` sectors are exact
> observable sectors rather than removable copies. The translation algebra
> separates them by distinct joint characters, so any observable-preserving
> quotient below three sectors can only delete a whole sector. But every
> two-generation flavor package has vanishing CP-odd Jarlskog invariant,
> whereas the retained CKM package has `J > 0`. Therefore the current flavor
> package itself requires three physical sectors.

## Validation

- [frontier_three_generation_observable_theorem.py](./../scripts/frontier_three_generation_observable_theorem.py)

Current main-branch runner state:

- `frontier_three_generation_observable_theorem.py`: `PASS=37`, `FAIL=0`
