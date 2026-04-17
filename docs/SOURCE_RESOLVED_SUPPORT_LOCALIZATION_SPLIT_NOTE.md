# Source-Resolved Support Localization Split

**Date:** 2026-04-05  
**Status:** bounded mechanistic split for why exact Green pockets survive while generated geometry fails

## Artifact chain

- [`scripts/source_resolved_support_localization_split_probe.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_support_localization_split_probe.py)
- [`logs/2026-04-05-source-resolved-support-localization-split-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-support-localization-split-probe.txt)

## Question

Why does the exact-lattice Green/self-consistent pocket survive while the compact generated family fails?

This split probe stays deliberately narrow:

- exact lattice, `h = 0.25`
- compare the retained clipped source placement against an interior source placement
- compare both exact cases against the compact generated family
- measure one mechanistic culprit only: detector support localization

## Frozen result

The frozen probe uses:

- exact lattice family:
  - `h = 0.25`, `W = 3`, `L = 6`
  - source strength `s = 0.004`
  - two source placements:
    - clipped: `source_z = 3.0`
    - interior control: `source_z = 2.5`
- generated family:
  - `4` seeds
  - `16` layers
  - `24` nodes/layer
  - `connect_radius = 3.2`
  - same source strength

Support metrics were read on the detector layer using the self-consistent Green field:

| case | source nodes | centroid shift | `N_eff` | `N_eff/N_det` | top-10 fraction | `supp(>=1% peak)` | peak share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| exact-clipped | `4` | `+1.505023e-02` | `497.63` | `0.796` | `0.044` | `1.000` | `0.005` |
| exact-centered | `5` | `+1.767362e-02` | `497.66` | `0.796` | `0.044` | `1.000` | `0.005` |
| generated-mean | `4` | `-8.440598e-02` | `2.51` | `0.104` | `0.496` | `0.311` | `0.255` |

## Safe read

The split is clean:

- exact clipped and exact interior are essentially identical in detector support
- source clipping is therefore **not** the main explanation
- generated geometry collapses detector support dramatically
- the generated family concentrates the detector probability into a very small subset of nodes

## Honest limitation

This probe does not prove the full causal mechanism.

The strongest bounded inference is:

- exact lattices sustain broad downstream detector support
- compact generated geometry strongly localizes the support
- the failure is therefore much more consistent with **connectivity / detector support localization** than with source-cluster clipping

## Branch verdict

Treat this as a real mechanistic split:

- exact support is broad and stable under the clipping control
- generated support is sharply localized
- the retained Green/self-consistent pocket likely depends on broad downstream connectivity support that the generated family does not provide
