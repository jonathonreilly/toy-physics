# Koide delta Dai-Freed open-trivialization no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_dai_freed_open_trivialization_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use the Dai-Freed determinant-line picture to turn closed APS eta into the open
selected-line Berry endpoint:

```text
Dai-Freed trivialization + eta_APS -> theta_end - theta0 = 2/9.
```

## Executable theorem

The retained closed support value remains exact:

```text
eta_APS = 2/9.
```

An open determinant-line phase decomposes as:

```text
open_phase = path_holonomy + endpoint_section_end - endpoint_section_start.
```

The runner verifies that the endpoint section can fit `eta_APS` for any path
holonomy:

```text
s1 = s0 - h + 2/9.
```

Likewise the path holonomy can fit `eta_APS` for any endpoint sections:

```text
h = s0 - s1 + 2/9.
```

## Obstruction

Dai-Freed theory needs a specified boundary Dirac family, filling, and endpoint
boundary data.  The current retained Koide packet supplies the closed fixed
point eta value; it does not supply endpoint sections for the selected line.

Writing a section difference as:

```text
(eta_end - eta_start)/2
```

the condition that it equals `2/9` requires:

```text
eta_end - eta_start = 4/9.
```

That is new boundary endpoint data, not a consequence of the closed eta number.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION = endpoint_boundary_data_for_selected_line_not_retained
```

## Why this is not closure

Dai-Freed is the right mathematical language for a future bridge, but it does
not remove the need for a physical selected-line endpoint trivialization.  The
closed APS value remains support until that boundary data is derived.

## Falsifiers

- A retained boundary Dirac family on the selected line with canonical endpoint
  sections whose difference is fixed before using `eta_APS` as a target.
- A Dai-Freed functor from the retained `Z_3` fixed-point eta calculation to
  the selected open Berry path.
- A proof that all admissible endpoint trivializations collapse to the one
  giving `theta_end-theta0=2/9`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_dai_freed_open_trivialization_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_DAI_FREED_OPEN_TRIVIALIZATION_NO_GO=TRUE
DELTA_DAI_FREED_OPEN_TRIVIALIZATION_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION=endpoint_boundary_data_for_selected_line_not_retained
```
