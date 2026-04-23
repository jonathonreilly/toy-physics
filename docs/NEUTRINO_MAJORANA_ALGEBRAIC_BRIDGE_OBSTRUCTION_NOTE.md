# Majorana Algebraic Bridge Obstruction Theorem

**Date:** 2026-04-15
**Status:** exact frontier boundary on the obvious local-to-generation bridge class
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_algebraic_bridge_obstruction.py`

## Question

After the exact local selector fixes the self-dual Majorana point

`rho = 1`,

could an obvious finite **algebraic/spectral** bridge from that selected local
ray to the current three-generation texture class already select the absolute
staircase anchor?

This is the sharper form of the remaining escape hatch:

- maybe the current stack still lacks only a better algebraic combination
  between the selected local block and the `A/B/epsilon` texture
- maybe a Schur complement, spectral gap, determinant coefficient, or similar
  generation-side construction already breaks the residual homogeneity

## Bottom line

No.

On the current exact stack, once the selected local family and the current
generation texture are both homogeneous in the same positive scale `lambda`,
the whole obvious algebraic/spectral bridge class remains trapped in two
categories only:

1. **homogeneous quantities** with definite scaling weight in `lambda`
2. **normalized ratios** that are exactly scale-free

That covers the obvious candidate bridge data:

- full bridge blocks
- Schur complements
- characteristic-polynomial coefficients
- eigenvalue gaps
- singular values
- normalized eigenvalue/singular-value ratios

So no construction in that bridge class can pick a finite absolute staircase
anchor by itself.

The blocker sharpens again:

> the missing object must now go beyond the current algebraic/spectral
> local-to-generation bridge class, or introduce a genuinely new absolute-scale
> datum

## Inputs

This theorem combines:

- [NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md](./NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md)
- [NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md](./NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md)
- [NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md)

Those notes already prove:

1. the selected local self-dual family is only the positive ray
   `K_sd(lambda) = lambda (sigma_z + sigma_x)`
2. the current `Z_3` texture class remains homogeneous under the same positive
   rescaling
3. the current stack therefore does not yet lift the selected local point to
   an absolute staircase anchor

So the remaining loophole is now:

> maybe some finite algebraic or spectral bridge on top of those exact objects
> already breaks the homogeneity

## Exact theorem

### 1. The obvious full bridge block is homogeneous

Take the selected local family `lambda K_sd`, any fixed generation
representative `M_0`, and any fixed scale-independent bridge tensor `C_0`.

Then the full candidate bridge block has the form

`B(lambda) = [[lambda K_sd, lambda C_0], [lambda C_0^dag, lambda M_0]]`

so

`B(lambda) = lambda B(1)`.

Therefore the normalized full bridge block is identical across all positive
rescalings.

### 2. Schur-complement bridges remain degree-one

For the same bridge block, the Schur complement on the generation side is

`S(lambda) = lambda M_0 - (lambda C_0^dag)(lambda K_sd)^(-1)(lambda C_0)`

which reduces exactly to

`S(lambda) = lambda [M_0 - C_0^dag K_sd^(-1) C_0]`.

So even the obvious Schur bridge carries the same overall degree-one scaling
weight.

### 3. The obvious spectral bridge data are homogeneous or scale-free

From `B(lambda) = lambda B(1)` it follows exactly that:

- characteristic-polynomial coefficient of degree `r` scales as `lambda^r`
- eigenvalues and singular values scale linearly in `lambda`
- eigenvalue gaps scale linearly in `lambda`
- normalized eigenvalue/singular-value ratios are scale-invariant

So the obvious spectral bridge data again split only into:

- homogeneous scale carriers
- scale-free normalized ratios

Neither class can select a finite absolute scale on its own.

## The theorem-level statement

**Theorem (Algebraic bridge obstruction on the current exact Majorana stack).**
Assume:

1. the selected local self-dual Majorana family is a positive ray
2. the current retained three-generation texture class is homogeneous under
   the same positive rescaling
3. the candidate local-to-generation bridge is built from a finite number of
   current-stack algebraic/spectral operations such as block assembly, Schur
   complements, spectral coefficients, eigenvalue/singular-value gaps, and
   normalized ratios

Then every such bridge quantity is either:

1. homogeneous with definite scaling weight in the same positive parameter, or
2. exactly scale-invariant after normalization

Therefore no quantity in that algebraic/spectral bridge class can by itself
select a finite absolute Majorana staircase anchor.

## What this closes

This closes the next honest loophole:

- maybe the current stack already contains the right data, and only lacks a
  more clever algebraic bridge between the selected local point and the
  generation texture

Answer: no, not within the obvious finite algebraic/spectral bridge class.

## What this does not close

This note does **not** prove:

- that no future non-algebraic bridge can exist
- that no new absolute-scale datum can be derived
- that the universal-theory program is ruled out

It is a theorem about the **current algebraic/spectral bridge class on the
current exact stack**.

## Consequence for DM

For the DM denominator this means:

- the local Dirac lane is exact
- the local Majorana self-dual point is exact
- the obvious algebraic/spectral lift from that local point to the generation
  texture is now also exhausted

So full zero-import `eta`, and therefore full zero-import DM closure, still
requires a genuinely new non-homogeneous bridge beyond that class or a new
absolute-scale datum.

## Safe wording

**Can claim**

- the obvious algebraic/spectral bridge class on the current stack is exhausted
- Schur-complement and spectral bridge candidates remain homogeneous or
  scale-free
- the missing object must go beyond that class or add a new absolute-scale
  datum

**Cannot claim**

- that no future bridge can ever be found
- that no future absolute-scale datum can be derived

## Command

```bash
python3 scripts/frontier_neutrino_majorana_algebraic_bridge_obstruction.py
```
