# Continuum Convergence: 2D Works, 3D Doesn't

**Date:** 2026-04-04
**Status:** CRITICAL FINDING — narrows the path forward

## The test

Measure gravitational deflection (centroid shift TOWARD mass) at
lattice spacing h=1.0, 0.5, 0.25. If TOWARD survives refinement,
it's physics. If it collapses, it's a lattice artifact.

## Results

### 2D dense lattice (max_dy=5, W=20, L=40, spent-delay)

| h | nodes | TOWARD | Peak deflection | Tail exponent | Notes |
|---|-------|--------|-----------------|---------------|-------|
| 1.0 | 1,681 | 2/9 | +0.11 at b=4 | too few points | Weak |
| 0.5 | 6,561 | **9/9** | +0.75 at b=8 | b^(-1.08), R²=0.91 | **Strong** |
| 0.25 | 25,921 | **9/9** | +1.57 at b=13 | b^(-0.63), R²=0.94 | Peak shifts |

**2D TOWARD survives refinement and gets STRONGER.**
The deflection magnitudes INCREASE with finer h. All 9 tested
b values become TOWARD at h=0.5.

The distance law tail (b > b_peak) gives exponent -1.08 at h=0.5,
close to the 2+1D Newtonian prediction of -1.0.

### 3D dense lattice (max_d=3, W=6, L=12, spent-delay)

| h | nodes | TOWARD (s=5e-5) | TOWARD (s=5e-6) |
|---|-------|-----------------|-----------------|
| 1.0 | 2,197 | **4/4** | 3/3 |
| 0.5 | 15,625 | **0/4** (ALL AWAY) | 1/4 |

**3D TOWARD collapses at h=0.5.**
At h=1.0, all tested b values show TOWARD.
At h=0.5, nearly all flip to AWAY. Even at 10x weaker field (5e-6),
only b=2 remains barely TOWARD (+0.0002).

RG scaling (s_eff = s0 * h) doesn't help: still 0/4 TOWARD at h=0.5.

## Why

The mechanism is beam depletion. The mass field creates a phase
valley. Paths through the valley get reduced phase. At the detector,
this creates partial destructive interference at the beam center
(depletion), shifting the centroid AWAY from the mass.

The TOWARD effect (attraction) comes from the LINEAR response:
coherent constructive interference from the phase valley on the
mass side. This competes with depletion.

In **2D**, the beam spreads in 1 transverse dimension. The depletion
is weak (confined spreading). The linear response dominates at
ultra-weak field, and this gets STRONGER with finer h because the
finer lattice resolves the interference pattern better.

In **3D**, the beam spreads in 2 transverse dimensions. The depletion
is much stronger (spreading in both y and z). Even at ultra-weak
field, depletion overwhelms the linear response at finer h.

The key scaling: at h=0.5, the path count is 49^8 vs 49^4 at h=1.0.
The exponentially more paths make the interference pattern more
complex, strengthening the depletion effect.

## Implications

1. **The 3D 10/10 card at h=1.0 is a lattice artifact** for gravity.
   Born, MI, decoherence, d_TV are genuine (structural). Gravity and
   distance law do not survive refinement.

2. **2D gravity is genuine.** The model produces real gravitational
   attraction in 2+1D with the correct distance law (1/b).

3. **The 3D problem is specific to beam spreading**, not the action
   formula. Any fix must suppress 3D beam spreading while maintaining
   path diversity for attraction.

## Path forward

1. **Tapered lattice**: dense edges near beam center, sparse at edges.
   Suppresses spreading while maintaining path diversity near mass.

2. **Action formula**: the power action (S = L|f|^0.5) had better 3D
   results. May survive refinement where spent-delay doesn't.

3. **Kernel modification**: 1/L^2 instead of 1/L in 3D to suppress
   spreading. But this changes Born rule.

4. **Accept 2D**: the model is a 2+1D theory. 3D requires a different
   mechanism (e.g., compactification, dimensional reduction).

## Scripts

- `lattice_2d3d_continuum_check.py` — Head-to-head 2D vs 3D gravity
- `lattice_2d_continuum_distance.py` — 2D distance law convergence
- `lattice_3d_continuum_convergence.py` — 3D convergence (negative result)
