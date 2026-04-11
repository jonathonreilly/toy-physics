# Staggered Two-Body Flux and Mid-Plane Current Observables

**Date:** 2026-04-11
**Script:** `scripts/frontier_staggered_two_body_flux_observables.py`
**Status:** Observable 1 marginal (66.7%), Observable 2 fails (0%)

## Context

Centroid-based observables for the staggered two-body lane have been ruled out:
blocked-centroid packet-level splits show opposite signs, 26% drift, and 100%
force-balance failure. Detector-side transfer was also negative. This probe
moves to graph-native transport observables: probability current on edges.

## Observables

### Observable 1: Local Momentum Flux (packet shell)

For each packet, sum the probability current J_{ij} = -2 Im(conj(psi_i) H_{ij} psi_j)
over edges crossing a shell of radius 1.2 sigma around the packet center. Compare
shared-field evolution vs self-only control. Acceptance: delta_flux inward for both
packets on the same row.

### Observable 2: Mid-Plane Probability Current

Sum J_{ij} over edges crossing the plane at x = midpoint between the two packets.
Compare shared vs self-only. Acceptance: all 5 early-time steps have consistent
sign for delta_mid = J_mid(shared) - J_mid(self_only).

## Parameters

| Parameter | Value |
|-----------|-------|
| MASS | 0.30 |
| G | 50.0 |
| MU2 | 0.001 |
| DT | 0.08 |
| N_STEPS | 8 |
| SIGMA | 0.80 |
| sides | 12, 14, 16 |
| distances | 3, 4, 5, 6, 7 |
| placements | centered, face_offset, corner_offset |

## Results

### Reference: Exact partner-force

45/45 rows attractive (100%). The force itself remains clean.

### Observable 1: Packet Shell Flux

**Overall:** 30/45 pass the both-inward gate (66.7%) -- MARGINAL.

Breakdown by lattice size:
- side=12: 0/15 pass (delta_flux_A is negative on all rows)
- side=14: 15/15 pass
- side=16: 15/15 pass

All three placements show the same 10/15 pattern (the failing rows are exactly
the side=12 family). This is consistent with a boundary artifact: the side=12
lattice is too small for the shell measurement to be clean. Packets at distance
3-7 on a 12-site lattice leave very little room between the shell boundary and
the lattice edge.

Power-law fits on passing rows are poor: R2 ~ 0.02 for both delta_flux_A and
delta_flux_B vs distance. The flux magnitudes do not track the 1/r^2 force law.

### Observable 2: Mid-Plane Probability Current

**Overall:** 0/45 pass the sign-consistency gate -- FAIL.

The delta_mid values are extremely small (order 1e-6 to 1e-3) and flip sign
within the 5-step early window on every row. The mid-plane current is too noisy
relative to signal to serve as a reliable observable. The mid-plane sits in a
symmetric location where A's rightward current and B's leftward current partially
cancel, leaving a tiny residual that is dominated by numerical noise.

## Assessment

| Observable | Gate | Verdict |
|------------|------|---------|
| Packet shell flux | 66.7% both-inward | MARGINAL (clean on side >= 14, fails on side=12) |
| Mid-plane current | 0% sign-consistent | FAIL (signal below noise floor) |

The packet shell flux shows real signal on adequately sized lattices: the shared
field systematically draws probability inward relative to self-only evolution.
However, the effect does not scale cleanly with distance (poor power-law fit),
and the side=12 failures indicate sensitivity to boundary conditions.

The mid-plane current is not viable. The symmetry of the setup forces near-perfect
cancellation at the midplane, leaving only numerical residuals.

## Next Steps

- The packet shell flux could be refined by restricting to side >= 14 and testing
  whether a wider shell radius or directional (x-only edges) measurement improves
  the distance scaling.
- Consider impulse-based observables: integrate the momentum transfer over time
  rather than measuring instantaneous current.
- The mid-plane current as defined here should be abandoned for the symmetric
  two-packet setup.
