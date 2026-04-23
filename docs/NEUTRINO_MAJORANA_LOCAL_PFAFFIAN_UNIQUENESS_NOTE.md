# Majorana Local Pfaffian Uniqueness

**Date:** 2026-04-15
**Status:** exact one-generation local bilinear uniqueness theorem on the
main-derived neutrino lane
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_local_pfaffian_uniqueness.py`

## Question

The current branch already shows:

- the missing object reduces to one charge-`2` primitive
- any local bilinear realization has one complex source slot
- the one-generation local block is canonically `mu J_2`

At that point, is the Pfaffian/Nambu realization still just one convenient
example, or is it actually forced on the retained **local bilinear** lane?

## Bottom line

It is forced.

On the retained local bilinear Majorana lane:

1. every local completion reduces to the canonical antisymmetric block
   `A_M(mu) = mu J_2`
2. the finite Grassmann amplitude of that bilinear block is exactly its
   Pfaffian
3. independent antisymmetric sectors multiply under Pfaffian factorization
4. therefore the unique additive CPT-even scalar generator is `log|Pf|`

For the canonical one-generation block this collapses to

`W_M(mu) = log(mu) + const`.

So if the missing primitive is realized **locally at bilinear level**, then
its microscopic realization and local bosonic observable principle are already
fixed. The remaining open question is only whether the axiom turns that
primitive on.

## Inputs

This theorem combines five exact surfaces already on branch:

- [NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md](./NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md)
- [NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md](./NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md)
- [NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md](./NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md)
- [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)

The logic mirrors the determinant-side observable principle, but now on the
one-generation local antisymmetric pairing block.

## Exact theorem

There are four exact steps.

### 1. The local bilinear completion is already canonical

The unique-source-slot and canonical-local-block theorems reduce any
one-generation local bilinear completion to

`A_M(mu) = mu J_2`, with
`J_2 = [[0,1],[-1,0]]`

and `mu >= 0` after the existing phase-removal theorem.

So there is no remaining local realization family to choose.

### 2. The finite local Grassmann amplitude is Pfaffian

For a quadratic antisymmetric Grassmann block

`(1/2) psi^T A psi`,

the finite Berezin integral is exactly

`Z[A] = Pf(A)`.

On the canonical one-generation block,

`Pf(A_M(mu)) = mu`.

So the local microscopic amplitude is the Pfaffian itself, not the determinant.
The determinant is only

`det(A_M) = mu^2`,

which squares away the primitive amplitude.

### 3. Independent antisymmetric sectors multiply

For block-diagonal antisymmetric sectors,

`Pf(A_1 ⊕ A_2) = Pf(A_1) Pf(A_2)`.

So by the same multiplicative-to-additive logic used on the determinant lane,
the unique additive CPT-even scalar generator is

`W = log|Pf(A)| + const`.

### 4. The canonical one-generation generator is `log(mu)`

Applying that to the canonical block gives

`W_M(mu) = log|Pf(mu J_2)| + const = log(mu) + const`.

Its exact local source response is therefore

`dW_M / dmu = 1 / mu`.

So once the local bilinear primitive exists, the one-generation local
pairing-side observable principle is fixed completely.

## The theorem-level statement

**Theorem (Local Pfaffian uniqueness on the Majorana bilinear lane).**
Assume the current branch’s retained local-bilinear Majorana hypothesis:

1. a future charge-`2` primitive is realized locally on the unique channel
2. that local realization is bilinear in Grassmann variables

Then:

1. the one-generation local block is canonically `A_M(mu) = mu J_2`
2. its exact finite Grassmann amplitude is `Pf(A_M) = mu`
3. independent local antisymmetric sectors factorize multiplicatively under
   Pfaffian
4. the unique additive CPT-even scalar generator on that lane is `log|Pf|`
5. equivalently, the canonical one-generation local bosonic generator is
   `W_M(mu) = log(mu) + const`

So on the retained local bilinear lane, the Pfaffian realization is forced,
not optional.

## Relationship to the earlier Majorana notes

This sharpens the current Majorana chain:

1. [NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md](./NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md)
   reduces the problem to one missing primitive
2. [NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md](./NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md)
   reduces any local bilinear realization to one complex slot
3. [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
   reduces that local realization to the canonical block `mu J_2`
4. this note says the resulting local bilinear realization is uniquely
   Pfaffian, with local generator `log(mu)`

So the Pfaffian extension should no longer be described merely as "one admitted
example" on the retained local bilinear lane. It is the unique local bilinear
realization once that lane is admitted.

What remains unclosed is not the local realization family. It is the
existence/activation theorem for the primitive itself.

## What this closes

This closes the last local-bilinear ambiguity on the Majorana lane.

The branch no longer needs to leave open:

- whether a local bilinear realization should be determinant or Pfaffian
- whether the one-generation local bosonic generator should be something other
  than `log|Pf|`
- whether the local one-generation pairing block carries any structure beyond
  `mu`

Those questions are now exact.

## What this does not close

This note does **not** prove:

- that the charge-`2` primitive exists in the full axiom
- that the axiom turns on a nonzero `mu`
- that the three-generation Majorana texture is fully derived
- that Pfaffian is the unique realization beyond the local bilinear lane

It is a uniqueness theorem for the **retained local bilinear** lane only.

## Safe wording

**Can claim**

- on the local bilinear Majorana lane, the Pfaffian realization is forced
- the canonical one-generation local bosonic generator is `log(mu)`
- the remaining honest blocker is primitive existence / activation, not local
  realization type

**Cannot claim**

- the full axiom already forces the primitive to exist
- the full DM denominator is closed

## Command

```bash
python3 scripts/frontier_neutrino_majorana_local_pfaffian_uniqueness.py
```
