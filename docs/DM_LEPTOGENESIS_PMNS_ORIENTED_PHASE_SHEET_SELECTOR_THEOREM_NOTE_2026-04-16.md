# DM Leptogenesis PMNS Oriented-Phase Sheet-Selector Theorem

**Date:** 2026-04-16  
**Status:** exact selector-reduction theorem on the PMNS comparator gate  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_oriented_phase_sheet_selector_theorem.py`

## Question

After the projected-source selector has been reduced to `sign(A13)`, what is
the smallest upstream microscopic selector object on the active PMNS family?

## Bottom line

It is exactly the oriented phase bit

- `sign(sin(delta))`

on the fixed native `N_e` seed surface and its positive interior.

The constructive witness and its CP-flipped partner already agree on all
current exact even active data:

- `x`
- `y`
- `xi`
- `eta`
- `cos(delta)`
- `E1`
- `E2`
- flavored transport
- the current exact even selector objectives

What still differs is only the odd phase orientation:

- `sin(delta) > 0` on the constructive witness
- `sin(delta) < 0` on its CP-flipped partner

and on the positive seed surface that is exactly the projected-source bit:

- `A13 = 2 x1 y3 sin(delta)`
- `sign(A13) = sign(sin(delta))`

So the smallest upstream PMNS selector object is one-bit:

- `sign(sin(delta))`

## Why this is sharper

The minimal `A13` theorem already reduced the projected-source selector to one
odd slot on `dW_e^H`.

This theorem lifts that one-bit selector all the way upstream to the active
charged-sector data themselves.

So the remaining PMNS microscopic selector target is no longer a vague
“full-`D` sheet law.” It is:

- an oriented-phase law forcing `sin(delta) > 0`

on the positive seed surface.

## Exact consequence

Any theorem-grade microscopic selector upstream of `dW_e^H` must reduce to the
oriented phase choice

- `sin(delta) > 0`

equivalently

- `A13 > 0`

on the constructive sheet.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_oriented_phase_sheet_selector_theorem.py
```
