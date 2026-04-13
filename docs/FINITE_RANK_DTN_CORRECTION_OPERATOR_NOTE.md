# Projected DtN Correction Operator for the Finite-Rank Non-`O_h` Sector

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_finite_rank_dtn_correction_operator.py`  
**Status:** Exact projected microscopic correction operator plus bounded active-mode consequence

## Purpose

The earlier gravity notes had already established three separate facts:

1. the exact sewing shell is a lattice-native discrete DtN object
2. the non-`O_h` remainder on the sewing band lives on four active cubic
   orbit channels
3. the current exact local `O_h` and broader finite-rank families excite the
   same universal active orbit pattern after normalization

What was still missing was the operator-level statement that ties those
observations to the microscopic lattice solve itself.

This note closes that gap at the reduced active-sector level.

## Exact projected correction operator

Let `R = 4` and consider the sewing band `3 < r <= 5`. On that band the
anisotropic shell remainder

`delta_sigma = sigma_R - sigma_rad`

has support only on the four active orbit channels

`(3,2,2)`, `(3,3,0)`, `(4,1,0)`, `(4,1,1)`.

Now choose the four normalized orbit-channel basis sources on that band and
apply the exact microscopic lattice solve. The resulting map from orbit-
channel source coefficients to orbit-channel correction coefficients is the
projected DtN / Schur-complement response operator.

The script constructs that operator directly from the lattice solve. It does
not fit the matrix from family data.

## Exact structural result

The projected active-sector operator has exact row antisymmetry:

- the `(3,2,2)` row is the negative of the `(4,1,0)` row
- the `(3,3,0)` row is the negative of the `(4,1,1)` row

So the correction operator factors through the two pair channels

- `(3,2,2) / (4,1,0)`
- `(3,3,0) / (4,1,1)`

This is the finite-dimensional quotient of the microscopic DtN map that
governs the non-`O_h` sewing-band deviation.

## Bounded active-mode consequence

On that reduced pair quotient, the operator has two nonzero singular values.
Its leading output singular vector aligns with the universal orbit pattern
already extracted from the exact local `O_h` and finite-rank source families.

So the universal non-`O_h` sewing-band correction is not an ad hoc fit:

> it is the leading output mode of the exact microscopic projected DtN
> correction operator on the active orbit quotient

The finite-rank family also lands very close to that same line, so the
observed correction is governed by the same lattice operator rather than by
family-specific tuning.

## What this closes

This closes the strongest remaining operator-level ambiguity on the active
non-`O_h` sector:

> the correction pattern is already an exact microscopic boundary operator on
> the active orbit quotient, not a post hoc regression on shell data

## What this still does not close

This note still does **not** close:

1. the derivation of the full 4D spacetime closure
2. the lift from the active pair quotient to the complete nonlinear sewing
   law
3. the exact scalar amplitude relation between the support Schur complement
   and the observed active singular mode

## Updated gravity target

After this note, the perturbative target narrows again:

- the non-`O_h` correction is an exact projected DtN / Schur-complement
  operator on the active orbit quotient
- the remaining theorem target is to derive the scalar amplitude on that
  quotient directly from the support renormalization, then promote the result
  into the full 4D closure
