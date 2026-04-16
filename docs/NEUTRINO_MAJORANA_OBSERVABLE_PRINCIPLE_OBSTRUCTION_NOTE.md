# Majorana Observable-Principle Obstruction

**Date:** 2026-04-15  
**Status:** exact current-atlas obstruction on the main-derived neutrino lane  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_observable_principle_obstruction.py`

## Question

The mainline atlas now contains the exact scalar observable principle:

`W[J] = log|det(D+J)| - log|det D|`.

Can that source-response toolkit, as it currently stands, activate or force the
remaining unique charge-`2` Majorana source slot?

## Bottom line

No.

The current observable-principle toolkit is a **scalar bosonic generator on the
retained normal source family**. Those retained source directions lie in the
fermion-number charge-zero sector. The unique Majorana seed lies in charge
`-2`.

Therefore the current observable-principle jet can organize and normalize
charge-zero responses, but it cannot activate or force the charge-`2` Majorana
slot.

Equivalently: on the current stack, the observable principle is not the missing
Majorana activation law.

## Inputs

This theorem combines four already-established exact surfaces:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md](./NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md)
- [NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md](./NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md)
- [NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md)

The exact chain is now:

1. the current bosonic observable generator is fixed and determinant-based
2. the missing neutrino object has been reduced to one new charge-`2`
   primitive on one unique channel
3. any local bilinear realization of that primitive has one complex source slot
4. the current retained normal grammar cannot force the Pfaffian family

So the next honest question is whether the current source-response toolkit
already closes that gap.

## Exact theorem

There are three exact pieces.

### 1. The current observable domain is charge-zero

The present observable-principle source family uses ordinary normal sources
`J` in the `c^dag c` sector.

Those directions commute with the exact fermion-number generator `N`, so they
stay in charge zero.

By contrast, the unique local Majorana seed transforms with charge `-2`.

So the observable-principle domain and the Majorana seed lie in different exact
charge sectors on the retained stack.

### 2. The full observable jet depends only on retained normal data

For the current scalar generator,

`W[J] = log|det(K+J)| - log|det K|`,

the exact local derivatives are

`dW/dj_x = Re Tr[(K+J)^(-1) P_x]`

and

`d^2W/dj_x dj_y = - Re Tr[(K+J)^(-1) P_x (K+J)^(-1) P_y]`.

So the full current observable-principle jet

`(W, grad W, Hess W, ...)`

is a functional only of the retained normal kernel `K` and the retained normal
source family.

It carries no independent charge-`2` datum.

### 3. That jet is constant across the Pfaffian amplitude family

Take the exact one-parameter family of candidate pairing sectors

`Delta(mu) = mu S_unique`.

The retained normal data are the same for every `mu`, but the pairing sector is
different for different `mu`.

Therefore the full current observable-principle jet is identical for every
member of that family, even though the pairing amplitude changes.

So no current atlas theorem built only from the observable-principle jet can
distinguish:

- `mu = 0`
- `mu != 0`

or force a specific nonzero `mu`.

## The theorem-level statement

**Theorem (Current observable-principle obstruction on the Majorana lane).**
Assume the current `main` atlas observable principle, the retained normal
source grammar, the unique-channel reduction on the Majorana lane, and the
local source-slot theorem. Then:

1. the current observable-principle domain lies entirely in the charge-zero
   normal source sector
2. the full current observable-principle jet depends only on retained normal
   data
3. the exact family `Delta(mu) = mu S_unique` has one retained normal
   observable-principle jet for all `mu`
4. therefore no current atlas theorem built only from the retained
   observable-principle toolkit can activate or force the unique charge-`2`
   Majorana source slot

Equivalently: the present observable principle is an exact scalar/normal tool,
not the missing Majorana activation law.

## Relationship to the other Majorana notes

The Majorana lane now has four distinct exact boundaries:

1. [NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md](./NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md)
   reduces the problem to one missing charge-`2` primitive
2. [NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md](./NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md)
   reduces any local bilinear realization to one complex slot
3. [NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md)
   closes the generation / `Z_3` escape hatch
4. this note closes the current atlas observable-principle escape hatch

So the current branch no longer has a credible "maybe the present toolkit
already forces it" route on either the flavor side or the source-response side.

## What this closes

This closes the mainline-atlas version of the open question:

- maybe the exact observable principle already contains the missing activation
  law if we differentiate it the right way

Answer: no.

So the search space tightens again:

- not another determinant/source-response refinement on the current retained
  normal grammar
- but a genuinely new charge-`2` primitive, source family, or pairing-side
  observable principle beyond the current one

## What this does not close

This note does **not** prove:

- that no future charge-`2` source principle can be derived
- that Pfaffian/Nambu is impossible
- that the full neutrino or DM denominator problem is closed negatively

It is an exact obstruction for the **current atlas toolkit only**.

## Safe wording

**Can claim**

- the current observable principle is exact but scalar/normal
- its full retained observable jet is blind to the Majorana amplitude `mu`
- the current atlas source-response toolkit cannot activate or force the unique
  charge-`2` Majorana slot
- the remaining honest task is a genuinely new charge-`2` primitive or source
  law beyond the retained normal grammar

**Cannot claim**

- the framework can never derive such a law
- the final neutrino answer is negative in principle

## Command

```bash
python3 scripts/frontier_neutrino_majorana_observable_principle_obstruction.py
```
