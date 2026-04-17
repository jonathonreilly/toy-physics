# Weak-Coupling Sign-Sensitivity Note

**Date:** 2026-04-11  
**Script:** `frontier_weak_coupling_battery.py`  
**Status:** exploratory positive, not blocker closure

## Question

Does the corrected parity-coupled staggered graph lane become more
sign-sensitive in the weak-coupling regime than it is at the stronger retained
operating points?

This probe is explicitly **not** a replacement for the retained irregular
directional-observable blocker note. It is a regime-finding experiment.

## Setup

- graph families:
  - random geometric
  - growing
  - layered cycle
- seeds: `42..46`
- sizes:
  - random geometric `side=8`
  - growing `n_target=64`
  - layered cycle `layers=8`, `width=8`
- couplings tested: `G=5`, `G=10`
- observables:
  - width asymmetry `w_asym`
  - spectral gap ratio
  - shell-force TOWARD count `tw_a`, `tw_r`

At each point the probe compares:

- attractive parity coupling
- repulsive parity coupling
- zero-field control

## Measured Result

### `G = 5`

- `14/15` runs have `w_asym < 1`
- mean width effect: `9.5%`
- random geometric and layered-cycle families separate cleanly
- one growing run is borderline (`w_asym = 1.0100`)
- repulsive shell-force counts are often `0/40`, but not always:
  - one random-geometric seed gives `22/40`
  - two random-geometric seeds give `4/40`

### `G = 10`

- `14/15` runs have `w_asym < 1`
- mean width effect: `13.5%`
- one growing run still flips the asymmetry the wrong way (`w_asym = 1.0725`)
- repulsive shell-force counts are again often `0/40`, but not universally:
  - random-geometric seeds give `4/40`, `4/40`, `8/40` on several runs

## Safe Read

The weak-coupling regime is the strongest currently known **sign-sensitive
regime** on the irregular graph families:

- attractive coupling almost always contracts more than repulsive coupling
- attractive coupling almost always widens the spectral gap more than
  repulsive coupling
- the shell-force sign shows much stronger separation than at the higher-`G`
  retained operating points

This is a real and useful result.

## What This Does NOT Close

This note does **not** close the off-lattice sign-selection blocker.

Why:

- the asymmetry is not universal (`14/15`, not `15/15`)
- the repulsive shell-force row is not cleanly `0/40` everywhere
- the observables are still regime-dependent and not yet frozen into the
  retained irregular graph battery semantics

So the correct interpretation is:

> the irregular graph lane has a strong weak-coupling sign-sensitive regime,
> but it still lacks one fully frozen graph-native directional observable that
> closes the blocker across families and operating points.

## Next Acceptance Gate

To promote this from exploratory positive to retained closure, one of these
must happen:

1. the weak-coupling asymmetry and shell-force separation freeze cleanly on a
   larger and more diverse retained family set, or
2. one graph-native observable is shown to stay sign-selective across both the
   weak-coupling and current retained structural operating points.
