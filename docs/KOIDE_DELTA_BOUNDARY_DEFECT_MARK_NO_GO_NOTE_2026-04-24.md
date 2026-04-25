# Koide delta boundary-defect mark no-go

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_delta_boundary_defect_mark_no_go.py`
**Status:** executable no-go; a boundary defect must be oriented to close delta

## Theorem Attempt

Derive the selected rank-one endpoint mark from a boundary defect/source
insertion.  If the defect selected the Brannen line, it would remove the
spectator channel.

## Result

Negative.

An invariant defect on the unmarked primitive block is scalar:

```text
D = lambda I.
```

It supports the whole primitive block, not a selected line.

A rank-one defect does select a line, but only after choosing an orientation

```text
P(alpha) = |cos(alpha), sin(alpha)><cos(alpha), sin(alpha)|.
```

The selected channel is

```text
selected_channel = cos(alpha)^2
spectator_channel = sin(alpha)^2.
```

Closure requires

```text
alpha = 0  (mod the unoriented line)
c = 0.
```

The defect orientation is therefore the missing selected endpoint mark.

## Residual

```text
RESIDUAL_MARK = retained_boundary_defect_orientation_selecting_Brannen_line
RESIDUAL_TRIVIALIZATION = selected_endpoint_basepoint_c_equals_zero
COUNTERSTATE = rank_one_defect_oriented_to_spectator_or_mixed_line
NEXT_ATTACK = derive_oriented_defect_from_source_asymmetry_or_accept_explicit_primitive
```

## Hostile Review

This route is conditionally useful but not retained closure.  A selected
oriented defect would close the channel part, but deriving that orientation is
the remaining theorem.

## Verification

```bash
python3 scripts/frontier_koide_delta_boundary_defect_mark_no_go.py
python3 -m py_compile scripts/frontier_koide_delta_boundary_defect_mark_no_go.py
```
