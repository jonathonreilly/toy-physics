# Exact Schur Normal-Form Class Uniqueness Note

**Date:** 2026-04-15
**Status:** bounded support theorem
**Primary runner:** `scripts/frontier_yt_exact_schur_normal_form_uniqueness.py`

## Role

This note addresses the next microscopic question after introducing the exact
Schur coarse bridge operator:

> once the theorem object is the exact Schur coarse operator on the forced UV
> window, can it still wander across multiple normal-form classes within the
> intrinsic package-scale remainder budget?

The answer on the current package is no.

This is not yet full microscopic uniqueness of the bridge itself. It is the
stronger intermediate result that the **coarse operator’s normal-form class is
now unique on the current tested scale**.

## Setup

The previous note
[YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md](./YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md)
already promotes the theorem object from the scanned proxy family to the exact
Schur coarse bridge operator on the forced UV window.

The current package also already has intrinsic operator-scale budgets for the
first deviations above the local selector:

- higher-order local scale: `7.123842e-3`
- nonlocal operator scale: `5.023669e-3`

So the remaining uniqueness question is no longer about arbitrary profiles. It
is about the class of exact Schur coarse operators compatible with those
intrinsic package-scale perturbations.

## Theorem statement

> **Exact Schur Normal-Form Class Uniqueness Theorem.**
> Let `K_eff` be the exact Schur coarse bridge operator on the forced UV
> window, and let the admissible exact coarse operators be those obtained from
> the same positive local selector plus intrinsic local/nonlocal perturbations
> at or below the current package remainder scales.
>
> Then every admissible exact coarse operator remains in the same affine
> normal-form class: its response is still nearly affine on the forced UV
> window, and its deviation from the reference coarse-operator response stays
> inside the current conservative bridge budget.

So the current package no longer has normal-form ambiguity at the coarse-operator
level.

## Meaning

This closes one real gap.

Before this note, the current package could still be read as:

- the exact object exists,
- but perhaps several different coarse normal forms remain compatible with the
  same intrinsic package budgets.

After this note, the stronger safe read is:

- the exact object exists,
- and within the intrinsic package-scale perturbation class it remains in one
  unique affine normal-form class.

What remains open is therefore narrower still:

> prove that the true microscopic bridge lies in this admissible Schur class.

That is a different theorem from normal-form uniqueness itself.

## What the runner checks

The runner samples a broad deterministic class of admissible exact Schur coarse
operators by perturbing the reference local selector with:

- smooth local diagonal modes up to the higher-order package scale
- quasi-local symmetric tails up to the nonlocal operator package scale

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
> by the intrinsic package-scale remainder budgets, the admissible operator does
> not jump between multiple distinct normal-form classes.

That means the remaining `y_t` gap is no longer normal-form ambiguity. It is
the microscopic theorem that the exact interacting bridge belongs to this
already-unique Schur class.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with two
substantive observations:

1. The exact Schur coarse-operator setup and the intrinsic package-scale
   remainder budgets are imported from upstream rows rather than closed
   in this packet.
2. The runner samples a finite deterministic perturbation grid; the
   universal quantifier over every admissible exact coarse operator
   would also need an analytic or certified covering argument from the
   sampled grid to the full admissible class.

The note already states both qualifications in the "Setup" and "Honest
boundary" sections above. This addendum makes the upstream citations
explicit so the audit citation graph can track them, and acknowledges
the finite-sampling boundary on the runner's universal claim.

This addendum is graph-bookkeeping only. It does not change the
conditional status, does not promote the row, and does not modify the
theorem statement, the perturbation class, or the remainder budgets.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream
authorities the exact-Schur-class normal-form argument relies on. It
does not promote this note or change the audited claim scope.

- [YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md](YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md)
  for the exact Schur coarse-grained bridge operator on the forced UV
  window that supplies the reference operator and the affine
  normal-form coordinate.
- [YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md](YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md)
  for the higher-order local scale `7.123842e-3` that bounds the local
  diagonal perturbation amplitude in the runner's admissible class.
- [YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md](YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md)
  for the nonlocal operator scale `5.023669e-3` that bounds the
  quasi-local symmetric tail amplitude in the runner's admissible class.
- [YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md](YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md)
  for the leading-order Hessian selector that picks out the affine
  normal-form coordinate the runner checks across the perturbed class.
- [YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md](YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md)
  for the rearrangement step that pushes admissible perturbation mass
  toward the UV window where the affine normal form is checked.
