# Koide Q cobordism / invertible-phase source no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_cobordism_invertible_phase_source_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use a broad topological classification to force the remaining Q source:

```text
cobordism / invertible phase class
  -> equal C3 center source
  -> K_TL = 0.
```

## Executable theorem

The Q residual is a continuous source state:

```text
u = p(P_plus)
p(P_perp) = 1-u
0 < u < 1.
```

Retained invertible phase classes are discrete or locally constant topological
sectors.  The runner verifies that a finite class:

```text
k mod n
```

has no dependence on `u`.

## Obstruction

A continuous map from the connected source interval to a discrete topological
sector is constant.  A fixed invertible phase class permits both closing and
non-closing source states:

```text
u = 1/3 -> Q = 1,   K_TL = 3/8
u = 1/2 -> Q = 2/3, K_TL = 0
u = 2/3 -> Q = 1/2, K_TL = -3/8.
```

Thus cobordism data can constrain anomaly sectors, but not the real
center-source scalar.

## Source-functor escape hatch

A map from a topological class to the source state:

```text
u = a * class + b
```

requires:

```text
b = 1/2
```

on the trivial class.  That offset is the missing source primitive unless a
retained boundary/source functor derives it.

Allowing a continuous theta angle also does not close Q: the theta angle then
is the new real source parameter.

## Residual

```text
RESIDUAL_SCALAR = center_label_source_u_minus_one_half_equiv_K_TL
RESIDUAL_FUNCTOR = topological_phase_to_C3_center_source_not_retained
```

## Why this is not closure

The route strengthens the anomaly/topology audit.  It shows why topological
classification alone cannot select a continuous normalized source state.  A
positive result would need a new boundary/source functor that couples the
topological sector to the C3 center labels.

## Falsifiers

- A retained cobordism invariant whose boundary value is a real source state,
  not merely a discrete phase class.
- A theorem deriving the source offset `b=1/2` from a physical boundary functor.
- A mixed topological/source response whose vanishing is equivalent to
  `u=1/2`.

## Boundaries

- Covers discrete or locally constant invertible phase classifications and
  continuous theta-angle escape hatches.
- Does not refute a future retained source functor from topology to the C3
  center state.

## Hostile reviewer objections answered

- **"Cobordism is more general than anomalies."**  Yes; the generality still
  gives topological sectors, not the continuous source value.
- **"Use a theta response."**  That adds a continuous parameter and moves the
  residual to theta.
- **"Use the trivial phase."**  The trivial phase supports both rank and
  equal-label center states.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_cobordism_invertible_phase_source_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_COBORDISM_INVERTIBLE_PHASE_SOURCE_NO_GO=TRUE
Q_COBORDISM_INVERTIBLE_PHASE_SOURCE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL
RESIDUAL_FUNCTOR=topological_phase_to_C3_center_source_not_retained
```
