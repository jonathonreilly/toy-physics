# Cycle-Bearing Break Frontier Note

**Date:** 2026-04-10  
**Script:** `frontier_staggered_cycle_break_frontier.py`

## Purpose

This note freezes the first honest larger-graph break frontier for the retained
staggered cycle battery.

The retained cycle battery itself is still frozen separately in:

- [`CYCLE_BATTERY_NOTE_2026-04-10.md`](./CYCLE_BATTERY_NOTE_2026-04-10.md)
- [`CYCLE_BATTERY_SCALED_NOTE_2026-04-10.md`](./CYCLE_BATTERY_SCALED_NOTE_2026-04-10.md)

This frontier map asks a different question:

- how far does the retained battery survive when the graphs get larger?
- where is the first real failure once we push beyond benign retained graphs?

## Larger Retained Sweep

The retained battery does **not** break on size alone through side `18`
(`324` nodes) on the three admissible cycle-bearing families.

| Family | side=14 | side=16 | side=18 |
|---|---:|---:|---:|
| Random geometric | `9/9` | `9/9` | `9/9` |
| Growing | `9/9` | `9/9` | `9/9` |
| Layered cycle | `9/9` | `9/9` | `9/9` |

Representative frontier values at `side=18`:

- Random geometric: `J_span=4.3838e-05`, `G_eff=32.9`, `spectral_ratio=0.368`
- Growing: `J_span=8.9831e-05`, `G_eff=968.8`, `spectral_ratio=0.032`
- Layered cycle: `J_span=5.0942e-04`, `G_eff=10.4`, `spectral_ratio=0.465`

## First Honest Failure

The first clean break frontier appears on the larger random-geometric family
when dense cross-color shortcuts are added.

Boundary sweep on random geometric:

| side | extra shortcuts | score | `J_span` | gauge |
|---|---:|---:|---:|---|
| `14` | `4` | `9/9` | `2.1718e-05` | PASS |
| `14` | `5` | `9/9` | `3.7174e-06` | PASS |
| `16` | `5` | `9/9` | `4.3364e-05` | PASS |
| `18` | `4` | `9/9` | `2.1718e-05` | PASS |
| `18` | `5` | `8/9` | `6.6346e-07` | FAIL |

The first failure is therefore:

- `random_geometric`, `side=18`, `extra=5`
- score drops from `9/9` to `8/9`
- the failing row is native gauge closure
- `J_span` collapses below the retained threshold

## Family Comparison At The Same Boundary

The same dense-shortcut perturbation does **not** break the other tested
cycle-bearing families at `side=18`:

- Growing, `extra=5`: `9/9`, `J_span=1.0135e-05`, PASS
- Layered cycle, `extra=5`: `9/9`, `J_span=4.6913e-06`, PASS

So the frontier is family-specific:

- random geometric is the first to lose native gauge under shortcut density
- growing and layered cycle remain retained at the same perturbation level

## Interpretation

The retained force-first rows remain stable at the frontier:

- Born
- linearity
- additivity
- force sign
- iterative stability
- norm
- family robustness
- force-gap characterization

The first honest break is a **native gauge/current collapse**, not a force
sign failure. That keeps the reading consistent with the retained battery:

- force-first physics survives larger size
- the boundary shows up in gauge/current closure under shortcut density
- B9 remains characterization only, with the Poisson-scale gap unchanged in
  sign and stability

## Takeaway

The frozen side `8/10/12` sibling was not the end of the story, but raw size
alone is still not enough to break the retained battery.

The first real larger-graph frontier is:

- **random geometric, side=18, dense shortcuts = 5**
- `8/9`, with native gauge failing

That is the boundary to use in future work.
