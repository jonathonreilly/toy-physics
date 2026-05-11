# Mirror Gravity Probe Note

**Date:** 2026-04-03  
**Status:** bounded - bounded or caveated result note
**Claim type:** bounded_theorem

**Audit-conditional perimeter (2026-05-01):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = medium`, `chain_closes = false`, and `claim_type
= bounded_theorem`. The audit chain-closure explanation is exact:
"The fixed-anchor runner reproduces the mass-window fits, and the
current distance sweep supports the peak/plateau interpretation, but
the note's N=60 tail-fit claim depends on a missing tail log or
unregistered runner parameters. The comparison to other hard-geometry
lanes is also not registered as a one-hop authority here." This
rigorization edit only sharpens the boundary of the conditional
perimeter; nothing here promotes audit status. The supported
content of this note is the fixed-anchor mass-window fits at N=25,
40, 60 (registered against
[`scripts/mirror_gravity_fixed_anchor.py`](../scripts/mirror_gravity_fixed_anchor.py))
and the peak/plateau distance interpretation at N=25, 40, 60
(registered against
[`scripts/mirror_gravity_distance_sweep.py`](../scripts/mirror_gravity_distance_sweep.py)).
The N=60 tail-fit (`delta ~ C * b^0.000`) cited under §"Fixed-Mass
Distance Sweep / N=60" is governed by the additional tail log
[`logs/2026-04-03-mirror-gravity-distance-sweep-tail.txt`](../logs/2026-04-03-mirror-gravity-distance-sweep-tail.txt)
which is not in the audit packet's load-bearing one-hop set. The
§"Retained Conclusion" comparison to "other hard-geometry lanes" is
bounded interpretation that depends on cross-lane comparisons not
registered in this note's one-hop authority chain. The supported
perimeter is just the fixed-anchor mass-window fits and the peak/
plateau qualitative read; the N=60 tail-fit and cross-lane comparison
are out-of-perimeter bounded narration.

This note freezes the narrow mirror-only gravity probe requested after the
retained mirror chokepoint pocket was established.

The probe was intentionally limited to the retained strict mirror pocket:

- strict chokepoint mirror DAGs only
- `NPL_HALF = 50` (`100` total nodes per layer)
- `layer2_prob = 0.0`
- fixed-anchor mass window, then a fixed-mass distance sweep
- no edits to the core mirror scripts

Scripts:

- [`scripts/mirror_gravity_fixed_anchor.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_gravity_fixed_anchor.py)
- [`scripts/mirror_gravity_distance_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_gravity_distance_sweep.py)

Logs:

- [`logs/2026-04-03-mirror-gravity-fixed-anchor.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-gravity-fixed-anchor.txt)
- [`logs/2026-04-03-mirror-gravity-distance-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-gravity-distance-sweep.txt)
- [`logs/2026-04-03-mirror-gravity-distance-sweep-tail.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-gravity-distance-sweep-tail.txt)

## 1. Fixed-Anchor Mass Window

The fixed-anchor mass window on the retained mirror pocket is **positive but
weakly structured**.

### `N = 25`

- `M = 1, 2, 3, 5, 8, 12, 16`
- fit window: `M in {2,3,5,8}`
- fit:
  - `delta ~= 0.9496 * M^0.109`
  - `R^2 = 0.420`

### `N = 40`

- fit:
  - `delta ~= 0.8617 * M^0.089`
  - `R^2 = 0.050`

### `N = 60`

- fit:
  - `delta ~= 0.9869 * M^0.130`
  - `R^2 = 0.116`

### Narrow read

- the mirror pocket does show positive gravity response across the fixed-anchor
  sweep
- the response is **sublinear** and the fit quality is poor to modest
- compared with the other hard-geometry lanes, this is **not** a cleaner mass
  law

## 2. Fixed-Mass Distance Sweep

The fixed-mass distance sweep is the more informative mirror gravity check.

### `N = 25`

- fixed `mass_count = 4`
- the mean response peaks near `b = 8`
- the sweep does **not** produce enough tail points for a review-safe fit

### `N = 40`

- fixed `mass_count = 4`
- the mean response peaks near `b = 8`
- the tail beyond the peak is too flat to support a meaningful power law

### `N = 60`

- fixed `mass_count = 4`
- the mean response peaks near `b = 10`
- tail fit on the strict mirror geometry:
  - `delta ~= C * b^0.000`

### Narrow read

- the mirror pocket has a real positive gravity response
- but the distance curve is **peak + plateau**, not a clean falling tail
- that is weaker than the review-safe fixed-geometry gravity tail on the other
  lanes

## Retained Conclusion

The strict mirror pocket is still real as a bounded coexistence pocket:

- Born-clean on the retained rows
- gravity-positive
- decohering

But on the gravity side, the new mirror-only probe does **not** show a cleaner
mass window or a cleaner distance law than the other hard-geometry lanes.

So the current safe statement is:

- **mirror = retained bounded coexistence pocket**
- **mirror = not yet the best gravity-side lane**

The strongest gravity-side lane remains generated asymmetry-persistence + layer
norm, while the strongest joint coexistence lane remains dense central-band +
layer norm.
