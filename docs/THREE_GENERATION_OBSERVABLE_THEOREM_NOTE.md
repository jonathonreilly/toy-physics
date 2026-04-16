# Three-Generation Observable Theorem Note

**Date:** 2026-04-15
**Status:** exact conditional support theorem on the retained three-generation / flavor surface
**Script:** `scripts/frontier_three_generation_observable_theorem.py`
**Authority role:** theorem-facing support note showing that the retained
`hw=1` triplet cannot be reduced below three sectors inside the exact retained
translation-observable class once the retained CKM witness is imposed

## Safe statement

On the current retained package surface, the three `hw=1` sectors are exact
observable sectors of the Hamiltonian. More precisely:

- the exact lattice translation algebra separates `X1`, `X2`, `X3` by three
  distinct joint characters
- any quotient that claims to preserve those exact translation observables
  must intertwine them, and within that class a `3 -> 2` quotient can only
  delete one whole sector
- any two-generation flavor package has vanishing CP-odd Jarlskog invariant
  `J = 0`
- the promoted CKM package contributes the retained witness `J > 0`

Therefore, conditional on the retained CKM witness, no
translation-observable-preserving reduction to fewer than three sectors
reproduces the current retained flavor package.

## Role in the package

This note is not the original three-generation claim surface. That remains
[THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md).

Its narrower job is to close the exact scientific point:

> why the retained triplet sectors are physically distinct sectors of the
> observable theory, and why the retained CKM witness is incompatible with any
> exact observable-preserving collapse below three sectors.

The package now has two complementary three-sector protection layers:

1. **Algebraic / full-space no-rooting**
   [frontier_generation_rooting_undefined.py](./../scripts/frontier_generation_rooting_undefined.py)
   proves that Cl(3)-preserving taste removal is not a legal operation on the
   full `C^8` taste surface.
2. **Observable / retained-sector incompatibility**
   [frontier_three_generation_observable_theorem.py](./../scripts/frontier_three_generation_observable_theorem.py)
   proves that on the retained `hw=1` physical sector, any quotient that
   preserves the exact translation observables is incompatible with the
   retained CKM witness once the sector count is reduced below three.

## Input surface

This theorem uses only current retained package ingredients:

1. the exact `hw=1` triplet on the physical `Z^3` surface
2. the physical-lattice boundary isolated in
   [GENERATION_AXIOM_BOUNDARY_NOTE.md](./GENERATION_AXIOM_BOUNDARY_NOTE.md)
3. the promoted CKM closure package in
   [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)

No observed quark masses, fitted generation labels, or new continuum flavor
assumptions are introduced here.

The role of item 3 is explicitly conditional: this note does not use the CKM
closure package to derive the existence of three sectors from scratch. It uses
the already promoted retained-surface witness `J > 0` to test whether an
admissible two-sector quotient could still carry the current flavor package.

## Assumptions and dependency boundary

This note is exact **on a stated retained package surface**. Its assumptions
should be read narrowly:

1. **Physical-lattice reading.**
   The `hw=1` triplet is retained as physical sector structure on the same
   physical-lattice surface used throughout the current matter package.
2. **Admissible observable-preserving quotients.**
   A putative reduction to fewer than three sectors is called admissible only
   if it is a linear surjection

   `Q : H_hw=1 -> H_red`

   and if the exact retained translation observables are claimed to descend to
   the quotient. On this note's surface, that observable-preservation claim is
   exactly the existence of quotient operators `T'_mu` satisfying

   `Q T_mu = T'_mu Q`, for `mu in {x,y,z}`,

   for some quotient representation `T'_mu` on `H_red`.
   This note proves a classification theorem only for that exact
   translation-intertwining class. Coarse-grained or non-observable reductions
   that do not preserve the retained translation algebra are outside scope.
3. **Flavor witness surface.**
   The contradiction to two sectors uses the already promoted CKM package as a
   retained-surface witness. This note does **not** re-derive that package or
   use it to prove that three sectors exist from scratch; it proves the
   conditional statement that, once the retained witness `J > 0` is imposed,
   no admissible two-sector quotient can reproduce it.

So the theorem is:

- exact as a quotient-classification theorem on the retained observable
  surface
- exact as a conditional incompatibility theorem between any admissible
  two-sector quotient and the retained witness `J > 0`
- not a standalone replacement for the CKM closure note or the physical-lattice
  boundary note

## Theorem statement

> **Conditional Three-Generation Observable Incompatibility Theorem.**
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
> quotient that preserves those exact retained translation observables must
> therefore be a translation-intertwining quotient. Any such quotient from
> `H_hw=1` to a two-dimensional quotient space must have a one-dimensional
> invariant kernel, and the only such invariant lines are
> `span(X1)`, `span(X2)`, `span(X3)`.
> Therefore a legal `3 -> 2` quotient can only delete one whole sector; it
> cannot identify two sectors while preserving the observable algebra.
>
> Every two-generation flavor package has `J = 0`. If one also imposes the
> retained CKM witness `J > 0` from the promoted CKM package on the same
> retained surface, then the delete-one-sector quotient is incompatible with
> that witness.
>
> Therefore, conditional on the retained CKM witness, no admissible
> translation-observable-preserving reduction to fewer than three sectors
> reproduces the current retained flavor package.

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

Any admissible observable-preserving quotient must have translation-invariant
kernel, because the exact retained translation observables are required to
descend to the quotient. Because the only common translation eigenlines are
the three sector lines, every legal `3 -> 2` quotient can only delete one
sector. Identification kernels such as `X1 - X2` are not
translation-invariant and therefore do not define legal observable quotients.

This is the exact place where the admissibility definition matters: the theorem
does not classify arbitrary nonlinear, coarse-grained, or non-observable
identifications. It classifies reductions that preserve the exact retained
translation algebra of the physical sector.

### 4. Two-generation CP witness vanishes

For a generic `U(2)` matrix,

`U_11 U_22 U_12* U_21* = -cos^2(theta) sin^2(theta) in R`,

so the CP-odd plaquette invariant has zero imaginary part. Therefore every
two-generation flavor package has `J = 0`.

### 5. Conditional retained CKM witness is nonzero

The promoted CKM package on the retained surface gives

- `|V_us| = 0.227269`
- `|V_cb| = 0.042174`
- `|V_ub| = 0.003913`
- `delta = 65.905 deg`
- `J = 3.331e-5 > 0`.

This is not used here as an independent derivation of three sectors. It is used
only as the retained witness that an admissible delete-one-sector quotient
would have to reproduce. But every such quotient is two-generation and
therefore has `J = 0`, so it cannot carry the retained witness.

## What this closes

This closes the exact point that remained implicit in the earlier
three-generation discussion:

- the retained triplet sectors are not just structural placeholders
- within the exact translation-observable class, they are the minimal sector
  count compatible with the retained CKM witness

So the package no longer relies only on:

- "rooting is undefined on the full taste space"

It now also has:

- "the retained CKM witness is incompatible with any admissible observable
  quotient below three sectors."

## What this does not close

This note does **not** claim:

- an independent first-principles derivation of three generations without the
  retained CKM witness
- a full `1+1+1` first-principles mass hierarchy
- a standalone purely spatial chirality theorem
- a complete neutrino-generation closure

Those remain separate tasks.

It also does **not** claim a theorem about arbitrary sector-relabeling maps or
effective coarse-grained reductions outside the retained observable-algebra
surface. The theorem is specifically about admissible
translation-observable-preserving reductions.

## Paper-safe wording

> On the retained physical-lattice surface, the translation algebra already
> separates the three `hw=1` sectors by distinct joint characters. Any quotient
> that preserves those exact translation observables can therefore only delete
> a whole sector, not identify two sectors. Since every two-generation flavor
> package has vanishing CP-odd Jarlskog invariant, the retained CKM witness
> `J > 0` is incompatible with any such quotient. Thus, conditional on the
> retained CKM package, the current flavor surface requires three sectors
> within the exact translation-observable class.

## Validation

- [frontier_three_generation_observable_theorem.py](./../scripts/frontier_three_generation_observable_theorem.py)

Current main-branch runner state:

- `frontier_three_generation_observable_theorem.py`: `PASS=37`, `FAIL=0`
