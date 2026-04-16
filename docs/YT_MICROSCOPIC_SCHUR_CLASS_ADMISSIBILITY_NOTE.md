# Microscopic Schur-Class Admissibility Note

**Date:** 2026-04-15
**Status:** bounded support theorem
**Primary runner:** `scripts/frontier_yt_microscopic_schur_class_admissibility.py`

## Role

This note addresses the last structural objection left after:

- the exact coarse-grained bridge operator;
- exact Schur normal-form uniqueness;
- the Schur stability gap.

The remaining question was:

> perhaps the exact interacting bridge exists, but axiom-native microscopic
> local positive realizations still reduce into some other coarse class not
> captured by the current Schur normal form.

The current package answer is now no on the current tested scale.

## Theorem statement

> **Microscopic Schur-Class Admissibility Theorem.**
> Start from axiom-native microscopic bridge operators on the accepted UV
> window that are:
>
> - finite;
> - local / quasi-local in the lattice variables;
> - symmetric positive definite;
> - reduced exactly by Schur/Feshbach marginalization.
>
> Then, on the current package locality tube around the accepted bridge data,
> every surviving exact microscopic reduction lands in the same unique stable
> Schur normal-form class and stays inside the current conservative endpoint
> budget.

So the current package no longer carries a separate microscopic-admissibility loophole
at this scale.

## What changed

Earlier bridge results had already shown:

1. the theorem object is the exact coarse Schur operator;
2. that coarse operator has a unique normal-form class under intrinsic package
   local/nonlocal budgets;
3. that class sits in an open stability basin.

What remained open was whether microscopic local positive bridge operators
could reduce outside that class anyway.

This note closes that current-tested-scale loophole.

## Meaning

The read is now:

- the microscopic bridge is reduced exactly by Schur complement;
- local positive microscopic realizations compatible with the branch bridge
  data reduce into the same unique stable Schur class;
- the remaining YT gap is not coarse-class admissibility;
- it is only the explicit endpoint budget carried by that exact bridge.

That is a cleaner endgame than “the bridge is still bounded because the exact
microscopic object may not even belong to the class we are using.”

## Honest boundary

This note still does **not** prove:

- vanishing of the explicit endpoint budget;
- unbounded `y_t`;
- that every conceivable microscopic realization outside the tested locality
  tube must do the same.

What it *does* prove is the stronger tested-scale statement needed now:

> within the axiom-native microscopic locality tube around the accepted bridge
> data, microscopic admissibility into the exact Schur class is closed.

That means the remaining status question is no longer structural. It is purely
about the size and interpretation of the remaining explicit bridge budget.
