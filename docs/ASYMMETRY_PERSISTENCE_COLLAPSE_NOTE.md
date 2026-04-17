# Asymmetry Persistence + Collapse Note

**Date:** 2026-04-02  
**Status:** bounded pilot complete

## Question

Does the generated asymmetry-persistence geometry remain useful when we add
stochastic collapse?

This pilot compares, on the same dense 3D generated graphs:

- baseline generated geometry
- asymmetry persistence only
- collapse only
- asymmetry persistence + collapse

When feasible, it also compares linear propagation against per-layer
normalization.

Script:
[scripts/asymmetry_persistence_collapse_pilot.py](/Users/jonreilly/Projects/Physics/scripts/asymmetry_persistence_collapse_pilot.py)

Log:
[logs/2026-04-02-asymmetry-persistence-collapse-pilot.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-02-asymmetry-persistence-collapse-pilot.txt)

## Setup

- dense generated 3D graphs
- `N=80` with `npl=50`
- `N=100` with `npl=60`
- thresholds `0.00, 0.10, 0.20`
- `8` matched seeds
- collapse probability `p=0.2`
- `10` Monte Carlo realizations

## Strongest retained rows

### Unitary rows report `pur_min`

| N | threshold | baseline `pur_min` | persistence `pur_min` | layernorm persistence `pur_min` | keep% |
|---|---:|---:|---:|---:|---:|
| 80 | 0.10 | 0.998 | 0.981 | 0.889 | 97.4% |
| 80 | 0.20 | 0.998 | 0.981 | 0.881 | 97.2% |
| 100 | 0.10 | 0.989 | 0.947 | 0.869 | 98.0% |
| 100 | 0.20 | 0.989 | 0.953 | 0.860 | 97.7% |

### Collapse rows report averaged detector purity

| N | threshold | baseline collapse purity | persistence collapse purity | layernorm collapse purity | persistence+collapse LN |
|---|---:|---:|---:|---:|---:|
| 80 | 0.10 | 0.272 | 0.292 | 0.218 | 0.232 |
| 80 | 0.20 | 0.272 | 0.289 | 0.218 | 0.233 |
| 100 | 0.10 | 0.249 | 0.269 | 0.221 | 0.205 |
| 100 | 0.20 | 0.249 | 0.265 | 0.221 | 0.216 |

## Narrow conclusion

The generated asymmetry-persistence geometry remains useful in the unitary
lane: it lowers `pur_min`, and layernorm stacks on top of it at both
`N=80` and `N=100`.

On the collapse side, the same geometry is not a broad win. In the linear
collapse rows it slightly raises detector purity, so it does not clearly
improve decoherence. The only retained collapse-side pocket is narrow:
at `N=100`, `threshold=0.10`, layernorm plus persistence+collapse lowers
collapse purity to `0.205`, below the layernorm-only baseline `0.221`.

So the safe summary is:

- persistence is a real unitary decoherence aid
- collapse is not generically helped by persistence
- there is one narrow `N=100` layernorm-assisted pocket worth keeping
  alive, but not a scalable collapse rescue

