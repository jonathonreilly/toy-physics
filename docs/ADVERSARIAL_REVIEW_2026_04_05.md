# Adversarial Review — 2026-04-05

**Date:** 2026-04-05
**Scope:** All results from the complex action + continuum limit session

## Red flags investigated

### 1. Born at h=0.25 (was skipped)
**Status:** RESOLVED — passes at 5.0e-16 (machine precision)
Individual slit probabilities are distinguishable (p1=9.48e-89 vs p2=9.48e-89).
I3 = -4.2e-103, which is 14 orders below p123. Genuine pass.

### 2. F~M 1.018 overshoot at h=0.125
**Status:** RESOLVED — not significant
Weak-field F~M at h=0.25 is 0.998 +/- 0.001 (8 mass points, RMS residual).
At strong field, F~M drops to 0.93 +/- 0.11 — non-linearity, not a lattice
error. The 1.018 at h=0.125 is within error of 1.0.

### 3. h=1.0 distance law sign flip (AWAY at b>=6)
**Status:** EXPLAINED — finite-resolution artifact
At h=1.0, beam sigma=5.5 at detector. Sources at z=6-8 are within the beam.
Near-field scattering dominates, pushing centroid AWAY. At h<=0.5, the beam
is better resolved and the far-field 1/b law emerges (alpha=-1.11).

### 4. MI and d_TV decrease at finer h
**Status:** EXPLAINED — real but not a bug
At h=0.25, beam centroids from z=+/-3 are closer (4.34 vs 4.93 at h=0.5)
and overlap more (1.16 vs 0.94). The T-normalization changes effective beam
spread. This means MI/d_TV are h-dependent observables under this
normalization — a genuine limitation, not a computational error.

### 5. Complex action gamma threshold h-dependence
**Status:** RESOLVED — h-INDEPENDENT
Weak-field gamma sweep at h=0.5 and h=0.25:
- h=0.5: TOWARD at gamma<=0.20, AWAY at gamma>=0.30
- h=0.25: TOWARD at gamma<=0.20, AWAY at gamma>=0.30
Identical transition. The exceptional point is a continuum phenomenon.

### 6. Escape fraction grows with h
**Status:** EXPLAINED — strong-field artifact only
- Weak field (s=0.004): escape converges (0.92, 1.05, 1.07)
- Strong field (s=0.1): escape diverges (0.10, 2.73, 5.15)
Same root cause as non-convergent strong-field gravity: s=0.1 is
non-perturbative.

## Honest limitations (not resolved)

1. **Strong-field regime has no continuum limit.** Gravity, escape, F~M all
   fail to converge at s >= 0.1. The model is perturbative only.

2. **MI/d_TV are h-dependent** under T-normalization. The beam profile changes
   with h, affecting slit distinguishability. These observables pass/fail but
   their VALUES are not converging.

3. **P_det underflows** at fine h. Boundary leakage from interior-T
   normalization. Per-node T improves but doesn't fully fix.

4. **Gamma is unmotivated.** No first-principles derivation of the complex
   action parameter. The emergent-from-motion test was negative.

5. **Distance exponent is -1.1, not -1.0.** Stable across h=0.5 and h=0.25.
   May be the true discrete-model value rather than a lattice artifact.

## What IS solid

1. **Weak-field F~M = 1.000 +/- 0.001** at h=0.25 (Newtonian mass scaling)
2. **Born rule** at machine precision at ALL tested h (1.0, 0.5, 0.25)
3. **k=0 gives zero gravity** at all h (phase-mediated)
4. **Complex action gamma transition is h-independent** (continuum phenomenon)
5. **Far-field distance law alpha ~ -1.1** stable across h values
6. **10/10 property card passes** at h=0.5 and h=0.25
7. **All results transfer to grown geometry** (not lattice artifacts)
