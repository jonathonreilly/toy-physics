# Source-Resolved Generated Support Recovery Note

**Date:** 2026-04-05  
**Status:** bounded partial recovery on the compact generated DAG family

## Artifact chain

- [`scripts/source_resolved_generated_support_recovery.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_generated_support_recovery.py)
- [`logs/2026-04-05-source-resolved-generated-support-recovery.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-generated-support-recovery.txt)

## Question

Can one simple connectivity-side modification partially recover broad downstream
detector support on the compact generated DAG family without broad tuning?

This probe stays deliberately narrow:

- compact generated 3D DAG family
- one connectivity-side tweak: next-layer `k`-nearest floor augmentation
- one source-resolved self-consistent Green readout
- one detector-side question: does support broaden, and does the centroid sign
  stay in the retained weak-field direction?

## Frozen result

The frozen probe uses:

- family seeds `0..3`
- `N_LAYERS = 16`
- `NODES_PER_LAYER = 24`
- `CONNECT_RADIUS = 3.2`
- source strength `s = 0.004`
- Green kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.50`
- field target max `0.02`
- connectivity tweak:
  - baseline adjacency plus next-layer `k`-nearest floor augmentation
  - `k_nearest = 3`
  - `min_edges = 5`

Zero-source sanity:

- baseline max `|zero-source shift| = 0.000e+00`
- tweak max `|zero-source shift| = 0.000e+00`

Aggregated detector readout:

| case | centroid shift | sign | `N_eff` | `N_eff/N_det` | top-10 fraction | `supp(>=1% peak)` | peak share |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| baseline generated family | `-4.357340e-02` | `AWAY` | `2.77` | `0.115` | `0.494` | `0.311` | `0.234` |
| baseline + `kNN` floor | `+3.850909e-01` | `TOWARD` | `6.00` | `0.250` | `0.975` | `0.458` | `0.439` |

Sign counts:

- baseline: `1/4` TOWARD
- tweak: `3/4` TOWARD

## Safe read

The connectivity tweak does recover something on the compact generated family:

- detector support broadens modestly by `N_eff`
- support above the `1%` peak threshold increases
- centroid sign flips back to `TOWARD` on the aggregated readout

## Honest limitation

This is still not a full transfer of the exact-lattice Green pocket.

The remaining concentration metrics are still strong:

- top-10 fraction stays high
- peak share remains large

So the tweak improves breadth and sign, but the detector distribution is still
substantially localized.

## Branch verdict

Treat this as a real partial recovery:

- baseline generated family is still localized and `AWAY`
- one simple connectivity-side modification partially broadens support
- the centroid moves back to `TOWARD`
- but the detector is still not broadly delocalized enough to call this a full
  generated-family transfer

