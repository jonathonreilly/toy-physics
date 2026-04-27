# Self-Consistent Back-Reaction: Horizons from Geometry

**Date:** 2026-04-05
**Status:** proposed_retained positive — Poisson self-gravity produces absorption threshold

## Artifact chain

- [`scripts/backreaction_poisson.py`](../scripts/backreaction_poisson.py)
- [`scripts/backreaction_selfconsistent.py`](../scripts/backreaction_selfconsistent.py)
- [`scripts/backreaction_emergent_gamma.py`](../scripts/backreaction_emergent_gamma.py) (bounded negative)

## The idea

In GR: matter curves spacetime, spacetime guides matter. Here:
1. Propagate on fixed field -> amplitude distribution |psi|^2
2. |psi|^2 generates additional field: f_self = G * sum |psi(x)|^2 / |y-x|
3. Re-propagate on updated field
4. Iterate to self-consistency

Born rule holds at each step (linear propagator on fixed field).
The field evolves between steps.

## Results

### Critical G for absorption

| G | deflection | direction | escape |
| ---: | ---: | --- | ---: |
| 0.005 | +1.10e-02 | TOWARD | 1.025 |
| 0.010 | +1.11e-02 | TOWARD | 1.002 |
| **0.011** | — | — | **~1.000** |
| 0.012 | +1.12e-02 | TOWARD | 0.992 |
| 0.020 | +1.15e-02 | TOWARD | 0.949 |
| 0.050 | +1.07e-02 | TOWARD | 0.751 |
| 0.100 | +1.60e-02 | TOWARD | 0.486 |

### Key properties of the threshold

- **Gravity preserved**: deflection is TOWARD at ALL G values
- **Smooth transition**: escape decreases monotonically from 1.03 to 0.49
- **Field-strength dependence**: stronger external field resists absorption
  (s=0.001: escape=0.92, s=0.016: escape=1.09 at G=0.02)

### Born rule

Born |I3|/P = 8.4e-16 on the converged field at G=0.1. The self-consistent
field is fixed after convergence, so the propagator is linear.

### Bounded negatives

1. **Edge addition**: extra edges at high-amplitude nodes absorbs amplitude
   even without field. The absorption is from topology change, not physics.
2. **Direct epsilon-gamma mapping**: back-reaction and complex action produce
   qualitatively similar physics but don't map quantitatively.

## What this means

The Poisson self-gravity produces a **gravitational collapse threshold**:
below G_crit ~ 0.011, the beam passes through with mild amplification.
Above G_crit, the beam is partially absorbed — a horizon-like effect.

This is the discrete analog of the Schrodinger-Newton equation.
The self-consistent field converges to a stable solution where:
- The beam curves toward the mass (gravity)
- Some amplitude is lost to the self-focused field (horizon)
- Born rule holds (linear propagation on converged field)

The complex action S = L(1-f) + i*gamma*L*f is the **effective theory**
of this back-reaction. It captures the qualitative physics (gravity +
absorption) in a single kernel, but gamma is not a simple function of G.
