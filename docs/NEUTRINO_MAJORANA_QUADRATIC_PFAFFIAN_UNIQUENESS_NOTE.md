# Majorana Quadratic Pfaffian Uniqueness

**Date:** 2026-04-15  
**Status:** exact finite-quadratic uniqueness theorem on the one-generation
Majorana lane; not an axiom-forcing theorem  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_quadratic_pfaffian_uniqueness.py`

## Question

The current lane already says that a future nonzero one-generation Majorana
response would require a new charge-`2` primitive and a new observable/source
grammar beyond the retained determinant lane.

Within the class of **finite quadratic fermionic completions**, is the
Pfaffian/Nambu route merely one convenient choice, or is it already unique?

## Bottom line

It is unique at quadratic level.

For a finite quadratic Grassmann completion:

1. the quadratic kernel contributes only through its antisymmetric part
2. the finite Berezin integral of `exp(1/2 theta^T A theta)` is exactly
   `Pf(A)`
3. independent quadratic sectors multiply at the partition level and therefore
   add at the `log|Pf|` level
4. on the one-generation local Majorana lane, the canonical block is still
   `A_M(mu) = mu J_2`

So inside the finite quadratic completion class, there is no second observable
grammar competing with Pfaffian. Any future non-Pfaffian route would have to
be genuinely **beyond quadratic Gaussian form**.

## Inputs

This theorem uses:

- [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
- [NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md)
- [NEUTRINO_MAJORANA_OBSERVABLE_GRAMMAR_BOUNDARY_NOTE.md](./NEUTRINO_MAJORANA_OBSERVABLE_GRAMMAR_BOUNDARY_NOTE.md)

The logical role is:

- the canonical-local-block note fixes the one-generation local charge-`2`
  direction to `mu J_2`
- the Pfaffian-extension note identifies one exact quadratic realization
- the observable-grammar boundary note says a future nonzero response requires
  a new grammar beyond the determinant lane

This note now closes the quadratic sub-question:

> if the new grammar is still finite and quadratic, does any alternative to
> Pfaffian remain?

Answer: no.

## Exact theorem

There are four exact steps.

### 1. Symmetric quadratic data drop out of Grassmann bilinears

For Grassmann variables `theta_i theta_j = - theta_j theta_i`, the quadratic
form

`1/2 theta^T M theta`

depends only on the antisymmetric part

`A = (M - M^T)/2`.

So a finite quadratic fermionic completion is already an antisymmetric-kernel
problem.

### 2. Finite quadratic Grassmann integration gives a Pfaffian

For even-dimensional antisymmetric `A`,

`Z_quad[A] = int dtheta exp(1/2 theta^T A theta) = Pf(A)`.

This is not a model choice. It is the exact finite Berezin integral.

### 3. Additivity forces `log|Pf|` on independent quadratic sectors

If

`A = A_1 ⊕ A_2`,

then

`Pf(A) = Pf(A_1) Pf(A_2)`.

So the same additive CPT-even scalar logic that gave `log|det|` on the normal
Gaussian gives

`W_quad[A] = log|Pf(A)|`

on the quadratic antisymmetric completion class.

### 4. The one-generation local block remains `mu J_2`

On the current one-generation Majorana lane, the local quadratic charge-`2`
completion is still the unique canonical block

`A_M(mu) = mu J_2`.

Its finite quadratic partition amplitude is

`Pf(A_M(mu)) = mu`.

So the one-generation local quadratic completion class has:

- one canonical block
- one quadratic partition law
- one additive CPT-even scalar generator `log|Pf|`

No second quadratic source-response grammar remains.

## The theorem

**Theorem (Quadratic Pfaffian uniqueness on the one-generation Majorana lane).**
Assume a future one-generation Majorana completion is finite and quadratic in
Grassmann variables. Then its microscopic kernel is antisymmetric, its exact
partition amplitude is Pfaffian, and its additive CPT-even scalar observable
grammar is `log|Pf|`. On the canonical one-generation local channel, the block
is `A_M(mu) = mu J_2`.

Equivalently: within the finite quadratic completion class, Pfaffian is not
just minimal but unique.

## What this closes

This closes the next honest science question after the observable-grammar
boundary.

Before:

- a future nonzero Majorana response required a new observable grammar beyond
  the determinant lane
- but one could still imagine multiple inequivalent quadratic grammars

After:

- no such quadratic ambiguity remains
- any future non-Pfaffian route would have to be genuinely non-quadratic

## What this does not close

This note does **not** prove:

- that a quadratic Pfaffian/Nambu sector is axiom-forced
- that the future extension must be quadratic
- that no non-quadratic charge-`2` completion could exist
- that the three-generation neutrino problem is closed

It is a quadratic-class uniqueness theorem only.

## Safe wording

**Can claim**

- every finite quadratic one-generation Majorana completion is Pfaffian in
  exact Grassmann integration
- within the quadratic class, Pfaffian is unique rather than merely minimal
- any future non-Pfaffian route would have to be non-quadratic

**Cannot claim**

- the Pfaffian sector is already axiom-forced
- all future charge-`2` routes must be quadratic
- the full neutrino problem is solved

## Command

```bash
python3 scripts/frontier_neutrino_majorana_quadratic_pfaffian_uniqueness.py
```
