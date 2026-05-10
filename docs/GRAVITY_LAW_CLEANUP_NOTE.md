# Gravity Law Cleanup Note

**Date:** 2026-04-02 (claim narrowed 2026-05-09 to primary-runner-backed evidence per audit `runner_artifact_issue` repair target).
**Status:** bounded null-result note — the registered primary runner shows a peaked positive distance response on its searched window, but does not support a clean promoted distance or mass force-law on currently-cached evidence.
**Primary runner:** [`scripts/gravity_distance_fixed_geometry.py`](../scripts/gravity_distance_fixed_geometry.py) (fixed-geometry generated-DAG distance sweep; load-bearing).
**Primary runner cached log:** [`logs/runner-cache/gravity_distance_fixed_geometry.txt`](../logs/runner-cache/gravity_distance_fixed_geometry.txt) — SHA-pinned cache that backs every load-bearing row in the "Runner-backed result (primary runner)" section below.
**Companion follow-up scripts (diagnostic-only, not load-bearing, no registered primary-runner cache):**

- [`scripts/gravity_mass_scaling_fixed_anchor.py`](../scripts/gravity_mass_scaling_fixed_anchor.py) — fixed-anchor mass scaling on generated DAGs.
- [`scripts/gravity_distance_channel_observables.py`](../scripts/gravity_distance_channel_observables.py) — channel-observable readout on the same fixed-geometry distance sweep.

These two scripts exist as exploratory follow-ups but neither is registered in the runner classification ledger and neither has a current SHA-pinned runner cache. They are **not load-bearing** for the bounded null-result claim below.

## Why these reruns were needed

Two older scripts were useful as exploratory scans but not clean enough for
strong claims:

- `scripts/gravity_distance_v2.py`
  - changed `y_range` with impact parameter `b`
  - so geometry and beam/support width changed at the same time as `b`
- `scripts/gravity_mass_scaling.py`
  - varied mass count by taking prefixes of a drifting candidate set
  - so count and source geometry moved together

The replacement runner below removes those confounds.

## Runner-backed result (primary runner, load-bearing)

The registered primary runner is `scripts/gravity_distance_fixed_geometry.py`.
Its cached output records a fixed-geometry distance sweep with one fixed graph
per seed; only the mass-anchor position moves with `b`.

From [`logs/runner-cache/gravity_distance_fixed_geometry.txt`](../logs/runner-cache/gravity_distance_fixed_geometry.txt):

- parameters used: `N=30`, `nodes_per_layer=60`, `y_range=18.0`,
  `connect_radius=3.5`, `mass_count=4`, `seeds=24`,
  `b ∈ {2.0, 4.0, 6.0, 8.0, 10.0, 12.0}`
- raw distance response on the cached sweep:
  - `b= 2.0`: `delta = -0.0914 ± 0.4295`  (`t = -0.21`)
  - `b= 4.0`: `delta = +0.0733 ± 0.4450`  (`t = +0.16`)
  - `b= 6.0`: `delta = -0.0048 ± 0.3427`  (`t = -0.01`)
  - `b= 8.0`: `delta = +0.3077 ± 0.4454`  (`t = +0.69`)
  - `b=10.0`: `delta = +0.8103 ± 0.3990`  (`t = +2.03`)
  - `b=12.0`: `delta = +1.0209 ± 0.4173`  (`t = +2.45`)
- peak mean deflection at `b = 12.0`
- the runner explicitly reports: "Not enough falling-tail points for a
  review-safe power-law fit."

These primary-runner rows are themselves the load-bearing evidence:

- a positive, statistically significant deflection signal exists at the peak
  (`b ∈ {10.0, 12.0}`)
- the cached sweep does not extend far enough past the peak to support a
  review-safe falling-tail power-law fit, so no clean `1/b^α` law can be
  promoted from the registered runner

## Out-of-scope diagnostic context (not load-bearing)

The two scripts below were drafted as follow-ups but neither has a registered
primary-runner classification or a current SHA-pinned cache. Any numerical
rows that previous revisions of this note quoted from these scripts (mass
exponents, channel-observable correlations, distance tail fits on a wider
`b` window) are **out-of-scope** for the bounded null-result claim and are
not reproduced here as load-bearing evidence.

### Fixed-anchor mass scaling (future work)

- diagnostic path: `scripts/gravity_mass_scaling_fixed_anchor.py`
- protocol: one fixed graph per seed, one fixed anchor `y = center + b_anchor`,
  `M` taken as prefixes of a frozen distance-ranked ordering of gravity-layer
  candidates
- registration status: not registered as a primary runner; no SHA-pinned
  runner cache
- promotion bar: a registered primary-runner mass-window fit on this script
  would have to clear a hard `R^2 >= 0.95` threshold on at least three `M`
  values, with a first-principles argument that the fitted exponent is the
  mass-coupling exponent

### Channel-observable readout (future work)

- diagnostic path: `scripts/gravity_distance_channel_observables.py`
- protocol: same fixed-geometry distance sweep as the primary runner, with
  bundle/channel observables (centroid, bundle bias, cancellation, effective
  channel count)
- registration status: not registered as a primary runner; no SHA-pinned
  runner cache
- promotion bar: a registered primary-runner channel-observable fit would
  have to demonstrate a cleaner law-like trend than the centroid-only
  primary runner above

These two follow-up lanes remain available as future-work options, but the
bounded null-result claim closes from the primary-runner cache alone and
does not depend on either of them.

## Current gravity-law status (primary-runner-backed)

What is supported by the registered primary runner:

- a statistically real positive deflection signal at the searched `b` peak
- a peaked distance response on the cached `b ∈ {2, 4, 6, 8, 10, 12}` sweep,
  with peak at `b = 12.0`

What is not supported by the registered primary runner:

- exact `1/b^2` as a locked distance law (no falling tail in the cached
  sweep, no review-safe power-law fit)
- exact `F ∝ M` as a locked mass law (no registered primary-runner cache for
  the mass-scaling follow-up)

Current safe wording (primary-runner-backed):

- **gravity signal is real on the registered primary-runner sweep**
- **exact force-law scaling is unresolved on currently-cached evidence**

## What this note does NOT claim

- A promoted `1/b^α` distance law on the generated-DAG gravity lane.
- A promoted `F ∝ M^α` mass law on the generated-DAG gravity lane.
- Any load-bearing conclusion drawn from the unregistered, uncached
  follow-up scripts (`gravity_mass_scaling_fixed_anchor.py`,
  `gravity_distance_channel_observables.py`).
- That a falling-tail power-law fit exists on the primary-runner cache; the
  cache explicitly reports the opposite.

## Audit boundary (2026-05-09 — claim narrowing per `runner_artifact_issue`)

The 2026-05-09 audit verdict on this note was `audited_conditional` with
the repair target:

> runner_artifact_issue: rerun or attach cached stdout for the exact note
> parameter sets, especially the `N=30 npl=90 y_range=28` distance sweep,
> the fixed-anchor mass sweep, and the channel-observable follow-up.

This revision takes the narrowing branch of the repair target. The bounded
null-result claim is now anchored entirely on the registered primary runner
(`scripts/gravity_distance_fixed_geometry.py`) and its current SHA-pinned
cache (`logs/runner-cache/gravity_distance_fixed_geometry.txt`). The earlier
quoted numerical rows on a wider `b ∈ {6, 10, 14, 18, 22, 26}` sweep at
`npl=90, y_range=28` and the fixed-anchor mass-scaling and channel-
observable rows are out-of-scope for this note's load-bearing claim until
those runners are registered and cached.

The bounded null-result holds from the primary-runner cache alone: a peaked
positive distance response with no review-safe falling-tail fit on the
cached `b` window.

## What would close this lane (future work)

Reinstating a promoted gravity force-law on the generated-DAG lane would
require:

1. Either extending the registered primary-runner sweep past the cached
   peak so a falling-tail power-law fit becomes review-safe with hard
   `R^2 >= 0.95`, **or** registering a new primary runner that captures
   the falling tail directly, with a SHA-pinned cache committed alongside.
2. Registering `gravity_mass_scaling_fixed_anchor.py` (or an equivalent
   fixed-anchor mass-scaling primary runner) in the runner classification
   ledger with a SHA-pinned cache, and clearing the same hard `R^2`
   threshold on a declared `M` window.
3. Registering `gravity_distance_channel_observables.py` (or equivalent)
   with a SHA-pinned cache if channel-observable evidence is to be made
   load-bearing.
4. A first-principles argument that the fitted exponent is the
   mass-coupling exponent, not just an empirical curve fit.

Until those steps land, the registered primary-runner evidence supports
only the bounded null-result above.
