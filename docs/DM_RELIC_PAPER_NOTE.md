# DM Relic Paper Note

**Date:** 2026-04-12
**Lane:** DM relic mapping

---

## Status

**BOUNDED** -- one-parameter consistency window.

R = 5.48 at g_bare = 1, matching R_obs = 5.47 to 0.25%.
The structural backbone (mass ratio, Casimir channels, Sommerfeld mechanism)
is parameter-free. The numerical value depends on one assumed coupling
(g_bare = 1) and two imported perturbative formulas (sigma_v, Coulomb shape).

This is NOT "DM relic abundance derived from the lattice axioms alone."

---

## Theorem / Claim

The Cl(3) lattice structure determines R = Omega_DM / Omega_b up to one
free parameter (the bare gauge coupling g at the lattice cutoff). At the
natural value g_bare = 1, R = 5.48. The consistency window g in [0.9, 1.1]
gives R in [5.2, 5.9], containing R_obs = 5.47.

---

## Assumptions

1. g_bare = 1 is ASSUMED (not derived from any lattice theorem).
2. The Coulomb potential V(r) = -C_F * alpha_s / r is IMPORTED from
   perturbative QFT (one-gluon exchange).
3. sigma_v = pi * alpha_s^2 / m^2 is IMPORTED from perturbative QFT
   (tree-level s-wave Born approximation).
4. The thermodynamic limit (lattice master equation -> Boltzmann equation)
   is demonstrated numerically, not proved as a theorem.

---

## Provenance Chain

```
R = (3/5) * (f_vis / f_dark) * S_vis

             NATIVE quantities (7)
             ----------------------
             mass ratio 3/5          Hamming weights on Cl(3) bit strings
             C_F(SU3) = 4/3          group theory of lattice gauge group
             dim_adj(SU3) = 8        group theory
             C2(SU2) = 3/4           group theory
             dim_adj(SU2) = 3        group theory
             g_* = 106.75            taste spectrum: 28 bosonic + 7/8 * 90 fermionic
             n_eq ~ exp(-m/T)        heat kernel on lattice

             DERIVED equations (5)
             ----------------------
             Boltzmann equation       thermodynamic limit of lattice master eq.
             Friedmann equation       Poisson coupling + spectral energy density
             H > 0                    spectral gap + 2nd law (boundary condition)
             x_F = 25                 lattice Boltzmann, Gamma_ann = H condition
             Sommerfeld formula       Schrodinger eq. / lattice Green's fn ratio

             ASSUMED inputs (1)
             ----------------------
             g_bare = 1               not derived; O(1) is natural but 1.000 is not forced

             IMPORTED formulas (2)
             ----------------------
             sigma_v = pi*alpha^2/m^2 perturbative QFT (tree-level Born)
             V(r) = -alpha/r          one-gluon exchange (Coulomb shape)
```

### Provenance flow diagram

```
  Cl(3) bit strings -----> mass ratio 3/5 --------\
                                                     \
  SU(3) x SU(2) --------> Casimir channels --------+--> R_base = 31/9
  (lattice gauge group)    f_vis, f_dark            /
                                                   /
  Plaquette action -------> alpha_plaq = 0.092 ---+
       |                        |                  |
  [ASSUMED: g_bare=1]           |                  |
                                v                  |
  [IMPORTED: V(r)=-a/r] --> Coulomb Sommerfeld --> S_vis = 1.592
                                ^                  |
  Taste spectrum --> g_*=106.75 |                  |
  Heat kernel ----> n_eq        |                  |
  Lattice master eq ----------> Boltzmann eq.      |
  Poisson coupling -----------> Friedmann eq.      |
  Spectral gap + 2nd law -----> H > 0              |
       |                        |                  |
       +-----> x_F = 25 -------+                  |
       |                                           |
  [IMPORTED: sigma_v=pi*a^2/m^2] (enters x_F)     |
                                                   v
                                            R = R_base * S_vis = 5.48
```

---

## What Is Actually Proved

1. The structural backbone R_base = (3/5) * (155/27) = 31/9 = 3.444
   is NATIVE: it follows from Hamming weights and Casimir algebra
   with zero free parameters.

2. The Sommerfeld enhancement S_vis = 1.592 is DERIVED from the
   Coulomb scattering formula (lattice Green's function ratio),
   but requires the IMPORTED Coulomb potential shape and the
   ASSUMED coupling g_bare = 1.

3. The freeze-out temperature x_F = 25 is DERIVED from the lattice
   Boltzmann equation, but the derivation uses the IMPORTED
   cross-section sigma_v = pi * alpha_s^2 / m^2. The result is
   log-insensitive to sigma_v (changing sigma_v by 2x shifts x_F
   by ~2 units, shifting R by ~1%).

4. g_* = 106.75 is NATIVE from the taste spectrum decomposition.

5. The Boltzmann and Friedmann equations are DERIVED from lattice
   quantities in the thermodynamic limit (demonstrated numerically,
   not proved as a theorem). This is a genuine advance over importing
   them as external cosmological machinery.

---

## Error Budget for R = 5.48

| Source                    | Parameter range     | R range       | delta_R/R |
|---------------------------|---------------------|---------------|-----------|
| g_bare uncertainty        | [0.9, 1.1]          | [4.99, 6.10]  | 20%       |
| x_F uncertainty           | [20, 30]            | [5.24, 5.71]  | 8.7%      |
| sigma_v coefficient       | [0.5x, 2x] nominal | via x_F: ~1%  | 1.0%      |
| Finite-lattice artifacts  | L=8 vs L->inf       | ~0.5%         | 0.5%      |

The dominant uncertainty is g_bare. Within the "natural coupling" window
g in [0.9, 1.1], R spans [4.99, 6.10]. R_obs = 5.47 sits comfortably
inside this range.

The 0.25% match at g_bare = 1 is striking but should be presented as
a consistency success inside a one-parameter window, not as a precision
prediction.

---

## What Remains Open

### To upgrade from BOUNDED to CLOSED:

1. **Derive g_bare from a lattice self-consistency condition.**
   Show that Cl(3) + anomaly cancellation + unitarity forces g to a
   specific value (e.g., via a UV fixed point or spectral constraint).
   This would eliminate the 1 ASSUMED input.

2. **Compute sigma_v directly from lattice correlators.**
   Use the optical theorem on lattice two-point functions to extract
   the annihilation cross-section without importing Feynman diagrams.
   This would eliminate 1 of the 2 IMPORTED formulas.

3. **Derive V(r) = -alpha/r from the lattice Green's function.**
   The 3D lattice Laplacian Green's function has the right 1/r form
   in the continuum limit, but the identification V_QCD = G_lattice
   requires an additional physical argument. Making this rigorous
   would eliminate the remaining IMPORTED formula.

4. **Prove the thermodynamic limit.**
   Show rigorously that the lattice master equation converges to the
   Boltzmann equation as N -> infinity for the Z^3 graph family.
   This would upgrade DERIVED items to PROVED.

None of these are achieved in the current scripts.

---

## How This Changes The Paper

### Replace the current DM section claim with:

> The Cl(3) lattice structure determines the dark-to-visible matter ratio
> up to one parameter: the bare gauge coupling g at the lattice cutoff.
> The structural factors (mass ratio 3/5, Casimir channel ratio 155/27)
> are parameter-free. The Sommerfeld enhancement introduces the coupling
> dependence. At the natural value g_bare = 1, R = 5.48, matching the
> observed R = 5.47 to 0.2%. The consistency window g in [0.9, 1.1]
> spans R in [5.2, 5.9], comfortably containing the observation.
>
> The freeze-out variables (g_* = 106.75, x_F = 25) are derived from
> the lattice taste spectrum and lattice Boltzmann equation respectively.
> The Boltzmann and Friedmann equations themselves follow from the lattice
> master equation and Poisson coupling in the thermodynamic limit.
>
> The base cross-section sigma_v = pi * alpha_s^2 / m^2 is the standard
> perturbative s-wave result; deriving it directly from lattice
> observables remains open.

### Do NOT write:

- "DM relic abundance derived from the lattice axioms alone"
- "Zero-parameter prediction"
- "Zero imported cosmological equations" (the synthesis script line 674
  overclaims this)
- "Gate closed" for this lane

---

## Commands Run

```
python scripts/frontier_dm_relic_paper.py
```

---

## Scripts and Notes Reviewed

- `scripts/frontier_dm_relic_mapping.py` (G_BARE = 1.0 at line 86)
- `scripts/frontier_dm_relic_gap_closure.py` (G_BARE = 1.0 at line 89)
- `scripts/frontier_dm_relic_synthesis.py` (G_BARE = 1.0 at line 88)
- `docs/CODEX_DM_RESPONSE.md` (provenance chain and objection verdicts)
- `review.md` (Codex audited state)
