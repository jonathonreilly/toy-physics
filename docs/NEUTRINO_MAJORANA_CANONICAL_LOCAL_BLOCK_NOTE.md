# Majorana Canonical One-Generation Local Block Theorem

**Date:** 2026-04-15  
**Status:** exact one-generation local normal-form theorem on the current
neutrino lane; not an existence theorem  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_canonical_local_block.py`

## Question

After the current one-generation lane has been reduced to one real amplitude

`mu >= 0`,

is there still any residual local matrix freedom in an antisymmetric
Majorana/Pfaffian realization, or is the microscopic `2 x 2` pairing block
already canonical?

## Bottom line

It is already canonical.

On the one-generation lane, the local antisymmetric `2 x 2` matrix space is
one-dimensional:

`wedge^2(C^2) = span_C { J_2 }`,

with

`J_2 = [[0,1],[-1,0]]`.

So every local antisymmetric pairing block is exactly

`A_M(m) = m J_2`.

The phase-removal theorem then says the complex slot `m` is basis-removable on
the current one-generation `nu_R` lane, so every such block is equivalent to
the unique real normal form

`A_M(mu) = mu J_2`, with `mu = |m| >= 0`.

Therefore the current one-generation local Majorana completion has **no
residual matrix or basis ambiguity beyond one real amplitude**.

## Inputs

This theorem uses:

- [NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md](./NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md)
- [NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md](./NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md)
- [NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md](./NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md)
- [NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md)

The current exact chain already fixes:

1. the unique local same-chirality seed `S_unique`
2. the unique local source slot `m`
3. the removal of the one-generation local phase

So the remaining local-form question is whether the antisymmetric block itself
still carries hidden basis freedom.

## Exact normal-form theorem

There are three exact steps.

### 1. The antisymmetric `2 x 2` complex matrix space is one-dimensional

For a `2 x 2` matrix

`A = [[a,b],[c,d]]`,

the antisymmetry condition `A^T = -A` forces

`a = d = 0`, `c = -b`.

So every antisymmetric `2 x 2` complex matrix is exactly

`A = b J_2`.

There is no larger local matrix family to classify.

### 2. Local phase removal fixes the unique real normal form

From the one-generation phase-removal theorem, the source slot

`m = |m| e^(i phi)`

can be rephased to the equivalent real-amplitude form with

`mu = |m|`.

So every local antisymmetric block is equivalent to

`A_M(mu) = mu J_2`, with `mu >= 0`.

### 3. All local unitary-congruence invariants collapse to `mu`

On the canonical block,

- `Pf(A_M) = mu`
- `det(A_M) = mu^2`
- the singular values are `(mu, mu)`
- `A_M^dag A_M = mu^2 I_2`

So every retained CPT-even scalar invariant of the one-generation local block
depends only on `mu`, not on any additional matrix coordinate.

## The theorem

**Theorem (Canonical one-generation Majorana local block).**
Assume the current framework axioms, the anomaly-fixed one-generation matter
closure, and a future local bilinear Majorana source completion on the unique
channel `S_unique`. Then the corresponding local antisymmetric microscopic
block is equivalent to the unique canonical normal form

`A_M(mu) = mu J_2`, with `mu >= 0`.

Equivalently: after fixing the unique source slot and removing its phase,
there is no residual one-generation local Majorana matrix freedom beyond one
nonnegative real amplitude `mu`.

## Relationship to the current chain

This sharpens the existing local chain:

1. [NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md](./NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md)
   fixes one complex local slot `m`
2. [NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md](./NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md)
   reduces that slot to one real amplitude `mu = |m|`
3. this note says the entire one-generation antisymmetric local block is then
   canonically fixed as `mu J_2`

So the next honest unknown is now even sharper:

- not a local matrix family
- not a complex slot
- not even a residual one-generation basis choice
- only the axiom-side activation law for the real amplitude `mu`

## What this closes

This closes the last one-generation local matrix ambiguity on the current
Majorana lane.

If a one-generation local Majorana completion is admitted, it does **not**
require:

- choosing among multiple antisymmetric block shapes
- tracking extra local basis parameters
- carrying a physical one-generation Majorana phase

The local block is already canonical.

## What this does not close

This note does **not** prove:

- that the Majorana primitive exists in the full axiom
- that `mu` is nonzero
- that `mu` is numerically fixed
- that the three-generation neutrino texture is closed
- that multi-generation relative Majorana phases are removable

It is a one-generation local normal-form theorem only.

## Safe wording

**Can claim**

- the current one-generation antisymmetric Majorana block is canonically
  `mu J_2`
- all retained one-generation local block invariants collapse to the single
  real amplitude `mu`
- there is no residual one-generation local matrix freedom beyond `mu`

**Cannot claim**

- the axiom already turns on `mu`
- the full three-generation neutrino problem is closed
- all future Majorana phases are removable

## Command

```bash
python3 scripts/frontier_neutrino_majorana_canonical_local_block.py
```
