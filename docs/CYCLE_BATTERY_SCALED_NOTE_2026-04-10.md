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

Five of the nine retained runs pass the same `9/9` battery. The current
miss pattern is:

- random geometric: `9/9` at side `8`, `10`, and `12`
- growing: `8/9` at side `8`, then `9/9` at side `10` and `12`
- layered cycle: `8/9` at side `8`, `10`, and `12`

| Family | side=8 | side=10 | side=12 |
|-----|:---:|:---:|:---:|
| Random geometric | 9/9 | 9/9 | 9/9 |
| Growing | 8/9 | 9/9 | 9/9 |
| Layered cycle | 8/9 | 8/9 | 8/9 |

## Key Numbers

### Random geometric

- `B4` force: `+1.9243e-02`, `+1.8456e-02`, `+2.0788e-02` TOWARD
- `B5` iterative stability: `15/15` TOWARD at all sizes
- `B8` native gauge: `R²=0.9968`, `0.9943`, `0.9853`
- `B9` force-gap / shell / spectral:
  - `G_eff = 60.3, 61.7, 57.7`
  - `shell_grad_ratio = 0.019, 0.020, 0.020`
  - `spectral_ratio(modes1-5) = 0.249, 0.288, 0.323`

### Growing

- `B4` force: `+8.9185e-04`, `+9.5717e-04`, `+3.9630e-04` TOWARD
- `B5` iterative stability: `15/15` TOWARD at all sizes
- `B8` native gauge: `R²=0.9867`, `0.9975`, `0.9943`
- `B9` force-gap / shell / spectral:
  - `G_eff = 319.3, 79.9, 176.7`
  - `shell_grad_ratio = 0.004, 0.003, 0.002`
  - `spectral_ratio(modes1-5) = 0.075, 0.052, 0.057`

### Layered cycle

- `B4` force: `+6.0615e-02`, `+6.1627e-02`, `+6.1735e-02` TOWARD
- `B5` iterative stability: `15/15` TOWARD at all sizes
- `B8` native gauge: `R²=0.9985`, `0.9888`, `0.9877`
- `B9` force-gap / shell / spectral:
  - `G_eff = 28.0, 27.6, 27.5`
  - `shell_grad_ratio = 0.045, 0.045, 0.045`
  - `spectral_ratio(modes1-5) = 0.332, 0.381, 0.413`

## What This Freezes

- The retained cycle battery is not a small-graph artifact: random geometric
  stays `9/9` through side `12`, growing recovers from an `8/9` side-`8`
  linearity miss to `9/9` at side `10` and `12`, and layered cycle
  consistently exposes the same `8/9` linearity miss.
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
