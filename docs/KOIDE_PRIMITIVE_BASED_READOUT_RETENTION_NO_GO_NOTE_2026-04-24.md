# Koide primitive-based readout retention no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_primitive_based_readout_retention_no_go.py`  
**Status:** no-go for retained-only promotion; primitive-based readout remains
a positive theorem only under a new physical law

## Theorem Attempt

The primitive-based readout packet closes the dimensionless Koide lane under
one explicit physical law:

```text
primitive_based_operational_boundary_readout
```

This audit asks the stronger Nature-grade question: does the current retained
`Cl(3)/Z3` and APS/boundary package already force that law?

Precise attempted theorem:

> Retained charged-lepton source and boundary readouts are primitive, based
> functors on the operational quotient; therefore source-visible C3 orbit
> labels, spectator boundary channels, and unbased endpoint phases are all
> excluded without adding a new primitive.

## Brainstormed Variants

1. **Source-orbit descent:** quotient-isomorphic source components must carry
   equal probability.
2. **Primitive boundary channel:** the selected Brannen line is the only
   boundary channel, so `spectator_channel=0`.
3. **Based endpoint lift:** endpoint-exact kernel phases vanish, so `c=0`.
4. **What if C3 labels remain physical?** Then `{0}` and `{1,2}` distinguish
   the source components and `w_plus` is free.
5. **What if the boundary has spectators?** Then the closed APS value can split
   across selected and spectator channels.
6. **What if the endpoint lift is unbased?** Then a constant endpoint-exact
   phase shifts the open value.

The route is strong because it unifies the Q and delta residuals, but it is not
retained unless these three exclusions are derived rather than named.

## Exact No-Go

### Q Side

Primitive source descent would impose:

```text
w = 1 - w
```

and hence:

```text
w = 1/2
K_TL = 0
Q = 2/3.
```

The retained embedded carrier still has source-visible C3 orbit labels:

```text
plus = {0}
perp = {1,2}
```

With those labels retained, normalization gives only:

```text
p_plus + p_perp = 1
```

so one scalar remains free.  The exact retained counterstate is:

```text
w_plus = 1/3
Q = 1
K_TL = 3/8.
```

### Delta Side

Primitive based boundary readout would impose:

```text
selected_channel = 1
spectator_channel = 0
c = 0
```

so:

```text
delta_open = eta_closed.
```

The retained boundary data do not force those constraints.  Exact
countermodels remain:

```text
selected=1/2, spectator=1/2, c=0 -> delta_open=1/9
selected=1, spectator=0, c=1/9 -> delta_open=1/3
```

with the closed APS support value still:

```text
eta_APS = 2/9.
```

## Hostile Review

- **Target import:** none.  `Q=2/3` and `delta=2/9` are not assumptions.
- **Hidden observational pin:** none.
- **Renamed primitive:** exact.  Primitive-based readout packages three
  residual constraints unless derived from retained physics.
- **Missing axiom link:** exact.  Current retained data do not exclude
  source-visible C3 labels, spectator boundary channels, or unbased endpoint
  lifts.
- **Closure claim:** rejected for retained-only closure.

## Residual

```text
RESIDUAL_SCALAR =
  derive_primitive_based_readout_law_from_retained_physics

RESIDUAL_Q =
  source_visible_C3_orbit_labels_not_excluded

RESIDUAL_DELTA =
  spectator_channel_or_unbased_endpoint_not_excluded
```

## Musk Simplification Pass

1. **Make requirements less wrong:** the requirement is not "accept a better
   readout law"; it is "derive why the physical readout must be primitive and
   based."
2. **Delete:** remove the delta spectator and basepoint clauses when working
   the Q-only lane; the Q obstruction is still just source-visible C3 labels.
3. **Simplify:** the Q proof reduces to one scalar equation `w=1/2`.
4. **Accelerate:** future Q attacks should test retained reasons why `{0}` and
   `{1,2}` cannot be source labels.
5. **Automate:** this runner prevents positive new-law packets from being
   promoted as retained closure.

## Verification

Run:

```bash
python3 scripts/frontier_koide_primitive_based_readout_retention_no_go.py
python3 scripts/frontier_koide_primitive_based_readout_nature_review.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_PRIMITIVE_BASED_READOUT_RETENTION_NO_GO=TRUE
Q_PRIMITIVE_BASED_READOUT_RETENTION_CLOSES_Q=FALSE
DELTA_PRIMITIVE_BASED_READOUT_RETENTION_CLOSES_DELTA=FALSE
RESIDUAL_SCALAR=derive_primitive_based_readout_law_from_retained_physics
RESIDUAL_Q=source_visible_C3_orbit_labels_not_excluded
RESIDUAL_DELTA=spectator_channel_or_unbased_endpoint_not_excluded
```
