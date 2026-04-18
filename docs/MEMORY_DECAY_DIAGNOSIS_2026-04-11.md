# Memory Signal Decay — Root Cause: Yukawa Screening

**Date:** 2026-04-11

## The Data
  N=41:  memory = +0.47 (strong — lattice within screening range)
  N=61:  memory = +0.013 (original result)
  N=81:  memory ~ 1e-5 (vanishing)
  N=101: memory ~ 1e-7 (gone)

## Root Cause: Yukawa screening mass μ=0.22

Screening length = 1/μ ≈ 4.5 sites. Markers at distance ~N/4:

| N | marker distance | exp(-μ·d) | exp(-2μ·d) |
|---|----------------|-----------|------------|
| 41 | ~10 | 0.11 | 0.012 |
| 61 | ~15 | 0.037 | 0.0014 |
| 81 | ~20 | 0.012 | 0.00015 |
| 101 | ~25 | 0.004 | 0.000016 |

Memory is quadratic in Φ, so it decays as exp(-2μd). The observed
7-order-of-magnitude drop from N=41 to N=101 matches this scaling.

Damping (γ=0.05) adds secondary suppression: exp(-γd/2c) ≈ 0.54
at d=25. Minor compared to Yukawa.

## Assessment

The N=41 signal is a FINITE-SIZE ARTIFACT. The entire ring (max
distance 20 sites) is within a few screening lengths. This creates
artificially strong field everywhere.

Genuine gravitational memory requires the signal to STABILIZE with
increasing N. Exponential decay to zero is the signature of screening.

## Fix

Set μ=0 (massless graviton). This eliminates exponential screening.
The 1D wave equation without mass has no attenuation — the pulse
propagates without decay. Memory should then be N-independent.

The memory result should be DOWNGRADED from the historical `bounded-retained` label to
exploratory/finite-size artifact until tested with μ=0.
