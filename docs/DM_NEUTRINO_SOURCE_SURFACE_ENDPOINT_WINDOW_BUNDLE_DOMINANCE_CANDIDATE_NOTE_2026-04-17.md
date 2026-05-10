# DM Neutrino Source-Surface Endpoint Window Bundle-Dominance Candidate

**Date:** 2026-04-17  
**Status:** bounded - bounded or caveated result note
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_endpoint_window_bundle_dominance_candidate.py`

## Inputs

This note depends on:

- [DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)

These supply the carrier normal form, the broad exact shift-quotient bundle
on `(m, delta, r31)`, and the active half-plane reduction this endpoint
bundle-dominance candidate is phrased on.

## Question

On the compact branch, can the endpoint `m` window already be pushed toward a
meaningful local dominance statement without reviving the deleted rival-window
candidate forest?

## Bottom line

Yes, as a broad exact-bundle dominance candidate.

Using the explicit exact shift-quotient bundle over `(m, delta, r31)`, the
endpoint window

- `m in [-1.899713, -1.87]`

was searched on the compact core box

- `delta in [-2.5, 2.5]`
- `r31 in [0.5, 4.0]`

and then challenged on two tails:

- high-`r31` tail with `r31 in {4.5, 5, 6, 8, 10}`
- high-|`delta`| tail with `|delta| in [3, 8]`

The best repair found on the broad compact box is

- `3.027555919409`

from a global differential evolution refinement on that compact box, at a
boundary point near

- `(-1.87, 1.14568951, 0.5)`

and this still stays above the preferred recovered floor

- `Lambda_+(x_*) = 1.586874714730`

by

- `1.440681204679e+00`.

## Tail challenges

The tested tails are much higher:

- high-`r31` best repair: `6.827113095219`
- high-|`delta`| best repair: `4.453361971274`

So on the tested exact-bundle domain, the endpoint window does not show any
near-floor rival competitor.

## Why this matters

This is stronger than just saying “endpoint is still open.”

It says that on a broad exact bundle box that already contains the lowest
tested endpoint basin, the repair remains safely above the preferred recovered
winner, and the obvious tails are even less competitive.

That does not prove the local dominance theorem, but it does move the endpoint
window from “generic rival uncertainty” to “strongly dominated candidate on the
tested bundle domain.”

## Honest boundary

This is not a theorem of global bundle dominance, not exact carrier
completeness, and not flagship closure.

It is a strong local endpoint exact-bundle dominance candidate on a broad core
box with explicit tail challenges. The remaining theorem gap is still the
upgrade from tested bundle dominance to certified local rival-window dominance.
