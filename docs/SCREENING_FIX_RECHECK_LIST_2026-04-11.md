# Screening Fix Recheck List

**Date:** 2026-04-11
**Root cause:** μ²=0.22 gives screening length 2.13 sites. This Yukawa
screening was hiding Newton's law (exponent -3.15 instead of -2.02) and
killing long-range signals throughout the entire project.

**Fix:** μ²=0.001 gives screening length 31.6 sites. With this value,
Newton's 1/r² law is recovered (exponent -2.02 ± 0.07).

## MUST RECHECK (Results that were killed or weakened by screening)

### 1. Gravitational Memory
**Original:** +0.013 at N=61, vanished at N=101
**Diagnosis:** Yukawa screening killed the signal at large N
**Recheck:** Run memory test with μ²=0.001. The wave should propagate
without exponential attenuation. Memory might persist at large N.
**Priority:** HIGH — was the first result killed by screening

### 2. Two-Body Staggered (Partner Kick)
**Original:** Narrow periodic resonance only with μ²=0
**Note:** Already tested with μ²=0 (no screening) but on PERIODIC lattice.
Need recheck on OPEN BC staggered with μ²=0.001 (small but nonzero reg).
**Priority:** HIGH — the staggered partner-kick observable is cleaner

### 3. Decoherence Rate (Diosi-Penrose Scaling)
**Original:** d-scaling -0.80 vs DP's -1.0, G and mass scaling wrong
**Diagnosis:** Yukawa screening suppresses the potential at large d,
steepening the effective d-scaling beyond -1.0. With μ²=0.001, the
potential is 1/r out to d=31, so DP scaling might emerge.
**Priority:** HIGH — could close the trajectory lane

### 4. Hawking-Page Entanglement Crossover
**Original:** KILLED — G_c drifts with L (34% spread)
**Diagnosis:** Screening changes the effective coupling at each lattice
size differently. With unscreened field, the crossover might stabilize.
**Priority:** MEDIUM — was killed, might be recoverable

### 5. BH Entropy Exponent
**Original:** S ~ |bnd|^1.76, not |bnd|^1.0. Coefficient G-dependent.
**Diagnosis:** Screening modifies the Dirac sea spectrum differently at
different G. The super-area exponent might be a screening artifact.
**Priority:** MEDIUM

### 6. Self-Gravity Contraction Ratios
**Original:** w = 0.40-0.76 at μ²=0.22
**Recheck:** Do contraction ratios change at μ²=0.001? Probably weaker
(longer-range field = less concentrated potential), but the sign should
be the same.
**Priority:** LOW — sign selectivity is robust, magnitude may change

### 7. Anderson Phase Map
**Original:** Gravity real in G=[2,20] at 13.2σ
**Recheck:** The "gravity is real" window might shift with μ²=0.001.
The spatial correlations from the Poisson kernel change character.
**Priority:** MEDIUM

### 8. Sign Selectivity
**Original:** 300/300 at G=3-15
**Recheck:** Probably robust (sign comes from |ψ|²≥0, not screening).
But the WINDOW G=3-15 might shift.
**Priority:** LOW — expected to survive

### 9. Boundary-Law Coefficient
**Original:** 2.7σ from Anderson disorder at μ²=0.22
**Recheck:** The coefficient alpha might change. The 2.7σ separation
from disorder might increase (longer-range correlations = more distinctive).
**Priority:** MEDIUM — could strengthen the result

### 10. Shapiro Delay
**Original:** +Φ delays by 20-28 steps, -Φ by 2-5 steps (not sign-selective)
**Diagnosis:** Yukawa screening reduces Φ at the detector. With μ²=0.001,
the field reaches the detector at full strength. The delay ratio might
become sign-selective.
**Priority:** MEDIUM

### 11. Cycle Battery / Retarded Family Closure
**Original:** 9/9, 9/9, 8/9 on cycle families
**Note:** These use GRAPH-based Poisson, not lattice. The screening
parameter enters identically. Should recheck at μ²=0.001.
**Priority:** LOW — the scores are already good

### 12. CDT Spectral Flow
**Original:** Sigmoid R²>0.989, promoted
**Already being rechecked:** Agent 6 (CDT quantitative) is running with μ²=0.001
**Priority:** ALREADY IN PROGRESS

## ALREADY RECHECKED (Done with μ²=0.001)

- Newton's distance law: -2.02 ± 0.07 ← CONFIRMED
- Newton's mass law: R²=0.987 ← CONFIRMED (was done at μ²=0.22 but
  the mass test used external source, not self-consistent Poisson)

## DOES NOT NEED RECHECK

- Born rule alpha test (doesn't depend on μ²)
- Eigenvalue statistics (spectrum changes but the GOE/Poisson question is independent)
- Geometry superposition (uses prescribed Φ, not Poisson)
- Parity coupling correction (structural, not μ²-dependent)
- Theory reduction (2 axioms — μ² is a parameter, not an axiom)
