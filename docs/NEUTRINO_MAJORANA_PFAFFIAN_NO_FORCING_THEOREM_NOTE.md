# Pfaffian No-Forcing Theorem

**Date:** 2026-04-15  
**Status:** exact no-forcing theorem on the current retained stack  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py`

## Question

Can any exact principle built only from the **current retained normal grammar**
force a Pfaffian/Nambu sector or a nonzero Majorana pairing amplitude?

## Bottom line

No.

There is an exact one-parameter family of Pfaffian extensions

`Delta(mu) = mu S_unique`

with:

- the same retained normal signature for all `mu`
- different Pfaffian sectors for different `mu`

Therefore no functional whose inputs are restricted to the retained normal
grammar can distinguish `mu = 0` from `mu != 0`.

That is the exact no-forcing theorem.

## Retained normal grammar

On the current stack, the microscopic grammar that is actually retained is:

- normal kernel `K`
- ordinary local sources `J` in the normal `c^dag c` sector
- determinant observables derived from `log|det(K+J)|`
- the exact operator-classification result fixing the unique `Delta L = 2`
  channel if one is ever added

This grammar does **not** include an antisymmetric pairing block as retained
input data.

## The theorem

**Theorem (Pfaffian no-forcing on the current retained stack).**
Let `R` denote the retained normal data of the present neutrino lane. Suppose a
candidate exact principle `P` depends only on `R`. Then `P` is constant on the
family `Delta(mu) = mu S_unique`, because all members of that family share the
same retained normal signature. But the Pfaffian sectors in that family are
distinct. Therefore `P` cannot force either:

1. the existence of a Pfaffian/Nambu sector, or
2. a nonzero value of the Pfaffian amplitude `mu`.

## What is still forced

One exact statement survives:

- if a `Delta L = 2` sector exists, it must live on one unique channel

So the stack fixes the **channel**, but not the **existence** or
**amplitude** of a Pfaffian sector.

## Relationship to the earlier notes

The lane is now sharply stratified:

1. [NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md](./NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md)
   fixes the unique allowed operator
2. [NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md](./NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md)
   proves the current determinant surface gives zero coefficient
3. [NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md)
   constructs the minimal exact beyond-determinant extension
4. [NEUTRINO_MAJORANA_PFAFFIAN_AXIOM_BOUNDARY_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_AXIOM_BOUNDARY_NOTE.md)
   shows that extension is not yet forced
5. this note proves the stronger statement:
   no exact principle built only from the current retained normal grammar can
   force it

## Safe wording

**Can claim**

- the current retained stack contains an exact no-forcing theorem for the
  Pfaffian/Nambu sector
- the current retained stack forces the unique `Delta L = 2` channel but not
  the existence of the sector or the value of `mu`

**Cannot claim**

- no future extension of the framework could ever force a Pfaffian sector
- the final neutrino answer is negative in principle

## Next honest task

The next real task is now very narrow:

- derive the missing object identified in
  [NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md](./NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md):
  a genuinely new charge-`2` microscopic primitive on the unique `nu_R`
  channel
- then test whether the axiom forces any realization of that primitive

Without such a new object, the current stack cannot close this lane.

## Command

```bash
python3 scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py
```
