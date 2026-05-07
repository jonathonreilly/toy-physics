# Mesoscopic Surrogate Threshold 2D Note

**Date:** 2026-04-04 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** bounded control note; finite 2D support sweep found no sharp threshold in two-stage sourced-response stability and is not a persistent-mass or inertial-response theorem.
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only; effective status is pipeline-derived after independent review.

## Artifact chain

- Script: [`scripts/mesoscopic_surrogate_threshold_2d.py`](../scripts/mesoscopic_surrogate_threshold_2d.py)
- Audit cache stdout:
  [`logs/runner-cache/mesoscopic_surrogate_threshold_2d.txt`](../logs/runner-cache/mesoscopic_surrogate_threshold_2d.txt)
- Frozen legacy log:
  [`logs/2026-04-04-mesoscopic-surrogate-threshold-2d.txt`](../logs/2026-04-04-mesoscopic-surrogate-threshold-2d.txt)

## Question

Does shrinking the surrogate-source support on the retained 2D ordered-lattice
family produce a clear threshold where the two-stage sourced-response control
breaks?

## Frozen setup

- retained 2D ordered-lattice family
- same broad surrogate construction as the frozen 2D two-stage companion
- support sweep over `topN = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 20, 25,
  32, 40, 49, 64, 81`
- stability criterion:
  - relative stage-1 / stage-2 ratio difference `<= 1%`
  - source carry `>= 0.99`

## Result

Every scanned `topN` value stayed stable.

The frozen rows show:

- the runner recomputes every listed support row from the 2D ordered-lattice
  harness
- the maximum relative stage-1 / stage-2 sourced-response ratio difference is
  `0.0066069`, below the `0.01` stability ceiling
- the support carry stays at `1.000` across the scan
- no support cutoff in the scanned range causes a stability collapse

The smallest scanned support, `topN = 1`, is already stable.

The current audit cache supplies the finite-computation packet with assertion
gates:

- `frozen_topN_support_list_scanned`
- `all_scanned_topN_stable`
- `stage_ratio_relative_error_within_one_percent`
- `support_carry_floor`
- `no_sharp_collapse_in_scanned_range`

## Safe read

This 2D control does **not** show a sharp localization threshold.

So on the retained 2D family:

- shrinking the source support is not the lever that produces a collapse
- the mesoscopic surrogate remains stable even at very small scanned support
- the honest next question is not "where is the 2D threshold?"
- the honest next question is whether a more localized source object can be
  built on a different retained family, or whether localization itself is the
  wrong knob

## Implication for the inertial-response lane

This note tightens the blocker rather than closing it:

- the broad mesoscopic surrogate survives support shrinkage in the retained
  2D family
- but the test does not produce a localized persistent-mass object
- so it remains a bounded control, not a persistent-mass theorem

The cheapest future move is therefore:

- try a smaller localized source object on another already-bounded family only
  if it preserves the same multistage sourced-response stability
- otherwise stop treating support shrinkage as the main bottleneck and move on
  to a genuinely different family or mechanism

## Audit boundary (2026-04-28)

The earlier status prose mixed bounded-control wording with a proposed
retention label, which was not a source-science statement and is no longer
used here. This note now carries only the bounded finite sweep and leaves all
audit verdicts to the independent audit lane.

## What this note does NOT claim

- A persistent-mass theorem.
- An inertial-response theorem.
- A sharp support-shrinking threshold (the sweep does not find one).

## What would close this lane (Path A future work)

A separate retained theorem deriving a persistent-mass object from the
sweep would require a registered runner with explicit pass thresholds
for what counts as "persistent mass" and "inertial response", with
assertion-gated support-shrinking criteria.
