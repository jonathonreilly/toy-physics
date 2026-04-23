# Majorana Staircase-Blindness Theorem

**Date:** 2026-04-15
**Status:** exact scale-boundary theorem on the current Majorana source stack
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_staircase_blindness_theorem.py`

## Question

Once the one-generation source ray and the three-generation `Z_3` texture class
are fixed, does the **current exact Majorana source stack** also fix the
absolute staircase level?

## Bottom line

No.

The current exact source stack is homogeneous under positive rescaling.

That means it fixes:

- the one-generation source **ray**
- the three-generation `Z_3` texture **class**

but not:

- the absolute amplitude of that ray
- the absolute staircase anchor of that texture class

So the live denominator blocker is now narrower than before:

> derive an exact scale-setting / staircase-selection principle for the
> already-fixed Majorana source class.

## Inputs

This theorem uses:

- [NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
- [NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md)

The current exact chain already fixes:

1. the one-generation new source direction to the ray `mu J_x`
2. the canonical local block `mu J_2`
3. the three-generation pairing class `Delta(M) = M \otimes J_2`
4. the `Z_3` texture shape `[[A,0,0],[0,eps,B],[0,B,eps]]`

So the remaining question is whether those exact structural tools already
distinguish `k = 7` from `k = 8`, or any other absolute staircase placement.

## Exact theorem

### 1. The one-generation ray is homogeneous

The canonical local block is

`A_M(mu) = mu J_2`.

For any positive rescaling `mu -> lambda mu`:

- the normalized block is unchanged
- the source **direction** is unchanged
- the Pfaffian generator shifts only by the additive constant `log(lambda)`

So the current exact local one-generation structure fixes a ray, not an
absolute scale.

### 2. The three-generation `Z_3` class is homogeneous

Take the `Z_3` texture

`M = [[A,0,0],[0,eps,B],[0,B,eps]]`

and rescale it by any positive `lambda`.

Then:

- the normalized pairing block `Delta(M) = M \otimes J_2` is unchanged
- the normalized singlet/doublet eigenvalue pattern is unchanged
- the exact `Z_3` texture class is unchanged

So the current exact generation-side structure fixes a matrix class up to
overall scale, not an absolute staircase anchor.

### 3. The charge sector is also homogeneous

Across the staircase-rescaled family:

- every pairing operator remains charge `-2`
- the operator norm scales linearly with the overall scale
- no current exact charge-classification statement distinguishes one
  staircase level from another

So the current exact source stack is structurally blind to the absolute level.

## The theorem-level statement

**Theorem (Majorana staircase-blindness on the current exact source stack).**
Assume:

1. the one-generation source-ray theorem
2. the canonical local block theorem
3. the three-generation `Z_3` texture class

Then the current exact structural data are homogeneous under positive
rescaling of the Majorana source amplitude. Equivalently:

1. the one-generation lane fixes a ray, not an absolute scale
2. the three-generation `Z_3` lift fixes a texture class, not an absolute
   staircase anchor
3. the present exact source stack therefore cannot distinguish the absolute
   Majorana staircase level

## What this closes

This closes one honest ambiguity in the current blocker wording:

- maybe the current exact Majorana structure already hides enough information
  to select the absolute staircase level

Answer: no.

So the blocker is not:

- pick a local source direction
- or re-scan the current exact Majorana structure for a hidden scale

It is:

- derive a genuinely new exact scale-setting principle for the already-fixed
  Majorana source class

## What this does not close

This note does **not** prove:

- that such a scale-setting principle cannot exist
- that the Majorana lane is closed negatively in principle
- that the three-generation relative amplitudes `A, B, eps` are already fixed

It is a theorem about the **current exact source stack** only.

## Safe wording

**Can claim**

- the current exact Majorana source stack is homogeneous under positive
  rescaling
- it fixes the source ray and the texture class, but not the absolute
  staircase level
- the live denominator blocker is now an exact scale-setting / staircase-
  selection problem

**Cannot claim**

- the staircase level can never be derived
- the final neutrino / DM closure is impossible in principle

## Command

```bash
python3 scripts/frontier_neutrino_majorana_staircase_blindness_theorem.py
```
