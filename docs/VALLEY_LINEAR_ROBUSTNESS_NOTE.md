# Valley-Linear Action Robustness Note

**Date:** 2026-04-04
**Status:** exploratory robustness memo pending a dedicated frozen sweep harness

## Action

`S = L(1-f)` — phase valley, linear in field `f`

This note records branch-side sweep results that are scientifically useful, but
it should not yet be read as a fully retained proof of robustness.

At the moment, the missing piece is a dedicated **script + log + note** chain
for the full sweep itself. Until that exists, the same-family comparison in
[`VALLEY_LINEAR_ACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/VALLEY_LINEAR_ACTION_NOTE.md)
is the stronger retained artifact.

## Reported robustness sweeps (all at h=0.5, 3D dense lattice, 1/L^2 kernel)

### Width sweep (L=12, max_d=3)

| W | nodes | Born | d_TV | MI | Decoh | Gravity | F∝M | Tail |
|---|-------|------|------|-----|-------|---------|-----|------|
| 4 | 7,225 | 2.1e-15 | 0.76 | 0.57 | 49.2% | +0.000114 T | 1.00 | n/a |
| 6 | 15,625 | 2.5e-15 | 0.78 | 0.61 | 49.5% | +0.000136 T | 1.00 | n/a |
| 8 | 27,225 | 2.5e-15 | 0.79 | 0.59 | 49.4% | +0.000144 T | 1.00 | -1.46 |
| 10 | 42,025 | 2.2e-15 | 0.79 | 0.57 | 49.4% | +0.000150 T | 1.00 | -1.08 |

### Connectivity sweep (L=12, W=8)

| max_d | Born | d_TV | MI | Decoh | Gravity | F∝M | Tail |
|-------|------|------|-----|-------|---------|-----|------|
| 1 (NN) | 6.9e-16 | 0.91 | 0.83 | 50.0% | +0.000229 T | 1.00 | -0.64 |
| 2 | 1.6e-15 | 0.77 | 0.60 | 48.4% | +0.000165 T | 1.00 | -0.36 |
| 3 | 2.5e-15 | 0.79 | 0.59 | 49.4% | +0.000144 T | 1.00 | -1.46 |

### Length sweep (W=8, max_d=3)

| L | Gravity | F∝M |
|---|---------|-----|
| 8 | +0.000114 T | 1.00 |
| 10 | +0.000133 T | 1.00 |
| 12 | +0.000144 T | 1.00 |
| 15 | +0.000164 T | 1.00 |
| 18 | +0.000178 T | 1.00 |

Gravity monotonically increases with L — persistent and strengthening.

## 2D comparison (branch-side read)

| Action | TOWARD | Tail | F∝M |
|--------|--------|------|-----|
| Valley-linear | 7/7 | b^(-2.27) | 1.00 |
| Spent-delay | 7/7 | b^(-1.08) | 0.45 |

The reported 2D comparison points in the same direction: valley-linear gives a
steeper distance read and linear `F∝M` on the tested slice.

## Mirror DAG transfer (bounded read)

| Action | TOWARD (8 seeds) |
|--------|-----------------|
| Spent-delay | 15/21 (71%) |
| Valley-linear | 10/21 (48%) |

The current branch-side read is that valley-linear is lattice-optimized. On the
tested random/mirror DAG slice, spent-delay gives more TOWARD gravity.

## Summary

The strongest safe summary today is:

- the valley-linear lane looks **promisingly robust** on the tested lattice
  parameter slices
- the branch-side sweeps report `F∝M = 1.00` and machine-clean Born across the
  tested rows
- the same branch-side memo also reports that the action does **not** transfer
  as well to mirror/random DAGs

What is **not** retained from this note yet:

- “robust across all parameter variations” as a canonical theorem
- “works across architectures”
- “the action choice is fully settled”

That stronger wording should wait for a dedicated frozen sweep harness and a
separate frozen transfer test.
