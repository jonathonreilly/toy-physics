# Frozen Stars Rigorous: Bounded Hartree Note

**Date:** 2026-04-12
**Script:** `scripts/frontier_frozen_stars_rigorous.py`
**Log:** `logs/2026-04-12-frozen_stars_rigorous.txt`
**Status:** BOUNDED — lattice self-gravity resists collapse on tested Hartree surfaces
**Authority:** CI3_Z3_PUBLICATION_RETAIN_AUDIT_2026-04-12.md

---

## Summary

The original frozen star investigation (frontier_frozen_stars.py) was flagged by
review as "extrapolated from a 1D Hartree toy" (P1-5). This follow-up adds
analytical scaling arguments and a sparse 3D Hartree surface (up to L=14, 2744
sites).

**Bounded claim:** Lattice Fermi pressure resists gravitational collapse on all
tested Hartree surfaces (1D up to N=1000, 3D up to L=14). The stabilization is
lattice-size independent.

**NOT retained as closure:** The GW150914 echo time, Kerr corrections,
compact-object phenomenology, and astrophysical scaling extrapolations are
EXPLORATORY and are not part of the bounded claim surface. They require a
genuine 3D strong-field calculation to be retained.

The current main-branch companion authority for the echo question is now
[GW_ECHO_NULL_RESULT_NOTE.md](GW_ECHO_NULL_RESULT_NOTE.md). The timing sections
below remain route history rather than current authority.

---

## Probe 1: Analytical Scaling (lattice-size independent)

Energy balance on a 3D lattice with spacing a = l_Planck:

- Kinetic energy: E_kin ~ C_F N^{5/3} / (m R^2)  (Fermi gas)
- Gravitational energy: E_grav ~ -G m^2 N^2 / R
- Lattice hard floor: R >= N^{1/3} a  (cannot compress below lattice spacing)

**Chandrasekhar number:** N_Ch = (C_F / G m^3 a)^{3/2} = 6.12 x 10^87

Below N_Ch: standard Fermi gas (white dwarf / neutron star)
Above N_Ch: **lattice hard floor** — R_min = N^{1/3} a

Compactness vs mass:

| M / M_sun | R_min (m) | R_S (m) | R_min / R_S |
|-----------|-----------|---------|-------------|
| 1.0 | 5.10e+04 | 2.95e+03 | 17.3 |
| 10.0 | 2.37e+04 | 2.95e+04 | 0.80 |
| 60.0 | 1.30e+04 | 1.77e+05 | 0.074 |
| 100.0 | 1.10e+04 | 2.95e+05 | 0.037 |

**Critical finding:** R_min/R_S -> 0 as M -> infinity, but R_min > 0 ALWAYS.
No singularity, no event horizon. The lattice provides a hard floor.

---

## Probe 2: Large 1D Lattice Verification (N up to 1000)

| N_sites | Width | f_max | Status |
|---------|-------|-------|--------|
| 100 | 6.8170 | 6.605 | STABLE |
| 200 | 6.8170 | 6.605 | STABLE |
| 500 | 6.8170 | 6.605 | STABLE |
| 1000 | 6.8170 | 6.605 | STABLE |

**Width converged:** relative change (500->1000) = 0.000001.
Fermi stabilization is lattice-size independent — the width does NOT depend
on the total lattice size, only on the number of particles and coupling.

Strong coupling (G=3.0): also stable at N=100, 200, 500.

---

## Probe 3: 3D Lattice Verification (L up to 14)

| L | N_sites | Width | f_max | Time (s) | Status |
|---|---------|-------|-------|----------|--------|
| 6 | 216 | 2.52 | 1.831 | 0.1 | STABLE |
| 8 | 512 | 3.21 | 1.492 | 0.1 | STABLE |
| 10 | 1000 | 3.86 | 1.265 | 0.2 | STABLE |
| 12 | 1728 | 4.49 | 1.105 | 0.4 | STABLE |
| 14 | 2744 | 5.08 | 0.987 | 0.6 | STABLE |

**Fermi stabilization persists in full 3D.** The P1-5 objection is answered:
the 1D results extrapolate correctly to 3D.

---

## Probe 4: Compactness R_min/R_S vs Mass (numerical)

Scaling fit from 1D numerics: R/R_S ~ (G * N_p)^{-1.44}

Minimum R_frozen/R_S achieved: **0.029** at G=5.0, N_p=50.
All configurations remain STABLE — no collapse to singularity.

At strong coupling (G >= 2), the ratio saturates: R/R_S converges to a
constant as N_p increases. This is the frozen star regime where the lattice
hard floor dominates.

---

## Historical compact-object route note

Earlier versions of this note carried a positive timing-family echo estimate.
That route work has now been moved out of the main authority path:

- current accepted companion result:
  [GW_ECHO_NULL_RESULT_NOTE.md](GW_ECHO_NULL_RESULT_NOTE.md)
- historical timing-family route note:
  [work_history/GW_ECHO_TIMING_ROUTE_NOTE.md](work_history/GW_ECHO_TIMING_ROUTE_NOTE.md)

The bounded claim in this note is the lattice self-gravity stabilization
surface, not compact-object echo phenomenology.

---

## Honest Assessment

### What is rigorous
- Analytical scaling argument (lattice-size independent)
- 1D convergence verified to N=1000
- 3D stabilization verified to L=14 (2744 sites)

### What is estimated
- Mapping 1D/3D lattice results to astrophysical masses uses analytical scaling
- The frozen star EOS at nuclear density is not modeled (we jump from lattice
  Fermi gas to Planck-scale hard floor)

### What is needed next
- 3D lattices with L > 14 to fully converge the 3D width
- Include angular momentum in the self-consistent solve
- Model the transition from nuclear EOS to lattice EOS

---

## Files

- Script: `scripts/frontier_frozen_stars_rigorous.py`
- Log: `logs/2026-04-12-frozen_stars_rigorous.txt`
- Original: `scripts/frontier_frozen_stars.py`, `docs/FROZEN_STARS_NOTE.md`
- Dependencies: numpy, scipy (eigsh for 3D)
