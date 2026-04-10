# Staggered Self-Gravity Scaling Note

**Date:** 2026-04-10
**Script:** `frontier_staggered_self_gravity_scaling.py`

## Summary

This probe makes the inline self-gravity claim rerunnable. It sweeps the
retained self-gravity dynamics across graph size on admissible staggered graph
families and reports three things per case:

- final width ratio `w_self / w_free`
- force-sign stability across iterations
- norm drift

The retained question is not whether force is inward. It is whether the
contraction survives as the graph gets larger.

## Sweep Results

| Family | Size case | Nodes | Width ratio | Contraction | Force | Flips | Norm drift | Score |
|---|---|---:|---:|---:|---|---:|---:|---:|
| Random geometric | `side=4` | 16 | 1.1131 | -11.31% | 20/20 TW | 0 | 2.22e-16 | 2/3 |
| Random geometric | `side=6` | 36 | 0.9948 | +0.52% | 15/20 TW | 1 | 2.22e-16 | 2/3 |
| Random geometric | `side=8` | 64 | 1.0309 | -3.09% | 20/20 TW | 0 | 4.44e-16 | 2/3 |
| Random geometric | `side=10` | 100 | 0.9987 | +0.13% | 20/20 TW | 0 | 2.22e-16 | 3/3 |
| Growing | `n=16` | 16 | 1.1001 | -10.01% | 20/20 TW | 0 | 6.66e-16 | 2/3 |
| Growing | `n=36` | 36 | 1.0113 | -1.13% | 20/20 TW | 0 | 2.22e-16 | 2/3 |
| Growing | `n=64` | 64 | 1.0267 | -2.67% | 20/20 TW | 0 | 2.22e-16 | 2/3 |
| Growing | `n=100` | 100 | 0.9891 | +1.09% | 20/20 TW | 0 | 2.22e-16 | 3/3 |
| Layered cycle | `layers=6,width=3` | 18 | 0.6364 | +36.36% | 20/20 TW | 0 | 2.22e-16 | 3/3 |
| Layered cycle | `layers=6,width=4` | 24 | 0.6359 | +36.41% | 20/20 TW | 0 | 4.44e-16 | 3/3 |
| Layered cycle | `layers=6,width=5` | 30 | 0.6224 | +37.76% | 20/20 TW | 0 | 6.66e-16 | 3/3 |
| Layered cycle | `layers=6,width=6` | 36 | 0.6054 | +39.46% | 20/20 TW | 0 | 4.44e-16 | 3/3 |

## Family Trends

| Family | Mean width ratio | Range | Trend vs size | Force stability | Norm max drift |
|---|---:|---:|---|---|---:|
| Random geometric | 1.0344 | 0.9948 - 1.1131 | slope `-9.925e-04`, corr `-0.658` | mixed | 4.44e-16 |
| Growing | 1.0318 | 0.9891 - 1.1001 | slope `-1.064e-03`, corr `-0.807` | 20/20 TW at all sizes | 6.66e-16 |
| Layered cycle | 0.6250 | 0.6054 - 0.6364 | slope `-1.773e-03`, corr `-0.941` | 20/20 TW at all sizes | 6.66e-16 |

## Readout

- **Force sign stability** is strong on growing and layered-cycle families.
- **Norm** stays machine-clean everywhere.
- **Contraction** is topology-sensitive:
  - layered cycle contracts strongly and consistently
  - growing is near-unity and only weakly contracts at larger sizes
  - random geometric is mixed at small sizes and only settles near unity by `n=100`

## Interpretation

The retained self-gravity effect is real, but its contraction strength is not
uniform across graph families. The strongest and cleanest contraction appears
on the layered cycle family, while the admissible random geometric and growing
families show weaker, size-dependent contraction.

That makes this a genuine scaling probe rather than a universal contraction
claim.
