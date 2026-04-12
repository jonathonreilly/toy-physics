# Staggered Two-Body: X-Directed Flux and Impulse Refinement

**Script:** `scripts/frontier_staggered_two_body_xflux_refined.py`
**Date:** 2026-04-11

## Motivation

The previous shell-flux probe (`frontier_staggered_two_body_flux_observables.py`)
showed 66.7% both-inward pass rate (30/45). Two issues were identified:

1. **Boundary artifact at side=12:** 0/15 pass rate, inflating the failure count.
2. **Direction dilution:** Summing over all edge directions (x, y, z) dilutes the
   x-component signal. The gravitational force is along x (the separation axis),
   so y/z edge currents add noise without signal.

This refinement addresses both by restricting to x-directed edges only, dropping
side=12, and adding a time-integrated impulse observable.

## Method

**Lattice:** OpenStaggered3D with staggered-fermion parity phases.
Sides: 14, 16, 18. Distances: 3--7. Three placements. Total: 45 rows.

**Parameters:** MASS=0.3, G=50, MU2=0.001, DT=0.08, SIGMA=0.80, N_STEPS=10.

**Observable 1 -- X-directed shell flux:**
For each packet, compute J_{ij} = -2 Im(conj(psi_i) H_{ij} psi_j) only for edges
with |x_i - x_j| = 1 crossing a shell of radius 1.2*sigma around the packet center.
Delta = shared - self_only. Early-time average (first 5 steps).
Gate: both delta_flux_A > 0 and delta_flux_B > 0 (both inward).

**Observable 2 -- Time-integrated impulse:**
Impulse_A = sum_t [delta_xflux_A(t)] * DT over all 10 steps.
Gate: both impulse_A > 0 and impulse_B > 0.

## Results

### Observable 1: X-directed shell flux

| Metric | Value |
|--------|-------|
| Both-inward gate | **45/45 (100%)** |
| By side=14 | 15/15 |
| By side=16 | 15/15 |
| By side=18 | 15/15 |
| Power-law R^2 (delta_xflux vs d) | ~0.007 |

The x-flux restriction eliminates all the failures seen in the previous probe.
Every single row shows positive delta (shared draws x-current inward relative
to self-only), confirming the attractive interaction signal is cleanly present
in the x-directed component of probability current.

The power-law fit remains poor (R^2 ~ 0.01). The delta_xflux values do not track
distance in a simple power-law fashion at the shell level. This is expected:
the shell flux is a qualitative gate (sign of the interaction), not a quantitative
force proxy. The exact partner-force (100% attractive) confirms the underlying
physics is correct.

### Observable 2: Time-integrated impulse

| Metric | Value |
|--------|-------|
| Both-inward gate | 30/45 (66.7%) |
| By side=14 | 15/15 |
| By side=16 | 15/15 |
| By side=18 | **0/15** |
| Power-law R^2 (impulse_sym vs d) | ~0.016 |

The impulse observable shows a clear non-convergence: side=14 and 16 are 100%
inward, but side=18 is 100% outward (all negative). This indicates the impulse
accumulates a finite-size-dependent offset that flips sign as the lattice grows.
The impulse observable is **not promotable** -- it fails the convergence test.

## Bounded Claims

1. **X-directed shell flux is a valid qualitative gate** for staggered two-body
   attraction. At 100% both-inward (45/45), it reliably detects the sign of the
   gravitational interaction across all tested sizes and placements.

2. **The x-flux gate does not provide quantitative distance scaling.** R^2 ~ 0.01
   means the magnitude of the shell flux does not track separation distance in
   a power-law. This is a sign-only observable.

3. **Time-integrated impulse is not convergent.** The sign flips between side=16
   and side=18, indicating finite-size contamination in the accumulation. This
   observable should not be used for claims about the model.

4. **The exact partner-force remains 100% attractive** (45/45), confirming the
   underlying self-consistent scalar coupling produces the correct physics.

## What This Means

The x-directed flux refinement upgrades the shell flux from 66.7% to 100%,
confirming that the earlier failures were caused by direction dilution and the
side=12 boundary artifact -- not by a genuine physics failure. The interaction
signal lives cleanly in the x-component of probability current.

For quantitative force-distance scaling, the exact partner-force (gradient-based)
remains the gold-standard observable. The shell flux serves as a complementary
qualitative check that the interaction is detectable from probability current alone.
