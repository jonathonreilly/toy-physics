# Koide delta unmarked-primitive naturality no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_unmarked_primitive_naturality_no_go.py`  
**Status:** executable no-go; unmarked primitive naturality does not select the Brannen line

## Theorem Attempt

Derive the selected endpoint support law from the unmarked real primitive
boundary object.  If naturality selected the charged Brannen rank-one line,
then

```text
selected_channel = 1
spectator_channel = 0
```

and the delta bridge would reduce to the endpoint basepoint law.

## Result

Negative.  The automorphism group of the unmarked rank-two primitive acts
transitively on rank-one lines.  No rank-one projector is invariant under this
group.

For a positive readout density

```text
rho = [[a,b],[b,d]]
```

`O(2)` naturality plus normalization gives

```text
rho = I/2.
```

Therefore every rank-one line has weight

```text
selected_channel = 1/2
spectator_channel = 1/2.
```

With `eta_APS=2/9`, even a based endpoint gives

```text
delta_open = 1/9,
```

not `2/9`.

## Conditional Boundary

If a selected rank-one mark is retained, then the channel obstruction is gone:

```text
rho = P_selected
selected_channel = 1
spectator_channel = 0.
```

But that mark is exactly the missing physical endpoint support law.  It is not
created by naturality of the unmarked primitive.

## Residual

```text
RESIDUAL_MARK = retained_selected_rank_one_endpoint_mark
RESIDUAL_CHANNEL = selected_channel_one_not_unmarked_natural
COUNTERSTATE = unmarked_natural_readout_selected_equals_one_half_delta_one_ninth
NEXT_ATTACK = derive_selected_rank_one_mark_from_boundary_source_or_defect
```

## Hostile Review

This is a structural no-go, not a value fit.  The APS value is introduced only
after the channel weights have been derived.  The obstruction is the absence of
a retained physical mark selecting one rank-one endpoint line inside the
unmarked primitive block.

## Verification

```bash
python3 scripts/frontier_koide_delta_unmarked_primitive_naturality_no_go.py
python3 -m py_compile scripts/frontier_koide_delta_unmarked_primitive_naturality_no_go.py
```
