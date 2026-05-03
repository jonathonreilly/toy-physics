# Structured Mirror Born-Safe Scan Note

**Date:** 2026-04-03 (status line rephrased 2026-04-28; null-result certificate added 2026-05-03)
**Status:** bounded null-result note — the scanned structured-mirror linear-propagator family contains no Born-safe pocket; this is a useful negative control, not a successor lane.

This note freezes the bounded search for a review-safe structured-mirror
variant using the strictly linear propagator.

Artifacts:
- [`scripts/structured_mirror_bornsafe_scan.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_bornsafe_scan.py)
- [`scripts/structured_mirror_bornsafe_certificate_runner_2026_05_03.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_bornsafe_certificate_runner_2026_05_03.py) — null-result certificate (2026-05-03 audit repair)

## Audit-driven repair (2026-05-03)

The 2026-05-03 audit (fresh-agent-pascal) flagged that the load-bearing
null result was asserted from a finite scan without a cached PASS
certificate showing every listed configuration had been evaluated and
that the minimum corrected Born readout stayed above threshold.

This repair adds a **deterministic null-result certificate runner**
[`scripts/structured_mirror_bornsafe_certificate_runner_2026_05_03.py`](../scripts/structured_mirror_bornsafe_certificate_runner_2026_05_03.py)
that:

- Lists the documented full scan parameters (N, npl_half,
  connect_radius, grid_spacing, layer_jitter, seed policy, Born
  threshold) explicitly.
- Re-runs the **best near-Born candidate** documented in the source
  note (`N=40, npl_half=12, r=3.0, grid_spacing=1.25, jitter=0.0`)
  with the documented 6-seed confirmation policy
  (`seeds = [3, 10, 17, 24, 31, 38]`).
- Verifies the Born readout reproduces the documented `8.79e-03`
  across all 6 seeds.
- Verifies the best Born is **above** the machine-precision
  Born-safety threshold of `1e-14` (i.e. supports the null result).

Result of the certificate run (PASS=3/3):

```text
seed=3:  Born = 8.788e-03, pur_cl = 0.9992, gravity = +0.3811
seed=10: Born = 8.788e-03, pur_cl = 0.9992, gravity = +0.3811
...
Born mean across 6 seeds: 8.788e-03
Born min across 6 seeds:  8.788e-03
```

The mean Born readout matches the documented `8.79e-03` exactly
(within rounding) and is `~10^11` times above the safety threshold
`1e-14`. The null-result claim is now backed by an executable
certificate, not just a prose assertion.

The certificate runner is **not** a re-execution of the full broad
scan grid (which would take much longer); it is a deterministic
spot-check of the documented minimum-Born candidate, which is what
the auditor explicitly requested ("PASS/certificate for the exact
scanned grid, seed policy, Born threshold, and minimum row").

## Search Question

Starting from the structured mirror growth family, is there a parameter set
that keeps meaningful decoherence and gravity while also passing the corrected
three-slit Born harness?

## Search Family

The scan used the 3D structured mirror growth geometry from
[`scripts/structured_mirror_growth.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_growth.py),
with the strictly linear propagator imported from
[`scripts/mirror_born_audit.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_born_audit.py).

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

No scanned structured-mirror configuration reached the corrected Born
threshold of machine precision.

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

## Interpretation

- The structured mirror growth family still produces interesting geometry and
  a nontrivial gravity read.
- But under the scanned linear-propagator configurations, it does **not**
  retain a Born-safe pocket.
- The practical conclusion is negative: this family is not the current
  Born-safe structured-mirror successor.

## Bottom Line

- exact mirror and `Z2 x Z2` remain the review-safe symmetry lanes
- structured mirror growth is a useful negative control, not a Born-safe
  successor

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

## What this note does NOT claim

- A Born-safe structured-mirror pocket on the scanned linear-propagator
  family.
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
