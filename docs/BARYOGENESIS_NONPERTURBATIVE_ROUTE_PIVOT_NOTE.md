# Baryogenesis Nonperturbative Route Pivot Note

**Date:** 2026-04-16
**Status:** bounded current-surface route theorem on `main`
**Script:** `scripts/frontier_baryogenesis_nonperturbative_route_pivot.py`

## Safe statement

Yes, baryogenesis is still open on the current package surface.

But the live route class is now much narrower than it was even a few notes ago.

On current `main`, any same-surface baryogenesis closure must be a genuinely
nonperturbative electroweak transition / sphaleron / transport route.

It can no longer be presented as a perturbative scalar-family rescue of the old
one-loop scalar-cubic ansatz.

## What is derived here

Two exact current-surface facts are now simultaneously in force:

1. the framework already contains the native electroweak nonperturbative
   `B+L`-violating / `B-L`-preserving channel
2. the strongest perturbative same-surface scalar package currently derived on
   `main` is still far too weak to close the old route

Those two facts together force the route pivot.

## Native nonperturbative electroweak channel

The retained one-generation taste surface already satisfies:

- baryon number `B` fails to commute with the electroweak `SU(2)` algebra
- linear `B-L` anomaly cancels exactly

That is the structural sphaleron statement:

- `B+L` can be violated by electroweak nonperturbative processes
- `B-L` remains protected

So the current framework already has a native nonperturbative baryon-violating
channel. No extra structural ingredient is needed for that part.

## Strongest perturbative scalar package on current `main`

The current scalar-side surface already fixes:

1. matched one-doublet selector-equivalent multiplicity

   `n_equiv,doublet = 1 + 1/sqrt(3)`

2. maximal exact APBC endpoint normalization band

   `A_inf / A_2 = 2/sqrt(3)`

If one grants the **largest exact APBC endpoint normalization** to the matched
one-doublet scalar package on the old imported one-loop scalar-cubic ansatz,
the strongest perturbative same-surface scalar upper bound is therefore

`n_equiv,max = (1 + 1/sqrt(3)) * (2/sqrt(3)) = 1.821367...`

The current old-route targets are still:

- `3.797000` on the `m_H = 119.77 GeV` support route
- `3.770048` on the `m_H = 125.10 GeV` canonical route

So even this maximally favorable perturbative same-surface scalar package
reaches only:

- about `48.0%` of the old target on the support route
- about `48.3%` of the old target on the canonical route

and that is **before** any screening penalty.

## Exact consequence

This means the current package no longer supports the weaker reading

> maybe a more careful perturbative combination of the existing scalar pieces
> still rescues the old route.

No.

The strongest currently derived perturbative same-surface scalar package still
falls short by more than a factor of `2`, even after granting the largest exact
APBC endpoint normalization and before any screening.

## Route pivot

Since the perturbative scalar-family rescue is dead on current `main`, while
the native nonperturbative electroweak `B+L` channel is already present, the
live baryogenesis route class on current `main` is now:

- a genuinely nonperturbative electroweak transition strength computation
- plus the corresponding sphaleron survival / washout computation
- plus transport / diffusion converting the weak CP source into frozen `η`

That is the correct next target.

## What this closes

This note closes the question:

> “Could the current package still close baryogenesis through a perturbative
> scalar-side rescue of the old route if the existing ingredients are combined
> more carefully?”

Answer:

- not on current `main`
- the combined exact current-surface perturbative scalar upper bound stays
  below half of the old target
- any live current-surface route must therefore pivot to a genuinely
  nonperturbative EWPT / sphaleron / transport computation

## What remains open

This note does **not** derive:

- the nonperturbative transition strength itself
- the sphaleron rate across the transition
- the transport / diffusion solution
- the final `η`

So baryogenesis remains open.

But the open object is now sharper:

- not “some better perturbative scalar bookkeeping”
- specifically the nonperturbative electroweak transition / transport bridge

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md](./BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md)
  fixed the exact one-doublet matching boundary
- [BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md](./BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md)
  killed the old 2HDM-like same-surface route
- [BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md](./BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md)
  killed the APBC rescue hatch for that route

This note is the next logical step:

- it packages the surviving route class explicitly

## Validation

- [frontier_baryogenesis_nonperturbative_route_pivot.py](./../scripts/frontier_baryogenesis_nonperturbative_route_pivot.py)
- [BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md](./BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md)
- [BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md](./BARYOGENESIS_THERMAL_ORDER_PARAMETER_UNIQUENESS_NOTE.md)
- [BARYOGENESIS_CLOSURE_GATE_NOTE.md](./BARYOGENESIS_CLOSURE_GATE_NOTE.md)

Current runner state:

- `frontier_baryogenesis_nonperturbative_route_pivot.py`: expected `PASS>0`,
  `FAIL=0`
