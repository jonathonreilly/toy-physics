# Mirror Chokepoint Note

**Date:** 2026-04-03 (downgraded 2026-04-28 per audit-lane verdict)
**Status:** bounded finite mirror chokepoint diagnostic across stitched parameter surfaces; not a single-surface family theorem and not an asymptotic claim.

This note freezes the current review-safe mirror result on the strict
chokepoint family in:

[`scripts/mirror_chokepoint_joint.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_chokepoint_joint.py)

Log:
[`logs/2026-04-03-mirror-chokepoint-joint.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-joint.txt)

Scaling log:
[`logs/2026-04-03-mirror-chokepoint-scale-r5p0-n50.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-scale-r5p0-n50.txt)

Sparse rescue log:
[`logs/2026-04-03-mirror-chokepoint-scale-r5p0-p2p02-n50.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-scale-r5p0-p2p02-n50.txt)

Boundary scan logs:
[`logs/2026-04-03-mirror-chokepoint-boundary-n45-r5p0.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-boundary-n45-r5p0.txt)
[`logs/2026-04-03-mirror-chokepoint-boundary-n50-r5p2.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-boundary-n50-r5p2.txt)
[`logs/2026-04-03-mirror-chokepoint-boundary-n55-r5p0.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-boundary-n55-r5p0.txt)
[`logs/2026-04-03-mirror-chokepoint-boundary-n55-r5p0-N100.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-boundary-n55-r5p0-N100.txt)
[`logs/2026-04-03-mirror-chokepoint-boundary-n55-r5p2-N100.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-boundary-n55-r5p2-N100.txt)
[`logs/2026-04-03-mirror-chokepoint-boundary-n60-r5p0-N100.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-boundary-n60-r5p0-N100.txt)
[`logs/2026-04-03-mirror-chokepoint-boundary-n60-r5p0-N120.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-boundary-n60-r5p0-N120.txt)

## Setup

- strict layer-1 chokepoint connectivity
- `NPL_HALF = 25` (`50` total nodes per layer)
- `k = 5.0`
- `16` seeds
- `N = 15, 25, 40, 60, 80, 100`

## Retained Rows

The bounded mirror pocket is Born-clean and gravity-positive on the strict
`NPL_HALF = 25` probe, and the denser strict `NPL_HALF = 50` probe retains the
same pocket through `N = 60` before failing at larger sizes. The later
boundary scan extends that retained pocket to `N = 80` and `N = 100` on the
dense `NPL_HALF = 55/60` probes:

| N | `d_TV` | `pur_cl` | `S_norm` | gravity | Born `|I3|/P` | `k=0` |
|---|---:|---:|---:|---:|---:|---:|
| 15 | `0.9716` | `0.5769±0.02` | `1.0006` | `+1.2927±0.691` | `5.84e-16` | `0.00e+00` |
| 25 | `0.8014` | `0.7329±0.05` | `0.9986` | `+2.2748±0.525` | `6.54e-16` | `0.00e+00` |
| 40 | `0.8006` | `0.8764±0.03` | `0.9965` | `+4.6161±0.721` | `1.01e-15` | `0.00e+00` |
| 60 | `0.5443` | `0.8971±0.03` | `1.0021` | `+3.6663±0.698` | `1.18e-15` | `0.00e+00` |
| 80 | `0.4291` | `0.8182±0.03` | `1.0029` | `+3.0551±0.672` | `2.43e-15` | `0.00e+00` |
| 100 | `0.2308` | `0.9043±0.02` | `1.0058` | `+1.3089±0.570` | `1.13e-15` | `0.00e+00` |

## Exploratory Rows

At the default strict settings and the denser `NPL_HALF=50` scaling probe,
the higher-N rows still did not retain enough successful seeds to freeze as a
bounded large-N joint result:

| N | verdict |
|---|---|
| 80 | FAIL |
| 100 | FAIL |

The dense `NPL_HALF = 55` and `NPL_HALF = 60` boundary scans close the
retained pocket:

| npl_half | connect_radius | N | verdict |
|---|---:|---:|---|
| 55 | `5.0` | 80 | retained, Born clean, gravity positive |
| 55 | `5.0` | 100 | gravity collapses to zero; not retained |
| 55 | `5.2` | 80 | retained, Born clean, gravity positive |
| 55 | `5.2` | 100 | gravity collapses to zero; not retained |
| 60 | `5.0` | 80 | retained, Born clean, gravity positive |
| 60 | `5.0` | 100 | retained, Born clean, gravity positive |
| 60 | `5.0` | 120 | Born still clean, but gravity collapses to zero; not retained |

The sparse same-side layer-2 rescue (`layer2_prob = 0.02`) was also only
partially helpful:

| N | `pur_cl` | gravity | verdict |
|---|---:|---:|---|
| 25 | `0.7128±0.05` | `+1.1909±0.800` | retained, but weaker than strict mirror |
| 40 | `0.8272±0.05` | `+2.5460±1.031` | retained, still below strict mirror gravity |
| 60 | `0.8718±0.04` | `+2.7086±0.937` | retained, but weaker than strict mirror |
| 80 | `0.9031±0.04` | `+1.9444±1.268` | exploratory only; Born not certified (`nan`) |
| 100 | FAIL | FAIL | no retained row |

## Narrow Read

- The mirror chokepoint lane is **real as a bounded pocket**.
- It is Born-clean at machine precision on the retained small-N rows.
- It keeps a strong decoherence-side advantage at `N=15`, `N=25`, `N=40`,
  `N=60`, `N=80`, and `N=100`.
- It also keeps positive gravity and the `k=0` control at zero on the retained
  rows.
- The mirror pocket now clearly extends past `N=60`; the farthest retained row
  is `N=100` on the `NPL_HALF = 60`, `connect_radius = 5.0` boundary scan.
- The pocket still does **not** survive to `N=120` in a gravity-positive way,
  so it is bounded rather than asymptotic.
- The sparse layer-2 rescue does not change that verdict; it helps a little at
  `N=80` but does not produce a cleaner large-`N` retention story than the
  dense boundary scan.

## Interpretation

The current safe statement is:

- **retained bounded mirror pocket:** yes
- **large-N mirror scaling:** yes, through `N=100`
- **Born + gravity + decoherence coexistence:** yes, through `N=100`
- **strict `NPL_HALF = 50` scaling probe:** retained through `N=60`, then
  fails at `N=80/100`

The dense large-`N` boundary extension is reproducible directly from the live
script with:

`python3 scripts/mirror_chokepoint_joint.py --npl-half 60 --connect-radius 5.0 --n-layers 40 60 80 100 120 --layer2-prob 0.0`

For review-hardening, the fast canonical regression gate keeps the strict
baseline check separate from that slower replay; use
[`scripts/canonical_regression_gate.py --slow`](/Users/jonreilly/Projects/Physics/scripts/canonical_regression_gate.py)
when you want both.

The next step is to test whether even denser `NPL`, larger radius, or sparse
same-side layer-2 links can extend the mirror pocket beyond `N=60` without
breaking the chokepoint Born check.

For the canonical fixed-family decoherence fit on the bounded dense boundary
mirror pocket, see:

[`docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md`](MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md)

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, leaf criticality):

> Issue: the finite mirror-chokepoint pocket is partly reproducible, but
> the proposed-retained packet depends on a stitched table whose `N=40`/
> `N=60` values are not recovered by the strict `NPL_HALF=25` `radius=4.0`
> baseline or by `NPL_HALF=25` `radius=5.0`, and several cited log files
> for the joint, scaling, sparse-rescue, and boundary scans are missing.

> Why this blocks: a hostile auditor can verify `N=15`/`N=25` on the
> strict baseline and the dense `NPL_HALF=60` `radius=5.0`
> `N=40/60/80/100` positive-gravity window with `N=120` collapse, but
> cannot certify the exact retained table or the through-`N=100`
> retention story as a single closed claim without knowing which archived
> parameter surface supports each row and without assertion-gated
> retention criteria.

The honest claim, per the audit verdict's "Claim boundary until fixed"
line, is:

> safe to claim a finite diagnostic pocket: strict `NPL_HALF=25`
> `radius=4.0` reproduces retained `N=15`/`N=25`, dense `NPL_HALF=60`
> `radius=5.0` reproduces positive-gravity Born-clean `k=0`-clean mirror
> rows through `N=100` and zero-gravity collapse at `N=120`; it is not
> yet a clean retained asymptotic or single-surface mirror-chokepoint
> theorem.

The Status line and "Interpretation" framing have been narrowed to match.

## What this note does NOT claim

- A single-parameter-surface mirror chokepoint family theorem.
- A clean asymptotic retention law — the through-`N=100` retention is on
  a specific dense parameter card, not a family-wide statement.
- That the canonical retained table is recoverable from a single
  registered runner invocation — the table is stitched across multiple
  surfaces (`NPL_HALF=25` `radius=4.0`, `NPL_HALF=25` `radius=5.0`,
  `NPL_HALF=50` scaling, `NPL_HALF=55/60` boundary scans, sparse layer-2
  rescue), and several of the cited log files are not present in the
  repo.
- That the sparse layer-2 rescue is closed — its `N=80` row is reported
  as "Born not certified (`nan`)" and `N=100` is FAIL.

## What would close this lane (Path A future work)

A future worker pursuing reinstatement of a clean mirror chokepoint
family claim would need to land all of the following:

1. A single registered runner invocation (or a per-row parameter-card
   table) that reproduces every retained row from one canonical command
   line, with the canonical command line registered in the note.
2. Archived versions of the cited log files that are currently missing
   from the repo: `2026-04-03-mirror-chokepoint-joint.txt`,
   `2026-04-03-mirror-chokepoint-scale-r5p0-n50.txt`,
   `2026-04-03-mirror-chokepoint-scale-r5p0-p2p02-n50.txt`, and the
   six `2026-04-03-mirror-chokepoint-boundary-*.txt` files.
3. Hard runner-side pass/fail gates for seed counts, `NPL_HALF`,
   `connect_radius`, `layer2_prob`, Born tolerance, `k=0`,
   gravity positivity/significance, decoherence ceiling, and the
   `N=120` failure boundary.
4. A reconciliation of the strict `NPL_HALF=25` baseline (where
   `N=40`/`N=60` do not match the retained table) with the dense
   `NPL_HALF=60` boundary (where they do) — either as a separate
   diagnostic or as a single-surface theorem.
