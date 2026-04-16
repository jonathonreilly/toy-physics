# Majorana Observable-Grammar Boundary

**Date:** 2026-04-15  
**Status:** exact current-stack boundary theorem on the one-generation
Majorana lane; not a no-go for all future extensions  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_observable_grammar_boundary.py`

## Question

Suppose the one-generation Majorana lane has already been reduced to the
canonical local block

`A_M(mu) = mu J_2`.

Would a future nonzero `mu` simply be a new coefficient inside the **current**
determinant observable principle, or would it require a genuinely new
source-response grammar?

## Bottom line

It would require a genuinely new source-response grammar.

On the retained stack, the exact observable principle is

`W_det[J] = log|det(D+J)| - log|det D|`,

with `J` living in the retained **normal charge-zero source sector**. Every
retained source derivative of `W_det` therefore stays inside the same
number-preserving grammar. That grammar has exact fermion-number `U(1)`, so it
cannot generate or parameterize the charge-`2` canonical Majorana amplitude
`mu`.

If one admits an antisymmetric pairing Gaussian instead, the exact additive
CPT-even scalar generator changes class:

`W_pf[A] = log|Pf(A)|`.

So a future nonzero Majorana response is not “just another coefficient” inside
the current determinant lane. It requires:

1. a genuinely new charge-`2` microscopic primitive, and
2. a new observable/source-response grammar, naturally Pfaffian on the minimal
   antisymmetric Gaussian surface

## Inputs

This theorem uses:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md](./NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md)
- [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
- [NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md)

The role of each input is precise:

- the observable-principle note fixes the current scalar generator class
- the finite-normal-grammar no-go fixes the exact `U(1)` obstruction on that
  class
- the canonical local-block note says the Majorana problem reduces locally to
  one real amplitude `mu`
- the Pfaffian extension note identifies the minimal exact beyond-determinant
  generator class once a pairing Gaussian is admitted

## Exact boundary theorem

There are three exact steps.

### 1. The current observable principle only sees the normal source grammar

On the retained stack, the exact additive CPT-even scalar generator is

`W_det[J] = log|det(D+J)| - log|det D|`.

Its source space is the retained normal source sector `J` in the `c^dag c`
grammar. Independent normal subsystems multiply at the partition level and add
at the `log|det|` level. No antisymmetric pairing block appears among the
retained source coordinates.

So the current scalar source-response theory is exactly the determinant/normal
grammar.

### 2. That grammar cannot carry the canonical Majorana amplitude

The canonical one-generation Majorana problem is one real amplitude `mu` on the
charge-`2` block `mu J_2`.

But the retained normal grammar has exact fermion-number `U(1)`. Every
retained source derivative of `W_det` remains charge-zero. Therefore the
current determinant observable principle cannot generate or parameterize
`mu != 0`.

Equivalently:

- the current stack can classify the Majorana channel
- the current stack can prove the current law `mu_current = 0`
- but the current stack cannot realize a nonzero `mu` without leaving the
  determinant source grammar itself

### 3. The minimal exact beyond-determinant response class is Pfaffian

If an antisymmetric pairing Gaussian is admitted, the partition amplitude is
Pfaffian:

`Z_pf[A] = Pf(A)`.

The same multiplicative-to-additive scalar logic then forces

`W_pf[A] = log|Pf(A)|`.

On the canonical one-generation block `A_M(mu) = (m_0 + mu) J_2`, this
generator responds directly to `mu`.

So the minimal exact route to a nonzero Majorana response is not:

> keep the current `log|det|` observable grammar and change one coefficient

but:

> admit a new charge-`2` microscopic sector and the matching Pfaffian
> observable grammar

## The theorem

**Theorem (Observable-grammar boundary on the one-generation Majorana lane).**
Assume the current retained observable principle, the retained finite normal
grammar, and the canonical one-generation Majorana block

`A_M(mu) = mu J_2`.

Then the current determinant observable principle cannot generate or
parameterize `mu != 0`. Any future nonzero one-generation Majorana response
requires a genuinely new charge-`2` microscopic primitive and a new
observable/source-response grammar beyond the retained determinant lane. On the
minimal antisymmetric Gaussian surface, that new scalar grammar is `log|Pf|`.

## What this closes

This closes the next honest interpretive gap after the current-stack zero law.

Before:

- a reader could still imagine that `mu != 0` might eventually appear as just
  another coefficient inside the current determinant response law

After:

- that reading is no longer honest
- the current determinant observable principle is itself part of the boundary
- a future nonzero Majorana response would require a new observable grammar,
  not merely a new fitted coefficient

## What this does not close

This note does **not** prove:

- that a Pfaffian/Nambu sector is axiom-forced
- that the future extension must be exactly the minimal Gaussian one
- that no other future charge-`2` observable grammar is possible in principle
- that the full three-generation neutrino problem is closed

It is a current-stack boundary theorem only.

## Safe wording

**Can claim**

- the current determinant observable principle cannot carry a nonzero
  one-generation Majorana amplitude
- a future nonzero `mu` would require both a new charge-`2` primitive and a new
  source-response grammar
- the minimal exact beyond-determinant grammar is Pfaffian on an antisymmetric
  Gaussian surface

**Cannot claim**

- the Pfaffian extension is already axiom-forced
- no future non-Pfaffian extension could ever exist
- the full neutrino problem is solved

## Command

```bash
python3 scripts/frontier_neutrino_majorana_observable_grammar_boundary.py
```
