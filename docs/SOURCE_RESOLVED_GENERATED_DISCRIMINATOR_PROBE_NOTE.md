# Source-Resolved Generated Discriminator Probe

**Date:** 2026-04-05
**Status:** discriminator probe, not a closure theorem

## Artifact chain

- [`scripts/source_resolved_generated_discriminator_probe.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_generated_discriminator_probe.py)
- [`logs/2026-04-05-source-resolved-generated-discriminator-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-generated-discriminator-probe.txt)

## Question

Is the best current generated-family bridge point limited mainly by
connectivity/support concentration, or by the field rule itself?

This probe stays narrow:

- compact generated 3D DAG family
- retained `kNN`-floor support rescue as the bridge family
- compare at most two bridge variants:
  - support rescue + static Green
  - support rescue + wavefield bridge
- exact zero-source reduction check
- one support metric: detector effective support `N_eff`
- one compact diagnostic: geometry-vs-field bottleneck label from the
  relative sign-count and support deltas

## Frozen result

The exact zero-source reduction survives both variants: `zero = 0.000e+00`.

Aggregated over seeds `0..3`:

- support rescue: `9/16` TOWARD, `N_eff = 5.31`
- wavefield bridge: `6/16` TOWARD, `N_eff = 5.14`

Compact discriminator:

- `delta_TOWARD = -3`
- `delta_N_eff = -0.18`
- `bottleneck = geometry-limited`

## Safe read

The wavefield bridge does not improve sign counts on top of the retained
support rescue, and it does not broaden detector support either.

That means the current generated-family bridge still looks family-limited by
connectivity/support concentration more than by the field rule itself.

The safest claim is:

- support rescue is real
- the wavefield bridge is real
- but on this compact generated family, the wavefield update does not overcome
  the geometry bottleneck

## Branch implication

This is a discriminator, not a closure result.

The right next generated-family question is not "can we keep tuning the same
bridge?"

It is:

- can a better geometry rule widen support enough to let the field rule matter?
- or do we need a genuinely new field architecture before the generated family
  can leave the bridge regime?
