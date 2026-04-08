# Wave Direct-dM H=0.25 Feasibility Note

**Date:** 2026-04-08
**Status:** minimal single-family feasibility probe

This note records the smallest practical question on the direct-dM lane:

> Can the existing matched-history direct-dM harness run at `H = 0.25`
> on this workstation for one family and one strength without destabilizing
> the claim surface?

The probe is intentionally narrow:

- one family / one geometry setup
- one strength, defaulting to `S_PHYS`
- one `H` point: `0.25`

If this probe completes in a reasonable wall time and memory footprint,
the main lane can add `H = 0.25` as one more retained point.
If not, the current matched-history lane should stay at `H = 0.5` and
`H = 0.35` and the flagship claim surface should not be widened yet.

## Result

The smallest `H = 0.25` run completed on this workstation for one
family and one strength, but it was not cheap:

- `family = Fam1`
- `strength = 0.004`
- `H = 0.25`
- `elapsed = 147.05 s`
- `peak RSS = 710192 KB` `~ 693 MB`
- `delta_hist = -0.001256`
- `R_hist = -20.12%`

That makes `H = 0.25` **feasible in principle** for a single-family
matched-history check, but too slow to treat as a routine addition to the
main lane without a stronger reason or a more optimized runner.

The safest current interpretation is:

- a single `H = 0.25` point can be added as a validation point
- it should not be promoted as broad retained evidence yet
- the main lane should still be considered anchored by `H = 0.5` and
  `H = 0.35` until we decide whether to pay the runtime cost for a
  larger `H = 0.25` batch

## Artifact chain

- [`scripts/wave_direct_dm_h025_feasibility_probe.py`](../scripts/wave_direct_dm_h025_feasibility_probe.py)
