# Source-Resolved Geometry-Rule Repair Probe

**Date:** 2026-04-05  
**Status:** geometry-repair probe, bounded negative with one partial improvement

## Artifact chain

- [`scripts/source_resolved_geometry_rule_repair_probe.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_geometry_rule_repair_probe.py)
- [`logs/2026-04-05-source-resolved-geometry-rule-repair-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-geometry-rule-repair-probe.txt)

## Question

The discriminator said the current generated-family bridge is geometry-limited.
Can one geometry-construction change widen support enough for the weak-field
sign and mass-law read to improve, without changing the field rule itself?

This probe stays geometry-only:

- baseline retained control: `kNN`-floor bridge on the compact generated DAG
  family
- repair candidate: the retained `kNN`-floor bridge plus an adaptive sector
  fan on the next layer
- one field rule only: static Green kernel
- one reduction check: zero source should still give exactly zero shift
- one support metric: detector effective support `N_eff`
- one weak-field metric: centroid sign count and centroid-shift exponent

## Frozen result

Exact zero-source reduction survives both variants:

- baseline zero-source shift: `0.000e+00`
- repair zero-source shift: `0.000e+00`

Aggregated over seeds `0..3`:

- baseline: `7/16` TOWARD, `N_eff = 5.06`, `F~M = 0.058`
- repair: `8/16` TOWARD, `N_eff = 2.80`, `F~M = 0.335`

Repair delta:

- `delta_TOWARD = +1`
- `delta_N_eff = -2.26`
- `baseline_alpha = 0.058`
- `repair_alpha = 0.335`

## Safe read

The geometry repair is not the support-broadening fix we wanted.

What it did do:

- slightly improved the weak-field sign count
- moved the centroid-shift exponent closer to a visible power law

What it did not do:

- it did not broaden detector support
- it did not recover a clean weak-field mass law
- it therefore does not escape the geometry-limited bottleneck

So the honest read is:

- the generated-family bridge is still geometry-limited
- this specific geometry-rule repair is a mixed partial improvement, not a
  closure
- a real escape hatch would need a different geometry rule, not another
  field-rule tweak

## Branch verdict

Treat this as a bounded negative with one useful partial.

The result is still valuable because it says the bottleneck is not solved by
simply layering a sector fan on top of the retained `kNN` floor.

The next generated-family question is therefore:

- can we design a geometry rule that genuinely widens support while keeping
  the weak-field lane alive?

