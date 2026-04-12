# Emergent GR Signature Consistency Checks

**Script:** `scripts/frontier_emergent_gr_signatures.py`
**Date:** 2026-04-11
**Status:** review hold; consistency checks only

## Summary

The valley-linear action `S = L(1-f)` on a 3D lattice with Poisson-sourced
field `f ~ s/r` reproduces several weak-field identities of the chosen action.
These checks show consistency with weak-field GR-style structures on this
surface, not an independent derivation of GR.

## Results

### Test 1: Gravitational Time Dilation — CONFIRMED (exact)

Phase accumulation rate = k(1-f). In a gravitational well (f > 0), phase
advances less. The ratio (1-f) matches the Schwarzschild metric component
g_00^{1/2} = (1 - 2GM/rc^2)^{1/2} to first order.

Measured/predicted ratio: 1.000000 +/- 0.000000

**Caveat:** This is exact by construction for S = L(1-f). The non-trivial
content is that the action form matches the GR prediction.

### Test 2: Weak Equivalence Principle — CONFIRMED (exact)

Deflection angle = dS/db is independent of wavenumber k. Tested k = 2 to 16:
relative spread = 0.0000%. All test particles follow the same geodesic.

**Caveat:** Exact because S = L(1-f) has no k-dependence. The WEP follows
from the action being a geometric property of paths, not of the propagating
particle.

### Test 3: Emergent Conformal-Metric Proxy — CONSISTENT

Effective metric g_ij = (1-f) delta_ij per lattice step (conformal to flat).
Isotropy verified to < 0.4% anisotropy at all tested radii. Matches weak-field
Schwarzschild in isotropic coordinates: g_ij = (1 + 2Phi/c^2)^2 delta_ij
with identification f = -2Phi/c^2.

Ricci scalar R away from source is O(|grad f|^2), consistent with vacuum GR
where curvature is sourced by the gradient of the potential.

### Test 4: Light Deflection Factor of 2 — CONDITIONAL COMPATIBILITY ONLY

If the spatial metric contributes (1-f) to the path length (conformal factor
on dl), the effective action becomes S_eff = L(1-f)^2, giving deflection
ratio FM/TD = 1.985 +/- 0.012, consistent with the GR factor of 2.

**Important caveat:** The axioms give S = L(1-f). The additional spatial
metric factor requires derivation from the propagator's full structure
(specifically, that the measure over paths includes the conformal path
length). This test shows the framework is *consistent with* GR light
bending, not that it *predicts* it without additional input.

## What is and is not claimed

**Claimed (bounded):**
1. `S = L(1-f)` reproduces the model's own time-dilation and k-independence
   identities exactly on this surface.
2. The tested isotropy and conformal-metric proxy are consistent with a
   weak-field GR-style reading, but are not an independent metric derivation.
3. The framework is *compatible with* the GR factor-of-2 light bending if an
   additional spatial-metric contribution is justified separately.

**Not claimed:**
- The factor-of-2 is not an independent prediction from the two axioms alone.
- The spatial metric contribution (1-f on path length) requires separate
  derivation.
- Tests 1 and 2 are exact consequences of the chosen action, not independent
  confirmations of GR.
- Strong-field GR effects (horizons, frame dragging, gravitational waves)
  are not tested here.
- The identification f = 2GM/rc^2 requires knowing the normalization of
  the Poisson source, which involves the growth rule details.

## Lattice details

- 3D ordered cubic lattice, N=31 (29,791 sites)
- Poisson solver: scipy sparse direct (Dirichlet BC)
- Field: s=1.0 point source at center
- Wavenumber: k=4.0 (except WEP test which sweeps k)
- Boundary effects: ~50% on f*r product at r=7 due to Dirichlet BC
  on small grid. Physics tests use differential quantities that cancel
  the smooth boundary offset.
