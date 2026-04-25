# Koide Q/delta residual cohomology obstruction no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py`  
**Status:** no-go; retained exactness names the kernels but does not choose the
zero section/basepoint

## Theorem Attempt

Try to derive the primitive-based readout/basepoint law from retained
exact-sequence or cohomological structure.  If the residual source label,
spectator channel, and endpoint-exact phase were coboundaries with canonical
zero representatives, the lane would close without adding a new physical law.

## Q Exact Sequence

Use reduced source coordinates:

```text
(t, z)
```

where `t` is the retained total and `z = <Z>` is the central label coordinate.
The retained projection is:

```text
pi_Q(t,z) = t.
```

The runner verifies:

```text
ker(pi_Q) = span{(0,1)} = span{Z}.
```

Kernel translations preserve the retained total:

```text
(t,z) -> (t,z+a).
```

The closing representative is the zero label:

```text
z = 0 -> w_plus = 1/2 -> K_TL = 0 -> Q = 2/3.
```

But a nonzero representative preserves the total and does not close:

```text
z = -1/3 -> w_plus = 1/3 -> K_TL = 3/8 -> Q = 1.
```

## Delta Exact Sequence

Use boundary coordinates:

```text
(selected, spectator, c)
```

with retained closed-total projection:

```text
pi_delta(selected,spectator,c) = selected + spectator.
```

The runner verifies:

```text
ker(pi_delta) =
  span{(-1,1,0), (0,0,1)}.
```

These are exactly:

```text
selected/spectator split
endpoint-exact shift.
```

After total normalization:

```text
delta_open / eta_APS - 1 = -spectator + c / eta_APS.
```

At `eta_APS = 2/9`:

```text
delta_open / eta_APS - 1 = -spectator + (9/2)c.
```

The zero representative closes:

```text
spectator = 0
c = 0.
```

Nonzero kernel representatives preserve the retained closed total but move the
open endpoint:

```text
spectator=1,   c=0   -> delta_open=0
spectator=1/2, c=0   -> delta_open=1/9
spectator=0,   c=1/9 -> delta_open=1/3.
```

## Section Obstruction

Exactness gives fibres, not canonical splittings.  The runner exhibits section
families:

```text
Q:     s_a(t) = (t, a t)
delta: s_(b1,b2)(1) = (1-b1, b1, b2).
```

The closing section is the special case:

```text
a = 0
b1 = 0
b2 = 0.
```

That choice is exactly the missing primitive-based readout/basepoint law, or an
equivalent retained canonical-section theorem.

## Residual

```text
RESIDUAL_SCALAR =
  canonical_zero_section_for_source_label_spectator_and_endpoint_kernel
RESIDUAL_Q =
  nontrivial_trace_kernel_span_Z
RESIDUAL_DELTA =
  nontrivial_closed_boundary_kernel_span_spectator_and_endpoint_exact
NEXT_THEOREM =
  retained_canonical_section_or_new_primitive_based_readout_law
```

## Falsifiers

- A retained exactness theorem whose kernel is trivial, not `span{Z}` on Q and
  not two-dimensional on delta.
- A retained naturality theorem proving the zero section is canonical before
  using the target endpoint.
- A retained boundary condition that kills both the spectator channel and
  endpoint-exact kernel as gauge.

## Hostile Review

- **Target import:** none.  The target values appear only as consequences of
  zero-kernel representatives or as countermodel comparisons.
- **Numerical tuning:** none; the obstruction is rank/nullity of exact symbolic
  maps.
- **Closure claim:** rejected.  This note proves why exactness alone cannot
  promote the new-law packet to retained-only closure.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_Q_DELTA_RESIDUAL_COHOMOLOGY_OBSTRUCTION_NO_GO=TRUE
Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_Q=FALSE
Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_DELTA=FALSE
Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_FULL_LANE=FALSE
RESIDUAL_SCALAR=canonical_zero_section_for_source_label_spectator_and_endpoint_kernel
RESIDUAL_Q=nontrivial_trace_kernel_span_Z
RESIDUAL_DELTA=nontrivial_closed_boundary_kernel_span_spectator_and_endpoint_exact
```
