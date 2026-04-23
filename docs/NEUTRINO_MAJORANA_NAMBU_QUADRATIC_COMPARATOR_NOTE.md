# Majorana Nambu Quadratic Comparator

**Date:** 2026-04-15
**Status:** exact local non-homogeneous comparator theorem on the admitted
Nambu family
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_nambu_quadratic_comparator.py`

## Question

Beyond the logarithmic radial observable, does the admitted local Nambu source
family carry any exact **non-homogeneous bosonic comparator** at all?

This is the sharp constructive question left by the latest blocker chain:

- the current retained normal observables are blind to the Majorana amplitude
- the admitted Nambu family carries the positive local radial observable
  `W_N = log ||s|| + const`
- the current exact source class still has no stationary scale from those
  logarithmic generators alone

So the honest next step is:

> is there a second exact local comparator on the same admitted pairing block,
> or is even that missing?

## Bottom line

Yes.

On the active local pseudospin kernel

`H(s) = x sigma_x + y sigma_y + z sigma_z`,

the unique minimal nontrivial polynomial spectral invariant is

`Q_2(s) = (1/2) Tr(H(s)^2) = ||s||^2`.

It is:

- exact
- local
- canonically invariant under the `SU(2)` basis action
- non-homogeneous on the pairing ray

On the pure-pairing ray `s = (mu, 0, 0)`, it reduces to

`Q_2(mu J_x) = mu^2`.

So the branch now has the missing **local non-homogeneous comparator object**.

What remains open is not comparator existence on the local block. It is:

1. the physical pairing-sector insertion / endpoint principle for that
   comparator
2. the lift of that principle to the full three-generation `Z_3` texture

## Inputs

This theorem combines:

- [NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md)
- [NEUTRINO_MAJORANA_NAMBU_RADIAL_OBSERVABLE_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_RADIAL_OBSERVABLE_NOTE.md)
- [NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md)

Those notes already prove:

1. the admitted local source family is the pseudospin triplet
   `span{J_x, J_y, J_z}`
2. the active local block is the `2 x 2` kernel
   `H(s) = x sigma_x + y sigma_y + z sigma_z`
3. the minimal additive CPT-even local bosonic scalar is
   `W_N = log ||s|| + const`
4. the genuinely new one-generation source increment is the pure-pairing ray
   `mu J_x` up to rephasing

So the remaining constructive question is whether the same local block carries
an exact non-logarithmic comparator.

## Exact theorem

### 1. The active local kernel squares to the radial norm

The Pauli algebra gives

`H(s)^2 = (x^2 + y^2 + z^2) I = ||s||^2 I`.

So the active local block carries an exact quadratic radial invariant.

### 2. The unique minimal polynomial invariant is `Q_2 = ||s||^2`

Define

`Q_2(s) = (1/2) Tr(H(s)^2)`.

Then

`Q_2(s) = ||s||^2`.

Also:

- `Tr(H) = 0`
- all odd traces vanish
- higher even traces reduce to powers of `Q_2`

So `Q_2` is the unique minimal nontrivial polynomial spectral invariant on the
local Nambu block.

### 3. `Q_2` is canonically invariant

Under local canonical basis changes,

`H(s) -> U H(s) U^dag`

with `U in SU(2)`,

the source vector rotates by the adjoint `SO(3)` action, but

`Q_2(s) = (1/2) Tr(H^2)`

is unchanged.

So `Q_2` is a genuine local comparator, not a basis choice artifact.

### 4. On the pure-pairing ray it becomes `mu^2`

On

`s = (mu, 0, 0)`,

we get

`Q_2 = mu^2`.

So the local admitted pairing ray now carries both:

- the logarithmic bosonic observable `W_N = log(mu) + const`
- the quadratic comparator `Q_2 = mu^2`

That is the first exact non-homogeneous local comparator on this lane.

## The theorem-level statement

**Theorem (Local quadratic comparator on the admitted Majorana Nambu
family).**
Assume:

1. the admitted local Nambu-complete source family on the unique Majorana
   block
2. its active local kernel `H(s) = x sigma_x + y sigma_y + z sigma_z`
3. canonical basis covariance on that block

Then:

1. the exact local quadratic spectral invariant
   `Q_2(s) = (1/2) Tr(H(s)^2)` exists
2. it equals `||s||^2`
3. it is invariant under the local `SU(2)` basis action
4. it is the unique minimal nontrivial polynomial spectral invariant on that
   block
5. on the pure-pairing ray it reduces to `Q_2 = mu^2`

So the branch now has a genuine local non-homogeneous comparator on the
admitted Majorana source family.

## Relationship to the radial observable and necessity theorems

This theorem does **not** contradict the old scale-selector necessity theorem.

Instead it sharpens it:

- the branch was missing a local non-homogeneous comparator object
- this note supplies that object exactly on the local Nambu block
- but later branch work still has to determine the finite-point selection law
  for how that comparator enters the physical local response

So the blocker changes again:

from

> find some new non-homogeneous comparator

to

> determine the finite-point selection / staircase-embedding law on the exact
> local comparator/response system, then lift that law to the full
> three-generation texture

## What this closes

This closes one real open question:

- does the admitted local Nambu family carry any exact non-homogeneous local
  comparator?

Answer: yes.

The exact local comparator is

`Q_2 = (1/2) Tr(H^2) = ||s||^2`.

## What this does not close

This note does **not** yet prove:

- the physical local free-energy / endpoint rule using `Q_2`
- a nonzero physical pairing amplitude
- the staircase anchor
- the three-generation `A/B/epsilon` amplitudes

Those are still open.

## Safe wording

**Can claim**

- the branch now has an exact local non-homogeneous comparator on the Majorana
  Nambu block
- the comparator is `Q_2 = ||s||^2`
- the remaining gap is now the physical insertion / normalization law for that
  comparator

**Cannot claim**

- the Majorana staircase anchor is already derived
- the DM denominator is closed

## Command

```bash
python3 scripts/frontier_neutrino_majorana_nambu_quadratic_comparator.py
```
