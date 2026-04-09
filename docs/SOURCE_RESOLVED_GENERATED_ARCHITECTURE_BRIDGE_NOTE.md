# Source-Resolved Generated Architecture Bridge Note

**Date:** 2026-04-05
**Status:** generated-family architecture bridge, not a closure theorem

## Artifact chain

- [`scripts/source_resolved_generated_architecture_bridge.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_generated_architecture_bridge.py)
- [`logs/2026-04-05-source-resolved-generated-architecture-bridge.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-generated-architecture-bridge.txt)

## Question

Can the retained generated-family support-recovery lesson be combined with a
simple field-architecture change to improve the weak-field mass law?

This probe stays deliberately narrow:

- compact generated 3D DAG family
- baseline connectivity versus retained `kNN`-floor support recovery
- static Green field versus a causal parent-averaged field update
- exact zero-source reduction check
- one support metric: detector effective support `N_eff`
- one mass-law metric: centroid-shift exponent across source strength

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
- architecture change:
  - causal parent-averaged field with `mix = 0.70`

Zero-source sanity:

- baseline static max `|zero-source shift| = 0.000e+00`
- baseline causal max `|zero-source shift| = 0.000e+00`
- tweaked static max `|zero-source shift| = 0.000e+00`
- tweaked causal max `|zero-source shift| = 0.000e+00`

Aggregated readout:

| case | centroid shift | sign rows | `N_eff` | fitted exponent |
| --- | ---: | ---: | ---: | ---: |
| baseline static | `+1.673792e-01` | `4/16` TOWARD | `2.69` | `+0.199` |
| baseline causal | `-4.081000e-02` | `3/16` TOWARD | `2.50` | `-0.308` |
| tweak static | `+3.850909e-01` | `9/16` TOWARD | `5.31` | `-0.316` |
| tweak causal | `+4.009000e-01` | `9/16` TOWARD | `5.67` | `+0.444` |

## Safe read

The connectivity lesson survives:

- the baseline generated family remains mixed across seeds and does not give a
  stable weak-field law
- the retained `kNN`-floor tweak broadens detector support
- the centroid sign moves back toward `TOWARD`

The architecture change also helps a little:

- the causal parent-averaged field improves the tweaked-family exponent in the
  aggregate summary
- the support metric broadens further
- the sign count improves on the retained family

## Honest limitation

This is still not a generated-family closure.

- the weak-field mass law does not become cleanly linear on either the baseline
  or tweaked family
- the causal field update improves the retained rescue, but only modestly
- the result is better interpreted as a bridge result than as a new law

## Branch verdict

Treat this as a real but bounded architecture bridge:

- support recovery alone is not enough
- support recovery plus a causal parent-averaged field is better
- the weak-field mass law improves, but does not fully close
- the next real question is whether a stronger propagating-field rule can do
  more than this causal smoothing step
