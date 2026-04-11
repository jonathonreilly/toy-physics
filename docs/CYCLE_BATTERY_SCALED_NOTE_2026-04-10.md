# Cycle-Bearing Graph Battery, Scaled

**Date:** 2026-04-10  
**Script:** `frontier_staggered_cycle_battery_scaled.py`

## Summary

This retained sibling freezes the larger-size claim for the same cycle-bearing
bipartite graph semantics used by the base cycle battery. The only change is
the size sweep:

- random geometric: `side = 8, 10, 12`
- growing: `n_target = side^2`
- layered cycle: `layers = side`, `width = side`

Eight of the nine retained runs pass the same `9/9` battery; the layered
cycle family now scores `8/9` because the B2 linearity row fails at the
corrected parity coupling.

| Family | side=8 | side=10 | side=12 |
|-----|:---:|:---:|:---:|
| Random geometric | 9/9 | 9/9 | 9/9 |
| Growing | 9/9 | 9/9 | 9/9 |
| Layered cycle | 8/9 | 8/9 | 8/9 |

## Key Numbers

### Random geometric

- `B4` force: `+1.6128e-02`, `+1.6521e-02`, `+1.7888e-02` TOWARD
- `B5` iterative stability: `15/15` TOWARD at all sizes
- `B8` native gauge: `R²=0.9968`, `0.9943`, `0.9853`
- `B9` force-gap / shell / spectral:
  - `G_eff = 16.7, 33.3, 18.6`
  - `shell_grad_ratio = 0.019, 0.020, 0.020`
  - `spectral_ratio(modes1-5) = 0.249, 0.288, 0.323`

### Growing

- `B4` force: `+7.1046e-04`, `+9.2542e-04`, `+3.7483e-04` TOWARD
- `B5` iterative stability: `15/15` TOWARD at all sizes
- `B8` native gauge: `R²=0.9867`, `0.9975`, `0.9943`
- `B9` force-gap / shell / spectral:
  - `G_eff = 201.4, 375.2, 431.3`
  - `shell_grad_ratio = 0.004, 0.003, 0.002`
  - `spectral_ratio(modes1-5) = 0.075, 0.052, 0.057`

### Layered cycle

- `B4` force: `+4.6572e-02`, `+4.7450e-02`, `+4.7645e-02` TOWARD
- `B5` iterative stability: `15/15` TOWARD at all sizes
- `B8` native gauge: `R²=0.9985`, `0.9888`, `0.9877`
- `B9` force-gap / shell / spectral:
  - `G_eff = 10.7, 10.6, 10.5`
  - `shell_grad_ratio = 0.045, 0.045, 0.045`
  - `spectral_ratio(modes1-5) = 0.332, 0.381, 0.413`

## What This Freezes

- The retained cycle battery is not a small-graph artifact: random geometric
  and growing keep the same `9/9` semantics at side `8`, `10`, and `12`, while
  layered cycle consistently exposes the same `8/9` linearity miss.
- Force remains the primary gravity observable.
- The force-gap row remains characterization only. It does not gate the pass.
- The larger sweep is honest about scale:
  - random geometric and growing keep the same sign/robustness pattern
  - layered cycle keeps the strongest inward force and the cleanest retained
    gauge response at all tested sizes, but the B2 linearity miss persists

## Relation To The Base Battery

This note does not replace [`CYCLE_BATTERY_NOTE_2026-04-10.md`](./CYCLE_BATTERY_NOTE_2026-04-10.md).
It freezes the larger-size sibling harness:

- same retained rows
- same force-first semantics
- larger graph sizes only

If future work changes the row meanings, this note should be treated as the
larger-size retained snapshot, not a new semantic standard.
