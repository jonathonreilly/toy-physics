# Majorana Background-Normalized Local Response Theorem

**Date:** 2026-04-15  
**Status:** exact local background-normalization theorem on the admitted
Majorana Nambu family  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_background_normalization_theorem.py`

## Question

After the local quadratic comparator theorem, does the admitted Majorana Nambu
family still lack a **canonically fixed endpoint/background normalization**, or
does the retained normal slice already provide it?

This is the constructive question left open by the earlier blocker chain:

- the local Nambu family already has the radial bosonic observable
  `W_N = log ||s|| + const`
- the local Nambu block already has the exact non-homogeneous comparator
  `Q_2 = ||s||^2`
- the old necessity wording said the branch still needed either a new
  non-homogeneous comparator or a canonically fixed background normalization

So the honest next move is:

> is the retained normal slice itself already the missing canonical background?

## Bottom line

Yes, on the exact local block.

On the admitted local Nambu family, write the active kernel as

`H(z,x,y) = z sigma_z + x sigma_x + y sigma_y`

with retained normal baseline

`H_0(z) = z sigma_z`.

Then the exact **background-normalized local bosonic response** is

`W_rel = (1/2) log(|det H| / |det H_0|) = (1/2) log(1 + rho^2)`

and the exact **background-normalized local quadratic comparator** is

`Q_rel = (Q_2(H) - Q_2(H_0)) / z^2 = rho^2`

where

`rho^2 = (x^2 + y^2) / z^2`.

So the branch no longer lacks a local non-homogeneous comparator or a local
background normalization. It now has both, exactly, on the admitted Majorana
source family.

What remains open is narrower:

1. a theorem that picks a finite nonzero point on this already-normalized
   response curve
2. the lift of that point-selection law to the full three-generation
   `Z_3` texture

## Inputs

This theorem combines:

- [NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md)
- [NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_NAMBU_RADIAL_OBSERVABLE_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_RADIAL_OBSERVABLE_NOTE.md)
- [NEUTRINO_MAJORANA_NAMBU_QUADRATIC_COMPARATOR_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_QUADRATIC_COMPARATOR_NOTE.md)

Those notes already prove:

1. the admitted local source family is the pseudospin triplet
   `span{J_x, J_y, J_z}`
2. the genuinely new source increment is the pure-pairing ray `mu J_x` up to
   rephasing
3. the positive local bosonic observable on that family is radial:
   `W_N = log ||s|| + const`
4. the unique minimal nontrivial polynomial spectral invariant on the active
   local block is `Q_2 = ||s||^2`

So the remaining constructive question is whether the retained normal slice
already supplies the missing reference surface.

## Exact theorem

### 1. The retained normal slice gives a canonical local baseline

On the admitted local Nambu block, the retained charge-zero direction is
exactly `J_z`.

So once the genuinely new source increment has been isolated in the transverse
pairing plane, the local active kernel splits exactly into:

- a retained normal baseline `z sigma_z`
- a genuinely new pairing increment `x sigma_x + y sigma_y`

That is already the canonical old/new split on the exact local block.

### 2. The relative bosonic generator is exact and additive-constant free

The active-block determinant is

`|det H(z,x,y)| = z^2 + x^2 + y^2`.

Therefore the exact relative bosonic generator against the retained baseline is

`W_rel = (1/2) log(|det H| / |det H_0|) = (1/2) log((z^2 + x^2 + y^2)/z^2)`

which simplifies to

`W_rel = (1/2) log(1 + rho^2)`

with

`rho^2 = (x^2 + y^2) / z^2`.

So the additive ambiguity of the raw logarithmic generator disappears once the
retained normal baseline is divided out.

### 3. The relative quadratic comparator is exact

The local quadratic comparator theorem already gives

`Q_2(H) = z^2 + x^2 + y^2`.

Subtracting the retained baseline and dividing by `z^2` gives

`Q_rel = (Q_2(H) - Q_2(H_0)) / z^2 = rho^2`.

So the same local block now carries both:

- a background-normalized bosonic response `W_rel = (1/2) log(1 + rho^2)`
- a background-normalized non-homogeneous comparator `Q_rel = rho^2`

### 4. The relative response is rephasing-invariant

Local `nu_R` rephasing rotates the pairing plane

`(x,y) -> (x',y')`

with fixed transverse radius `x^2 + y^2`.

So both `W_rel` and `Q_rel` depend only on `rho`, not on the arbitrary phase
inside the pairing plane.

### 5. The remaining gap is now finite-point selection, not comparator existence

The background-normalized local response curve is

`W_rel(rho) = (1/2) log(1 + rho^2)`

with comparator

`Q_rel(rho) = rho^2`.

Both are strictly monotone for `rho > 0`.

So the branch now has the exact normalized local response curve, but it still
does not yet have the theorem that selects a finite nonzero point on that
curve.

## The theorem-level statement

**Theorem (Background-normalized local Majorana response on the admitted
Nambu family).**
Assume:

1. the admitted local Nambu-complete source family
2. the retained normal slice `J_z`
3. the exact local radial bosonic observable
4. the exact local quadratic comparator

Then:

1. the retained normal slice provides a canonical local background baseline
2. the exact relative local bosonic response is
   `W_rel = (1/2) log(1 + rho^2)`
3. the exact relative local quadratic comparator is `Q_rel = rho^2`
4. both are invariant under local rephasing in the pairing plane
5. the remaining unresolved step is not comparator/background existence but
   finite-point selection on this already-normalized curve

So the old wording

> need a new non-homogeneous comparator or a canonically fixed background
> normalization

is no longer the right blocker on the local admitted source family.

## What this closes

This closes one real branch-level gap:

- does the admitted Majorana Nambu family still lack a local non-homogeneous
  comparator or local background normalization?

Answer: no.

The branch now has both:

- the exact local comparator `Q_2 = ||s||^2`
- the exact background-normalized local response curve
  `W_rel = (1/2) log(1 + rho^2)`, `Q_rel = rho^2`

## What this does not close

This note does **not** yet prove:

- a finite nonzero physical pairing amplitude
- an absolute staircase anchor
- the full three-generation `A/B/epsilon` amplitudes
- full zero-import `eta`

It only sharpens the blocker again.

## Relationship to the earlier necessity theorem

The earlier necessity theorem was correct on the **pre-existing logarithmic
observable family alone**.

This note closes one branch of that old necessity result positively:

- a local non-homogeneous comparator now exists
- a local background normalization now exists

So the remaining blocker is no longer

> comparator/background existence

but rather

> the finite-point selection / staircase-embedding law on the already-
> normalized local Majorana response curve

## Safe wording

**Can claim**

- the retained normal slice gives an exact local background normalization on
  the admitted Majorana Nambu family
- the exact relative local bosonic response is
  `W_rel = (1/2) log(1 + rho^2)`
- the exact relative local non-homogeneous comparator is `Q_rel = rho^2`
- the local blocker is now finite-point selection, not comparator/background
  existence

**Cannot claim**

- the Majorana staircase anchor is already derived
- the DM denominator is closed

## Command

```bash
python3 scripts/frontier_neutrino_majorana_background_normalization_theorem.py
```
