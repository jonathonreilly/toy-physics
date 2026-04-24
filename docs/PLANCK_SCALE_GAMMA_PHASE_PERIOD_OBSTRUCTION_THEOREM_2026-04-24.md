# Planck-Scale Gamma Phase-Period Obstruction Theorem

**Date:** 2026-04-24
**Status:** hbar/gamma no-go theorem for periodicity and finite-root routes alone
**Verifier:** `scripts/frontier_planck_gamma_phase_period_obstruction_theorem.py`

## Question

Can the remaining scalar

`gamma = Phi(I_16)`

be forced to equal `1` by phase periodicity alone, or by a finite root-of-unity
central level alone?

## Result

Not from phase periodicity or finite roots alone, on the current surface.

The primitive action phase enters as

`exp(i Phi)`.

The phase group only knows `Phi` modulo `2 pi`. Therefore phase periodicity can
identify

`Phi ~ Phi + 2 pi n`,

but it cannot distinguish the real representative `Phi = 1` from any other
representative without an additional real action-unit normalization.

Likewise, a finite central extension can quantize a phase level or root of
unity, but its natural units are periods or rational fractions of `2 pi`:

`Phi = 2 pi k / N`.

Setting this equal to `1` would require

`N = 2 pi k`,

which is impossible for integer `N, k` unless an extra non-periodic conversion
is introduced. Thus central-extension quantization can produce a level, but it
does not produce the dimensionless radian value `gamma = 1`.

## Scope Guardrail

This is a narrow no-go theorem. It does **not** block every central-extension
or projective-phase route.

It blocks only the following inference:

> because the primitive readout is a U(1) phase, or because a finite
> root-of-unity level exists, the real reduced action normalization is
> automatically `gamma = 1`.

The theorem leaves open any route that derives an additional real unit map,
for example:

1. a noncompact action-valued central extension whose primitive generator is
   normalized before exponentiation;
2. an index/spectral-flow theorem equating one primitive event cell with one
   real action unit;
3. a projective cocycle theorem deriving `q_atom = 1/16` directly in a
   consistently rewritten turns/cycles convention;
4. a microscopic action/Ward identity fixing `Phi(I_16)=1`.

The review instruction is therefore "do not close `gamma = 1` by bare
periodicity," not "abandon all projective or central-extension attacks."

## Theorem 1: U(1) periodicity does not select gamma one

The unitary readout is

`U = exp(i gamma)`.

For any integer `n`,

`exp(i gamma) = exp(i (gamma + 2 pi n))`.

Thus the periodic phase observable cannot select a unique real value of
`gamma`. It selects an equivalence class in `R / 2 pi Z`.

The statement

`gamma = 1`

is a real normalization statement, not a U(1)-periodicity theorem.

## Theorem 2: finite central roots do not give gamma one

Assume a finite central-extension route gives a primitive phase

`gamma = 2 pi k / N`,

with integers `k, N`.

If this is to equal `1`, then

`2 pi k = N`.

Since `pi` is irrational, no nonzero integer pair satisfies this equation.

Therefore finite root-of-unity quantization cannot derive the exact real value
`gamma = 1`.

It can still be useful, but only by changing the target. For example, it might
derive a phase measured in turns rather than radians. That would require
rewriting the action-phase reduction consistently. It is not the current
`q_atom = gamma/16` theorem.

## Adversarial Check

The possible objection is:

> A finite central extension can give a 16th root of unity, and the lane needs
> `1/16`; why is that not the same result?

Answer: it may be relevant, but it is not the same theorem unless the
normalization convention is rebuilt. A 16th root gives phase
`exp(2 pi i / 16)`. In the current action-phase convention, the exponent is
`exp(i Phi)`, so this corresponds to `Phi = 2 pi / 16`, not `Phi = 1/16` or
`gamma = 1`. To use the root-of-unity result, the program must rewrite the
elementary action-phase reduction in turns/cycles and track every `2 pi`
factor. That remains a legitimate open route.

## Consequence

The remaining `gamma = 1` theorem cannot come from:

1. bare U(1) phase periodicity alone;
2. finite root-of-unity central quantization alone;
3. another homogeneous trace/naturality argument.

It must come from a non-homogeneous real action-unit law:

`Phi(I_16) = 1`.

Equivalently:

`S_cell = hbar`.

That is an action-unit primitive or a theorem from a deeper microscopic action
normalization. It is not contained in the current event algebra plus phase
periodicity.

## Safe Claim

Use:

> Phase periodicity and central extensions can quantize phase classes, but they
> do not select the real reduced action value `gamma = 1`. The remaining hbar
> lock is a non-periodic action-unit normalization `Phi(I_16)=1`, unless the
> whole action-phase lane is consistently rewritten in a different convention.

Do not use:

> U(1) phase periodicity derives `gamma = 1`.

Do not use:

> Finite central extensions are irrelevant to the hbar lane.
