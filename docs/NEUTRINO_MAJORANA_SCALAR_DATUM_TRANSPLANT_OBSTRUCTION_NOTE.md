# Majorana Scalar-Datum Transplant Obstruction

**Date:** 2026-04-15
**Status:** exact frontier boundary on the current scalar-atlas reuse class
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_scalar_datum_transplant_obstruction.py`

## Question

Could one of the exact scalar atlas datums already derived on `main` serve as
the missing **absolute-scale datum** for the selected local Majorana lane?

This is the clean next rescue path after the self-dual and algebraic-bridge
obstructions:

- perhaps the hierarchy-side selector constant
  `C_4 = (7/8)^(1/4)`
- or the effective-potential endpoint constant
  `C_inf^(4D) = (3/4)^(1/8)`
- or their exact endpoint ratios

already supply the missing staircase anchor once transplanted into the selected
Majorana local-to-generation bridge.

## Bottom line

No.

On the current exact stack, those objects are just fixed positive scalar
constants. If they are transplanted multiplicatively into the selected local
Majorana block or the current local-to-generation bridge, the common staircase
scale still factors out exactly.

So the missing object sharpens again:

> it is not one of the current exact scalar atlas datums reused
> multiplicatively; it must be a genuinely new non-homogeneous bridge or a
> genuinely new absolute-scale datum beyond that current scalar class

## Inputs

This note combines:

- [HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md](./HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
- [HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md](./HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md](./NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md)
- [NEUTRINO_MAJORANA_ALGEBRAIC_BRIDGE_OBSTRUCTION_NOTE.md](./NEUTRINO_MAJORANA_ALGEBRAIC_BRIDGE_OBSTRUCTION_NOTE.md)

The first three provide the exact scalar atlas datums. The last two fix the
selected Majorana local ray and the already-exhausted obvious algebraic bridge
class.

## Exact theorem

### 1. The current scalar atlas datums are fixed constants

The tested exact scalar datums are:

- `C_4 = (7/8)^(1/4)`
- `C_inf^(4D) = (3/4)^(1/8)`
- `A_4 / A_2 = 8/7`
- `A_inf / A_2 = 2/sqrt(3)`

These are fixed positive dimensionless numbers. They are not new scale
variables on the Majorana lane.

### 2. Multiplicative transplantation leaves the staircase scale factored out

Let the selected local Majorana family be

`K_sd(lambda) = lambda K_*`

and let the current generation texture and bridge tensors be inserted into a
finite bridge block with the same common staircase scale `lambda`.

If a fixed scalar datum is transplanted multiplicatively into any subblock,
then the lifted block still has the form

`B(lambda; c_i) = lambda B(1; c_i)`.

So the normalized bridge block is identical across staircase rescalings.

### 3. Schur and spectral bridge data remain homogeneous or scale-free

Because the whole transplanted block still carries one exact overall factor
`lambda`, all the old consequences survive:

- Schur complements stay degree-one in `lambda`
- eigenvalue gaps stay degree-one in `lambda`
- singular values stay degree-one in `lambda`
- normalized ratios stay scale-free

So the scalar-atlas transplants do not generate a non-homogeneous bridge law.
They only modify fixed coefficients inside the same homogeneous class.

## The theorem-level statement

**Theorem (Scalar-datum transplant obstruction on the current exact Majorana
stack).** Assume:

1. the selected local Majorana family is a positive ray
2. the current generation texture class carries the same common positive
   staircase scale
3. one reuses any finite set of current exact scalar atlas datums only as fixed
   multiplicative coefficients in the local block, bridge tensors, generation
   texture, or lifted local-to-generation block

Then the full lifted block still factors as one overall positive scale times a
fixed matrix, and all associated Schur/spectral bridge data remain homogeneous
or scale-free.

Therefore no such scalar-atlas transplant can by itself select a finite
absolute Majorana staircase anchor.

## What this closes

This closes another honest loophole:

- maybe the missing absolute-scale datum is already present in the exact atlas,
  just in the wrong sector, and only needs to be transplanted into the
  Majorana lane

Answer: not within the current exact scalar-atlas class.

## What this does not close

This note does **not** prove:

- that no future non-scalar datum can exist
- that no future non-homogeneous bridge can exist
- that the universal-theory program is ruled out

It is a theorem about the **current exact scalar atlas data reused
multiplicatively on the current Majorana stack**.

## Consequence for DM

For the DM denominator this means:

- the local self-dual Majorana point is exact
- the current homogeneous `Z_3` lift is already closed negatively
- the obvious algebraic/spectral bridge class is already closed negatively
- the obvious exact scalar-atlas-datum reuse class is now also closed
  negatively

So full zero-import `eta`, and therefore full zero-import DM closure, still
requires a genuinely new non-homogeneous local-to-generation bridge or a
genuinely new absolute-scale datum beyond the current scalar-atlas class.

## Safe wording

**Can claim**

- the current exact scalar atlas datums do not rescue the Majorana staircase
  law by multiplicative transplantation
- the current scalar-atlas reuse class is exhausted
- the missing object must be genuinely new beyond that class

**Cannot claim**

- that no future absolute-scale datum can ever be derived
- that no future non-homogeneous bridge can ever be found

## Command

```bash
python3 scripts/frontier_neutrino_majorana_scalar_datum_transplant_obstruction.py
```
