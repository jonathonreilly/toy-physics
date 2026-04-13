# Elegant Closure Plan for the Three Live Gates

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Purpose:** Codex-owned plan for closing the remaining live flagship gates
without defaulting to a “compute-limited” story too early.

## Bottom line

The current repo does **not** justify calling the remaining live gates broadly
compute-limited.

The blockers are now narrower:

1. **DM relic mapping:** one reconciled baryogenesis transport surface
2. **Renormalized `y_t`:** one finite framework-to-SM gauge crossover theorem
3. **CKM:** a small number of analytic coefficients and one physical phase

So the next work should prefer math/physics closure over brute-force scans.

## 1. DM relic mapping

### Honest current blocker

DM is no longer blocked on freeze-out structure. It is blocked on `eta`.

More precisely, the remaining live problem is:

- no reconciled baryogenesis transport surface
- stale / imported `v_w`
- transport treated as independent scanned knobs instead of a coupled system
- unresolved choice of which `v/T` actually enters baryogenesis
- CP source still too ansatz-like

### Best elegant route

1. derive `T_n` from the existing bounce / effective-potential machinery
   using `S_3(T_n)/T_n ~ 140`
2. rebuild `v_w` on one reconciled native surface:
   - native Daisy EWPT
   - native / HTL `D_q*T`
   - native bounce wall profile
3. solve the **coupled** transport fixed point instead of scanning
   `D_q*T`, `v_w`, and `L_w*T` independently
4. derive the CP source from the wall profile / `Z_3` phase structure rather
   than compact ansatz form

### Why this beats brute force

The current “transport no-go” is not yet a theorem against the coupled system.
The first real non-compute target is to collapse the prefactor uncertainty by
deriving `T_n` and solving the coupled transport system on one reconciled
surface.

### Fallback if closure fails

Keep DM bounded as:

- strong derived numerator
- strong framework baryogenesis structure
- relic ratio derived up to `eta`

## 2. Renormalized `y_t`

### Honest current blocker

The live blocker is now singular:

- the framework-to-perturbative gauge crossover

The UV relation and its protection are strong; the missing piece is the map
from the raw lattice coupling to the effective low-energy gauge coupling that
should share the same boundary as `y_t`.

### Best elegant route

1. place the actual `Cl(3)` / `Z^3` Hamiltonian in a slowly varying SU(3)
   background field
2. do the same Schur-complement / Feshbach projection already verified on the
   real Hamiltonian
3. extract the induced low-energy gauge-kinetic coefficient
4. use that one-shot nonperturbative coefficient as the finite crossover map
5. keep `y_t / g_3 = 1/sqrt(6)` on that **effective** boundary
6. only then run the thresholded perturbative SM chain below the crossover

### Why this beats brute force

This is a finite matching theorem problem, not an open-ended step-scaling
campaign by default.

### Fallback if closure fails

Keep `y_t` bounded as:

- exact UV relation
- exact RG protection
- sub-percent Yukawa matching
- unresolved gauge crossover

## 3. CKM / quantitative flavor

### Honest current blocker

CKM is not blocked on “general lack of compute.” It is blocked on:

- absolute `c_23` / `S_23`
- sharp `c_13`
- the surviving rephasing-invariant phase

### Best elegant route

1. derive absolute `S_23` / `c_23` analytically from the existing
   sector-correction machinery, with no PDG back-calibration
2. derive `c_13` analytically from the full `3x3` NNI structure
   - Schur-complement / effective-mass-matrix route is preferred
3. derive the physical CKM phase from invariants built from the same
   EWSB-dressed mass matrices

### Why this beats brute force

The remaining unknowns are not a giant function space. They are a small number
of scalar coefficients plus one physical phase.

### Fallback if closure fails

Do one targeted compute program only on the single scalar that remains missing:

- absolute `K_23`
- or physical `c_13`

not a full-cluster “compute all of CKM” campaign.

## Recommended execution order

1. **DM first**
   - shortest path to a real theorem gain
   - the first concrete task is deriving `T_n`
2. **`y_t` second**
   - one clean finite matching theorem could close the lane
3. **CKM third**
   - still plausible analytically, but slightly more layered than DM/`y_t`
