# Continuum / Asymptotic Bridge Note

**Date:** 2026-04-01
**Purpose:** Separate finite-size artifacts from potentially retained
discrete structure. Gate C of the review-hardening backlog.

## What survives size growth

### Gravity (phase valley deflection)

| Dimension | N range tested | Signal at large N | Verdict |
|---|---|---|---|
| 2D modular | N=25-40 | delta=+2.5 at N=40 | Survives |
| 3D modular gap=3 | N=20-100 | t=+2.98 at N=100 | **Survives (weakening)** |
| 4D modular gap=3 | N=20-40 | t=+9.32 at N=40 | Survives (limited range) |

**Scaling behavior:** Gravity signal weakens at large N but stays
positive and significant through the tested range. At N=100 in 3D
(t=2.98), the signal is still above 2 SE. The weakening is gradual,
not a sharp cutoff.

**Verdict: SURVIVES.** Gravity is not a finite-size artifact.

### Decoherence (CL bath purity)

| Dimension | Best pur_cl | N range | Large-N trend |
|---|---|---|---|
| 2D modular | 0.885 (N=30) | N=12-100 | Stable ~0.94 for N≥40 |
| 3D modular | 0.849 (N=40-100) | N=12-100 | Stable ~0.85 |
| 4D modular gap=3 | 0.890 (N=80) | N=40-100 | Stable ~0.92 |
| 4D modular gap=5 | 0.911 (N=40) | N=40-100 | Stable ~0.94 |

**Scaling behavior:** Decoherence stabilizes to a family-dependent
floor. It does NOT collapse to pur_cl=1 through the tested range
on any modular family. The 3D floor (~0.85) is lower than 2D (~0.94).

**Important caveat:** The strict single-vs-double-slit visibility
gain (V_gain) is effectively flat at large N (~+0.005 for N≥40 in 3D).
The purity metric retains signal but the strictest interference-based
metric does not.

**Verdict: PARTIALLY SURVIVES.** Purity-based decoherence is stable.
Strict visibility gain does not survive.

### Born rule

| Dimension | I_3/P | N tested | Verdict |
|---|---|---|---|
| 2D grid | 4.7e-16 | N=40 | Machine precision |
| 3D chokepoint | 3e-16 | N=20-40 | Machine precision |
| 4D chokepoint | ~1e-16 | N=15-25 | Machine precision |

**Verdict: SURVIVES.** Born rule is exact for linear path-sum with
chokepoint barriers, at all tested sizes. This is a mathematical
property of linear amplitude propagation, not a finite-size effect.

### Mass scaling

| Dimension | Alpha | Convergence | Verdict |
|---|---|---|---|
| 3D (d=2 spatial) | 0.58 | YES (spread 0.083) | **Converges** |
| 4D (d=3 spatial) | 0.35-1.64 | NO (spread > 0.3) | **Does not converge** |

**Verdict: PARTIALLY SURVIVES.** 3D mass scaling has a proper
continuum limit (alpha → 0.58). 4D does not — alpha remains
parameter-sensitive across tested densities.

## What weakens with size

### Distance scaling (b-dependence)

b-independent at all sizes, all dimensions, all graph families.
This is structural, not a finite-size artifact. Tested at densities
from 15 to 120 nodes/layer with no change.

**Verdict: STRUCTURAL LIMITATION.** Does not weaken because it
was never there.

### Emergence (self-regulating gap)

| Rule | Useful N window | Large-N fate |
|---|---|---|
| Fixed threshold (2D) | N=40 marginal | CLT kills at N=80 |
| Fixed threshold (3D) | N=50 | Over-prunes at N=60 |
| Adaptive quantile (3D uniform) | **N=80** | Fails at N=100 |
| Adaptive quantile (3D hierarchical) | **N=80** | delta=-0.023 |
| Imposed modular gap | N=80 (3D), N=100 (4D) | Stable in range |

**Updated verdict: PARTIALLY SURVIVES through N=80 (sparse base) and
N=120 (dense base npl=60).** The adaptive quantile rule sustains
decoherence improvement on uniform 3D DAGs. Dense+prune extends the
window to N=120 (delta=-0.015, all seeds valid). Gravity is preserved
under pruning (t=4.0 vs 3.3 unpruned).

Birth/death and amplitude-guided growth did not improve over pruning.
Slit-conditioned growth failed (measurement incompatible with grown
topology). Dense+prune is the strongest retained emergence result.

**Caveats from review:**
- The smart-prune vs adaptive-quantile comparison does not actually
  compare two distinct algorithms (both call the same function)
- Mass scaling claims on pruned graphs are retracted (mass-position
  confound confirmed)
- The hierarchical alpha=0.71 is exploratory (not fixed-position clean)

### Strict visibility gain

In 3D modular gap=3, the strict single-vs-double-slit visibility
gain averages +0.005 for N≥40 — effectively zero. The broader
detector-profile contrast stays high, but the strictest metric
doesn't survive size growth.

**Verdict: VANISHES.** Strict visibility gain is a finite-size
artifact on the retained family.

## What is a discrete-family artifact

### 4D mass exponent

The alpha=1.07 ("F~M") result at one density point (npl=25, gap=5)
does not survive density variation. Alpha ranges from 0.35 to 1.64
across tested densities at gap=5. The "Newtonian" claim was a
parameter-specific result, not a universal feature.

### Preferential attachment gravity

Gravity works on uniform, hierarchical, and modular DAGs but fails
on preferential-attachment DAGs at N≥20. The hub_boost threshold
(~2.0) is family-specific — it's a property of the connectivity
distribution, not the propagator.

## Summary table

| Property | Finite-size artifact? | Survives scaling? |
|---|---|---|
| Gravity (attraction) | No | Yes (weakening) |
| Born rule | No | Yes (exact) |
| CL bath purity floor | No | Yes (family-dependent) |
| Mass scaling (3D) | No | Yes (converges to 0.58) |
| Cross-family gravity | No | Yes (4/5 families) |
| Distance law (b-indep) | No | N/A (structural) |
| Strict visibility gain | **Yes** | **No (vanishes at large N)** |
| Mass scaling (4D) | **Partially** | **Doesn't converge** |
| Emergence (gap dynamics) | **Partially** | **Sustains to N=80, wall at N=100** |

## What this means for the model

The retained results are:
1. Phase-valley gravity (survives, weakens slowly)
2. Born rule (exact, mathematical)
3. CL bath decoherence floor (stable, family-dependent)
4. 3D mass scaling continuum limit (alpha → 0.58)
5. Cross-family robustness (4 of 5 families)

The provisional/retracted results are:
1. 4D "F~M" mass scaling (parameter-sensitive)
2. Strict visibility gain (vanishes at large N)
3. Asymptotic emergence (N=80 on 3D, but N=100 is the wall)

The structural limitations are:
1. Distance law (b-independent, no avenue rescues it)
2. CLT convergence (eventually defeats all emergence rules)
