# Source-Resolved Generated Wavefield Transfer v2

**Date:** 2026-04-05  
**Status:** bounded generated-family no-go for the tested geometry-rule change

## Artifact chain

- [`scripts/source_resolved_generated_wavefield_transfer_v2.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_generated_wavefield_transfer_v2.py)
- [`logs/2026-04-05-source-resolved-generated-wavefield-transfer-v2.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-generated-wavefield-transfer-v2.txt)

## Question

Can a geometry-rule change that widens detector support make the retained
exact-lattice wavefield mechanism matter on the generated family?

This probe stays narrow:

- compact generated 3D DAG family
- retained `kNN`-floor bridge as the baseline
- new `z`-spread stencil as the geometry-rule change
- static Green vs wavefield on both geometries
- exact zero-source reduction check
- one support metric: detector effective support `N_eff`
- one mass-law metric: centroid-shift exponent across source strength

## Frozen result

The exact zero-source reduction survives both geometries:

- `zero = 0.000e+00`

Aggregated over seeds `0..3`:

- bridge / static: `9/16` TOWARD, `N_eff = 5.31`, `F~M = -0.316`
- bridge / wavefield: `6/16` TOWARD, `N_eff = 5.14`, `F~M = 0.098`
- z-spread / static: `10/16` TOWARD, `N_eff = 5.13`, `F~M = 0.103`
- z-spread / wavefield: `7/16` TOWARD, `N_eff = 4.68`, `F~M = -0.436`

Geometry delta relative to the retained bridge:

- static: `delta_TOWARD = +1`, `delta_N_eff = -0.18`, `delta_F~M = +0.419`
- wavefield: `delta_TOWARD = +1`, `delta_N_eff = -0.46`, `delta_F~M = -0.534`

## Safe read

The geometry-rule change does **not** produce the hoped-for transfer.

- The z-spread stencil slightly improves the centroid sign count in aggregate.
- It does **not** broaden detector support.
- It does **not** improve the wavefield mass-law read.
- The wavefield bridge stays geometry-limited on this family.

The safest claim is:

- the generated-family bridge remains narrow
- the tested geometry-rule change does not widen it in the right way
- the exact-lattice wavefield mechanism still does not become family-relevant on
  this generated bridge

## Honest limitation

This is a geometry-rule discriminator, not a closure theorem.

- it rules out one plausible support-spreading rule
- it does not rule out all possible generated-family geometries
- it does not change the current conclusion that this family is still
  bridge-only

## Branch verdict

Treat this as a bounded no-go for the tested geometry rule:

- exact zero-source reduction survives
- sign barely improves
- detector support does not widen
- the wavefield mass-law read worsens

So the next generated-family question is not another small z-spread tweak.
It is whether the geometry itself needs a more radical rule change before the
wavefield update can matter.
