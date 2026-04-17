# Three-Generation `Z_3` Majorana Non-Activation Theorem

**Date:** 2026-04-15  
**Status:** exact non-activation theorem on the current retained stack  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_z3_nonactivation_theorem.py`

## Question

After the one-generation Majorana lane has been reduced to:

- one unique charge-`2` channel
- one local source slot
- one real local amplitude `mu = |m|`

can the retained **three-generation** / `Z_3` structure itself turn that
source on and close the `A/B/epsilon` texture?

## Bottom line

No.

The three-generation / `Z_3` lift changes the **texture** of a would-be
Majorana pairing block, but not its fermion-number charge sector.

For any symmetric generation matrix `M`, the canonical pairing block

`Delta(M) = M \otimes J_2`

defines a charge-`-2` pairing operator on the finite fermionic surface. In
particular, the usual `Z_3` texture

`M_Z3 = [[A, 0, 0], [0, eps, B], [0, B, eps]]`

still lies entirely in that charge-`-2` sector.

Therefore the exact `U(1)` selection rule on the current finite retained normal
grammar forces its expectation to vanish.

So the retained three-generation / `Z_3` structure can organize an **already
activated** Majorana sector, but it cannot activate that sector on the current
stack.

## Inputs

This theorem reuses:

- [NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md](./NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md)
- [NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md)
- [THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md)
- [NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md](./NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md)
- [NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md](./NEUTRINO_MAJORANA_PHASE_REMOVAL_NOTE.md)

The exact chain already fixes:

1. the one-generation local Majorana source sector is unique
2. the current retained normal grammar cannot activate any charge-`2` object
3. the full three-generation matter structure is retained as physical species
   structure, but not as quantitative flavor closure

So the remaining honest question is whether the three-generation / `Z_3`
texture itself can rescue activation.

## Exact theorem

There are three exact steps.

### 1. Three-generation texture is still a pairing block

Let `M` be any symmetric `3 x 3` generation matrix and let `J_2` be the
canonical one-generation antisymmetric pairing block.

Then

`Delta(M) = M \otimes J_2`

is antisymmetric, so it defines a legitimate three-generation pairing block.

For the usual `Z_3` ansatz

`M_Z3 = [[A, 0, 0], [0, eps, B], [0, B, eps]]`,

the generation matrix organizes exactly one singlet eigenvalue `A` and one
doublet pair `eps ± B`.

So `A/B/epsilon` is a **texture structure**, not an activation law.

### 2. Every such texture stays in charge `-2`

On the canonical six-mode three-generation pairing surface, the operator
associated with `Delta(M)` has exact fermion-number charge `-2` for **every**
symmetric `M`.

So lifting from one generation to three generations does not move the object
out of the charge-`-2` sector.

### 3. The retained normal grammar still kills it

The current finite retained grammar is still charge-zero and exactly
`U(1)`-invariant.

Therefore every charge-`-2` operator continues to have zero expectation on
that finite surface, including the full three-generation / `Z_3` pairing
texture.

So the exact finite-grammar no-go survives the generation lift intact.

## The theorem-level statement

**Theorem (Three-generation / `Z_3` Majorana non-activation on the current
stack).**
Assume the current retained normal grammar, the retained three-generation
matter structure, and any symmetric three-generation coefficient matrix `M`
carried by the canonical pairing block `Delta(M) = M \otimes J_2`. Then:

1. `Delta(M)` remains a charge-`-2` pairing object
2. the exact `U(1)` selection rule of the retained normal grammar forces its
   expectation to vanish
3. in particular, the usual `Z_3` texture `[[A,0,0],[0,eps,B],[0,B,eps]]`
   cannot activate a Majorana sector on the current stack

Equivalently: three-generation / `Z_3` structure can shape a Majorana matrix
after activation, but it cannot provide the missing activation law.

## What this closes

This closes the next honest escape hatch:

- maybe the one-generation no-go disappears once the full three-generation
  `Z_3` texture is included

Answer: no.

So the blocker is now exact and sharper:

- not “derive the three-generation texture”
- not “refine the `Z_3` phase”
- but derive a genuinely new charge-`2` primitive / activation law beyond the
  retained normal grammar

Only after that can the generation / `Z_3` side organize the resulting
Majorana sector into `A/B/epsilon`.

## What this does not close

This note does **not** prove:

- that no future extension can activate the Majorana sector
- that `A/B/epsilon` can never be derived
- that the full neutrino or DM denominator problem is closed negatively

It is an exact non-activation theorem on the **current retained stack** only.

## Safe wording

**Can claim**

- the retained three-generation / `Z_3` lift does not evade the charge-`2`
  non-activation obstruction
- the `A/B/epsilon` texture can only shape an admitted pairing sector; it does
  not activate one on the present stack
- the remaining exact blocker is a genuinely new charge-`2` primitive /
  activation law

**Cannot claim**

- the framework can never derive the needed activation law
- the final neutrino answer is negative in principle

## Command

```bash
python3 scripts/frontier_neutrino_majorana_z3_nonactivation_theorem.py
```
