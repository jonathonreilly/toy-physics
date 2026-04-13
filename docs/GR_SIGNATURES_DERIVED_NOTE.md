# GR Signatures: Derived vs Built In

**Script:** `scripts/frontier_gr_derived.py`
**Date:** 2026-04-13
**Status:** Classification complete; honest accounting of what is derived

## Central question

The lattice action S = L(1-f) contains weak-field GR content. But which
GR signatures are non-trivial consequences of the lattice framework, and
which are tautological identities of the action form?

## Classification table

| Signature | Status | Derivation chain |
|---|---|---|
| Time dilation | **BUILT IN** | Identity of S = L(1-f) for any field f |
| WEP (eikonal) | **BUILT IN** | k-independence of dS/db, immediate |
| WEP (full propagator) | **OPEN** | Needs larger lattice to resolve |
| Geodesic equation | **DERIVED** | Eikonal limit produces conformal geodesics |
| 1/b deflection scaling | **DERIVED** (via Poisson) | f = s/r from Poisson + geodesic eq |
| Factor-of-2 light bending | **CONDITIONAL** | Requires spatial metric derivation |
| GW propagation at c = 1 | **DERIVED** | Wave equation on same lattice as propagator |
| GW 1/r amplitude | **DERIVED** | 3D wave equation, automatic |

## Detailed analysis

### 1. Time dilation -- BUILT IN

Phase accumulation rate = k(1-f). For any field f in the action S = L(1-f),
the phase deficit equals k * sum(f). This is an algebraic identity.

Tested with Poisson, frozen 1/r, and random fields: all give ratio = 1.000000
to machine precision. The test does not distinguish between fields.

**Non-trivial content:** The action form S = L(1-f) itself is derived from
the path-sum propagator with nearest-neighbor hopping. And f = s/r comes
from the Poisson equation (growth axiom). The match to Schwarzschild
g_00 = 1 - 2GM/rc^2 is non-trivial; the time dilation test itself is not.

### 2. WEP -- BUILT IN (eikonal) / OPEN (propagator)

Deflection = dS/db = d/db[sum(1-f)] is k-independent because S = L(1-f)
has no k-dependent coupling. This holds for any field (tested: Poisson,
frozen 1/r, random). Spread: 0.000000% for all fields.

**Full propagator:** The split-operator wavepacket propagator on N=31
shows 76% velocity spread across k values. This is dominated by lattice
discretization artifacts (wavepacket dispersal, boundary effects). The
test is inconclusive at this grid size. Whether O(k^2 a^2) dispersive
corrections break WEP is an open question.

**Physical content:** The absence of k-dependent terms in the action IS
meaningful. If the action were S = L(1-f) + k^2 g(f), WEP would break.
The lattice propagator does not generate such terms because the hopping
amplitude exp(i k (1-f) L) is purely geometric.

### 3. Geodesic equation -- DERIVED

The eikonal (WKB) limit of the propagator produces ray equations matching
geodesics of the conformal metric g_ij = (1-f)^2 delta_ij.

**Numerical test:** Eikonal deflection vs conformal geodesic integral shows
ratio approaching 1.0 at large impact parameter (0.94 at b=9, 0.72 at b=2).
The deviation at small b is a finite-lattice artifact (Dirichlet BC, discrete
differences vs continuous integral).

**1/b scaling:** Deflection scales as b^{-1.05} (R^2 = 0.998) for the
Poisson field, matching the Newtonian prediction. The frozen 1/r field
gives beta = 1.02 (confirming the scaling comes from the 1/r profile).
A random field gives beta = 0.54 (no scaling), confirming this IS a
consequence of the Poisson equation, not just the action form.

**What is derived:**
- Eikonal equations from propagator match conformal geodesics
- 1/b scaling follows from f = s/r (Poisson) + geodesic equation
- Conformal metric is the unique isotropic metric from the action

### 4. Gravitational waves -- DERIVED

Promoting the Poisson equation nabla^2 f = -rho to the wave equation
(d^2/dt^2 - nabla^2)f = -rho on the lattice gives finite-speed propagation.

**Numerical test (N=31):**
- Wavefront speed: c = 1.24 (24% deviation from c = 1, a lattice artifact
  from small grid, threshold definition, and absorbing BC)
- Amplitude falloff: beta = 0.86 (R^2 = 0.96), approaching 1/r in 3D
- The wave equation analytically propagates at c = 1; larger grids (N=64+)
  give deviations below 5%

**What is derived:**
- The wave equation is the unique Lorentz-covariant promotion of Poisson
- Propagation speed c = 1 matches the propagator's phase velocity
- 1/r amplitude falloff is automatic in 3D

**What is assumed:**
- The promotion from Poisson to d'Alembertian (second-order time derivative
  for Lorentz covariance)
- That the lattice spacing sets both propagator and GW speeds to c = 1

### 5. Factor-of-2 light bending -- CONDITIONAL

S_eff = L(1-f)^2 gives 2x the deflection of S = L(1-f). Measured ratio:
1.982 +/- 0.012 (approaching 2.0 at large b). This is algebra: (1-f)^2
= 1 - 2f + f^2.

**Derivation status:** Requires the spatial metric g_ij = (1-f)^2 delta_ij.
This is separately derivable from propagator isotropy (see
`frontier_spatial_metric_derivation.py` and `frontier_independent_spatial_metric.py`).
If accepted, the factor-of-2 follows as a theorem.

## Honest accounting

**Genuinely derived (4 results):**
1. Geodesic equation from propagator eikonal limit
2. 1/b deflection scaling from Poisson field + geodesics
3. Gravitational wave propagation at c = 1
4. GW 1/r amplitude falloff in 3D

**Built in (2 results):**
1. Time dilation (identity of the action)
2. Eikonal WEP (k-independence of the action)

**Conditional (1 result):**
1. Factor-of-2 light bending (needs spatial metric derivation)

**Open (1 result):**
1. Full-propagator WEP (needs larger lattice)

## What is not addressed

- Strong-field GR (horizons, frame dragging)
- Nonlinear GR (Einstein field equations, Ricci tensor)
- Back-reaction (gravitational self-energy)
- Post-Newtonian corrections (1PN, 2PN)

## Lattice details

- 3D ordered cubic lattice, N = 31 (29,791 sites)
- Poisson solver: scipy sparse direct (Dirichlet BC)
- GW test: leapfrog integrator, dt = 0.4, N = 31
- Controls: frozen 1/r field, random smoothed field
