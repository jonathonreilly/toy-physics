# Koide delta selected-line local boundary-source theorem

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_delta_selected_line_local_boundary_source_theorem.py`
**Status:** positive delta endpoint theorem under selected-line local boundary-source locality

## Theorem

On the retained actual selected-line `CP1` carrier, the endpoint source that is
local to a boundary point is a source on the pulled-back tautological fibre:

```text
End(L_chi)
```

not an arbitrary density on the ambient rank-two primitive block:

```text
End(V).
```

For the selected-line ray

```text
chi(theta) = (1, exp(-2 i theta)) / sqrt(2),
P_chi = |chi><chi|,
```

the embedded local source algebra is one-dimensional:

```text
End(L_chi) = C P_chi.
```

A normalized positive local source is therefore uniquely

```text
rho_boundary = P_chi.
```

This derives the selected endpoint mark:

```text
selected_channel = Tr(P_chi P_chi) = 1
spectator_channel = Tr(P_chi (I - P_chi)) = 0.
```

## Based Endpoint

The retained real selected-line section has a unique unphased boundary point:

```text
theta0 = 2 pi / 3.
```

For an affine endpoint coordinate

```text
endpoint(theta) = theta - theta0 + c,
```

the based real boundary section imposes

```text
endpoint(theta0) = 0 -> c = 0.
```

So the endpoint-exact torsor shift is removed by the based selected-line
section, not by choosing the value needed for `2/9`.

## Delta Consequence

The retained APS/ABSS computation gives:

```text
eta_APS = 2/9.
```

With selected-line local source support and the based endpoint:

```text
delta_physical = selected_channel eta_APS + c
               = 1 * eta_APS + 0
               = 2/9.
```

The theorem is symbolic in the closed value: it transfers arbitrary `eta` to
the open endpoint once `selected_channel=1` and `c=0` are derived.

## Why This Is Not Target Import

- `selected_channel=1` follows from the one-dimensional source algebra
  `End(L_chi)`.
- `c=0` follows from the based real section at the unphased endpoint.
- `2/9` enters only afterward as the independent APS value.
- Mixed selected/spectator counterstates are recovered exactly if the source
  domain is enlarged from `End(L_chi)` to ambient `End(V)`.

## Falsifier

The theorem is falsified if the physical Brannen endpoint source is an ambient
rank-two density:

```text
rho = p P_chi + (1-p)(I-P_chi),
```

rather than a selected-line local source.  Then:

```text
delta = p eta_APS,
```

and `p` remains free.

## Boundary

This theorem closes the oriented selected endpoint mark plus based endpoint
trivialization for the delta lane.  It does not address the separate Q/source
status or the overall lepton scale `v0`.

## Verification

```bash
python3 scripts/frontier_koide_delta_selected_line_local_boundary_source_theorem.py
python3 -m py_compile scripts/frontier_koide_delta_selected_line_local_boundary_source_theorem.py
```

Expected closeout:

```text
KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_THEOREM=TRUE
DELTA_ORIENTED_SELECTED_ENDPOINT_MARK_DERIVED=TRUE
DELTA_BASED_ENDPOINT_TRIVIALIZATION_DERIVED=TRUE
DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_CLOSES_DELTA=TRUE
DELTA_PHYSICAL=ETA_APS=2/9
NO_TARGET_IMPORT=TRUE
FALSIFIER=physical_endpoint_source_is_ambient_EndV_density_not_selected_line_local_source
BOUNDARY=Q_source_status_and_v0_not_addressed_by_this_delta_theorem
```
