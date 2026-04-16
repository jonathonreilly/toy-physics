# Current Atlas Charge-Two Primitive Non-Realization

**Date:** 2026-04-15  
**Status:** exact current-atlas boundary on the main-derived neutrino lane  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_current_atlas_nonrealization.py`

## Question

After reducing the open Majorana lane to one missing object,

> a genuinely new charge-`2` microscopic primitive on the unique `nu_R`
> channel,

does the **current main-branch atlas / retained matter toolkit already contain
such an object**?

## Bottom line

No.

The current atlas and retained matter toolkit supply:

- the unique anomaly-fixed channel `nu_R^T C P_R nu_R`
- the scalar determinant observable principle `log|det(D+J)|`
- the retained right-handed completion with `nu_R : (1,1)_0`
- several gravity/source/tensor primitives and bounded candidates

But none of the currently retained or atlas-listed objects is itself a
fermionic charge-`2` microscopic primitive on the `nu_R` channel.

So the current branch does **not** already contain the missing object under a
different name. The next step remains to derive a genuinely new one.

## What was checked

The current-atlas scan uses three exact repository-side facts.

### 1. The retained observable principle is scalar and normal

The atlas row

- `Observable principle`

and its authority note

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)

fix the current retained source-response generator to

`W[J] = log|det(D+J)| - log|det D|`.

That is scalar and determinant-based. It does not itself introduce a
charge-`2` pairing primitive.

### 2. The right-handed composite route does not realize the `nu_R` primitive

The retained one-generation matter closure gives the final right-handed branch

- `u_R : (1,3)_{+4/3}`
- `d_R : (1,3)_{-2/3}`
- `e_R : (1,1)_{-2}`
- `nu_R : (1,1)_0`

but the explicit spatial-composite audit in

- [frontier_right_handed_sector.py](./../scripts/frontier_right_handed_sector.py)

shows the antisymmetric `wedge^2(C^8)` singlet route only realizes the
degree-2 singlet quantum numbers for:

- `d_R`
- `e_R`

and explicitly misses:

- `u_R`
- `nu_R`

on that composite surface.

So the existing antisymmetric composite object on the spatial `C^8` side is
not the missing `nu_R` Majorana primitive.

### 3. The atlas primitives beyond the normal grammar are gravity/tensor-side

The atlas rows that explicitly introduce new primitives beyond the scalar
observable backbone are objects like:

- Route 2 exact bilinear tensor carrier `K_R`
- Route 2 tensor prototype `Theta_R^(0)`
- constructed support tensor primitive `Xi_R^(0)`
- tensorized Schur/Dirichlet primitive
- Route 2 spacetime tensor carrier
- universal tensor variational candidate

These are real and useful atlas tools, but they are support/tensor/gravity-side
objects, not fermionic `Delta L = 2` matter primitives.

So on the current atlas they are analogy surfaces only, not hidden solutions to
the neutrino Majorana lane.

## The theorem-level statement

**Theorem (Current-atlas non-realization of the Majorana charge-`2`
primitive).**
Assume the current `main` derivation atlas, the retained observable principle,
and the retained one-generation matter closure. Then:

1. the current atlas fixes the unique admissible local same-chirality
   Majorana channel on the anomaly-fixed branch
2. the current retained observable/source grammar remains scalar and
   determinant-based
3. the current retained right-handed composite constructions do not realize a
   `nu_R` charge-`2` primitive
4. the currently atlas-listed non-scalar primitives are tensor/gravity-side
   objects rather than fermionic `Delta L = 2` carriers

Therefore the current atlas/toolkit does not already contain the missing
charge-`2` Majorana primitive.

## What this closes

This closes the next honest search question:

- do we already have the needed Majorana primitive somewhere on `main` under a
  different gravity/source/composite label?

Answer: no.

So the search space tightens again:

- not another scan for a hidden existing object
- but derivation of a genuinely new object outside the retained normal grammar

The current-stack activation-law consequence is now separated explicitly in:

- [NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md](./NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md)
- `scripts/frontier_neutrino_majorana_current_stack_zero_law.py`

Current result there: because the retained grammar gives zero coefficient and
the current atlas adds no extra charge-`2` primitive, the present retained law
is `mu_current = 0`.

## What this does not close

This note does **not** prove:

- that no future axiom-side primitive can be derived
- that Pfaffian/Nambu is impossible
- that the full Majorana problem is closed negatively

It is a current-atlas non-realization boundary only.

## Safe wording

**Can claim**

- the current `main` atlas does not already supply the missing charge-`2`
  Majorana primitive
- the right-handed composite route on `C^8` is not that object
- the current atlas primitives beyond the scalar backbone are gravity/tensor
  analogy surfaces, not fermionic `Delta L = 2` realizations

**Cannot claim**

- the framework can never derive such a primitive
- the negative answer is final in principle

## Command

```bash
python3 scripts/frontier_neutrino_majorana_current_atlas_nonrealization.py
```
