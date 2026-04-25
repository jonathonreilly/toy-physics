# Koide primitive-based readout closure theorem

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_primitive_based_readout_closure_theorem.py`  
**Status:** positive closure under a new physical readout law; not retained-only closure

## New Physical Law

The charged-lepton source and boundary endpoint readouts are primitive, based
functors on the operational quotient:

```text
source:
  quotient-isomorphic source components carry no distinguishable charge;

boundary:
  the physical selected Brannen line is the primitive rank-one boundary channel;
  the endpoint lift is based at the vacuum/identity section.
```

Equivalently:

```text
source probabilities are invariant on quotient orbits;
spectator_channel = 0;
endpoint-exact kernel phase c = 0.
```

## Q Theorem

The two source components lie in one quotient orbit.  Descent gives:

```text
w_plus = w_perp
w_plus + w_perp = 1
```

therefore:

```text
w_plus = w_perp = 1/2
K_TL = 0
Q = 2/3.
```

This is the two-object case of general finite-orbit descent, not a fitted
Koide value.

## Delta Theorem

The open endpoint has:

```text
delta_open = selected_channel eta_closed + c.
```

Primitive based readout gives:

```text
selected_channel = 1
spectator_channel = 0
c = 0.
```

Therefore, for arbitrary closed `eta`:

```text
delta_open = eta_closed.
```

The retained APS calculation supplies the value:

```text
eta_APS = 2/9
```

so:

```text
delta_open = 2/9.
```

## Why This Is Not Target Import

- The source theorem is orbit descent plus normalization.  `Q` is computed
  afterward.
- The endpoint theorem is symbolic in `eta_closed`; it transfers arbitrary
  closed eta values.
- `2/9` enters only through the independent APS fixed-point computation.
- The basepoint statement is `c = 0` for all endpoints, not the value needed
  only for `2/9`.

## Falsifiers

The theorem fails as physics if any of the following are retained:

```text
source-visible quotient labels;
spectator boundary channel;
unbased endpoint lift.
```

Executable countermodels in the runner:

```text
w_plus = 1/3 -> Q = 1, K_TL = 3/8
selected = 1/2, spectator = 1/2, c = 0 -> delta_open = 1/9
selected = 1, spectator = 0, c = 1/9 -> delta_open = 1/3
```

## Nature-Grade Boundary

This packet closes the dimensionless lane only if the reviewer accepts the
new physical law:

```text
primitive_based_operational_boundary_readout
```

It does not claim that the previous retained `Cl(3)/Z3` and APS packet alone
forced the law.  If the law is rejected, the existing no-go artifacts remain
active.

## Verification

Run:

```bash
python3 scripts/frontier_koide_primitive_based_readout_closure_theorem.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected theorem closeout:

```text
KOIDE_PRIMITIVE_BASED_READOUT_CLOSURE_THEOREM=TRUE
KOIDE_Q_CLOSED_UNDER_PRIMITIVE_BASED_READOUT=TRUE
KOIDE_DELTA_CLOSED_UNDER_PRIMITIVE_BASED_READOUT=TRUE
KOIDE_DIMENSIONLESS_LANE_CLOSED_UNDER_PRIMITIVE_BASED_READOUT=TRUE
NEW_PHYSICAL_LAW=primitive_based_operational_boundary_readout
PREVIOUS_RETAINED_PACKET_CLOSURE_WITHOUT_NEW_LAW=FALSE
FALSIFIERS=source_visible_quotient_labels_or_spectator_channel_or_unbased_endpoint
```
