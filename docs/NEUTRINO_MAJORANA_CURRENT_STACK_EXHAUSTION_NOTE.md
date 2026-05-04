# Majorana Current-Stack Exhaustion

**Date:** 2026-04-15
**Status:** exact current-stack conclusion on the main-derived neutrino lane
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_current_stack_exhaustion.py`

## Question

After all current reductions and boundary theorems, can the **present retained
stack** still force a nonzero Majorana activation law?

## Bottom line

No.

The branch now has:

1. a unique admissible charge-`2` channel
2. a unique local source slot on that channel
3. a unique local bilinear realization if that lane is admitted
4. a proof that the current observable-principle toolkit is blind to the
   Majorana amplitude
5. a proof that the retained `Z_3` / flavor lift cannot activate it

So the current retained stack is exhausted on this question.

What remains is **not** another hidden theorem inside the present toolkit. It
is a genuinely new charge-`2` primitive or source principle beyond the current
retained stack.

## Exact logic

The current conclusion combines four already-exact surfaces.

### 1. If the primitive exists locally, its one-generation lane is fixed

The reduction, source-slot, canonical-block, and local-Pfaffian uniqueness
theorems together say:

- if a local bilinear charge-`2` primitive is admitted
- then the one-generation local lane is already canonically

  `A_M(mu) = mu J_2`

- with exact local bosonic generator

  `W_M(mu) = log(mu) + const`

So the open problem is not local realization type anymore.

### 2. The current retained normal data are blind to `mu`

The Pfaffian no-forcing and observable-principle obstruction results together
show:

- the retained normal signature is identical across the whole `mu` family
- the full retained observable-principle jet is identical across the same
  family
- but the local pairing amplitudes are genuinely different for different `mu`

So the current retained stack cannot distinguish:

- `mu = 0`
- `mu > 0`

from its retained data.

### 3. The retained flavor lift cannot rescue activation

The exact `Z_3` non-activation theorem shows that the retained three-generation
texture remains a charge-`2` object on the current normal grammar.

So `A/B/epsilon` can organize an **activated** Majorana sector, but it cannot
turn one on.

### 4. Therefore the current stack is exhausted

Once:

- the local lane is fixed if admitted
- the retained normal/source-response data are blind to `mu`
- and the retained flavor lift cannot activate `mu`

there is no credible activation route left inside the current retained stack.

That is the exact current-stack conclusion.

## The theorem-level statement

**Theorem (Current-stack exhaustion on the Majorana activation problem).**
Assume the current `main`-derived retained stack:

1. charge-`2` reduction to one unique `nu_R` channel
2. one-slot local bilinear reduction on that channel
3. local Pfaffian uniqueness on the retained local bilinear lane
4. determinant/source-response observable principle on the retained normal
   grammar
5. retained three-generation / `Z_3` structure

Then:

1. if a local bilinear primitive exists, its one-generation local realization
   is already fixed to the Pfaffian lane `A_M(mu) = mu J_2`
2. the current retained normal signature and observable-principle jet are
   identical across the full `mu` family
3. the retained `Z_3` / flavor lift cannot activate that family
4. therefore the current retained stack cannot force or derive a nonzero
   Majorana activation law

Equivalently: the current stack is exhausted negatively on this question. Any
full closure now requires a genuinely new charge-`2` primitive or source
principle beyond the retained stack.

## What this closes

This closes the last honest question of the form:

- maybe one more theorem inside the present stack will turn the Majorana slot
  on

Answer: no.

So the branch now has a definitive current-stack conclusion rather than an
open-ended blocker description.

## What this does not close

This note does **not** prove:

- that no future extension of the framework can derive the primitive
- that the final universal-theory program is impossible
- that a thermodynamic-limit / new-source / new-primitive route can never be
  found

It is a theorem about the **current retained stack only**.

## Consequence for DM

For the DM denominator, this means:

- the retained local Dirac lane is exact
- the local Majorana realization is exact **if** a primitive exists
- but the current retained stack does not derive the primitive itself

So full zero-import `eta`, and therefore full zero-import DM closure, is not
available on the current stack. The honest next move is no longer to search
inside the existing toolkit. It is to derive a genuinely new charge-`2`
primitive or explicitly extend the retained stack.

## Safe wording

**Can claim**

- the current retained stack is exhausted on the Majorana activation problem
- no theorem inside the present retained stack forces a nonzero Majorana
  activation law
- full closure now requires a new charge-`2` primitive or source principle
  beyond the retained stack

**Cannot claim**

- no future framework extension can ever close the lane
- the universal theory project is ruled out in principle

## Command

```bash
python3 scripts/frontier_neutrino_majorana_current_stack_exhaustion.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [neutrino_majorana_charge_two_primitive_reduction_note](NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md)
- [neutrino_majorana_unique_source_slot_note](NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md)
- [neutrino_majorana_local_pfaffian_uniqueness_note](NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md)
- [neutrino_majorana_z3_nonactivation_theorem_note](NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md)
- [neutrino_majorana_observable_principle_obstruction_note](NEUTRINO_MAJORANA_OBSERVABLE_PRINCIPLE_OBSTRUCTION_NOTE.md)
- [publication.ci3_z3.derivation_atlas](publication/ci3_z3/DERIVATION_ATLAS.md)
