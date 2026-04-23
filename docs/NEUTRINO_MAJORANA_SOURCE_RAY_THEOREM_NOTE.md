# Majorana Source-Ray Theorem

**Date:** 2026-04-15
**Status:** exact one-generation source-selection refinement on the admitted
local Nambu lane; not a scale-setting theorem
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_source_ray_theorem.py`

## Question

After the Nambu source principle, is the **genuinely new** one-generation
Majorana source still an arbitrary vector on

`span{J_x, J_y, J_z}`,

or is its direction already fixed?

## Bottom line

Its direction is already fixed, with one important qualifier.

The full admitted local source family remains the Nambu-complete pseudospin
triplet

`span{J_x, J_y, J_z}`.

That does **not** change.

But once we ask for the **new source increment beyond the retained normal
grammar**, the answer is no longer arbitrary:

1. the retained normal source already lives on `J_z`
2. the genuinely new increment therefore lies entirely in the transverse
   pairing plane `span{J_x, J_y}`
3. exact local `nu_R` rephasing acts as an `SO(2)` rotation on that plane
4. every nonzero transverse increment is therefore equivalent to the unique
   canonical pure-pairing ray

   `mu J_x`, with `mu >= 0`.

So the live denominator blocker is no longer a one-generation source-vector
direction. It is the absolute amplitude / staircase law and then the
three-generation lift.

## Scope clarification

This note is intentionally stronger than the earlier one-slot and phase-removal
results, but narrower than an overclaim:

- it does **not** say the admitted local source family collapses from
  `span{J_x, J_y, J_z}` to a line
- it does say the **new Majorana increment beyond the retained normal slice**
  collapses to one rephasing class, represented canonically by `mu J_x`

That is compatible with the Nambu source principle. The Nambu note fixes the
full admissible family. This note fixes the genuinely new direction inside that
family.

## Inputs

This theorem uses:

- [NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md](./NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md)
- [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
- [NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md)

The current exact chain already fixes:

1. one unique local Majorana source slot
2. one real local amplitude `mu >= 0` after `nu_R` rephasing
3. the admitted local quadratic source grammar as the Nambu-complete
   pseudospin triplet

So the remaining question is whether the **new** source increment inside that
triplet still carries local directional ambiguity.

## Exact theorem

### 1. The admitted local family splits exactly into retained and new pieces

On the two-mode local block:

- `J_z` is the exact charge-zero normal direction
- `span{J_x, J_y}` is the transverse pairing plane
- `J_z` is Frobenius-orthogonal to `J_x` and `J_y`

So every admitted local source decomposes uniquely as

`s = s_old + s_new`

with

- `s_old in span{J_z}`
- `s_new in span{J_x, J_y}`.

Since the retained normal grammar already contains `J_z`, the genuinely new
beyond-retained increment is exactly `s_new`.

### 2. The new increment is exactly the pairing plane

The transverse plane is exactly the unique complex pairing slot:

`m J_- + m^* J_+ = a J_x + b J_y`.

So the new increment is not another normal direction. It is the local pairing
sector already isolated by the source-slot theorem.

### 3. Local `nu_R` rephasing rotates that plane exactly

The `J_z` generator acts by exact `SO(2)` rotation on the transverse plane:

`U(theta) J_x U(theta)^dag = cos(theta) J_x + sin(theta) J_y`

`U(theta) J_y U(theta)^dag = -sin(theta) J_x + cos(theta) J_y`

with

`U(theta) = exp(-i theta J_z)`.

So any nonzero transverse increment

`a J_x + b J_y`

can be rotated to

`mu J_x`,  with `mu = sqrt(a^2 + b^2)`.

### 4. Therefore the new local source is one ray

Modulo the already-admitted local `nu_R` rephasing, every nonzero beyond-
retained one-generation Majorana source increment is equivalent to the unique
canonical pure-pairing ray

`mu J_x`,  with `mu >= 0`.

## The theorem-level statement

**Theorem (One-generation Majorana source-ray theorem on the admitted Nambu
lane).**
Assume:

1. the admitted local Nambu-complete source family
   `span{J_x, J_y, J_z}`
2. the retained normal source slice `span{J_z}`
3. the current exact local `nu_R` rephasing freedom

Then:

1. the genuinely new beyond-retained source increment lies entirely in the
   transverse pairing plane `span{J_x, J_y}`
2. that plane is exactly the unique local charge-`2` source slot
3. every nonzero increment in that plane is rephasing-equivalent to the
   canonical ray `mu J_x`, with `mu >= 0`

Equivalently: the one-generation source-direction problem is already closed.
Only the amplitude remains.

## What this closes

This closes one specific denominator-side ambiguity:

- is the new one-generation Majorana source still a free vector direction on
  the admitted local Nambu family?

Answer: no.

So the blocker is no longer:

- choose a one-generation source direction

It becomes:

- determine the absolute amplitude / staircase law for the already-fixed local
  source ray
- then lift that amplitude law to the three-generation texture

## What this does not close

This note does **not** prove:

- that the amplitude `mu` is nonzero
- that `mu` sits at a unique staircase level
- that the singlet/doublet texture amplitudes `A, B, eps` are numerically
  derived
- that full zero-import `eta` is now closed

It is a direction-selection theorem, not a scale-selection theorem.

## Safe wording

**Can claim**

- the admitted local Nambu family does not leave a free one-generation new
  source direction
- the genuinely new beyond-retained increment is exactly a pure-pairing ray
  up to local `nu_R` rephasing
- the local one-generation Majorana ambiguity now reduces to one nonnegative
  amplitude

**Cannot claim**

- the full local Nambu family itself collapses to a line
- the amplitude `mu` is already derived
- the Majorana staircase level is fixed

## Command

```bash
python3 scripts/frontier_neutrino_majorana_source_ray_theorem.py
```
