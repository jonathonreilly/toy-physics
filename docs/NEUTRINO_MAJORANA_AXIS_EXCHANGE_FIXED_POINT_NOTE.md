# Majorana Axis-Exchange Fixed-Point Theorem

**Date:** 2026-04-15
**Status:** exact local finite-point selector theorem on the admitted
background-normalized Majorana block, conditional on axis-exchange covariance
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_axis_exchange_fixed_point.py`

## Question

After the admitted Majorana Nambu family has been reduced to the exact
background-normalized local response curve

`W_rel(rho) = (1/2) log(1 + rho^2)`, `Q_rel(rho) = rho^2`,

does the local block still lack a canonical finite nonzero point, or is there
an exact selector already on the admitted block?

## Bottom line

Yes, there is now an exact local selector on the admitted block, with one
important boundary.

On the canonical local family

`K(rho) = sigma_z + rho sigma_x`,

the admitted pseudospin block carries an exact canonical exchange of the
retained normal axis and the canonical pairing axis. On the normalized local
ratio that exchange acts as

`rho -> 1/rho`.

Therefore any intrinsic finite-point selector on the already-normalized local
curve that is covariant under that exact axis exchange is forced to the unique
positive fixed point

`rho = 1`.

At that self-dual local point:

- `W_rel = (1/2) log 2`
- `Q_rel = 1`

So the branch no longer lacks a local finite-point selector on the admitted
background-normalized block.

But this theorem is still only **scale-relative**:

- joint positive rescaling leaves `rho = 1` unchanged
- so the absolute staircase anchor is still not fixed
- and the three-generation `Z_3` lift is still not closed

## Inputs

This theorem uses:

- [NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md)
- [NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md)

Those notes already prove:

1. the admitted local source family is the pseudospin triplet
   `span{J_x, J_y, J_z}`
2. the genuinely new one-generation source increment is the canonical
   pure-pairing ray `mu J_x` up to rephasing
3. the retained normal slice gives the exact background-normalized local
   response curve `W_rel(rho)`, `Q_rel(rho)`

So the remaining local question is no longer comparator existence or
background normalization. It is whether the admitted block already has an
exact finite-point selector on that normalized curve.

## Exact theorem

### 1. The normalized local family is one exact `2 x 2` pseudospin line

After rephasing to the canonical pairing ray and dividing by the retained
background coefficient `z != 0`, the admitted local family reduces to

`K(rho) = sigma_z + rho sigma_x`,

with

`rho = ||pairing|| / ||background|| >= 0`.

So the entire local selector problem is now one dimensionless curve.

### 2. The admitted local block has an exact normal-pairing axis exchange

On the active local pseudospin kernel, the canonical unitary

`U_ex = exp(-i pi sigma_z / 2) exp(-i pi sigma_y / 4)`

acts by

- `sigma_z -> -sigma_x`
- `sigma_x -> -sigma_z`

Therefore

`U_ex K(rho) U_ex^dag = - rho K(1/rho)`.

So the exact admitted local exchange acts on the normalized ratio by

`rho -> 1/rho`,

up to the physically irrelevant common sign and common scale factor already
removed by background normalization.

### 3. The unique positive exchange-fixed point is `rho = 1`

If the finite-point selector on the already-normalized local curve is required
to be covariant under that exact canonical exchange, then the selected point
must satisfy

`rho = 1/rho`.

On the positive branch this gives the unique solution

`rho = 1`.

So the local selector is not a free finite benchmark anymore. It is the
self-dual point of the exact admitted axis exchange.

### 4. The self-dual local response is exact

At `rho = 1`:

- `W_rel(1) = (1/2) log 2`
- `Q_rel(1) = 1`

So the local finite-point selector and the local normalized response now agree
exactly on one canonical self-dual point.

### 5. The theorem is still scale-relative

The self-dual condition fixes only the ratio

`rho = ||pairing|| / ||background|| = 1`.

Under joint positive rescaling

`(background, pairing) -> lambda (background, pairing)`,

the selected point `rho = 1` is unchanged.

Therefore this theorem does **not** yet fix:

- the absolute Majorana staircase anchor
- the overall Majorana source scale
- the full three-generation `A/B/epsilon` amplitudes

It closes the local finite-point selector, but not the absolute scale
embedding.

## The theorem-level statement

**Theorem (Axis-exchange fixed point on the admitted background-normalized
Majorana block).**
Assume:

1. the admitted local Nambu-complete source family
2. the canonical pure-pairing source ray up to rephasing
3. the exact background-normalized local response curve
4. that the local finite-point selector is covariant under the exact
   canonical exchange of the retained normal and pairing axes on that same
   admitted block

Then:

1. the local exchange acts as `rho -> 1/rho`
2. the unique positive exchange-fixed point is `rho = 1`
3. the exact selected local response is
   `W_rel = (1/2) log 2`, `Q_rel = 1`
4. this fixes the local finite-point selector only up to overall common
   scaling, so the absolute staircase anchor remains open

## Relationship to the earlier no-go theorems

This does **not** contradict the earlier no-stationary-scale theorem.

That theorem said the admitted Pfaffian/Nambu source class does not generate an
intrinsic stationary point from its scale-sensitive bosonic generator alone.

This note is different:

- it works on the later background-normalized local curve
- it adds the exact local axis-exchange covariance principle
- it then identifies the unique self-dual fixed point of that exchange

So the blocker shifts again:

from

> find a local finite-point selector on the normalized curve

to

> embed the now-selected self-dual local point into an absolute staircase law
> and the full three-generation `Z_3` texture

## What this closes

This closes one real local denominator-side gap:

- does the admitted background-normalized Majorana block still lack a local
  finite-point selector?

Answer: no, not once exact axis-exchange covariance on the admitted block is
imposed.

The local selected point is the self-dual point

`rho = 1`.

## What this does not close

This note does **not** yet prove:

- the absolute staircase anchor
- the absolute Majorana scale
- the full three-generation `A/B/epsilon` amplitudes
- full zero-import `eta`

It is a local finite-point selector theorem, not a full staircase-embedding
theorem.

## Safe wording

**Can claim**

- the admitted background-normalized Majorana block now has an exact local
  self-dual point under the canonical normal-pairing axis exchange
- the selected local point is `rho = 1`
- the local finite-point selector is therefore no longer the remaining blocker
- the remaining blocker is the absolute staircase embedding and three-
  generation lift

**Cannot claim**

- the absolute Majorana staircase anchor is already fixed
- the full denominator is closed
- full DM is zero-import derived

## Command

```bash
python3 scripts/frontier_neutrino_majorana_axis_exchange_fixed_point.py
```
