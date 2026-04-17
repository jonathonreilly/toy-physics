# Hard-Geometry Gravity Window Note

**Date:** 2026-04-03  
**Status:** bounded comparison, not a new law claim

This note compares the two retained hard-geometry families under the same
Born-safe lens:

- dense central-band hard geometry
- generated asymmetry-persistence hard geometry

The comparison uses the retained same-graph joint cards and the gravity-side
follow-ups already on `main`, plus the new exploratory sweep in
[`scripts/hard_geometry_gravity_window.py`](/Users/jonreilly/Projects/Physics/scripts/hard_geometry_gravity_window.py).

## What Is Supported

### Central-band

The cleanest same-graph central-band gravity row remains the dense
`N = 60` retained joint card:

- [`docs/CENTRAL_BAND_DENSE_JOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CENTRAL_BAND_DENSE_JOINT_NOTE.md)
- `LN + |y|`:
  - Born `|I3|/P = 0.000±0.000`
  - `pur_min = 0.875±0.125`
  - gravity `+0.455±0.384`

The central-band gravity-side mass follow-up is also useful:

- [`docs/CENTRAL_BAND_MASS_WINDOW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CENTRAL_BAND_MASS_WINDOW_NOTE.md)

On the densest slice we tested, the pruned LN row has the cleaner mass fit:

- `delta ~= 0.4704 * M^0.595`, `R^2 = 0.828`

### Generated asymmetry-persistence

The generated lane stays Born-clean on the corrected dense probe and carries
the stronger direct gravity rows at `N = 100`:

- [`docs/ASYMMETRY_PERSISTENCE_PILOT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ASYMMETRY_PERSISTENCE_PILOT_NOTE.md)
- [`docs/ASYMMETRY_PERSISTENCE_MASS_WINDOW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ASYMMETRY_PERSISTENCE_MASS_WINDOW_NOTE.md)

Dense `N = 100` rows show:

- threshold `0.10`
  - `pur_cl = 0.932±0.039`
  - gravity `+1.716±0.784`
  - keep rate `97.9%`
- threshold `0.20`
  - `pur_cl = 0.921±0.043`
  - gravity `+2.102±0.825`
  - keep rate `97.7%`

The mass-window summary is also strong and review-safe:

- threshold `0.10`, LN:
  - `delta ~= 0.4032 * M^0.420`, `R^2 = 0.970`
- threshold `0.20`, LN:
  - `delta ~= 0.5332 * M^0.262`, `R^2 = 0.892`

## Narrow Conclusion

The strongest gravity pocket worth carrying forward is the
generated-asymmetry family at dense `N = 100`.

Reason:

- it stays Born-clean in the corrected dense probe
- it keeps a stronger direct gravity signal than the simple central-band
  joint card
- it also gives the cleaner mass-response fit on the generated side

The central-band family is still important, but mostly as the simpler
Born-safe control and the cleanest small-`N` same-graph witness.

So the current hard-geometry story is:

- **best direct gravity pocket:** generated asymmetry-persistence
- **best simple control pocket:** dense central-band
- **best emergent lesson:** hard geometry remains the shared enabler, but the
  generated geometry lane currently looks like the better gravity carrier

