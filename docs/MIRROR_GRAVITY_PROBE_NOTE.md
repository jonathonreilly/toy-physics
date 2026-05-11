# Mirror Gravity Probe Note

**Date:** 2026-04-03 (load-bearing scope narrowed to the registered
fixed-anchor mass-window runner cache 2026-05-10)
**Status:** bounded null-result note — on the registered mirror-gravity
fixed-anchor mass-window cache (`logs/runner-cache/mirror_gravity_fixed_anchor.txt`),
the strict mirror chokepoint pocket shows positive but weakly fit
mass-window response (`R^2 <= 0.420`), so no clean mirror mass law is
supported on the searched fixed-anchor windows. The fixed-mass
distance-tail sweep and cross-lane comparison are historical context
pending a registered tail-sweep runner cache and registered cross-lane
dependency citations.
**Claim type:** bounded_theorem
**Primary runner (load-bearing):** [`scripts/mirror_gravity_fixed_anchor.py`](../scripts/mirror_gravity_fixed_anchor.py)
**Primary runner registered cache (load-bearing):** [`logs/runner-cache/mirror_gravity_fixed_anchor.txt`](../logs/runner-cache/mirror_gravity_fixed_anchor.txt)

**Review repair perimeter (2026-05-01 generated-audit context):**
Generated-audit context before this narrowing identified this chain-closure
blocker:
"The fixed-anchor runner reproduces the mass-window fits, and the
current distance sweep supports the peak/plateau interpretation, but
the note's N=60 tail-fit claim depends on a missing tail log or
unregistered runner parameters. The comparison to other hard-geometry
lanes is also not registered as a one-hop authority here." This
rigorization edit narrows the load-bearing boundary to the registered
fixed-anchor mass-window cache; nothing here promotes audit status.
The supported content of this note is the fixed-anchor mass-window
fits at N=25, 40, 60. The N=60 tail-fit (`delta ~ C * b^0.000`) cited
under §"Fixed-Mass Distance Sweep / N=60" is governed by the additional tail log
[`logs/2026-04-03-mirror-gravity-distance-sweep-tail.txt`](../logs/2026-04-03-mirror-gravity-distance-sweep-tail.txt)
which is not in the audit packet's load-bearing one-hop set. The
§"Retained Conclusion" comparison to "other hard-geometry lanes" is
bounded interpretation that depends on cross-lane comparisons not
registered in this note's one-hop authority chain. The supported
perimeter is just the fixed-anchor mass-window fits; the distance-tail
fit and cross-lane comparison are out-of-perimeter bounded narration.

This note freezes the narrow mirror-only gravity probe requested after the
retained mirror chokepoint pocket was established. The 2026-05-10 narrowing
restricts the load-bearing scope to the registered fixed-anchor mass-window
runner-cache; the fixed-mass distance-tail material below is recorded as
historical context only and is not load-bearing for the bounded null
result.

The probe was intentionally limited to the retained strict mirror pocket:

- strict chokepoint mirror DAGs only
- `NPL_HALF = 50` (`100` total nodes per layer)
- `layer2_prob = 0.0`
- fixed-anchor mass window only on the load-bearing scope; the fixed-mass
  distance sweep is recorded as historical context, not load-bearing
- no edits to the core mirror scripts

Load-bearing script and registered cache:

- [`scripts/mirror_gravity_fixed_anchor.py`](../scripts/mirror_gravity_fixed_anchor.py)
- [`logs/runner-cache/mirror_gravity_fixed_anchor.txt`](../logs/runner-cache/mirror_gravity_fixed_anchor.txt)

Historical context (not load-bearing):

- [`scripts/mirror_gravity_distance_sweep.py`](../scripts/mirror_gravity_distance_sweep.py) — distance-sweep runner; no registered runner-cache artifact in `logs/runner-cache/` for the tail-fit row, so the `N=60` distance-tail fit is recorded here as historical readout only.
- [`logs/2026-04-03-mirror-gravity-fixed-anchor.txt`](../logs/2026-04-03-mirror-gravity-fixed-anchor.txt) (original completed log; the registered cache above is load-bearing)
- [`logs/2026-04-03-mirror-gravity-distance-sweep.txt`](../logs/2026-04-03-mirror-gravity-distance-sweep.txt) (historical context only)
- [`logs/2026-04-03-mirror-gravity-distance-sweep-tail.txt`](../logs/2026-04-03-mirror-gravity-distance-sweep-tail.txt) (historical context only)

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

## 2. Fixed-Mass Distance Sweep (historical context, not load-bearing)

The fixed-mass distance sweep below is retained for audit-trail context
only. It is **not** load-bearing for any claim in this note: no registered
`logs/runner-cache/` artifact backs the `N=60` distance-tail fit, and the
historical distance-sweep log is not registered as a one-hop dependency.
A future repair could either register a tail-sweep runner-cache or remove
this section.

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

## Bounded Conclusion (load-bearing scope)

The load-bearing claim, restricted to the registered fixed-anchor mass-
window cache, is a bounded null result on mass-window fit quality:

- positive but weakly structured mass-window response on the strict mirror
  pocket at `N ∈ {25, 40, 60}`
- fit qualities `R^2 = 0.420 / 0.050 / 0.116` are all well below any
  promotable bar (e.g. `R^2 ≥ 0.95`), so no clean mirror mass law is
  supported on the searched fixed-anchor windows
- the strict mirror chokepoint pocket itself remains a separate bounded
  coexistence pocket; that status is owned by
  [`docs/MIRROR_CHOKEPOINT_NOTE.md`](MIRROR_CHOKEPOINT_NOTE.md) and its
  registered certificate runner, not this probe

## Out-of-load-bearing scope

The following are preserved here as audit-trail context only and are not
load-bearing for any claim in this note:

- the fixed-mass distance-sweep tail fit at `N=60` (no registered runner-
  cache artifact)
- any cross-lane "best gravity-side lane" ranking (no registered one-hop
  dependency on the comparator hard-geometry-lane artifacts)

## Audit boundary (2026-05-10)

This revision addresses the generated-audit repair target:

> other: restore/register the tail sweep artifact or runner arguments and
> cite the comparator hard-geometry lane results used for the ranking.

This revision narrows the load-bearing scope to the registered fixed-
anchor mass-window cache. The distance-tail material is demoted to
historical context, and the cross-lane comparator ranking is removed from
the load-bearing read. A future repair could re-register a tail-sweep
runner-cache and add explicit one-hop dependencies on the comparator
notes if the cross-lane ranking is to be reinstated as load-bearing.
