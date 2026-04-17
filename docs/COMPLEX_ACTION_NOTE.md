# Complex Action: Gravity + Horizons Unification

**Date:** 2026-04-05
**Status:** retained positive — complex action unifies gravity and horizons while preserving Born rule

## Artifact chain

- [`scripts/complex_action_harness.py`](../scripts/complex_action_harness.py)
- [`logs/2026-04-05-complex-action-harness.txt`](../logs/2026-04-05-complex-action-harness.txt)

## Question

Can a single complex-valued action unify gravity (real phase) and horizons
(imaginary decay) in one propagator kernel, while preserving the Born rule?

## Construction

The action is:

    S = L(1 - f) + i * gamma * L * f

where f is the gravitational field (s/r). The kernel becomes:

    exp(i*k*S) = exp(i*k*L*(1-f)) * exp(-k*gamma*L*f)

- Real part: standard valley-linear gravity (deflection toward source)
- Imaginary part: field-dependent amplitude decay (horizon) or growth (superradiance)
- gamma = 0: recovers the standard real-action propagator exactly

## Frozen results

### Gamma sweep (s=0.1, strong field)

| gamma | deflection | direction | escape |
| ---: | ---: | --- | ---: |
| -0.50 | +5.378e-01 | TOWARD | 43.59 |
| -0.20 | +2.896e-01 | TOWARD | 7.94 |
| 0.00 | +9.340e-02 | TOWARD | 2.73 |
| 0.05 | +3.863e-02 | TOWARD | 2.10 |
| 0.10 | -1.792e-02 | AWAY | 1.61 |
| 0.15 | -7.599e-02 | AWAY | 1.24 |
| 0.20 | -1.353e-01 | AWAY | 0.96 |
| 0.50 | -5.075e-01 | AWAY | 0.21 |
| 1.00 | -1.134e+00 | AWAY | 0.018 |
| 2.00 | -2.189e+00 | AWAY | 0.0002 |

### Born test (three-slit with gravitational field)

| gamma | |I3|/P |
| ---: | ---: |
| 0.0 | 2.0e-15 |
| 0.5 | 8.0e-16 |
| 1.0 | 2.4e-15 |

Machine-precision zero at all gamma values.

### Weak-field mass scaling (s = 0.001 to 0.008)

| gamma | F~M exponent | direction |
| ---: | ---: | --- |
| 0.00 | 0.991 | TOWARD |
| 0.05 | 0.986 | TOWARD |
| 0.10 | 0.977 | TOWARD |
| 0.20 | 0.811 | TOWARD |
| 0.50 | 1.018 | AWAY |
| 1.00 | 1.007 | AWAY |

### Reduction check

- Standard propagator delta: +9.340e-02
- Complex(gamma=0) delta: +9.340e-02
- Match: exact (within machine precision)

## Safe read

The retained statements:

1. **Born rule holds at machine precision for all gamma.** The propagator is
   linear in psi (the kernel depends on the field, not on the amplitude), so
   Born is structurally guaranteed regardless of gamma. This is confirmed
   numerically: |I3|/P < 3e-15 everywhere.

2. **Newtonian mass scaling F~M=1.0 is preserved** in both the attractive
   (TOWARD, gamma < 0.1) and absorptive (AWAY, gamma > 0.5) regimes. The
   weak-field exponents are 0.99 and 1.01 respectively.

3. **A clean exceptional point exists** at gamma ~ 0.08-0.10 (strong field)
   where gravity changes sign from TOWARD to AWAY. In the weak-field regime,
   the transition is broader (0.1 < gamma < 0.5) because the imaginary
   contribution scales with f.

4. **The escape fraction smoothly interpolates** from amplification (escape > 1
   for gamma < 0.2) through unity (gamma ~ 0.2) to deep absorption
   (escape = 0.0002 at gamma = 2.0).

5. **The AWAY direction is NOT anti-gravity.** It is the centroid shift caused
   by preferential absorption of near-source paths. The paths closest to the
   mass source experience the strongest field and therefore the strongest
   imaginary decay. The surviving paths are biased away from the source.

## What this means

The complex action is a one-parameter family that continuously interpolates
between:

- Pure gravity (gamma = 0): standard Newtonian deflection
- Gravity + weak horizon (gamma ~ 0.1): TOWARD with mild absorption
- Horizon-dominated (gamma > 0.5): AWAY with strong absorption

The key insight: **gravity and horizons are not separate phenomena** in this
model. They are the real and imaginary parts of a single complex action. The
Born rule holds throughout because linearity is preserved.

## Honest limitations

1. The TOWARD-to-AWAY transition at gamma ~ 0.08 is for a specific lattice
   (h=0.5, W=6, L=30). The threshold may shift at different resolutions.

2. The mass scaling breakdown at the exceptional point (F~M^0.81 at gamma=0.2)
   is expected: the real and imaginary contributions nearly cancel, making
   the residual scaling non-trivial.

3. This does NOT yet demonstrate actual black hole physics (photon sphere,
   Schwarzschild radius, Hawking radiation). It demonstrates the mechanism
   by which a complex action produces horizon-like behavior.

4. The gamma parameter is currently free. A physical prediction would require
   deriving gamma from the underlying theory (e.g., gamma ~ v/c for a
   moving source, or gamma ~ rs/r for a Schwarzschild-like solution).

## Next steps

- Check whether gamma can be derived from the lattice structure (rather than
  imposed by hand)
- Test on generated geometry (not just regular lattice)
- Look for photon sphere / light ring signature at intermediate gamma
- Check whether negative gamma (superradiance) has physical interpretation
