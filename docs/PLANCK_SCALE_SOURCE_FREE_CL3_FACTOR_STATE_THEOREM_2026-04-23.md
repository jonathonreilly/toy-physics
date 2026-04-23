# Planck-Scale Source-Free `Cl(3)` Factor State Theorem

**Date:** 2026-04-23  
**Status:** branch-local direct theorem candidate on the last Planck blocker  
**Audit runner:** `scripts/frontier_planck_source_free_cl3_factor_state_theorem.py`

## Question

Can the bare-factor source-free state law

`rho_sf = I_2 / 2`

be derived from the accepted local algebra `Cl(3)` itself rather than from the
support-only one-axiom Hilbert note?

## Bottom line

Yes, in the following exact branch-local form.

The accepted minimal stack fixes the physical local algebra as `Cl(3)`:
[MINIMAL_AXIOMS_2026-04-11.md](./MINIMAL_AXIOMS_2026-04-11.md).

Over the standard spinor carrier, `Cl(3)` is the full two-level matrix algebra
`M_2(C)` up to exact algebra isomorphism. A source-free local state on the bare
local algebra may not depend on a chosen spinor frame / matrix presentation, so
it must be invariant under exact inner automorphisms

`A -> U A U^dagger`.

That invariance forces the unique normalized state

`rho_sf = I_2 / 2`.

So the factor law needed by the direct Planck route can be tied much more
closely to the accepted local algebra than before.

## Why this improves the lane

The previous branch-local state-law theorem used the bare `C^2` factor and
unitary no-datum invariance. Hostile review correctly noted that this looked
like a fresh Hilbert-side state-selection principle.

This note moves one step more native:

- accepted local algebra is `Cl(3)`;
- `Cl(3)` carries no preferred source-free spinor frame;
- source-free state must therefore be invariant under exact local inner
  automorphisms;
- on `M_2(C)`, that forces `I_2/2`.

So the remaining branch-local burden is reduced further: the factor law is now
anchored directly in the accepted local algebra rather than in a support-only
Hilbert reformulation.

## Inputs

This note uses:

- [MINIMAL_AXIOMS_2026-04-11.md](./MINIMAL_AXIOMS_2026-04-11.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [PLANCK_SCALE_SOURCE_FREE_LOCAL_FRAME_WELL_DEFINEDNESS_THEOREM_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_LOCAL_FRAME_WELL_DEFINEDNESS_THEOREM_2026-04-23.md)

## Setup

Take the accepted local algebra

`A_loc = Cl(3)`.

On its spinor carrier this is represented as the full two-level matrix algebra

`A_loc ~= M_2(C)`.

Call a local state `rho_sf` **source-free on the bare local algebra** if:

1. it is positive and normalized;
2. it depends on no added local source datum;
3. it is unchanged by exact inner automorphisms of the bare local algebra.

The last line is the native algebraic form of:

> source-free local physics may not depend on a chosen spinor frame.

## Theorem 1: source-free `Cl(3)` factor state is tracial

Let `rho` be a normalized positive state on the spinor carrier of `Cl(3)` and
assume

`U rho U^dagger = rho`

for every unitary implementing an exact inner automorphism of `M_2(C)`.

Then

`rho = I_2 / 2`.

### Proof

The invariance condition implies `rho` commutes with the full inner
automorphism image, hence with all of `M_2(C)`.

Therefore `rho` lies in the center of `M_2(C)`, so

`rho = lambda I_2`.

Normalization gives

`Tr(rho) = 2 lambda = 1`,

so

`lambda = 1/2`.

Therefore

`rho = I_2 / 2`.

## Corollary 1: the factor law used by the direct Planck route is now native to `Cl(3)`

The previously promoted bare-factor law

`rho_sf(C^2) = I_2/2`

can now be read instead as

`rho_sf(Cl(3) factor) = I_2/2`.

That is a stronger anchoring because it uses the accepted local algebra itself.

## Honest status

This does **not** by itself finish the entire Planck lane.

What it does is remove one major hostile-review objection: the two-level
source-free factor law no longer has to be presented as generic Hilbert-side
guesswork. It can be presented as the source-free state law of the accepted
local algebra `Cl(3)`.

The remaining branch-local issue is then the exact lift from those source-free
local factors to the full time-locked cell.
