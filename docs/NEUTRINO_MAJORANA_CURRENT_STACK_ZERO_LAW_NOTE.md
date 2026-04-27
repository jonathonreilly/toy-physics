# Majorana Current-Stack Zero Law for `mu`

**Date:** 2026-04-15
**Status:** exact current-stack theorem on the proposed_retained one-generation
Majorana lane; not a negative theorem for all future extensions
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_current_stack_zero_law.py`

## Question

After the current one-generation local Majorana block has been reduced to the
canonical form

`A_M(mu) = mu J_2`,

what is the **actual activation law** for the real amplitude `mu` on the
current retained atlas / current retained microscopic stack?

## Bottom line

On the current retained stack, the activation law is the zero law:

`mu_current = 0`.

This is an exact current-stack theorem, not a statement about every future
extension of the framework.

The reason is the conjunction of three exact facts already established on this
branch:

1. the one-generation local Majorana block is canonically parameterized by one
   real amplitude `mu`
2. the full retained finite normal grammar has exact fermion-number `U(1)`,
   which kills the charge-`2` Majorana coefficient exactly
3. the current `main` atlas does not already contain any additional fermionic
   charge-`2` primitive that could source a nonzero `mu`

So on the stack that is actually retained today, the exact effective Majorana
activation law is trivial:

`mu_current = 0`.

## Inputs

This theorem uses:

- [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
- [NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md](./NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md)
- [NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md](./NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md)
- [NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md)

The role of each input is sharp:

- the canonical-local-block note says there is only one current local scalar to
  determine, namely `mu`
- the finite-normal-grammar note says the retained grammar sets that scalar to
  zero exactly
- the current-atlas non-realization note says no other currently retained atlas
  primitive shifts that zero
- the no-forcing theorem says the current retained normal data cannot force any
  nonzero Pfaffian amplitude behind the scenes

## Exact zero-law theorem

There are three exact steps.

### 1. The current one-generation Majorana coordinate is one real scalar `mu`

By the canonical local-block theorem, any one-generation local Majorana
completion is equivalent to

`A_M(mu) = mu J_2`, with `mu >= 0`.

So the current activation-law question is scalar, not matrix-valued:

> what value does the retained stack assign to `mu`?

### 2. On the retained normal grammar, the answer is exactly zero

By the finite normal-grammar no-go theorem, every finite retained microscopic
family built from the current charge-zero normal grammar has exact
fermion-number `U(1)`. The unique Majorana bilinear has charge `+-2`, so its
expectation and coefficient vanish exactly on that full retained surface.

Equivalently: when the current stack is projected onto the unique canonical
Majorana slot, the extracted amplitude is

`mu = 0`.

### 3. The current atlas adds no further charge-`2` source term

The current-atlas non-realization theorem closes the only remaining loophole on
the present branch:

- the retained observable backbone is still scalar/determinant-based
- the current right-handed composite route does not realize the `nu_R`
  primitive
- the currently atlas-listed beyond-scalar primitives are tensor/gravity-side,
  not fermionic charge-`2` carriers

So there is no currently retained extra object on `main` that could shift the
exact retained answer away from zero.

The Pfaffian no-forcing theorem sharpens the same statement from the opposite
side: nothing built only from current retained normal data can force `mu != 0`.

## The theorem

**Theorem (Current-stack zero law for the one-generation Majorana amplitude).**
Assume the current `main` derivation atlas, the retained observable backbone,
the anomaly-fixed one-generation matter closure, and the current retained
finite normal grammar. Then the effective activation law on the canonical
one-generation Majorana block is

`mu_current = 0`.

Equivalently: on the stack that is actually retained today, the canonical
local block is

`A_M = 0 * J_2`.

## What this closes

This closes the present-tense activation-law question on the current branch.

Before this note:

- the local form was reduced to one real amplitude `mu`
- but the status of the actual current-stack law was still phrased as open

After this note:

- the current retained law is no longer open
- it is exactly the zero law `mu_current = 0`

So the remaining honest frontier changes again:

- not "what is the current retained value of `mu`?"
- but "what genuinely new axiom-side charge-`2` primitive, if any, changes the
  zero law?"

## What this does not close

This note does **not** prove:

- that no future extension can ever generate `mu != 0`
- that the full framework forbids Majorana masses in principle
- that a future admitted charge-`2` primitive is impossible
- that the three-generation neutrino problem is closed negatively

It is a current-stack theorem only.

## Safe wording

**Can claim**

- on the current retained atlas / retained microscopic grammar, the effective
  one-generation Majorana activation law is `mu_current = 0`
- the present branch already fixes the canonical local block to `A_M = 0`
- any nonzero future Majorana amplitude requires a genuinely new axiom-side
  charge-`2` primitive outside the current retained stack

**Cannot claim**

- the framework can never produce a nonzero Majorana amplitude
- the negative answer is final in principle
- the full neutrino problem is solved

## Command

```bash
python3 scripts/frontier_neutrino_majorana_current_stack_zero_law.py
```
