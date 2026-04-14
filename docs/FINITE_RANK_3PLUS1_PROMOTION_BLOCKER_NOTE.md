# Finite-Rank `3+1` Promotion Blocker: the Missing Tensor Polarization Lift

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_finite_rank_3plus1_promotion_blocker.py`  
**Status:** exact finite-rank projected DtN operator plus exact scalar active-quotient amplitude law; `3+1` tensor promotion still blocked

## Purpose

The finite-rank widening lane now has two exact ingredients:

1. the projected DtN / Schur correction operator on the active orbit quotient
2. the exact support-renormalized scalar amplitude law on the active quotient

The remaining question is whether those two exact objects already force a full
lapse-shift-spatial `3+1` matching law.

This note answers that question sharply:

> they do not.

## What is exact

The widening lane has an exact projected microscopic correction operator on
the active orbit quotient, and after support renormalization the active
correction collapses exactly through the scalar total charge
`Q_eff = 1^T q_eff`.

So the current finite-rank exact data determine:

- the active orbit quotient operator
- the scalar active-quotient amplitude
- the scalar/isotropic exterior reduction

That is enough for the source-to-exterior and scalar source-to-metric
architecture.

## Why tensor promotion still fails

The exact finite-rank active quotient is still scalar after renormalization.
The support-to-active response operator is rank one, and the scalar active law
factors through a single channel:

`delta_sigma_active = Q_eff * m_active`

That means the exact current stack carries one active scalar degree of freedom
after quotienting.

The full `3+1` metric, by contrast, needs a tensor polarization split into at
least:

- lapse
- shift
- spatial trace / shear

The current exact finite-rank stack does not contain an exact operator that
splits the scalar active quotient into those distinct tensor channels.

So the best honest conclusion is:

> the projected DtN correction operator plus the exact scalar active-quotient
> law are not enough to force the full tensorial `3+1` matching map.

## Exact minimal missing primitive

The missing primitive is now sharper than the previous blocker:

> an exact `3+1` polarization lift `Pi_3+1` that maps the scalar active
> quotient into independent lapse, shift, and spatial-trace/shear channels.

Equivalently, the finite-rank lane still lacks a tensor-valued quotient
operator that separates the exact scalar active amplitude into the metric
components needed for full `3+1` closure.

## Verdict

Finite-rank widening now has:

- exact projected DtN correction operator: yes
- exact support-renormalized active-quotient amplitude law: yes
- exact scalar/isotropic `3+1` reduction: yes
- exact tensorial `3+1` matching map: no

So the widening lane has moved one theorem step further, but the remaining gap
is not more scalar structure. It is the missing tensor polarization lift.
