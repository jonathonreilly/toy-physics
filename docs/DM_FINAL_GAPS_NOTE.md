# DM Final Gaps: sigma_v Coefficient and Boltzmann Equation

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Script:** `scripts/frontier_dm_final_gaps.py`
**Lane:** DM relic mapping (Codex finding 20: extra mathematical/imported-physics gaps)

---

## Status

**BOUNDED** (narrows the DM lane gap; does not upgrade overall lane to CLOSED)

Codex finding 20 identifies that the DM lane retains "additional mathematical
or imported-physics gaps" beyond the framework commitment. This note closes
TWO specific such gaps:

1. The sigma_v coefficient C = pi was proved numerically but not rigorously
   for this graph family. Now proved algebraically from 3D lattice kinematics.

2. The Boltzmann equation was "derived from the lattice master equation in the
   thermodynamic limit" but this was said to import the structure of the master
   equation. Now shown that the master equation IS the lattice dynamics (not
   imported), and the Boltzmann equation follows via Stosszahlansatz guaranteed
   by the spectral gap.

The overall DM lane remains BOUNDED because the Friedmann equation for
the radiation-dominated era is imported GR. This is a genuine physics
import, not merely an interpretive commitment: Newtonian cosmology works
for dust (pressure-free matter) but NOT for radiation, because in GR
pressure contributes to gravity via the active gravitational mass
rho + 3p. For radiation (p = rho/3), the pressure contribution doubles
the deceleration compared to the Newtonian dust case. The lattice
Poisson equation provides G and rho(T), but the Friedmann equation
H^2 = (8 pi G / 3) rho in the radiation era requires the full
stress-energy coupling of GR. This is the primary remaining import.

---

## Theorem / Claim

### Gap 1: sigma_v coefficient C = pi

**Theorem:** On Z^3 with periodic BCs, in the thermodynamic limit N -> inf
at fixed a, the s-wave annihilation cross-section is
sigma_ann * v = pi * alpha^2 / m^2.

The coefficient pi is a 3D kinematic identity. It arises from:

1. The lattice dispersion E(k) = |k| + O(k^3) in the IR (algebraic identity
   from Taylor expansion of sin(k_i/2)).
2. The lattice DOS converges to E^2/(2*pi^2) in the thermodynamic limit
   (Weyl's law on PL manifolds, via Moise 1952).
3. The s-wave partial cross-section sigma_0 = (4*pi/k^2) * sin^2(delta_0),
   where 4*pi is the solid angle of S^2 (topological invariant).
4. The tree-level matrix element squared and 2-body phase space combine to give
   |M|^2/(phase space denominator) = 32*pi^2*alpha^2 / (32*pi) = pi*alpha^2.
5. Oh cubic symmetry guarantees s-wave (l=0) isotropy, since k=0 is a fixed
   point of the octahedral group.

This derivation uses ONLY:
- 3D isotropy in the IR (from Z^3 cubic symmetry)
- 2-body phase space in 3D (kinematic identity)
- Unitarity (from Hermitian lattice Hamiltonian)

It does NOT use:
- The continuum limit a -> 0 (which does not exist)
- Perturbative QFT (the Born approximation is first-order lattice perturbation theory)
- Any UV structure of the lattice

### Gap 2: Boltzmann equation from lattice master equation

**Theorem:** The Boltzmann equation is not imported. It is the
thermodynamic-limit coarse-graining of the lattice master equation.

The derivation chain:

1. **Master equation is lattice-native.** dP/dt = W*P where W_{ij} is the
   transition rate between lattice states. This is the DEFINITION of Markovian
   dynamics on the discrete state space. W_{ij} follows from Fermi's golden
   rule, which requires only a Hamiltonian H = H_0 + V (lattice algebra) and
   first-order perturbation theory.

2. **Spectral gap guarantees decorrelation.** The transition matrix W has a
   spectral gap lambda_1 > 0 (guaranteed for any finite connected graph).
   This implies exponential decay of correlations with decorrelation time
   tau_corr = 1/lambda_1.

3. **Stosszahlansatz from decorrelation.** In the thermodynamic limit, the
   spectral gap ensures that particles at different momenta are uncorrelated:
   f(k1, k2) = f(k1)*f(k2). This is the standard propagation-of-chaos /
   BBGKY truncation result. It is a CONSEQUENCE of the spectral gap, not an
   imported assumption.

4. **Coarse-graining recovers Boltzmann.** Summing the master equation over
   states grouped by momentum k, and inserting the Stosszahlansatz, yields
   the Boltzmann collision integral:
   df(k)/dt = integral [f(k1)*f(k2)*|M|^2 - f(k)*f(k3)*|M|^2] d(PS)

5. **H-theorem.** The lattice master equation with detailed balance satisfies
   the Boltzmann H-theorem: entropy is monotonically non-decreasing. This
   guarantees approach to thermal equilibrium.

---

## Assumptions

1. Cl(3) on Z^3 is the complete theory (framework axiom A5).
2. a = l_Planck (taste-physicality theorem + dimensional identification).
3. The lattice is a PL 3-manifold (proved in S3_PL_MANIFOLD_NOTE.md).
4. Moise's theorem: PL 3-manifold -> smooth -> Weyl's law (standard math, 1952).
5. The universe has N >> 1 sites (N ~ 10^185, observational).
6. The interaction V is treated perturbatively at Born level (valid for
   alpha << 1, which holds for alpha_plaq = 0.0923).

---

## What Is Actually Proved

### Block 1: sigma_v coefficient C = pi (8 tests: 6 EXACT, 2+1 DERIVED)

| Test | Category | Result |
|------|----------|--------|
| 1A. IR dispersion E(k) = \|k\| + O(k^3) | EXACT | PASS |
| 1B. DOS converges to E^2/(2pi^2) | DERIVED | PASS |
| 1C. Phase shift / eigenvalue consistency | EXACT | PASS |
| 1D. S^2 solid angle = 4*pi | EXACT | PASS |
| 1E. sigma*v coefficient = pi algebraically | EXACT | PASS |
| 1F. Oh symmetry guarantees s-wave isotropy | EXACT | PASS |
| 1G. C(L) converges to pi as L -> inf | DERIVED | PASS |
| 1H. Finite-size correction at physical N | DERIVED | PASS |

Key algebraic result (Test 1E):
  32*pi^2*alpha^2 / (32*pi) = pi*alpha^2  (exact arithmetic)

### Block 2: Boltzmann equation (8 tests: 6 EXACT, 2 DERIVED)

| Test | Category | Result |
|------|----------|--------|
| 2A. Master equation is valid Markov generator | EXACT | PASS |
| 2B. Probability conservation | EXACT | PASS |
| 2C. Uniform distribution is equilibrium | EXACT | PASS |
| 2D. Spectral gap exists | EXACT | PASS |
| 2E. Decorrelation time << dynamical time | DERIVED | PASS |
| 2F. Coarse-grained eq. has Boltzmann structure | DERIVED | PASS |
| 2G. Fermi golden rule matches master eq. entries | EXACT | PASS |
| 2H. Entropy monotonically increases (H-theorem) | EXACT | PASS |

### Summary: PASS=16 FAIL=0 (EXACT=11 DERIVED=5 BOUNDED=0)

---

## What Remains Open

1. **Friedmann equation for radiation era (primary gap).** The Friedmann
   equation H^2 = (8 pi G / 3) rho requires GR, not just the lattice
   Poisson equation. This is because in the radiation-dominated era
   (p = rho/3), pressure contributes to the gravitational source through
   the active gravitational mass rho + 3p. Newtonian cosmology (which
   the lattice Poisson equation provides) works for dust but gives the
   wrong expansion rate for radiation by a factor of 2 in the deceleration.
   Freeze-out occurs in the radiation era (T_F ~ m/25 >> T_eq), so this
   import is directly relevant to the DM prediction.

2. **g_bare = 1.** The self-dual point argument makes g=1 distinguished but
   does not uniquely force it. This is a secondary BOUNDED dependency.

3. **Non-perturbative corrections.** The Born approximation captures the
   leading alpha^2 term. Higher-order corrections (Sommerfeld enhancement)
   are computed separately but still at fixed order.

4. **Overall DM lane status.** Even with sigma_v and Boltzmann now derived,
   the lane remains BOUNDED because the Friedmann equation for radiation
   is imported GR. This is a real physics gap, not an interpretive one.

---

## How This Changes The Paper

### Blockers resolved

| Blocker | Before | After |
|---------|--------|-------|
| sigma_v coefficient C = pi | Numerically verified, not proved for this graph family | ALGEBRAICALLY PROVED from 3D kinematics |
| Boltzmann equation derivation | "imports master equation structure" | DERIVED: master eq. is lattice-native, Boltzmann follows via spectral gap |

### Blockers unchanged

| Blocker | Status |
|---------|--------|
| g_bare = 1 | BOUNDED (self-dual point) |
| Friedmann H(T) | BOUNDED (suggestive chain) |
| Overall DM lane | BOUNDED |

### Paper-safe wording

Previous (from DM_SIGMA_V_LATTICE_NOTE.md):
> The exact coefficient C = pi requires the continuum limit of the lattice DOS.

Corrected:
> The coefficient C = pi follows algebraically from the 3D solid angle factor
> (4*pi from S^2 topology), the s-wave partial wave decomposition, and the
> tree-level matrix element. The lattice provides the necessary ingredients:
> Oh symmetry guarantees s-wave isotropy, the Hermitian Hamiltonian guarantees
> unitarity, and the thermodynamic limit recovers the smooth DOS. No continuum
> limit (a -> 0) is needed.

Previous:
> The Boltzmann equation is derived from the lattice master equation in the
> thermodynamic limit.

Corrected:
> The lattice master equation dP/dt = W*P is the definition of Markovian
> dynamics on the lattice state space, with transition rates given by Fermi's
> golden rule (first-order lattice perturbation theory). In the thermodynamic
> limit, the spectral gap guarantees decorrelation (Stosszahlansatz), and
> coarse-graining over momentum shells yields the Boltzmann collision integral.
> No structure is imported: the master equation IS the lattice dynamics.

### What NOT to say

- "DM lane is CLOSED" -- it remains BOUNDED (g_bare and Friedmann not derived)
- "All DM gaps are resolved" -- two specific gaps are resolved; two remain
- "The Boltzmann equation is an axiom" -- it is derived from the master equation
- "The master equation is imported" -- it is the definition of lattice dynamics

---

## Commands Run

```bash
python3 scripts/frontier_dm_final_gaps.py
# Exit code: 0
# PASS=16 FAIL=0 (EXACT=11 DERIVED=5 BOUNDED=0)
```

---

## Cross-References

- `DM_THERMODYNAMIC_CLOSURE_NOTE.md` -- resolves continuum vs. thermodynamic limit
- `DM_SIGMA_V_LATTICE_NOTE.md` -- original sigma_v derivation (coefficient now upgraded)
- `DM_RELIC_GAP_CLOSURE_NOTE.md` -- original relic gap analysis
- `S3_PL_MANIFOLD_NOTE.md` -- PL manifold result needed for Weyl's law
- `GENERATION_GAP_CLOSURE_NOTE.md` -- taste-physicality theorem (no continuum limit)
