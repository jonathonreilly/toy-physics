# Source-Resolved Generated Support + Mass Scaling

**Date:** 2026-04-05  
**Status:** bounded partial recovery on the compact generated DAG family, but
not a mass-scaling closure

## Artifact chain

- [`scripts/source_resolved_generated_support_mass_scaling.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_generated_support_mass_scaling.py)
- [`logs/2026-04-05-source-resolved-generated-support-mass-scaling.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-generated-support-mass-scaling.txt)

## Question

Does the retained compact generated-family support-recovery tweak also restore
the weak-field mass-scaling class?

This probe stays deliberately narrow:

- compact generated 3D DAG family
- one connectivity-side tweak: next-layer `k`-nearest floor augmentation
- one self-consistent Green readout
- one support metric: detector effective support `N_eff`
- one mass-scaling observable: centroid-shift exponent across source strength

## Frozen result

The frozen probe uses:

- family seeds `0..3`
- `N_LAYERS = 16`
- `NODES_PER_LAYER = 24`
- `CONNECT_RADIUS = 3.2`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- Green kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.50`
- field target max `0.02`
- connectivity tweak:
  - baseline adjacency plus next-layer `k`-nearest floor augmentation
  - `k_nearest = 3`
  - `min_edges = 5`

Zero-source sanity:

- baseline max `|zero-source shift| = 0.000e+00`
- tweak max `|zero-source shift| = 0.000e+00`

Aggregated detector / scaling readout:

| case | centroid shift | sign rows | `N_eff` | fitted exponent |
| --- | ---: | ---: | ---: | ---: |
| baseline generated family | `-4.357340e-02` | `0/4` TOWARD | `2.66` | `-0.299` |
| baseline + `kNN` floor | `+3.850909e-01` | `2/4` TOWARD | `5.25` | `-0.152` |

## Safe read

The connectivity tweak does recover something on the compact generated family:

- detector support broadens by `N_eff`
- the aggregated centroid sign moves back toward `TOWARD`

But the mass-scaling class does **not** recover:

- the fitted centroid-shift exponent remains far from the retained linear class
- the baseline and tweak both sit in a non-Newtonian regime on this family
- the tweak improves breadth and sign, not the weak-field mass-law

## Honest limitation

This is still not a full generated-family transfer of the exact-lattice Green
pocket.

The remaining concentration metrics are still strong, and the source-response
scaling is not linear.

## Branch verdict

Treat this as a real partial recovery:

- baseline generated family is still localized and `AWAY`
- one simple connectivity-side modification partially broadens support
- the centroid moves back toward `TOWARD`
- but the weak-field mass-scaling class does not come back
- so this is a support/sign rescue, not a generated-family closure
