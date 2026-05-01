# Staggered Self-Gravity Scaling Note

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-10
**Script:** `frontier_staggered_self_gravity_scaling.py`

## Summary

This probe makes the inline self-gravity claim rerunnable. It sweeps the
retained self-gravity dynamics across graph size on admissible staggered graph
families and reports three things per case:

- final width ratio `w_self / w_free`
- inward-sign stability across iterations under the prescribed attractive coupling
- norm drift

After the two-sign audit, the retained question is not whether the irregular
proxy reads inward. It is whether the contraction survives as the graph gets
larger under the corrected parity coupling.

## Sweep Results

| Family | Size case | Nodes | Width ratio | Contraction | Force | Flips | Norm drift | Score |
|---|---|---:|---:|---:|---|---:|---:|---:|
| Random geometric | `side=4` | 16 | 0.8800 | +12.00% | 20/20 TW | 0 | 5.55e-16 | 3/3 |
| Random geometric | `side=6` | 36 | 0.6396 | +36.04% | 20/20 TW | 0 | 8.88e-16 | 3/3 |
| Random geometric | `side=8` | 64 | 0.6184 | +38.16% | 20/20 TW | 0 | 6.66e-16 | 3/3 |
| Random geometric | `side=10` | 100 | 0.6026 | +39.74% | 20/20 TW | 0 | 2.22e-16 | 3/3 |
| Growing | `n=16` | 16 | 0.6848 | +31.52% | 20/20 TW | 0 | 2.22e-16 | 3/3 |
| Growing | `n=36` | 36 | 0.6806 | +31.94% | 20/20 TW | 0 | 6.66e-16 | 3/3 |
| Growing | `n=64` | 64 | 0.6711 | +32.89% | 20/20 TW | 0 | 4.44e-16 | 3/3 |
| Growing | `n=100` | 100 | 0.6760 | +32.40% | 20/20 TW | 0 | 4.44e-16 | 3/3 |
| Layered cycle | `layers=6,width=3` | 18 | 0.4487 | +55.13% | 20/20 TW | 0 | 4.44e-16 | 3/3 |
| Layered cycle | `layers=6,width=4` | 24 | 0.4356 | +56.44% | 20/20 TW | 0 | 2.22e-16 | 3/3 |
| Layered cycle | `layers=6,width=5` | 30 | 0.4284 | +57.16% | 20/20 TW | 0 | 2.22e-16 | 3/3 |
| Layered cycle | `layers=6,width=6` | 36 | 0.4216 | +57.84% | 20/20 TW | 0 | 2.22e-16 | 3/3 |

## Family Trends

| Family | Mean width ratio | Range | Trend vs size | Force stability | Norm max drift |
|---|---:|---:|---|---|---:|
| Random geometric | 0.6852 | 0.6026 - 0.8800 | slope `-2.773e-03`, corr `-0.773` | 20/20 TW at all sizes | 8.88e-16 |
| Growing | 0.6781 | 0.6711 - 0.6848 | slope `-1.172e-04`, corr `-0.723` | 20/20 TW at all sizes | 6.66e-16 |
| Layered cycle | 0.4336 | 0.4216 - 0.4487 | slope `-1.472e-03`, corr `-0.986` | 20/20 TW at all sizes | 4.44e-16 |

## Readout

- **Inward proxy stability** is strong on all three families.
- **Norm** stays machine-clean everywhere.
- **Contraction** is topology-sensitive but now clearly present on every
  family:
  - layered cycle contracts most strongly and consistently
  - growing contracts moderately and stably
  - random geometric contracts strongly enough that the larger sizes are all
    well below unity

## Interpretation

The retained self-gravity effect is real, and the corrected parity coupling
strengthens contraction across all three graph families. The strongest and
cleanest contraction still appears on the layered cycle family, but the random
geometric and growing families are no longer near-unity edge cases.

That makes this a genuine scaling probe rather than a universal contraction
claim.
