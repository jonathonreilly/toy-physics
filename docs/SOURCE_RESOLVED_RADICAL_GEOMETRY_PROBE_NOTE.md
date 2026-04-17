# Source-Resolved Radical Geometry Probe

**Date:** 2026-04-05  
**Status:** bounded negative for the tested geometry rule

## Artifact chain

- [`scripts/source_resolved_radical_geometry_probe.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_radical_geometry_probe.py)
- [`logs/2026-04-05-source-resolved-radical-geometry-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-radical-geometry-probe.txt)

## Question

Can a materially different generated-family geometry construction widen
downstream support enough for the retained exact-lattice wavefield mechanism
to matter on the generated family?

This probe stays narrow:

- compact generated 3D DAG family
- retained `kNN`-floor bridge as the baseline geometry
- radical downstream-reach fan as the tested geometry rule
- static Green vs wavefield on each geometry
- exact zero-source reduction check
- detector effective support `N_eff`
- centroid sign counts and a weak-field `F~M` fit

## Frozen result

Exact zero-source reduction survives both geometries:

- `zero = 0.000e+00`

Aggregated over seeds `0..3`:

- bridge / static: `9/16` TOWARD, `N_eff = 5.31`, `F~M = -0.316`
- bridge / wavefield: `6/16` TOWARD, `N_eff = 5.14`, `F~M = 0.098`
- radical / static: `7/16` TOWARD, `N_eff = 5.68`, `F~M = 0.090`
- radical / wavefield: `0/16` TOWARD, `N_eff = 5.05`, `F~M = -0.113`

Geometry delta relative to the retained bridge:

- static: `delta_TOWARD = -2`, `delta_N_eff = +0.36`, `delta_F~M = +0.407`
- wavefield: `delta_TOWARD = -6`, `delta_N_eff = -0.09`, `delta_F~M = -0.210`

## Safe read

The radical geometry rule does **not** produce the hoped-for transfer.

What it does do:

- slightly broadens detector support in the static case
- keeps exact zero-source reduction intact
- changes the geometry enough to move the mass-law read

What it does not do:

- it does not improve the weak-field sign count in aggregate
- it does not improve the wavefield mass-law read
- it does not make the generated-family bridge geometry-transfer relevant in
  the way we want

## Honest limitation

This is a geometry-rule discriminator, not a closure theorem.

- it rules out one more plausible support-widening construction
- it does not rule out all possible generated-family geometries
- it does not change the current conclusion that this family remains
  bridge-only

## Branch verdict

Treat this as a bounded no-go for the tested geometry rule:

- exact zero-source reduction survives
- support can move a little in the static case
- but the wavefield update does not become more relevant on this family

The next generated-family question is therefore not another small fan or
sector repair.
It is whether the geometry itself needs a more radical rule change, or a
different family altogether, before the wavefield update can matter.
