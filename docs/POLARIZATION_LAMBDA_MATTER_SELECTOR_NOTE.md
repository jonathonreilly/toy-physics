# Polarization Lambda Matter/Anomaly Selector Audit

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Ownership:** matter/anomaly selector only  
**Scope:** test whether anomaly-forced `3+1`, left/right-handed structure,
matter-current coupling, or canonical stress/momentum channels distinguish
the two universal weight-1 sectors and thereby fix `lambda`

## Verdict

The matter/anomaly stack does **not** canonically fix `lambda`.

What it does fix is real:

- anomaly-forced time gives a single clock and a definite chirality/orientation;
- the matter/generation theorems distinguish taste orbits and RH completion;
- current and stress/momentum probes produce exact observables on the atlas.

What it does **not** do is choose between the two universal weight-1 sectors.
Every exact matter/anomaly probe currently available is either common-mode on
that multiplicity space or acts on a different representation sector
altogether.

So the strongest exact conclusion from the matter/anomaly stack is negative:

> the remaining `lambda` freedom survives as the connected `SO(2)` residual
> gauge on the dark plane.

## What was checked

### 1. Anomaly-forced `3+1`

[`ANOMALY_FORCES_TIME_THEOREM.md`](/private/tmp/physics-review-active/docs/ANOMALY_FORCES_TIME_THEOREM.md)
fixes the temporal direction:

`d_t = 1`.

That is an exact orientation result, but it acts on the time/orientation
structure, not on the universal weight-1 multiplicity space. The time selector
audit already shows that the exact Route-2 semigroup and phase bridge are
common-mode across the weight-1 sectors.

So anomaly-forced `3+1` does not determine `lambda`.

### 2. Left/right-handed structure

[`RIGHT_HANDED_SECTOR_NOTE.md`](/private/tmp/physics-review-active/docs/RIGHT_HANDED_SECTOR_NOTE.md)
and the generation anomaly notes do fix the fermionic completion story:

- 3D taste space has no chirality by itself;
- the 4D extension supplies chirality;
- anomaly cancellation fixes the RH hypercharges;
- discrete `Z_3` and continuous anomaly structure constrain generation
  assignment.

But those results live in the matter/generation sector, not in the universal
`weight-1` complement sector that carries `lambda`.

The generation theorem distinguishes orbit sectors in taste space. It does not
choose between the two universal weight-1 doublets.

### 3. Matter-current coupling

The transport/current probes do not distinguish the two weight-1 sectors.

Relevant audits:

- [`STAGGERED_TWO_BODY_LINK_CURRENT_NOTE_2026-04-11.md`](/private/tmp/physics-review-active/docs/STAGGERED_TWO_BODY_LINK_CURRENT_NOTE_2026-04-11.md)
- [`STAGGERED_TWO_BODY_MOMENTUM_FLUX_NOTE_2026-04-11.md`](/private/tmp/physics-review-active/docs/STAGGERED_TWO_BODY_MOMENTUM_FLUX_NOTE_2026-04-11.md)

Both exact transport probes keep the force channel but fail as selectors:

- the mid-plane link current stays `0/45` inward;
- the packet-local momentum flux stays `0/45` inward.

So matter-current coupling does not supply a canonical selector for the two
weight-1 sectors.

### 4. Canonical stress/momentum channels

The stress law is exact at orbit-mean resolution, but not sector-selective.

Relevant audits:

- [`REDUCED_OUTER_SHELL_STRESS_LAW_NOTE.md`](/private/tmp/physics-review-active/docs/REDUCED_OUTER_SHELL_STRESS_LAW_NOTE.md)
- [`ORBIT_MEAN_WHOLE_SHELL_STRESS_LAW_NOTE.md`](/private/tmp/physics-review-active/docs/ORBIT_MEAN_WHOLE_SHELL_STRESS_LAW_NOTE.md)

These notes show:

- exact reduced outer-shell stress on the static isotropic bridge;
- exact orbit-mean whole-shell stress;
- bounded within-orbit corrections for the broader finite-rank family.

But orbit-mean stress is still not a canonical section of the universal
weight-1 complement. It preserves the residual `SO(2)` orbit freedom instead of
choosing an angle.

## Strongest matter/anomaly statement

The strongest exact statement the matter/anomaly stack gives is:

1. time/orientation is fixed;
2. chirality/RH completion is fixed;
3. generation orbits are distinguished in taste space;
4. current and stress observables remain common-mode on the universal
   weight-1 multiplicity space.

Therefore the universal lift remains

`L_lambda(D) = (cos(lambda) D, sin(lambda) D)`

with `lambda` unfixed.

## Exact residual obstruction

The exact residual obstruction is still:

> the connected `SO(2)` dark-plane gauge, equivalently the one-parameter
> family `L_lambda`.

The matter/anomaly atlas does not supply a primitive that turns the shared
orbit coordinate into a canonical section.

## Bottom line

The matter/anomaly stack is strong enough to fix the matter sector and the
time/chirality structure, but it does **not** distinguish the two universal
weight-1 sectors. The remaining obstruction is exact and one-parameter.
