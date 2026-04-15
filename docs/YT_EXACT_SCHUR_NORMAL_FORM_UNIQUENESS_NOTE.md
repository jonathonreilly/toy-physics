# Exact Schur Normal-Form Class Uniqueness Note

**Date:** 2026-04-15
**Status:** bounded support theorem
**Primary runner:** `scripts/frontier_yt_exact_schur_normal_form_uniqueness.py`

## Role

This note addresses the next microscopic question after introducing the exact
Schur coarse bridge operator:

> once the theorem object is the exact Schur coarse operator on the forced UV
> window, can it still wander across multiple normal-form classes within the
> intrinsic branch-scale remainder budget?

The answer on the current branch is no.

This is not yet full microscopic uniqueness of the bridge itself. It is the
stronger intermediate result that the **coarse operator’s normal-form class is
now unique at branch scale**.

## Setup

The previous note
[YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md](./YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md)
already promotes the theorem object from the scanned proxy family to the exact
Schur coarse bridge operator on the forced UV window.

The current branch also already has intrinsic operator-scale budgets for the
first deviations above the local selector:

- higher-order local scale: `7.123842e-3`
- nonlocal operator scale: `5.023669e-3`

So the remaining uniqueness question is no longer about arbitrary profiles. It
is about the class of exact Schur coarse operators compatible with those
intrinsic branch-scale perturbations.

## Theorem statement

> **Exact Schur Normal-Form Class Uniqueness Theorem.**
> Let `K_eff` be the exact Schur coarse bridge operator on the forced UV
> window, and let the admissible exact coarse operators be those obtained from
> the same positive local selector plus intrinsic local/nonlocal perturbations
> at or below the current branch remainder scales.
>
> Then every admissible exact coarse operator remains in the same affine
> normal-form class: its response is still nearly affine on the forced UV
> window, and its deviation from the reference coarse-operator response stays
> inside the current conservative bridge budget.

So the branch no longer has normal-form ambiguity at the coarse-operator
level.

## Meaning

This closes one real gap.

Before this note, the branch could still be read as:

- the exact object exists,
- but perhaps several different coarse normal forms remain compatible with the
  same intrinsic branch budgets.

After this note, the stronger safe read is:

- the exact object exists,
- and within the intrinsic branch-scale perturbation class it remains in one
  unique affine normal-form class.

What remains open is therefore narrower still:

> prove that the true microscopic bridge lies in this admissible Schur class.

That is a different theorem from normal-form uniqueness itself.

## What the runner checks

The runner samples a broad deterministic class of admissible exact Schur coarse
operators by perturbing the reference local selector with:

- smooth local diagonal modes up to the higher-order branch scale
- quasi-local symmetric tails up to the nonlocal operator branch scale

For every surviving positive-definite operator it checks:

1. positivity
2. affine normal-form residual
3. response distance to the reference operator
4. slope drift
5. intercept drift

## Honest boundary

This note still does **not** prove:

- full microscopic uniqueness of the exact interacting bridge
- vanishing of the remainder terms
- unbounded `y_t`

What it does prove is narrower and useful:

> once the exact bridge is reduced to the Schur coarse operator and restricted
> by the intrinsic branch-scale remainder budgets, the admissible operator does
> not jump between multiple distinct normal-form classes.

That means the remaining `y_t` gap is no longer normal-form ambiguity. It is
the microscopic theorem that the exact interacting bridge belongs to this
already-unique Schur class.
