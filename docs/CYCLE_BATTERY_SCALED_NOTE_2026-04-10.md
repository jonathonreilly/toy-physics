# Cycle-Bearing Graph Battery, Scaled

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-10  
**Script:** `frontier_staggered_cycle_battery_scaled.py`

## Summary

This retained sibling freezes the larger-size claim for the same cycle-bearing
bipartite graph semantics used by the base cycle battery. It inherits the same
family-appropriate source convention as the base battery: growing is anchored
to the deepest reachable node and layered cycle to a max-degree interior node.
The only change is the size sweep:

- random geometric: `side = 8, 10, 12`
- growing: `n_target = side^2`
- layered cycle: `layers = side`, `width = side`

All nine retained runs now pass the same `9/9` battery:

- random geometric: `9/9` at side `8`, `10`, and `12`
- growing: `9/9` at side `8`, `10`, and `12`
- layered cycle: `9/9` at side `8`, `10`, and `12`

| Family | side=8 | side=10 | side=12 |
|-----|:---:|:---:|:---:|
| Random geometric | 9/9 | 9/9 | 9/9 |
| Growing | 9/9 | 9/9 | 9/9 |
| Layered cycle | 9/9 | 9/9 | 9/9 |

## Key Numbers

### Random geometric

- `B4` force: `+1.9243e-02`, `+1.8456e-02`, `+2.0788e-02` TOWARD
- `B5` iterative stability: `15/15` TOWARD at all sizes
- `B8` native gauge: `R²=0.9968`, `0.9943`, `0.9853`
- `B9` force-gap / shell / spectral: characterization only

### Growing

- `B4` force: `+1.0997e-02`, `+2.1029e-03`, `+7.6498e-04` TOWARD
- `B5` iterative stability: `15/15` TOWARD at all sizes
- `B8` native gauge: `R²=0.9867`, `0.9975`, `0.9943`
- `B9` force-gap / shell / spectral: characterization only

### Layered cycle

- `B4` force: `+2.3645e-02`, `+2.5023e-02`, `+2.5740e-02` TOWARD
- `B5` iterative stability: `15/15` TOWARD at all sizes
- `B8` native gauge: `R²=0.9985`, `0.9888`, `0.9877`
- `B9` force-gap / shell / spectral: characterization only

## What This Freezes

- The retained cycle battery is not a small-graph artifact: random geometric,
  growing, and layered cycle all stay `9/9` through side `12`.
- Force remains the primary gravity observable.
- The force-gap row remains characterization only. It does not gate the pass.
- The larger sweep is honest about scale:
  - random geometric and growing keep the same sign/robustness pattern
  - layered cycle keeps the strongest inward force and the cleanest retained
    gauge response at all tested sizes

## Relation To The Base Battery

This note does not replace [`CYCLE_BATTERY_NOTE_2026-04-10.md`](./CYCLE_BATTERY_NOTE_2026-04-10.md).
It freezes the larger-size sibling harness:

- same retained rows
- same force-first semantics
- larger graph sizes only

If future work changes the row meanings, this note should be treated as the
larger-size retained snapshot, not a new semantic standard.
