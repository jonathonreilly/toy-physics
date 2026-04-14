# Finite-Rank Support-Renormalized Active-Shell Amplitude Law

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_finite_rank_support_active_amplitude_law.py`  
**Status:** exact scalar amplitude law on the active quotient; bounded `3+1` metric reduction remains open

## Purpose

The projected DtN correction operator on the finite-rank widening class
already isolates a finite active orbit quotient. The remaining question is
whether the microscopic support renormalization itself determines the active
quotient amplitude, rather than merely the active direction.

This note closes that scalar ambiguity.

## Exact scalar amplitude law

On the current finite-rank widening class, the microscopic support-to-active
response operator is exact rank one.

Let `q_eff` be the renormalized support weights and let

`Q_eff = 1^T q_eff`

be the total renormalized support charge.

Then the active-sector correction factors exactly through `Q_eff`:

`delta_sigma_active = Q_eff * m_active`

and the same law holds on the active pair quotient.

Here `m_active` is the universal unit-charge active mode on the reduced
quotient. The exact local `O_h` and broader finite-rank source families both
satisfy this law at machine precision.

## What this closes

This closes the remaining scalar-amplitude ambiguity on the active orbit
quotient:

> the active correction is not only governed by an exact projected DtN /
> Schur-complement operator, but also by an exact support-renormalized
> scalar amplitude law.

So the active quotient is now controlled by:

1. the exact projected DtN correction operator
2. the exact support-renormalized amplitude law through `Q_eff`

## What this does not close

This note still does **not** close the tensorial `3+1` matching map. The
active quotient amplitude is exact, but the promotion from that scalar law to
the full tensorial `3+1` metric remains open.

## Updated target

After this note, the finite-rank widening frontier narrows to:

> derive the tensorial `3+1` matching law from the exact support-renormalized
> active-shell amplitude law and the projected DtN correction operator.

The sharper missing primitive is now isolated in:

- [FINITE_RANK_3PLUS1_PROMOTION_BLOCKER_NOTE.md](./FINITE_RANK_3PLUS1_PROMOTION_BLOCKER_NOTE.md)
