# Majorana Nambu Radial Observable

**Date:** 2026-04-15
**Status:** exact local bosonic-observable theorem on the admitted Nambu family
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_nambu_radial_observable.py`

## Question

Once the local Nambu-complete source family is admitted on the unique
Majorana block, what is the minimal canonically invariant **local bosonic
observable** on that block?

This is the constructive question left open by the earlier negative chain:

- the retained normal observable principle is scalar/charge-zero only
- the local Pfaffian lane is exact on the pure-pairing ray
- the full admitted Nambu family is the local pseudospin triplet

So the honest next local step is:

> what bosonic observable lives on that whole admitted local Nambu family?

## Bottom line

The admitted local Nambu block is a radial spectral family.

Writing the local source vector as

`s = (x, y, z)`

on the pseudospin basis `J_x, J_y, J_z`, the associated `2 x 2` active-block
kernel is

`H(s) = x sigma_x + y sigma_y + z sigma_z`.

Its spectrum is exactly

`spec(H(s)) = { -||s||, +||s|| }`.

So any canonically invariant local spectral scalar depends only on the radial
norm

`r = ||s|| = sqrt(x^2 + y^2 + z^2)`.

The minimal additive CPT-even scalar on that local family is therefore

`W_N(s) = (1/2) log|det H(s)| = log r + const`.

On the pure-pairing ray `s = (mu, 0, 0)`, this reduces exactly to

`W_N(mu J_x) = log(mu) + const`,

matching the earlier local Pfaffian generator.

So this is a genuine positive beyond-retained-stack bosonic observable on the
admitted Nambu family. But it still does **not** select a nonzero scale.

## Inputs

This theorem combines:

- [NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md)
- [NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md](./NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md)

Those notes already prove:

1. the admitted local source family is the pseudospin triplet
   `span{J_x, J_y, J_z}`
2. the genuinely new one-generation source increment is the pure-pairing ray
   `mu J_x` up to rephasing
3. on that pure-pairing ray the local bosonic generator is `log(mu)`

So the remaining constructive local question is how to extend that bosonic
observable to the full admitted local Nambu family.

## Exact theorem

### 1. The active local Nambu block is a `2 x 2` pseudospin kernel

On the active one-generation local block, the admitted source coordinates
`(x, y, z)` act as one spin-1/2 pseudospin kernel

`H(s) = x sigma_x + y sigma_y + z sigma_z`.

So canonical basis changes act by `SU(2)` conjugation on `H(s)` and by the
adjoint `SO(3)` rotation on the source vector `s`.

### 2. The spectrum depends only on the radial norm

The kernel satisfies

`H(s)^2 = (x^2 + y^2 + z^2) I = r^2 I`.

So its eigenvalues are exactly

`{ -r, +r }`.

Therefore every canonically invariant spectral scalar on this local family is a
function only of `r`.

### 3. The minimal additive CPT-even scalar is `log r`

The determinant is

`det H(s) = -r^2`.

So the minimal additive CPT-even spectral scalar is

`W_N(s) = (1/2) log|det H(s)| = log r + const`.

This is the natural Nambu-complete analogue of the earlier local Pfaffian
generator.

### 4. The pure-pairing ray reduces to the earlier Pfaffian lane

On the pure-pairing ray

`s = (mu, 0, 0)`,

we have `r = mu`, so

`W_N(mu J_x) = log(mu) + const`.

So this positive local Nambu observable is consistent with the earlier exact
pairing result.

## The theorem-level statement

**Theorem (Local Nambu radial observable on the admitted Majorana source
family).**
Assume:

1. the admitted local Nambu-complete source family on the unique Majorana
   block
2. canonical basis covariance on that block
3. the minimal additive CPT-even local bosonic scalar is taken from the
   spectral data of the active local kernel

Then:

1. the local active kernel is `H(s) = x sigma_x + y sigma_y + z sigma_z`
2. its spectrum depends only on the radial norm `r = ||s||`
3. the minimal canonically invariant local bosonic scalar is
   `W_N(s) = log r + const`
4. on the pure-pairing ray this reduces to `log(mu) + const`

So the branch now has a positive local bosonic observable on the full admitted
Nambu family, not only on the pure-pairing ray.

## What this closes

This closes one constructive local question:

- what bosonic observable lives on the admitted local Nambu family?

Answer:

> the minimal canonically invariant local bosonic observable is radial in the
> pseudospin norm and equals `log ||s|| + const`.

That is stronger than only saying the pairing ray is Pfaffian.

## What this does not close

This note does **not** prove:

- a nonzero physical pairing amplitude
- an absolute staircase anchor
- a full Majorana scale-selection law

In fact it clarifies the remaining blocker:

on the pure-pairing ray this observable is still only `log(mu)`. Later branch
work adds the exact local quadratic comparator `Q_2 = ||s||^2` and the exact
background-normalized local response curve, so the remaining blocker is no longer
comparator/background existence. It is finite-point selection on that
already-normalized curve.

## Relationship to the no-stationary-scale theorem

The no-stationary-scale theorem was negative:

- the admitted source class has no intrinsic selected scale

This note is positive but compatible:

- it identifies the minimal exact local bosonic observable on that admitted
  family
- that observable is radial
- on the pure-pairing ray it still reduces to `log(mu)`

So the branch now knows both:

1. what the local Nambu-complete bosonic observable is
2. why that still does not select the scale

## Safe wording

**Can claim**

- the admitted local Nambu family carries a minimal radial bosonic observable
- the local bosonic scalar is `log ||s|| + const`
- on the pure-pairing ray it reduces exactly to `log(mu)`
- this still leaves the physical scale law open

**Cannot claim**

- the Majorana staircase anchor is now derived
- the DM denominator is fully closed

## Command

```bash
python3 scripts/frontier_neutrino_majorana_nambu_radial_observable.py
```
