# Mirror + Grown Combined Note

**Date:** 2026-04-03 (status line rephrased 2026-04-28 per audit-lane verdict; load-bearing scope narrowed to the standalone finite grown-mirror negative-control table 2026-05-10 per audit `scope_too_broad` repair target).
**Status:** bounded standalone finite negative-control note — the grown-symmetry scout produces a finite reproducible table over `d_growth ∈ {2, 3}` and `n_layers ∈ {18, 25, 30, 40}`, with weak joint performance (small `1 - pur_min`, mostly small or negative gravity). The cross-lane "does not approximate the higher-symmetry mirror / Z2 x Z2 benefit" claim is recorded as supporting context only and is not load-bearing here, since the comparator notes are not registered as one-hop dependencies.
**Claim type:** bounded_theorem
**Primary runner (load-bearing):** [`scripts/mirror_grown_combined.py`](../scripts/mirror_grown_combined.py).
**Primary runner registered cache (load-bearing):** [`logs/runner-cache/mirror_grown_combined.txt`](../logs/runner-cache/mirror_grown_combined.txt) — registered cached stdout (`exit_code=0`, `status=ok`) backing every row in the table below.

This note records the grown-symmetry scout. The 2026-05-10 narrowing
restricts the load-bearing scope to the standalone finite table reproduced
from the registered runner cache; the cross-lane comparator language is
demoted to out-of-load-bearing context.

Historical log (audit-trail):

[`logs/2026-04-03-mirror-grown-combined.txt`](../logs/2026-04-03-mirror-grown-combined.txt)

## Question

Can a grown symmetry scaffold approximate the retained `Z2xZ2` benefit near
the grown-graph density optimum, instead of relying on an imposed symmetry
construction?

The script tests:

- `d_growth = 2` with a y-mirror scaffold
- `d_growth = 3` with a y-mirror scaffold
- `n_layers = 18, 25, 30, 40`
- `npl = 30`

## Results (load-bearing — read directly from the registered cache)

The grown mirror scout produces a finite reproducible table on the
registered runner cache. The values below are read directly from
`logs/runner-cache/mirror_grown_combined.txt` and reflect the registered
seed seed-set used by that cache; small numerical differences from any
prior run reflect different stochastic seeds and are expected.

### `d_growth = 2` (3D, Z2 y-mirror)

| N | pur_min | 1-pur_min | gravity | n_ok |
|---|---:|---:|---:|---:|
| 18 | `0.9686` | `0.0314` | `-0.284` | `16` |
| 25 | `0.9646` | `0.0354` | `-0.008` | `16` |
| 30 | `0.9627` | `0.0373` | `-0.018` | `16` |
| 40 | `0.9821` | `0.0179` | `+1.030` | `16` |

### `d_growth = 3` (4D, Z2 y-mirror)

| N | pur_min | 1-pur_min | gravity | n_ok |
|---|---:|---:|---:|---:|
| 18 | `0.9702` | `0.0298` | `+0.246` | `16` |
| 25 | `0.9542` | `0.0458` | `+0.002` | `16` |
| 30 | `0.9239` | `0.0761` | `+0.031` | `16` |
| 40 | `0.9424` | `0.0576` | `+0.419` | `16` |

The standalone narrow read on these registered rows: small `1 - pur_min`,
gravity weakly distributed around zero with a single positive outlier near
`N = 40` for `d_growth = 2`, and small or near-zero gravity elsewhere. As
a finite standalone table this is a useful negative control on this
scout family.

## Narrow Read (load-bearing)

- The grown mirror scout produces a finite reproducible table on the
  registered runner cache (`d_growth ∈ {2, 3}`, `n_layers ∈ {18, 25, 30,
  40}`).
- The joint performance on this standalone table is weak: small
  `1 - pur_min` across all rows, gravity weakly distributed around zero
  with a single positive outlier near `N = 40` for `d_growth = 2`.

## Out-of-load-bearing scope

The following are recorded for context but are not load-bearing for any
claim in this note:

- Any quantitative comparison to the mirror chokepoint pocket or the
  `Z2 x Z2` lane (those comparator notes are not registered as one-hop
  dependencies here; the standalone table above does not require them).
- Any "approximation to the higher-symmetry mirror / `Z2 x Z2` benefit" claim; the
  load-bearing scope is just the standalone scout table.

## Conclusion (standalone, load-bearing scope)

The grown mirror scout, read as a finite standalone table on the
registered runner cache, is a useful negative control on this scaffold:
small `1 - pur_min` and weak gravity. As a standalone control row, this
is closed by the registered cache. Any cross-lane "successor lane"
language would require registered one-hop dependencies on the comparator
lane notes and is out-of-load-bearing here.

## Audit boundary (2026-05-10 — load-bearing scope narrowed to the standalone table)

This revision addresses the generated-audit repair target:

> scope_too_broad: add classified C PASS lines for the grown-scout
> metrics and cite/register the mirror and Z2xZ2 comparison rows, or
> narrow the note to a standalone finite negative control.

This revision takes the second branch of the repair target: the load-
bearing claim is narrowed to the standalone finite negative-control
table read directly from the registered runner cache. Cross-lane
comparator language is demoted to out-of-load-bearing context.

## Audit boundary (2026-04-28)

The earlier Status line read "exploratory only; does not approximate the
`proposed_retained` higher-symmetry benefit". The audit-lane parser
classified the row as `proposed_retained` because the literal token
appeared in the Status string — but the sentence and the note both say
this is an exploratory negative control, not a retained successor lane.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: The queue records this as `proposed_retained` because the
> Status line mentions the `proposed_retained` higher-symmetry benefit,
> but the source explicitly states 'exploratory only' and concludes
> this grown mirror scaffold is not the successor lane. Why this
> blocks: an exploratory negative control cannot be ratified as
> retained; doing so would invert the source's conclusion.

## What this note does NOT claim

- A successor lane to the mirror or `Z2 x Z2` higher-symmetry families.
- Any quantitative cross-lane approximation claim on the grown scout.
- That the grown mirror scaffold should be retained at any tier.

## What would close this lane (Path A future work)

A future worker pursuing reinstatement of a grown-symmetry successor
lane would need to author a separate retained note with a runner that
actually reproduces the mirror / `Z2 x Z2` higher-symmetry benefit on a
generated scaffold, plus registered one-hop dependencies on the
comparator artifacts.
