# Majorana One-Generation Phase Removal Theorem

**Date:** 2026-04-15
**Status:** exact one-generation local-form refinement on the current neutrino
lane; not an existence theorem
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_phase_removal.py`

## Question

The current local-form theorem says any future one-generation local bilinear
Majorana source completion has one complex slot

`m in C`

on the unique seed

`S_unique = nu_R^T C P_R nu_R`.

Is the phase of that slot physical on the current one-generation lane, or can
it be removed?

## Bottom line

It can be removed.

Because the anomaly-fixed one-generation source lives on the unique gauge
singlet

`nu_R : (1,1)_0`,

a local rephasing of the `nu_R` field rotates

`S_unique -> e^(-2 i alpha) S_unique`.

So for any complex local source slot

`m = |m| e^(i phi)`,

choosing

`alpha = phi / 2`

maps the Hermitian deformation

`m S_unique + m^* S_unique^dag`

to the equivalent real-amplitude form

`|m| (S_unique + S_unique^dag)`.

Therefore the current one-generation local Majorana source slot has **no
physical phase**. Modulo local `nu_R` rephasing, the unknown reduces from a
complex number `m` to one nonnegative real amplitude

`mu = |m|`.

The resulting local block is now sharpened one step further by:

- `NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md`
- `scripts/frontier_neutrino_majorana_canonical_local_block.py`

Current result there: the full one-generation antisymmetric local block is
canonically `mu J_2`, so no residual local matrix freedom remains beyond
`mu`.

## Inputs

This theorem uses:

- [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](./ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
- [NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md](./NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md)
- [NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md](./NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md)
- [NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md)

The current exact chain already fixes:

1. `nu_R` is the unique one-generation gauge singlet on the retained branch
2. the admissible local charge-`2` channel is exactly `S_unique`
3. any local bilinear completion carries one complex slot `m`

So the remaining local question is whether that slot carries a physical phase.

## Exact phase-removal theorem

There are three exact steps.

### 1. The source acts on a gauge singlet

On the retained one-generation branch,

`nu_R : (1,1)_0`.

So local phase rotation of `nu_R` does not disturb the
`SU(3)_c x SU(2)_L x U(1)_Y` representation data.

### 2. The bilinear has charge two under that rephasing

Under

`nu_R -> e^(-i alpha) nu_R`,

the unique same-chirality bilinear transforms as

`S_unique -> e^(-2 i alpha) S_unique`.

Its Hermitian conjugate transforms with the opposite phase.

### 3. The phase of `m` is removable

For

`m = |m| e^(i phi)`,

the Hermitian local deformation is

`delta I_M = m S_unique + m^* S_unique^dag`.

Choosing

`alpha = phi / 2`

gives the equivalent form

`delta I_M ~ |m| (S_unique + S_unique^dag)`.

So at one generation the slot phase is basis-removable, and only `|m|` is a
local invariant.

## Pfaffian interpretation

On the admitted minimal antisymmetric `2 x 2` block

`A_M(m) = m J_2`,

the Pfaffian is

`Pf(A_M) = m`,

but the retained CPT-even scalar generator is

`log|Pf(A_M)| = log|m|`.

So the one-generation Pfaffian realization also sees only the amplitude

`mu = |m|`.

That does **not** say phases are never physical in larger neutrino sectors. It
only says the single local source slot on the current one-generation lane has
no invariant phase.

## The theorem

**Theorem (One-generation Majorana phase removal on the current lane).**
Assume the current framework axioms, the retained one-generation matter
closure, and a future local bilinear Majorana source deformation on the unique
channel `S_unique`. Then the deformation

`delta I_M(m) = m S_unique + m^* S_unique^dag`

is equivalent under local `nu_R` rephasing to

`delta I_M(mu) = mu (S_unique + S_unique^dag)`,

with one nonnegative real amplitude

`mu = |m|`.

Equivalently: the current one-generation local Majorana source slot has no
physical phase.

## What this closes

This closes the next honest local parameter-count question:

- after fixing the unique source slot `m`, how much invariant local data is
  left?

Answer:

- one nonnegative real amplitude `mu`

So the next microscopic unknown is now even narrower:

- not a complex slot `m`
- not a residual one-generation antisymmetric block shape
- but the activation law for one real amplitude `mu`

## What this does not close

This note does **not** prove:

- that the Majorana primitive exists in the full axiom
- that `mu` is nonzero
- that `mu` is fixed numerically
- that relative Majorana phases in a future `3 x 3` texture are removable

It is a one-generation local-form theorem only.

## Safe wording

**Can claim**

- the one-generation local Majorana source slot has no physical phase
- modulo `nu_R` rephasing, the local unknown reduces to one real amplitude
  `mu = |m|`
- the one-generation Pfaffian block also depends only on `|m|` at the retained
  CPT-even scalar-generator level

**Cannot claim**

- all Majorana phases in the full three-generation problem are removable
- the axiom already turns on `mu`
- the Majorana problem is closed

## Command

```bash
python3 scripts/frontier_neutrino_majorana_phase_removal.py
```
