# Source-Resolved Green Robustness Sweep

**Date:** 2026-04-05  
**Status:** bounded local robustness region for the source-resolved exact Green pocket

## Artifact chain

- [`scripts/source_resolved_green_robustness.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_green_robustness.py)
- [`logs/2026-04-05-source-resolved-green-robustness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-green-robustness.txt)
- [`docs/SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md)
- [`docs/SOURCE_RESOLVED_EXACT_GREEN_SCALING_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_EXACT_GREEN_SCALING_NOTE.md)

## Question

Is the source-resolved Green pocket just a tuned point, or does it have a real
local neighborhood of nearby kernels and source-cluster shapes that still
passes the hard gates?

This sweep stays deliberately small:

- same exact lattice family as the retained pocket
- a local kernel neighborhood around the retained `(mu, eps)` choice
- a local source-cluster neighborhood around the retained cross cluster
- the same source-strength ladder and detector readout as the pocket

## Frozen result

The frozen sweep uses:

- exact 3D lattice with `h = 0.5`, `W = 3`, `L = 20`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- target max `|f| = 0.02`

Kernel neighborhood:

| `mu` | `eps` | `TOWARD` | `F~M` | `|green/inst|` | status |
| ---: | ---: | ---: | ---: | ---: | --- |
| `0.04` | `0.25` | `4/4` | `1.002` | `0.973` | PASS |
| `0.04` | `0.50` | `4/4` | `1.001` | `1.250` | PASS |
| `0.04` | `0.75` | `4/4` | `1.001` | `1.421` | PASS |
| `0.08` | `0.25` | `4/4` | `1.002` | `0.959` | PASS |
| `0.08` | `0.50` | `4/4` | `1.000` | `1.235` | PASS |
| `0.08` | `0.75` | `4/4` | `0.999` | `1.409` | PASS |
| `0.12` | `0.25` | `4/4` | `1.002` | `0.934` | PASS |
| `0.12` | `0.50` | `4/4` | `0.999` | `1.204` | PASS |
| `0.12` | `0.75` | `4/4` | `0.998` | `1.375` | PASS |

Cluster neighborhood:

| cluster | `TOWARD` | `F~M` | `|green/inst|` | status |
| --- | ---: | ---: | ---: | --- |
| `cross5` | `4/4` | `1.000` | `1.235` | PASS |
| `line3` | `4/4` | `1.002` | `1.213` | PASS |
| `skew4` | `4/4` | `0.999` | `1.134` | PASS |

Safe read:

- exact zero-source reduction survives throughout the tested local neighborhood
- the Green pocket keeps the weak-field `TOWARD` sign throughout the sweep
- the mass-scaling class stays essentially linear throughout the sweep
- the dynamic field remains nontrivial across nearby kernel and cluster choices

## Honest limitation

This is local robustness, not a full self-consistent field theory.

- the sweep stays on the same exact lattice family as the retained pocket
- it does not test generated geometry
- it does not test refinement beyond the exact-family basin

## Branch verdict

Treat this as a real bounded positive:

- the source-resolved exact Green pocket is not a one-off point
- it has a small but real local robustness region
- together with the larger exact-lattice scaling companion, it is the strongest
  current self-generated-field pocket in the moonshot lane
