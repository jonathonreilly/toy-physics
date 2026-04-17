# Why h=0.125 Fails: Retained Derivation

**Date:** 2026-04-06
**Status:** retained negative — h=0.125 failure is diagnosed and quantified

## Root cause

Three independent mechanisms compound to destroy the signal:

### 1. Boundary leakage accelerates with h

The interior transfer norm T is used to normalize ALL nodes, but boundary
nodes have fewer valid edges. The corner transfer norm is only 44% of
interior T:

| h | T_interior | T_corner | corner/interior |
| ---: | ---: | ---: | ---: |
| 0.500 | 5.081 | 2.458 | 0.484 |
| 0.250 | 5.802 | 2.651 | 0.457 |
| 0.125 | 6.468 | 2.824 | 0.437 |

Boundary nodes retain only 44% of their amplitude per layer instead of 100%.

### 2. Beam width exceeds half the lattice at h=0.125

| h | beam sigma (mid) | W_phys | sigma/W |
| ---: | ---: | ---: | ---: |
| 0.500 | 3.10 | 10.0 | 0.31 |
| 0.250 | 3.06 | 10.0 | 0.31 |
| 0.125 | **6.10** | 10.0 | **0.61** |

At h=0.125, the beam sigma DOUBLES compared to h=0.5. This pushes
amplitude into boundary nodes where it leaks.

The sigma increase is from the finer lattice: more layers (241 vs 61)
means more steps for the beam to spread. The beam width grows as
sqrt(N) ~ sqrt(L/h), so sigma ~ sqrt(1/h). At h=0.125: sigma ~
sqrt(8) * sigma(h=1) ~ 2.8 * sigma(h=1).

### 3. Per-layer probability loss compounds exponentially

| h | nl | retention/layer | P_det |
| ---: | ---: | ---: | ---: |
| 0.500 | 61 | 0.890 | 3.7e-59 |
| 0.250 | 121 | 0.812 | 1.1e-88 |
| 0.125 | 241 | 0.727 | 1.6e-136 |

P_det = (retention)^nl. At h=0.125: 0.727^241 ~ 10^-33.
Combined with geometric spreading: P_det = 1.6e-136.

### 4. The AWAY result is noise

At P_det = 1.6e-136, the centroid measurement has SNR = 0.5 (below
the significance threshold of 3.0). The "AWAY" direction is statistical
noise from the 10^-136 amplitude, not a real physical effect.

## The fix required

Two things would resolve h=0.125:

1. **Per-node T normalization**: use T_i (the actual transfer norm for
   node i, accounting for its boundary position) instead of T_interior.
   This was tested and partially helps (P_det improves from 1e-137 to
   7e-99) but doesn't fully fix it because even the per-node T doesn't
   account for the beam spreading into more boundary nodes.

2. **Wider lattice**: W must scale as sqrt(1/h) to keep sigma/W constant.
   At h=0.125: need W ~ 10 * sqrt(4) = 20. This gives ~25M nodes,
   which is feasible with numpy but slow (~2 hours).

Alternatively: accept h=0.25 as the finest confirmed lattice spacing.
The physics (F~M, Born, gravity, distance law) is well-established at h=0.25.
