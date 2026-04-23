# Majorana Source-Response Matching Obstruction

**Date:** 2026-04-15
**Status:** exact frontier boundary on the current source-response matching class
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_source_response_matching_obstruction.py`

## Question

After the exact local self-dual Majorana point is fixed, could the branch
derive the absolute staircase anchor by **matching exact local source-response
values** directly to current generation-side source-response observables?

This is a sharper rescue path than the earlier algebraic-bridge and
scalar-datum routes:

- not "reuse a fixed atlas constant multiplicatively"
- not "build a cleverer finite algebraic bridge"
- but rather:

> equate the exact local self-dual values
> `W_rel = (1/2) log 2`, `Q_rel = 1`
> to exact generation-side pairing observables and solve for the absolute
> staircase scale

## Bottom line

No.

On the current exact stack, the obvious source-response matching class fails in
two complementary ways:

1. **absolute matches** depend on the arbitrary normalization of the
   homogeneous generation representative
2. **relative/normalized matches** remove that arbitrariness, but then they
   fix only ratios to an arbitrary reference scale, not the absolute staircase
   anchor

So the missing object sharpens again:

> it must go beyond the current source-response matching class, or introduce a
> genuinely new non-homogeneous bridge or absolute-scale datum

## Inputs

This note combines:

- [NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md](./NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md)
- [NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md](./NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md)
- [NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_ALGEBRAIC_BRIDGE_OBSTRUCTION_NOTE.md](./NEUTRINO_MAJORANA_ALGEBRAIC_BRIDGE_OBSTRUCTION_NOTE.md)

Those notes already prove:

1. the exact local self-dual response values are
   `W_rel = (1/2) log 2`, `Q_rel = 1`
2. the current one-generation and three-generation Majorana structures are
   homogeneous under positive rescaling
3. the obvious finite algebraic/spectral bridge class is already exhausted

So the remaining loophole is:

> perhaps direct matching of exact local and generation-side source-response
> observables still fixes the absolute scale

## Exact theorem

### 1. Absolute matches depend on arbitrary representative normalization

Write the current homogeneous generation representative as

`M = lambda sigma M_hat`,

where:

- `lambda` is the physical staircase scale we want
- `sigma` is the arbitrary normalization of the homogeneous representative
- `M_hat` is a fixed shape representative

Then the current exact absolute generation observables behave as:

- Pfaffian/log response:
  `W_abs = log|det M| = 3 log lambda + 3 log sigma + const`
- quadratic comparator:
  `Q_abs = ||Delta(M)||^2 = lambda^2 sigma^2 const`

So matching either absolute observable to the exact local self-dual values
determines only the product `lambda sigma`, not `lambda` by itself.

### 2. Relative matches remove that dependence but also remove the absolute anchor

If one instead uses relative/normalized observables to remove the arbitrary
representative normalization, then:

- relative log responses depend only on `lambda / lambda_ref`
- relative quadratic responses also depend only on `lambda / lambda_ref`

So the matching problem becomes:

> choose `lambda` relative to an arbitrary reference scale `lambda_ref`

That is not an absolute staircase law.

### 3. The current generation-side observables are themselves homogeneous

This is the deeper reason the matching route fails:

- the absolute Pfaffian/log response is affine in `log lambda`
- the absolute quadratic comparator is homogeneous of degree `2`

So the current generation-side source-response observables already lie on the
same homogeneous scale family. Matching them to fixed local constants cannot
turn that family into an absolute anchor.

## The theorem-level statement

**Theorem (Source-response matching obstruction on the current exact Majorana
stack).** Assume:

1. the exact local self-dual Majorana response values
2. the current homogeneous three-generation Majorana pairing class
3. the current generation-side absolute or relative source-response
   observables built from the Pfaffian/log generator and quadratic comparator

Then:

1. absolute source-response matching fixes only the product of staircase scale
   and representative normalization
2. relative/normalized matching removes that normalization but fixes only
   ratios to an arbitrary reference scale
3. therefore no match in that current source-response class can by itself fix
   the absolute Majorana staircase anchor

## What this closes

This closes another honest loophole:

- maybe the branch already has the right exact observables, and only lacks the
  idea to equate the local self-dual response values to generation-side
  source-response values

Answer: not within the current exact source-response matching class.

## What this does not close

This note does **not** prove:

- that no future non-homogeneous matching principle can exist
- that no future absolute-scale datum can be derived
- that the universal-theory program is ruled out

It is a theorem about the **current exact source-response matching class on
the current Majorana stack**.

## Consequence for DM

For the DM denominator this means:

- the local self-dual Majorana point is exact
- the current homogeneous `Z_3` lift is already closed negatively
- the obvious algebraic/spectral bridge class is already closed negatively
- the current scalar-atlas datum reuse class is already closed negatively
- the obvious current source-response matching class is now also closed
  negatively

So full zero-import `eta`, and therefore full zero-import DM closure, still
requires a genuinely new non-homogeneous local-to-generation bridge or a
genuinely new absolute-scale datum beyond the present matching class.

## Safe wording

**Can claim**

- the current exact source-response matching class does not rescue the
  Majorana staircase law
- absolute matches depend on arbitrary representative normalization
- relative matches fix only ratios to an arbitrary reference scale

**Cannot claim**

- that no future source-response bridge can ever exist
- that no future absolute-scale datum can ever be derived

## Command

```bash
python3 scripts/frontier_neutrino_majorana_source_response_matching_obstruction.py
```
