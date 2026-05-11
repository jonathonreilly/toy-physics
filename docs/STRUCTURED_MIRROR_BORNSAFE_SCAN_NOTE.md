# Structured Mirror Born-Safe Scan Note

**Date:** 2026-04-03 (status line rephrased 2026-04-28; certificate runner added 2026-05-03; sliced runner added 2026-05-09; load-bearing claim narrowed to the registered 32-config slice 2026-05-10 per audit `scope_too_broad` repair target).
**Status:** bounded null-result note — on the registered 32-config sliced linear-propagator audit-packet runner, no structured-mirror configuration reaches the documented Born-safety threshold (`1e-14`); this is a useful negative control on the sliced family, not a successor lane. The 540-config full-grid scan log remains supporting context for the broader exhaustion claim, which is explicitly scoped here as out-of-load-bearing pending registration of a full-grid runner-cache artifact.
**Claim type:** bounded_theorem

This note freezes the bounded search for a review-safe structured-mirror
variant using the strictly linear propagator. The load-bearing scope is
the registered 32-config sliced runner; the broader 540-config exhaustion
claim is recorded as supporting context only.

**Primary runner:** [`scripts/structured_mirror_bornsafe_sliced_runner_2026_05_09.py`](../scripts/structured_mirror_bornsafe_sliced_runner_2026_05_09.py)
— registered sliced independent runner; recomputes corrected Born `|I3|/P`
from first principles via the same `propagate_LINEAR` import the slow scan
uses, on a 32-config representative slice (best near-Born candidate, grid
corners, center, near-best neighbourhood, jittered slice) at the canonical
6-seed protocol. Asserts grid minimum stays above the documented machine-
precision Born-safety threshold (`1e-14`); exits nonzero if any sliced
config beats the threshold (which would invalidate the null result and
re-open the lane). On the live import, the slice's grid minimum is
`4.6428e-03`, in the same order of magnitude as the documented best
(`8.79e-03`), eleven orders of magnitude above the threshold. Cached
stdout: [`logs/runner-cache/structured_mirror_bornsafe_sliced_runner_2026_05_09.txt`](../logs/runner-cache/structured_mirror_bornsafe_sliced_runner_2026_05_09.txt).

**Supporting certificate:** [`scripts/structured_mirror_bornsafe_certificate_runner_2026_05_03.py`](../scripts/structured_mirror_bornsafe_certificate_runner_2026_05_03.py)
— constants-certificate runner; PASS=3/3 confirms the documented best
near-Born readout is consistent with the scan evidence at the audit-packet
level.

**Companion runner:** [`scripts/structured_mirror_bornsafe_scan.py`](../scripts/structured_mirror_bornsafe_scan.py)
— the original (slow) parameter-grid scan (540 configurations, 2 seeds per
config + 6-seed confirmation on the best candidate). Reproducible but
slower than the sliced lane.

**Cached scan log:** [`logs/2026-04-03-structured-mirror-bornsafe-scan.txt`](../logs/2026-04-03-structured-mirror-bornsafe-scan.txt)
— completed stdout from the slow scan covering all 540 configurations.
The documented best near-Born candidate
`N=40, npl_half=12, connect_radius=3.0, grid_spacing=1.25, layer_jitter=0.0`
appears at line ~225 with the documented `Born=8.79e-03, d_TV=0.1208, pur_cl=0.9992,
S_norm=0.0009, gravity=+0.3811`, including the 6-seed confirmation.
RETAINED POCKET: none found.

## Review-loop runner attachment (2026-05-09 update)

The 2026-05-03 audit flagged the note's null-result claim as lacking a
registered runner that recomputes the grid minimum from first principles.
The 2026-05-03 repair attached a constants-certificate runner that
verified consistency with the scan evidence but did not re-execute the
underlying first-principles computation.

The 2026-05-09 repair attaches a sliced independent runner
(`scripts/structured_mirror_bornsafe_sliced_runner_2026_05_09.py`) that:

1. recomputes corrected Born `|I3|/P` from first principles per-config
   using the same `propagate_LINEAR` propagator as the slow companion
   scan;
2. covers a 32-config representative slice spanning grid corners,
   center, near-best neighbourhood, and jittered configurations;
3. runs the canonical 6-seed protocol per config;
4. asserts the sliced grid minimum stays above `1e-14` (Born-safety
   threshold); exits nonzero if any sliced config beats that threshold.

The sliced lane is the new audit-packet runner. The 540-config slow
scan and its cached log remain supporting context for the broader
exhaustion claim.

## Search Question

Starting from the structured mirror growth family, is there a parameter set
that keeps meaningful decoherence and gravity while also passing the corrected
three-slit Born harness?

## Search Family

The scan used the 3D structured mirror growth geometry from
[`scripts/structured_mirror_growth.py`](../scripts/structured_mirror_growth.py),
with the strictly linear propagator imported from
[`scripts/mirror_born_audit.py`](../scripts/mirror_born_audit.py).

Scanned parameters:

- `d_growth = 2`
- `N = 25, 30, 40`
- `npl_half = 8, 12, 16, 20`
- `connect_radius = 2.5, 3.0, 3.5, 4.0, 4.5`
- `grid_spacing = 1.0, 1.25, 1.5`
- `layer_jitter = 0.0, 0.15, 0.3`
- `2` seeds per config in the broad sweep
- a follow-up `6`-seed confirmation on the best near-Born candidate

The scan measured:

- `d_TV`
- `pur_cl`
- `S_norm`
- gravity
- corrected Born `|I3|/P`
- `k=0` gravity control

## Result

On the registered 32-config sliced runner (the load-bearing audit-packet
runner here), no structured-mirror configuration reaches the corrected
Born-safety threshold (`1e-14`). The 540-config slow scan over the full
parameter family is consistent with this conclusion but is out-of-load-
bearing pending registration of a full-grid runner-cache artifact.

The best near-Born candidate in the broad sweep was:

- `N = 40`
- `npl_half = 12`
- `connect_radius = 3.0`
- `grid_spacing = 1.25`
- `layer_jitter = 0.0`
- `d_TV = 0.1208`
- `pur_cl = 0.9992`
- `S_norm = 0.0009`
- gravity `+0.3811`
- Born `8.79e-03`
- `k=0 = 0.00e+00`

That candidate was then re-run with `6` seeds and kept the same Born
readout, so it is not a seed fluke.

### Sliced verification (2026-05-09)

The sliced independent runner re-executed the same first-principles
propagator on a 32-config representative slice (best near-Born candidate
+ grid corners + center + near-best neighbourhood + jittered slice),
each at the canonical 6-seed protocol. The sliced grid Born minimum is
`4.6428e-03` (achieved at `N=40, npl_half=12, connect_radius=3.0,
grid_spacing=1.25, layer_jitter=0.30`), in the same order of magnitude
as the documented best near-Born candidate (`8.79e-03`) and eleven
orders of magnitude above the Born-safety threshold (`1e-14`). The
sliced runner exits zero and is registered as the audit-packet
runner; the 540-config slow scan remains supporting context.

## Interpretation

- The structured mirror growth family still produces interesting geometry and
  a nontrivial gravity read.
- But under the scanned linear-propagator configurations, it does **not**
  retain a Born-safe pocket.
- The practical conclusion is negative: this family is not the current
  Born-safe structured-mirror successor.

## Bottom Line

- exact mirror and `Z2 x Z2` remain the review-safe symmetry lanes
- structured mirror growth is a useful negative control on the registered
  32-config sliced family, not a Born-safe successor; the broader
  540-config exhaustion claim is supporting context only

## Audit boundary (2026-04-28)

The earlier Status line read "no `proposed_retained` Born-safe
structured-mirror pocket found in the scanned linear family", which the
audit-lane parser read as a `proposed_retained` claim even though the
literal sentence said the opposite. The Status line has been rephrased
to a positive bounded null-result framing.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: this is a parser false positive for the audit queue: the
> status line contains the token `proposed_retained` only inside the
> negative statement that no `proposed_retained` Born-safe structured-
> mirror pocket was found.

The note's actual content is a search that failed to find a Born-safe
pocket, plus the best near-Born candidate which was confirmed with 6
seeds. That is a negative control, not a retained or proposed-retained
claim.

## Audit boundary (2026-05-10 — load-bearing scope narrowed to the registered 32-config slice)

This revision addresses the generated-audit repair target:

> scope_too_broad: Split a clean slice-only bounded claim or supply/
> register the full 540-config scan artifact needed to close the broader
> exhaustion claim.

This revision takes the first branch of the repair target: the load-bearing
claim is now narrowed to the registered 32-config sliced runner audit-packet
runner. The 540-config full-grid slow scan and its historical log remain
supporting context for the broader exhaustion claim, which is explicitly
out-of-load-bearing pending registration of a `logs/runner-cache/`
artifact. The constants-certificate runner and the sliced runner remain
the audit-packet authorities.

## What this note does NOT claim

- A Born-safe structured-mirror pocket on the registered 32-config sliced
  family.
- That the broader 540-config full-grid scan is itself a closed audit-
  packet exhaustion proof; the full-grid slow log is supporting context
  only and the full-grid runner-cache is not yet registered.
- That structured mirror growth is a successor lane to exact mirror or
  `Z2 x Z2`.
- That the best near-Born candidate (`Born 8.79e-03`) clears any
  Born-safety threshold.

## What would close this lane (Path A future work)

Reinstating a Born-safe structured-mirror successor would require:

1. A registered runner whose corrected Born `|I3|/P` lands at machine
   precision (≤ `1e-14`) on at least one structured-mirror parameter
   set.
2. A registered runner that holds across at least 6 seeds at the same
   Born tolerance.
3. A coexistence demonstration of decoherence and gravity together with
   the Born-safe pocket on the same parameter set.

## Registered runner artifacts

The registered sliced runner verifies a representative 32-config slice rather
than the full 540-config scanned family. The companion full-grid scan source
is present in the worktree:

- Sliced runner (registered, fast slice): `scripts/structured_mirror_bornsafe_sliced_runner_2026_05_09.py`
  with cache `logs/runner-cache/structured_mirror_bornsafe_sliced_runner_2026_05_09.txt`.
- Constants certificate runner (registered): `scripts/structured_mirror_bornsafe_certificate_runner_2026_05_03.py`.
- Full-grid scan runner source (slow, 540 configs): `scripts/structured_mirror_bornsafe_scan.py`.
- Full-grid scan completed log: `logs/2026-04-03-structured-mirror-bornsafe-scan.txt`
  (recorded stdout from a prior run covering all 540 configurations; not yet
  registered in `logs/runner-cache/`).

The bounded scope is therefore: the sliced runner closes the representative
slice plus the documented near-best region; the full 540-config exhaustion
claim relies on the prior recorded log, not a current registered cache.
Registering a full-grid `logs/runner-cache/` artifact remains the residual
gap.
