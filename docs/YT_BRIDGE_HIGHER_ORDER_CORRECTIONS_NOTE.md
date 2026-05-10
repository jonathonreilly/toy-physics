# `y_t` Bridge Higher-Order Corrections Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_bridge_higher_order_corrections.py`

## Role

This note pushes one layer beyond the local-Hessian selector.

The previous branch result identified the leading selector on the forced
UV-localized bridge window as a positive local quadratic term. The natural next
question is whether the next corrections in that same local expansion stay
parametrically small.

This runner treats the current constructive UV-localized bridge as the leading
quadratic piece and probes one-parameter amplitude deformations around it.

## What was checked

The runner:

- reconstructs the current best constructive UV-localized bridge
- scales its bridge surplus by a local amplitude parameter `a`
- fits the accepted low-energy endpoint `y_t(v)` as a polynomial in
  `delta = a - 1`
- compares the cubic and quartic contributions to the quadratic leading term
  on a small neighborhood around the selector

This is a direct hierarchy test on the current viable family, not a new search
for a better bridge shape.

## Result

The best constructive bridge remains the same narrow UV-localized profile:

- shape: `logistic`
- center fraction: `0.975`
- width fraction: `0.020`
- endpoint: `y_t(v) = 0.917605`
- deviation from accepted target: `+0.0005%`

The local amplitude expansion around the selector point is:

`y_t(a) = c0 + c1*δ + c2*δ^2 + c3*δ^3 + c4*δ^4`

with:

- `c0 = 0.91760483`
- `c1 = 0.02750406`
- `c2 = 0.00497496`
- `c3 = -0.00034980`
- `c4 = -0.00004606`

On the probe tube `|δ| <= 0.10`:

- quadratic magnitude: `4.974959e-05`
- cubic magnitude: `3.498024e-07`
- quartic magnitude: `4.605867e-09`
- `|cubic + quartic| / quadratic = 7.123842e-03`

Fit quality for the fourth-order amplitude model:

- `RMSE = 6.360240e-13`
- `RMSE / span = 1.156384e-10`

## Checks

All explicit checks passed:

- best constructive bridge stays within `0.1%` of the accepted endpoint
- cubic plus quartic corrections stay below `1%` of the quadratic term on the
  `10%` amplitude tube
- the cubic term itself stays below `1%` of the quadratic term on that tube
- the quartic term is negligible at that scale
- the fourth-order fit reconstructs the amplitude scan essentially exactly

## Meaning

The leading local-Hessian selector remains the right description on the viable
UV-localized bridge family.

The higher-order local corrections are present, but they are parametrically
subleading on the probe window:

> quadratic leading piece dominates, cubic is small, quartic is smaller still.

So this branch does **not** lose control when the selector is expanded one order
higher. It stays in the perturbative hierarchy we wanted.

## Honest boundary

This is still a bounded-support result.

It quantifies the higher-order corrections above the current selector, but it
does **not** prove the exact microscopic origin of that selector and it does
**not** remove the residual `y_t` bound.

The remaining open question is the microscopic mechanism that enforces the
positive local quadratic selector in the first place.

## Honest auditor read

The 2026-05-04 audit recorded this row as `audited_conditional` with the
substantive observation that the load-bearing hierarchy is conditional
on a chosen constructive bridge family and on embedded calibrated inputs
(including the imported physical endpoint used to select the best
bridge). The hierarchy ratio `|cubic + quartic|/quadratic = 7.124e-3`
is therefore an amplitude-tube hierarchy on the existing viable family,
not a first-principles bound on the exact microscopic bridge.

This addendum is graph-bookkeeping only. It does not change the
conditional status, does not promote the row, and does not modify the
amplitude-scan numerics or their bounded scope.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream
authorities the amplitude hierarchy result reuses. It does not promote
this note or change the audited claim scope.

- [YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
  for the constructive UV-localized family the amplitude scan deforms.
- [YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md](YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md)
  for the leading positive local quadratic selector this note expands
  one order higher.
- [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md)
  for the forced UV-localized class on which the amplitude tube is
  defined.
