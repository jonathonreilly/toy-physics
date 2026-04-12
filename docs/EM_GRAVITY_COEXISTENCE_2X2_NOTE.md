# Gravity + EM Coexistence 2x2 Factorial Control

**Status:** bounded-retained  
**Runner:** `scripts/em_gravity_coexistence_2x2.py`  
**Gate:** Promotion Playbook section 4a (2026-04-12)

## Surface

- 16^3 open cubic lattice (4096 sites)
- Poisson-solved gravitational field f(r) (point source at center)
- Coulomb potential V(r) = Q/r (same source position)
- Path-sum (ray-sum) propagator: rays along x, deflection = dPhi/db

## Design

Four cells on the same surface, same ray geometry:

| Cell    | Gravity | EM  | Action per step                   |
|---------|---------|-----|-----------------------------------|
| H0      | off     | off | k                                 |
| Hg      | on      | off | k(1-f)                            |
| Hem     | off     | on  | k + qV                            |
| Hg+Hem  | on      | on  | k(1-f) + qV                      |

Readout: ray deflection = Phi(b+1) - Phi(b), where Phi(b) is the
accumulated action along a ray at impact parameter b from the source.

## Decision Statistic

Mixed residual:

    R_GE = defl(Hg+Hem) - defl(Hg) - defl(Hem) + defl(H0)

By linearity of action accumulation:

    S(Hg+Hem) = k(1-f) + qV
    S(Hg) + S(Hem) - S(H0) = k(1-f) + (k + qV) - k = k(1-f) + qV

So R_GE = 0 exactly.

## Results

Measured across b = 2..6, both q = +3 and q = -3:

- R_GE(q+): max |R| = 1.4e-14 (machine epsilon)
- R_GE(q-): max |R| = 1.4e-14 (machine epsilon)
- |R_GE / delta_g|: < 1.5e-13

All residuals are at floating-point noise level.

## Secondary Checks

- **EM +/- cancellation (pure EM):** delta_em(q+) + delta_em(q-) = 0 to
  machine precision at all b.
- **EM +/- cancellation (joint cell):** defl(Hg+E+) + defl(Hg+E-) - 2*defl(Hg)
  = 0 to machine precision. Turning on EM does not break gravity symmetry.
- **Gravity sign:** Positive deflection (consistent sign at all b), nonzero.
- **EM opposite signs:** q+ and q- produce opposite deflections at all b.

## What Is Supported

- On the path-sum ray propagator, gravity and EM enter through additive
  contributions to the action. The 2x2 mixed residual is exactly zero
  by linearity of action accumulation.
- Charge-sign cancellation is exact in both the pure-EM and joint cells.
- Neither sector interferes with the other: turning on EM does not change
  the gravity readout, and turning on gravity does not change the EM readout.

## What Is Not Supported

- This is a kinematic (ray-optics) result, not a dynamical wave-propagation
  result. The exact zero follows from linearity of the action sum, not from
  a nontrivial cancellation in a Hamiltonian evolution.
- No claim of coexistence in a single Hamiltonian with wave-packet dynamics
  (the staggered Hamiltonian has the epsilon sign issue for charge conjugation).
- No claim of gauge invariance or magnetic-sector coexistence.
- No claim about nonlinear or backreaction regimes.

## Remaining Closure

- A wave-packet-level (dynamical) coexistence control that also passes the
  2x2 residual test would strengthen this to a retained claim. The path-sum
  ray approach gives exact zero by construction; a Hamiltonian-evolution
  version would be a nontrivial test.
