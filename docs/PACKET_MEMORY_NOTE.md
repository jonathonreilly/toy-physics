# Packet Memory: Initial Conditions Survive to Detector

**Date:** 2026-04-06
**Status:** retained positive for Tier A (memory), partial for Tier B (shape), Tier C open

## Artifact chain

- [`scripts/packet_memory.py`](../scripts/packet_memory.py)
- [`logs/2026-04-06-packet-memory.txt`](../logs/2026-04-06-packet-memory.txt)

## Question

Does initial-condition information survive propagation to the detector,
and does it carry physical content (gravitational response)?

## Tier A: Packet memory survives — POSITIVE

Overlap at detector (NL=30) for packets at different initial z-offsets:

| offset | overlap with origin | decoherent? |
| ---: | ---: | --- |
| 0 | 0.99 | no |
| 1 | 0.83 | no |
| 2 | 0.42 | YES |
| 3 | 0.18 | YES |
| 8 | 0.12 | YES |

Packets separated by ≥ 2 lattice units are distinguishable at the detector.

### Memory decays with path length but slowly

| NL | overlap (origin vs z=2) |
| ---: | ---: |
| 15 | 0.19 |
| 25 | 0.36 |
| 30 | 0.42 |
| 40 | 0.56 |

At NL → ∞: overlap → 1 (all memory lost). But at NL=30 there is
still 58% distinguishability.

### Gravity depends on packet identity

| packet | gravitational deflection |
| --- | ---: |
| origin | +0.0151 |
| z=+1 | +0.0102 |
| z=+2 | +0.0051 |
| z=+3 | +0.0002 |
| z=-2 | +0.0107 |

3× variation in gravitational response across packets. Packet identity
carries physics.

## Tier B: Shape partially converges — PARTIAL

Packet width (sigma_z) at detector:

| packet | sigma_z |
| --- | ---: |
| narrow (origin) | 3.01 |
| medium (3x3) | 2.49 |
| offset (z=+2) | 2.98 |

Centroid survives strongly (offset at +1.09 vs origin at -0.09).
Width converges toward propagator natural mode (~3.0) with 17%
residual difference at NL=30.

## Tier C: Inertial response — OPEN

Not yet tested. Would require applying a uniform field to different
packets and measuring whether they accelerate differently.

## Honest read

The model supports "detector-readable packet memory" but not
"persistent localized objects." The centroid is the primary
surviving information. Width converges over long paths. The
persistent-object closure stands for sharp localization, but
the mesoscopic memory lane is open.
