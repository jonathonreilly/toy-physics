# DM Thermodynamic Closure: Continuum Limit Dependency Resolved

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Script:** `scripts/frontier_dm_thermodynamic_closure.py`
**Lane:** DM relic mapping (remaining "continuum limit" dependency)

---

## Status

**BOUNDED** (upgrades internal consistency; does not upgrade overall lane status)

The DM lane's remaining "continuum limit" dependency -- specifically, that
the sigma_v coefficient C -> pi and Stefan-Boltzmann rho ~ T^4 require a
"continuum limit" -- is resolved. These are THERMODYNAMIC limits (a = l_Planck
fixed, N -> infinity), not the forbidden continuum limit (a -> 0, which does
not exist per the taste-physicality theorem).

This resolves an internal inconsistency in the DM lane documentation: previous
notes (DM_SIGMA_V_LATTICE_NOTE.md, DM_RELIC_GAP_CLOSURE_NOTE.md) described
certain steps as requiring the "continuum limit" when they actually require
only the thermodynamic limit. The overall DM lane status remains BOUNDED
because of the remaining g_bare = 1 self-dual point assumption.

---

## Theorem / Claim

**Claim (structural clarification):** The three "continuum limit"
dependencies identified in the DM sigma_v and relic gap closure notes are
actually thermodynamic limits:

1. **C(L) -> pi** (sigma_v coefficient): convergence of the lattice density
   of states to the Brillouin zone integral. This is N -> infinity at fixed a,
   not a -> 0.

2. **rho ~ T^4** (Stefan-Boltzmann): convergence of the lattice energy sum
   to the BZ integral. Again N -> infinity at fixed a.

3. **x_F convergence**: the freeze-out ratio converges as the lattice spectral
   density fills in. Again N -> infinity at fixed a.

The two limits are structurally different:

| | Continuum limit | Thermodynamic limit |
|---|---|---|
| **Parameter varied** | a -> 0 | N -> infinity |
| **What is fixed** | L = Na | a = l_Planck |
| **UV physics** | Changes (Lambda_UV -> inf) | Unchanged (Lambda_UV = pi/a) |
| **IR physics** | Fixed | More modes (dk -> 0) |
| **Existence in Cl(3)** | FORBIDDEN (no LCP) | EXISTS (universe is large) |
| **Generation structure** | DESTROYED | PRESERVED |

---

## Assumptions

1. Cl(3) on Z^3 is the complete theory (framework axiom).
2. a = l_Planck (taste-physicality theorem + dimensional identification).
3. The PL manifold result: the cubical lattice IS a PL 3-manifold.
4. Moise's theorem: PL 3-manifold -> smooth -> Weyl's law applies.
5. The universe has N >> 1 Planck-volume sites (N ~ 10^185).

Assumptions 1-2 are the framework axiom and a consequence of the
taste-physicality theorem (GENERATION_GAP_CLOSURE_NOTE.md).
Assumption 3 is proved in S3_PL_MANIFOLD_NOTE.md.
Assumption 4 is a standard mathematical theorem (Moise 1952).
Assumption 5 is observational.

---

## What Is Actually Proved

### The structural distinction (Block 1, 3 EXACT tests)

**1A. [EXACT] Wilson masses are fixed in lattice units.**
m_lattice = 2r|s| does not depend on any parameter that is being sent to a
limit. The taste-physicality theorem proves there is no tunable coupling, no
Line of Constant Physics, and no a -> 0 procedure.

**1B. [EXACT] The thermodynamic limit exists.**
The physical universe has N ~ 10^185 lattice sites (at a = l_Planck). The
thermodynamic limit N -> infinity is the statement that finite-size corrections
are small, which they are: O(N^{-2/3}) ~ 10^{-120}.

**1C. [EXACT] The two limits operate on different parameters.**
The UV lattice dispersion omega(k) = 2*sqrt(sum sin^2(k_i/2)) differs from
the continuum dispersion omega = |k| by O(1) at k ~ pi/a. This UV discrepancy
persists in the thermodynamic limit (and should -- the UV is physical). It
vanishes only in the continuum limit (which is forbidden).

### Weyl's law convergence (Block 2, 2 DERIVED tests)

**2A. [DERIVED] Eigenvalue counting converges.**
On the periodic L^3 lattice, the integrated eigenvalue count N(lambda) converges
to the BZ integral prediction: ratio = 0.980 at L=16 (2% deviation).

**2B. [DERIVED] Convergence rate is O(L^{-1.84}).**
The deviation |N/N_Weyl - 1| scales as L^{-1.84}, faster than O(L^{-3/2}).
This is consistent with Weyl's law subleading correction on a 3-torus.

### DOS and sigma_v coefficient (Block 3, 3 DERIVED tests)

**3A. [DERIVED] DOS converges to BZ integral.**
At L=20, the lattice DOS at E=1.0 matches the BZ integral (a=1 fixed) within
7%. The target is the BZ integral, NOT the continuum free-particle DOS.

**3B. [DERIVED] Integrated count converges to BZ integral.**
N_lat(lambda=2.0) / N_BZ = 0.982 at L=20 (2% deviation). The integrated
counting function is smoother than the differential DOS.

**3C. [DERIVED] Finite-size correction negligible at physical N.**
Power-law extrapolation: |correction| ~ V^{-0.53}. At V ~ 10^180:
|correction| ~ 10^{-96}. Negligible.

### Stefan-Boltzmann (Block 4, 2 DERIVED tests)

**4A. [DERIVED] rho_lattice converges to rho_BZ (not to rho_SB directly).**
At L=16, T=0.3: rho_lat/rho_BZ = 0.993 (0.7% deviation). The lattice
energy density converges to the BZ integral result, which in turn equals
Stefan-Boltzmann at low T/E_Planck.

**4B. [DERIVED] Lattice correction O((aT)^2) negligible at physical T_F.**
At freeze-out T_F ~ 40 GeV, E_Planck ~ 10^19 GeV: (aT)^2 ~ 10^{-35}.

### PL manifold bridge (Block 5, 2 EXACT tests)

**5A. [EXACT] Periodic lattice is a PL 3-manifold.**
All vertices have degree 6; links are octahedra (chi=2 = S^2). This is the
link condition for PL manifolds.

**5B. [EXACT] PL -> smooth -> Weyl's law.**
Moise (1952): every PL 3-manifold has a compatible smooth structure. Weyl's
law applies to the Laplacian on smooth compact manifolds. Therefore Weyl's law
applies to the lattice Laplacian in the thermodynamic limit.

### Taste-physicality cross-check (Block 6, 3 tests: 2 EXACT, 1 DERIVED)

**6A. [EXACT] Continuum limit destroys generation structure.**
Only 1/8 taste states survive a -> 0. The 1+3+3+1 orbit decomposition is lost.

**6B. [EXACT] Thermodynamic limit preserves generation structure.**
All 8 taste states with masses m_W = 2r|s| are independent of N. The orbit
decomposition is intact.

**6C. [DERIVED] The "continuum" DOS target is actually the BZ integral.**
At L=20, the lattice DOS ratio to the BZ integral (at fixed a=1) is 1.04.
The BZ integral is computed at fixed lattice spacing -- it IS the
thermodynamic limit, not the continuum limit.

### Summary: PASS=15 FAIL=0 (EXACT=7 DERIVED=8)

---

## What Remains Open

1. **g_bare = 1.** The self-dual point argument (DM_SIGMA_V_LATTICE_NOTE.md)
   makes g=1 a distinguished value but does not uniquely force it. This is the
   remaining BOUNDED dependency in the DM lane.

2. **Overall DM lane status.** The thermodynamic closure resolves the
   "continuum limit" inconsistency but does not change the overall lane status.
   The lane remains BOUNDED because of g_bare = 1 and because the full
   Boltzmann/Friedmann mapping is a structural consistency, not a derivation
   from axioms alone.

3. **Non-perturbative sigma_v.** The Born approximation gives the leading
   alpha^2 term. Higher-order corrections are not computed.

---

## How This Changes The Paper

### Corrects a misidentification

Previous DM notes (DM_SIGMA_V_LATTICE_NOTE.md, DM_RELIC_GAP_CLOSURE_NOTE.md)
listed "continuum limit" as a dependency for C -> pi and rho ~ T^4. This was a
misnomer. The actual dependency is the thermodynamic limit (N -> infinity, a
fixed), which:

- **EXISTS** (unlike the continuum limit, which is forbidden)
- **Is guaranteed** by Weyl's law on PL manifolds
- **Preserves** all lattice physics (generation structure, UV cutoff, taste
  masses)
- **Has negligible corrections** at physical N ~ 10^185

### Cross-references

This note draws on two results from other lanes:

1. **Taste-physicality theorem** (GENERATION_GAP_CLOSURE_NOTE.md): proves
   the continuum limit a -> 0 does not exist. Without this, the distinction
   between continuum and thermodynamic limits would not be sharp.

2. **PL manifold result** (S3_PL_MANIFOLD_NOTE.md): proves the cubical lattice
   IS a PL 3-manifold. This guarantees Weyl's law applies, which is the
   mathematical backbone of the thermodynamic limit convergence.

### Paper-safe wording

Previous (from DM_SIGMA_V_LATTICE_NOTE.md):
> The coefficient C -> pi requires the continuum limit of the lattice DOS.

Corrected:
> The coefficient C -> pi follows from Weyl's law on the PL lattice manifold
> in the thermodynamic limit (N -> infinity at fixed a = l_Planck). This is
> not the continuum limit (a -> 0), which does not exist in the Cl(3) framework.
> At physical N ~ 10^185, finite-size corrections are O(10^{-96}).

### What NOT to say

- "DM lane is CLOSED" -- it remains BOUNDED (g_bare = 1 is not derived)
- "Continuum limit exists" -- it does NOT exist (taste-physicality theorem)
- "No limiting procedure needed" -- the thermodynamic limit IS a limit, just
  a different (and physically benign) one

### Net effect on DM lane blockers

| Blocker | Before | After |
|---------|--------|-------|
| C -> pi (sigma_v coefficient) | "requires continuum limit" | RESOLVED (thermodynamic limit) |
| rho ~ T^4 (Stefan-Boltzmann) | "requires continuum limit" | RESOLVED (thermodynamic limit) |
| x_F convergence | "thermodynamic limit" | Unchanged (already correctly identified) |
| g_bare = 1 | BOUNDED (self-dual point) | Unchanged |
| Boltzmann/Friedmann mapping | STRUCTURAL consistency | Unchanged |

Two blockers resolved. The remaining blockers (g_bare, Boltzmann/Friedmann)
are unchanged.

---

## Commands Run

```bash
python3 scripts/frontier_dm_thermodynamic_closure.py
# Exit code: 0
# PASS=15 FAIL=0 (EXACT=7 DERIVED=8 BOUNDED=0)
```

---

## Key References

1. Moise (1952). Affine structures in 3-manifolds, V. Annals of Math. 56.
2. Weyl (1911). Asymptotic distribution of eigenvalues. Math. Annalen 71.
3. GENERATION_GAP_CLOSURE_NOTE.md -- taste-physicality theorem (no continuum limit)
4. S3_PL_MANIFOLD_NOTE.md -- lattice is a PL 3-manifold
5. DM_SIGMA_V_LATTICE_NOTE.md -- sigma_v derivation (corrected dependency)
6. DM_RELIC_GAP_CLOSURE_NOTE.md -- relic gap closure (corrected dependency)
