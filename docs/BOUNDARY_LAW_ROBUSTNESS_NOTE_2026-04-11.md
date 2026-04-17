# Boundary-Law Robustness Addendum

**Date:** 2026-04-11  
**Status:** supporting robustness note for the bounded boundary-law probe

Primary artifact:
- `/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_boundary_law_robustness.py`

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

Counted BFS-ball surface:
- total configs: `100`
- `R^2 > 0.95`: `100/100`
- `R^2 > 0.99`: `79/100`
- `R^2` range: `0.975520` to `1.000000`
- `R^2` mean ± std: `0.995000 ± 0.006390`

Nontrivial subsets:
- `side >= 8`: `80/80` above `0.95`, min `0.975520`, mean `0.993749`
- `side >= 10`: `60/60` above `0.95`, min `0.975520`, mean `0.993337`

Partition check at `side=10, G=10`:
- BFS-ball: `0.996408 ± 0.001480`, min `0.994763`
- rectangular: `0.982002 ± 0.006375`, min `0.969595`
- random: `0.995118 ± 0.003120`, min `0.989110`

## Caveats

- `20/100` counted fits come from `side=6`, where only `2` radii are available.
  Those are two-point fits, so `R^2 = 1.0` there is automatic.
- The `100/100` figure applies only to the BFS-ball sweep. The partition
  generalization evidence is smaller and separate.
- This is a robustness addendum for the bounded many-body-style boundary-law
  result. It is not, by itself, a holography proof.

## Strongest Honest Claim

On the 2D periodic staggered lattice with small positional jitter, the
Dirac-sea entanglement entropy remains highly linear in boundary size across
the audited BFS-ball surface (`5` sides × `4` couplings × `5` seeds = `100`
fits), with every counted fit above `R^2 = 0.95`. Complementary rectangular
and random partition checks at `side=10, G=10` also stay above `R^2 = 0.95`.
