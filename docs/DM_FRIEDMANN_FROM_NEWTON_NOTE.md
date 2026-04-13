# First Friedmann Equation from Newtonian Cosmology on Z^3

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Script:** `scripts/frontier_dm_friedmann_from_newton.py`
**Lane:** DM relic mapping (tightening the Friedmann sub-gap)

---

## Status

**BOUNDED** (upgrades one sub-step; does not close the DM lane)

This note narrows one specific gap in the DM relic mapping chain: the use
of the Friedmann equation H^2 = (8 pi G / 3) rho was previously classified
as "GR input."  We show it is Newtonian cosmology, which is already derived
from the lattice.

---

## Theorem / Claim

**Theorem.** The first Friedmann equation H^2 = (8 pi G / 3) rho follows
from Newtonian gravity applied to a homogeneous expanding sphere.  It does
not require general relativity.  On Z^3 with Cl(3), all ingredients are
lattice-derived:

1. Newton's law F = G M1 M2 / r^2 (from lattice Poisson equation).
2. The shell theorem (from Gauss's law on Z^3).
3. Energy conservation for an expanding shell (first law of thermodynamics).

The pressure term rho + 3p appears only in the **second** Friedmann equation
(the acceleration equation a''/a = -(4 pi G / 3)(rho + 3p)), which is NOT
needed for computing H(T) at freeze-out.

**Reference:** Milne, Q.J. Math. 5 (1934); McCrea & Milne, Q.J. Math. 5 (1934).

---

## The Derivation

### Step 1: Newtonian shell argument

Consider a homogeneous sphere of density rho.  A thin shell of mass m at
radius R feels only the interior mass M(R) = (4/3) pi R^3 rho (shell
theorem from Gauss's law on Z^3).

The kinetic + potential energy of the shell:

    E = (1/2) m R_dot^2 - G M(R) m / R

For a spatially flat universe (E = 0, corresponding to k = 0):

    (1/2) R_dot^2 = G (4/3) pi R^2 rho

Dividing by R^2 and defining H = R_dot / R:

    H^2 = (8 pi G / 3) rho

This is **identical** to the GR first Friedmann equation for k = 0.

### Step 2: Where pressure enters (and where it does not)

The **second** Friedmann equation (acceleration) is:

    a'' / a = -(4 pi G / 3)(rho + 3p)

In Newtonian gravity, the source of gravity is mass density rho alone.
In GR, the source is the active gravitational mass rho + 3p.  This
difference is real and important for the acceleration.

But the **first** Friedmann equation H^2 = (8 pi G / 3) rho involves
only rho (the energy density), not rho + 3p.  This equation is the same
in Newton and GR.

### Step 3: What freeze-out needs

The freeze-out condition is:

    Gamma_ann(T_F) = H(T_F)

where Gamma = n_eq <sigma v> is the annihilation rate and H(T_F) is the
Hubble parameter at freeze-out.  This requires H(T), which comes from
the first Friedmann equation.  The second Friedmann equation (acceleration)
is not used anywhere in the standard freeze-out calculation.

### Step 4: rho(T) from the lattice

The energy density at temperature T is:

    rho(T) = (pi^2 / 30) g_star T^4

This comes from the lattice spectral sum (see DM_THEOREM_APPLICATION_NOTE.md,
Step 4b).  At freeze-out temperatures T ~ 40 GeV << M_Pl ~ 10^19 GeV,
the lattice-to-continuum corrections are O((aT)^2) ~ 10^{-35}.

### Step 5: Assembling H(T)

Combining Newton (giving G) and the spectral sum (giving rho(T)):

    H(T) = sqrt(8 pi G rho(T) / 3) = sqrt(8 pi^3 g_star / 90) T^2 / M_Pl

Every ingredient is lattice-derived:

| Quantity | Source | Status |
|----------|--------|--------|
| G = 1/(4 pi) | Lattice Poisson Green's function | EXACT |
| rho(T) = (pi^2/30) g_star T^4 | Lattice spectral sum | DERIVED |
| g_star = 106.75 | Taste spectrum counting | EXACT |
| Shell theorem | Gauss's law on Z^3 | EXACT |
| H^2 = (8piG/3)rho | Newton + E = 0 | DERIVED |

---

## Assumptions

1. **Cl(3) on Z^3** (framework axiom).
2. **Flatness k = 0.**  The Newtonian derivation gives H^2 = (8piG/3)rho
   only for E = 0 (k = 0).  Flatness would follow from S^3 compactification,
   which is itself bounded.
3. **Thermodynamic limit** N >> 1 (rho(T) from the spectral sum).
4. **T << pi/a** (physical temperatures far below the lattice cutoff).

---

## What Is Actually Proved

1. The **first** Friedmann equation H^2 = (8piG/3)rho is identical in
   Newton and GR for k = 0.  (Mathematical identity, exact.)
2. Newton's law on Z^3 + shell theorem + energy conservation give this
   equation.  (Lattice-derived, exact on the framework surface.)
3. rho(T) from the lattice spectral sum.  (Derived, with negligible
   lattice corrections at physical temperatures.)
4. The **second** Friedmann equation (rho + 3p) is NOT needed for freeze-out.
   (Structural check, exact.)

**Upgrade:** In DM_THEOREM_APPLICATION_NOTE.md, Step 4d was listed as
BOUNDED (GR input).  The sub-step of obtaining H(T) from rho(T) and G
is now DERIVED: it uses Newtonian cosmology, which is derived from the
lattice Poisson equation.

**Not upgraded:** The flatness assumption (k = 0) remains bounded.  The
overall DM lane remains bounded per review.md.

---

## What Remains Open

1. **k = 0 flatness.**  The Newtonian argument gives H^2 = (8piG/3)rho
   only for the zero-energy (flat) case.  S^3 compactification would
   provide k = 0 naturally, but that lane is bounded.

2. **g_bare = 1.**  Still bounded (Cl(3) normalization argument).

3. **Stosszahlansatz.**  The Boltzmann coarse-graining step remains
   bounded at the paper bar.

4. **eta (baryon asymmetry).**  Still observational input.

5. **Overall DM lane.**  Remains BOUNDED per review.md.

---

## How This Changes The Paper

### Sub-gap narrowing

The DM relic mapping chain in the paper currently has three BOUNDED steps.
This note converts one sub-step (Friedmann equation as "GR input") to
DERIVED.

Before:

| Step | Status |
|------|--------|
| Master equation -> Boltzmann | DERIVED |
| sigma v from lattice T-matrix | DERIVED |
| H(T) from Friedmann equation | **BOUNDED (GR input)** |
| x_F from Gamma = H | DERIVED |
| R = 5.48 | BOUNDED |

After:

| Step | Status |
|------|--------|
| Master equation -> Boltzmann | DERIVED |
| sigma v from lattice T-matrix | DERIVED |
| H(T) from Newtonian cosmology | **DERIVED** |
| x_F from Gamma = H | DERIVED |
| R = 5.48 | BOUNDED (from k=0, g_bare) |

### Paper-safe wording

> The expansion rate H(T) used in the freeze-out calculation does not
> require general relativity.  The first Friedmann equation
> H^2 = (8 pi G / 3) rho is a consequence of Newtonian gravity applied
> to a homogeneous expanding sphere (Milne 1934; McCrea & Milne 1934).
> On Z^3, Newton's law is derived from the lattice Poisson equation, and
> the energy density rho(T) is computed from the lattice spectral sum.
> The pressure contribution rho + 3p enters only the acceleration equation,
> which is not needed for freeze-out.

### What NOT to say

- "DM lane is CLOSED" -- it remains BOUNDED
- "The Friedmann equation is fully derived" -- only the FIRST equation
  is derived; the second still requires GR
- "No GR input remains" -- flatness (k=0) and the second equation are
  still bounded
- "This removes the main DM obstruction" -- the main obstructions
  (g_bare, Stosszahlansatz, eta) are elsewhere

---

## Commands Run

```bash
python3 scripts/frontier_dm_friedmann_from_newton.py
# Exit code: 0
# PASS=13 FAIL=0 (EXACT=8 DERIVED=3 BOUNDED=2)
```

---

## Cross-References

- `NEWTON_LAW_DERIVED_NOTE.md` -- Newton's law from lattice Poisson equation
- `DM_THEOREM_APPLICATION_NOTE.md` -- the full DM chain (Step 4d upgraded)
- `DM_STOSSZAHLANSATZ_NOTE.md` -- Stosszahlansatz sub-gap (still bounded)
- `DM_FINAL_GAPS_NOTE.md` -- overall DM gap map
- `OMEGA_LAMBDA_DERIVATION_NOTE.md` -- cosmological pie chart (uses same H(T))
