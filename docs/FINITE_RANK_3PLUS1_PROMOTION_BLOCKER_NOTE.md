# Finite-Rank `3+1` Promotion Blocker: the Missing Tensor Polarization Lift

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_finite_rank_3plus1_promotion_blocker.py`  
**Status:** exact finite-rank projected DtN operator plus exact scalar active-quotient amplitude law and exact Route 2 bilinear support carrier; `3+1` tensor promotion still blocked

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

The current Route 2 interface also supplies an exact support-side bilinear
carrier

`K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`

with `u_E = <E_x, q>`, `u_T = <T1x, q>`, and the exact scalar background
datum `delta_A1`.

So the current finite-rank exact data determine:

- the active orbit quotient operator
- the scalar active-quotient amplitude
- the scalar/isotropic exterior reduction
- the exact support-side bilinear carrier on the bright support channels

That is enough for the source-to-exterior and scalar source-to-metric
architecture.

## Why tensor promotion still fails

The exact finite-rank active quotient is still scalar after renormalization.
The support-to-active response operator is rank one, and the scalar active law
factors through a single channel:

`delta_sigma_active = Q_eff * m_active`

That means the exact current stack carries one active scalar degree of freedom
after quotienting.

The active orbit quotient itself does have a nontrivial second direction on the
projected DtN side, but the support side does not provide a second canonical
generator for it. Concretely, the exact support response matrix has identical
columns, so its image is one-dimensional. The exact projected DtN operator is
rank two on the active pair quotient, but the support span can only align with
one of the two active singular directions. The orthogonal active direction is
not canonically sourced by the current finite-rank support data.

The singular-value audit makes this precise:

- support singular spectrum: one dominant mode, the rest numerical nulls
- active pair quotient singular spectrum: two genuine modes
- two valid `3+1` completions differ by a large frame rotation

In the current exact run, the frame delta between two valid completions is
`1.149e+00`. That is not a numerical accident; it is the exact signature of a
noncanonical polarization choice on the current support stack.

The full `3+1` metric, by contrast, needs a tensor polarization split into at
least:

- lapse
- shift
- spatial trace / shear

The current exact finite-rank stack does not contain an exact operator that
splits the scalar active quotient into those distinct tensor channels. The
projected DtN operator is already rank two on the active orbit pair quotient,
but the support-renormalized source side still collapses to rank one. The
exact support-side bilinear carrier `K_R` is the strongest exact support-side
specialization we currently have, but it still does not canonically source the
second active quotient mode. So there is no canonical exact path from the
scalar quotient to a lapse/shift/shear polarization frame.

So the best honest conclusion is:

> the projected DtN correction operator plus the exact scalar active-quotient
> law are not enough to force the full tensorial `3+1` matching map.

## Exact minimal missing primitive

The missing primitive is now sharper than the previous blocker:

> an exact `3+1` polarization lift `Pi_3+1` that maps the scalar active
> quotient into independent lapse, shift, and spatial-trace/shear channels.

Equivalently, the finite-rank lane still lacks a tensor-valued support
observable or polarization frame that resolves the exact scalar active
amplitude into the metric components needed for full `3+1` closure before the
quotient collapses to rank one.

The minimal extra primitive is therefore:

> a tensor-valued support-side polarization frame on the active quotient,
> with rank at least three before the scalar renormalization step, so that
> lapse, shift, and spatial-trace/shear are all represented by independent
> support-side generators rather than by the single scalar total-charge mode.

The current stack only supplies one support-side generator after
renormalization, so the missing primitive is not a better scalar fit. It is
the extra tensorial support frame needed to source the second active direction
canonically before any scalar collapse.

## Support-side polarization-frame attempt

The finite-rank support data were checked directly for a canonical
polarization frame on the active quotient. The exact result is that the
support-side response remains rank one after renormalization, while the active
quotient is rank two. The second active quotient direction cannot be sourced
canonically from the current support span without adding new independent
support generators before the scalar collapse.

The exact attempt and the rank obstruction are recorded in:

- [FINITE_RANK_SUPPORT_POLARIZATION_FRAME_NOTE.md](./FINITE_RANK_SUPPORT_POLARIZATION_FRAME_NOTE.md)

## Verdict

Finite-rank widening now has:

- exact projected DtN correction operator: yes
- exact support-renormalized active-quotient amplitude law: yes
- exact scalar/isotropic `3+1` reduction: yes
- exact tensorial `3+1` matching map: no

So the widening lane has moved one theorem step further, but the remaining gap
is not more scalar structure. It is the missing tensor polarization lift.
