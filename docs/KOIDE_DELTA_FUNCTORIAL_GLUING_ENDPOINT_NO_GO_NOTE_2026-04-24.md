# Koide delta functorial-gluing endpoint no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_functorial_gluing_endpoint_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Strengthen the Dai-Freed/determinant-line route with functorial gluing:

```text
closed APS phase + gluing functor
  -> selected open line carries the whole eta_APS
  -> delta_physical = 2/9.
```

## Executable theorem

Functorial gluing gives an additive law:

```text
eta_closed = phase_selected + phase_complement  (mod 1).
```

For the retained closed value:

```text
eta_closed = 2/9.
```

The runner verifies:

```text
phase_complement = 2/9 - phase_selected.
```

So gluing leaves one split parameter.

## Obstruction

Many selected endpoints obey the same gluing law:

```text
selected = 0,    complement = 2/9
selected = 1/18, complement = 1/6
selected = 1/9,  complement = 1/9
selected = 2/9,  complement = 0
selected = 1/3,  complement = -1/9.
```

The desired Brannen bridge is the special split:

```text
selected = eta_APS
complement = 0.
```

That is a boundary condition or endpoint-trivialization statement, not a
consequence of gluing alone.

## Endpoint sections

Endpoint sections can make the complement vanish:

```text
s1 = s0 - complement.
```

But functoriality checks additivity after endpoint sections are chosen; it does
not derive those sections.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_SPLIT = closed_APS_gluing_does_not_select_open_segment
```

## Why this is not closure

The gluing theorem is necessary for any future positive Berry/APS bridge, but
it does not choose which open segment carries the closed APS phase.  A
Nature-grade proof still needs a physical boundary condition assigning the full
closed eta to the selected Brannen line.

## Falsifiers

- A retained gluing theorem whose complement segment is canonically zero.
- A selected-line boundary condition fixed before using `2/9`.
- A proof that the selected Brannen path is the entire closed APS loop.

## Boundaries

- Covers additive determinant-line/Dai-Freed gluing of one closed phase into a
  selected open segment plus complement.
- Does not refute a stronger physical boundary-condition theorem.

## Hostile reviewer objections answered

- **"Gluing is functorial."**  Yes; functoriality leaves a split parameter.
- **"Set the complement to zero."**  That is the missing endpoint boundary
  condition.
- **"The selected line is physically preferred."**  Preference of the line does
  not assign it the whole closed APS phase.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_functorial_gluing_endpoint_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_FUNCTORIAL_GLUING_ENDPOINT_NO_GO=TRUE
DELTA_FUNCTORIAL_GLUING_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_SPLIT=closed_APS_gluing_does_not_select_open_segment
```
