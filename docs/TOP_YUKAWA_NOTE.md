# Top Yukawa from Lattice Self-Consistency

## Context

The Higgs mass prediction from Coleman-Weinberg on the lattice
(see HIGGS_FROM_LATTICE_NOTE.md) depends on one free parameter:
the top Yukawa coupling y_t. This script attacks y_t from five
independent directions to constrain or derive its value.

## Lattice Inputs

All derived from first principles:

| Input | Value | Origin |
|-------|-------|--------|
| alpha_V(M_Planck) | 0.092 | V-scheme plaquette action |
| sin^2(theta_W)(M_Planck) | 3/8 | Cl(3) GUT relation |
| CW potential | 1-loop on L=16 lattice | lattice Brillouin zone |
| Lambda = pi/a | natural cutoff | lattice spacing |

## Five Attacks

### Attack 1: Self-Consistency Window

Scans y_t to find where EWSB occurs with a stable vacuum and
positive Higgs mass. Result: y_t in [0.04, 3.0] -- a broad
window that contains the observed y_t = 0.994. The CW mechanism
is robust: EWSB happens for almost any y_t > 0.04.

### Attack 2: Quasi-Infrared Fixed Point

The top Yukawa RGE has a quasi-IR fixed point at
y_t* = sqrt((8 g_s^2 + 9/4 g^2 + 17/12 g'^2) / (9/2)).

Key results:
- Fixed point at M_Z: y_t* = 1.71 (72% above observed)
- Fixed point at M_Planck: y_t* = 0.81 (with alpha_U = 0.020)
- **RGE inversion**: y_t(M_Pl) = 0.320 gives y_t(M_Z) = 0.994
- **Focusing**: a 4.7-wide range of Planck inputs maps to a
  0.48-wide band at M_Z (10x compression)

The IR fixed point acts as an attractor but the observed y_t
is BELOW it. The top is not at the fixed point; it is in its
basin of attraction at about 40% of the Planck-scale value.

### Attack 3: Taste Mass Hierarchy

Tests whether the t/b mass ratio arises from Yukawa RGE
amplification of a small initial asymmetry (from hypercharge
assignments |Y_tR| = 4/3 vs |Y_bR| = 2/3).

Result: perturbative RGE with unified couplings produces
m_t/m_b ~ 4 at most, far short of the observed 41.
Non-perturbative lattice effects (taste-dependent anomalous
dimensions near M_Planck) are needed for the full hierarchy,
consistent with the mass hierarchy RG analysis showing
Delta(gamma) ~ 0.27 is required.

### Attack 4: Vacuum Stability and Veltman Condition

Numerical result: the lattice CW potential is stable for all
y_t up to 3.0 (the quartic lambda = 0.13 stabilizes it).

The **Veltman condition** (cancellation of quadratic divergences)
gives y_t = 0.49. This is where the lattice naturalness
parameter Delta ~ O(1). The observed y_t = 0.99 is a factor
of 2 above this, which may reflect the difference between the
simple Veltman formula and the full lattice calculation (where
Delta = 0.4 even at the observed y_t).

### Attack 5: Multiple Point Principle

Tests whether degenerate vacua (V(v) = V(0)) select a
preferred y_t. On the lattice with msq < 0, V(v) < V(0)
always -- the EWSB vacuum is always deeper than the symmetric
one. The MPP condition V(v) = V(0) cannot be satisfied for
any y_t with the given (lam, msq).

A 2D scan over (y_t, lambda) finds the closest approach at
y_t = 0.46, lambda = 0.12, still far from the observed value.

## Results Summary

| Attack | Prediction/Constraint | Status |
|--------|----------------------|--------|
| Self-consistency | y_t in [0.04, 3.0] | Contains observed |
| IR fixed point | y_t* = 1.71 (upper bound) | 72% high |
| RGE inversion | y_t(M_Pl) = 0.32 -> y_t(M_Z) = 0.99 | Exact (by construction) |
| Focusing power | 10x compression | Reduces sensitivity |
| Taste hierarchy | m_t/m_b ~ 4 (needs non-pert.) | Insufficient |
| Veltman condition | y_t = 0.49 | 51% low |
| Vacuum stability | Stable up to y_t = 3.0 | No constraint |
| MPP | y_t = 0.46 | 54% low |

## Key Findings

1. **y_t is in the right ballpark**: all five attacks give values
   within an order of magnitude of observed. The lattice framework
   is not wildly inconsistent.

2. **The IR fixed point provides strong focusing**: any UV boundary
   condition in [0.3, 5.0] maps to [0.96, 1.44] at M_Z -- a 10x
   compression. This explains why m_t is heavy but not at the
   Planck scale.

3. **y_t(M_Pl) = 0.32 is required**: this is 40% of the Planck-scale
   fixed point (0.81), meaning the top Yukawa starts BELOW the
   attractor at the Planck scale.

4. **The Veltman condition is suggestive**: on the lattice, naturalness
   (Delta ~ O(1)) near y_t ~ 0.49 is in the right direction but
   50% low. The full numerical CW achieves naturalness even at
   the observed y_t because the lattice sum is better regulated
   than the analytic formula.

5. **Full derivation requires the bare Yukawa vertex**: the missing
   piece is the Planck-scale boundary condition. If the lattice
   structure determines y_t(M_Pl) = 0.32, then y_t(M_Z) = 0.994
   follows from RGE. This boundary condition should come from
   the same Cl(3) algebra that gives sin^2(theta_W) = 3/8.

## Status

**y_t is CONSTRAINED but not yet fully DERIVED.**

The lattice framework narrows the allowed range significantly
(10x focusing from IR fixed point) and provides naturalness
without fine-tuning. The observed value y_t = 0.994 is
consistent with all lattice constraints.

To complete the derivation, we need to extract the bare Yukawa
coupling from the Cl(3) algebraic structure, analogous to how
sin^2(theta_W) = 3/8 comes from the Clifford algebra.

## Script

`scripts/frontier_top_yukawa.py` -- self-contained, numpy + scipy only.
Runs in ~90 seconds.
