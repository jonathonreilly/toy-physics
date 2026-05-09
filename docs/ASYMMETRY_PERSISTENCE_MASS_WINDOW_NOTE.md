# Asymmetry Persistence Mass Window Note

This note records the gravity-side follow-up for the generated hard-geometry
lane.

**Primary runner:** [`scripts/asymmetry_persistence_mass_scaling.py`](../scripts/asymmetry_persistence_mass_scaling.py)

The retained log is:

- [`logs/2026-04-02-asymmetry-persistence-mass-scaling.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-02-asymmetry-persistence-mass-scaling.txt)

## Setup

- `N = 100`
- thresholds `0.0`, `0.1`, `0.2`
- `8` seeds
- `npl = 60`
- anchor `b = 6.0`
- mass counts `M = 1, 2, 3, 5, 8, 12`

## What The Summary Shows

The generated lane is not a trivial flat control. The pruned LN rows give the
cleanest mass-response windows on the retained generated family.

- threshold `0.10`, LN:
  - `delta ~= 0.4032 * M^0.420`
  - `R^2 = 0.970`
- threshold `0.20`, LN:
  - `delta ~= 0.5332 * M^0.262`
  - `R^2 = 0.892`

The plain baseline is weaker:

- threshold `0.00`, linear:
  - `delta ~= 0.8508 * M^0.101`
  - `R^2 = 0.592`

## Narrow Conclusion

The generated hard-geometry lane has a real, bounded mass-response window.
It is not a clean asymptotic gravity law, but it is a review-safe gravity-side
signal on the retained generated family.

