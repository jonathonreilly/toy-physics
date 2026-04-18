# Boundary-Law Robustness Addendum

**Date:** 2026-04-11  
**Status:** supporting robustness note for the bounded boundary-law probe

Primary artifact:
- `/Users/jonreilly/Projects/Physics/scripts/frontier_boundary_law_robustness.py`

Companion retained note:
- [`HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md`](HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md)

## What Was Rerun

Rerun command:

```bash
source /tmp/physics_venv/bin/activate && python scripts/frontier_boundary_law_robustness.py
```

Surface tested by the counted BFS-ball sweep:
- sides: `6, 8, 10, 12, 14`
- couplings: `G = 0, 5, 10, 20`
- seeds: `42, 43, 44, 45, 46`
- total counted BFS-ball fits: `100`

Separate partition check:
- `side = 10`
- `G = 10`
- partitions: BFS-ball, rectangular, random

## Exact Rerun Numbers

This note reflects the current-main minimum-image rerun on the periodic surface.

Counted BFS-ball surface:
- total configs: `100`
- `R^2 > 0.95`: `100/100`
- `R^2 > 0.99`: `78/100`
- `R^2` range: `0.974518` to `1.000000`
- `R^2` mean ± std: `0.994607 ± 0.007004`

Partition check at `side=10, G=10`:
- BFS-ball: `0.995138 ± 0.001668`
- rectangular: `0.994513 ± 0.002123`
- random: `0.995500 ± 0.002903`

## Caveats

- `20/100` counted fits come from `side=6`, where only `2` radii are available.
  Those are two-point fits, so `R^2 = 1.0` there is automatic.
- The `100/100` figure applies only to the BFS-ball sweep. The partition
  generalization evidence is smaller and separate.
- This is the corrected minimum-image periodic rerun; older pre-fix torus
  numbers should not be reused.
- This is a robustness addendum for the bounded many-body-style boundary-law
  result. It is not, by itself, a holography proof.

## Strongest Honest Claim

On the 2D periodic staggered lattice with small positional jitter, the
Dirac-sea entanglement entropy remains highly linear in boundary size across
the audited BFS-ball surface (`5` sides × `4` couplings × `5` seeds = `100`
fits), with every counted fit above `R^2 = 0.95`. Complementary rectangular
and random partition checks at `side=10, G=10` also stay above `R^2 = 0.95`.
