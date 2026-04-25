# Koide delta tautological pure-state support theorem

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_tautological_pure_state_support_theorem.py`  
**Status:** positive theorem under pure selected-line boundary semantics

## Theorem

On the actual selected-line `CP1` route, the physical boundary object is the
tautological pure state line

```text
chi(theta) = (1, exp(-2 i theta))/sqrt(2).
```

It has rank-one projector

```text
P_chi = |chi><chi|.
```

A normalized positive source supported on this one-dimensional line has the
form

```text
rho = lambda P_chi
Tr(rho)=1 => lambda=1.
```

Therefore

```text
selected_channel = Tr(rho P_chi) = 1
spectator_channel = 0.
```

## Delta Consequence

The real-section basepoint theorem gives

```text
c = 0.
```

The independent APS computation gives

```text
eta_APS = 2/9.
```

Thus

```text
delta_open = selected_channel * eta_APS + c = 2/9.
```

## Boundary And Falsifier

This theorem depends on retaining the actual selected-line boundary object as a
pure tautological state.  It is falsified if the physical boundary source is
instead allowed to be an arbitrary mixed density on the full rank-two primitive
block:

```text
rho = p P_chi + (1-p)(I-P_chi).
```

That mixed semantics is exactly the old selected-projector no-go class.  The
new theorem excludes it by object type: a mixed density on the full primitive
block is not a section/source supported on the tautological line.

## Verdict

```text
KOIDE_DELTA_TAUTOLOGICAL_PURE_STATE_SUPPORT_THEOREM=TRUE
DELTA_TAUTOLOGICAL_PURE_STATE_SUPPORT_CLOSES_MARK=TRUE
DELTA_TAUTOLOGICAL_PURE_STATE_SUPPORT_CLOSES_DELTA=TRUE
DELTA_PHYSICAL=ETA_APS=2/9
REQUIRED_SEMANTICS=physical_boundary_object_is_tautological_pure_selected_line
FALSIFIER=mixed_boundary_density_on_full_primitive_block_is_physical
```

## Verification

```bash
python3 scripts/frontier_koide_delta_tautological_pure_state_support_theorem.py
python3 -m py_compile scripts/frontier_koide_delta_tautological_pure_state_support_theorem.py
```
