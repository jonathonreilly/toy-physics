# Nonlinear Propagator Breaks Born Rule and Gravity Simultaneously

## Result

A nonlinear modification to the path-sum propagator simultaneously
breaks the Born rule (I_3 != 0) and produces wrong gravitational
physics (repulsive force). The Born rule and attractive Newtonian
gravity are both consequences of linear amplitude superposition.

## Method

Three propagator types tested on a lattice:

1. **Linear**: psi_out = sum K_ij * psi_in(j)
2. **Quadratic**: psi_out = sum K_ij * |psi_in(j)| * psi_in(j)
3. **Cubic**: psi_out = sum K_ij * psi_in(j)^3

For each, measured the Sorkin parameter I_3 via a three-slit geometry
(2D, 20x21 lattice) and gravitational deflection via propagation
through a 1/r potential (2D, 40x60 lattice, weak-field regime).

## Key Table

| Propagator | I_3/P     | beta  | alpha | Force sign |
|------------|-----------|-------|-------|------------|
| Linear     | < 1e-16   | 1.014 | 1.27  | attractive |
| Quadratic  | 1.94e-01  | 0.997 | 1.63  | REPULSIVE  |
| Cubic      | 2.35e-01  | 0.992 | 1.32  | REPULSIVE  |

## Interpretation

The linear propagator produces I_3 = 0 (to machine precision) and
attractive gravity with beta = 1 (mass law). Both nonlinear
propagators produce I_3 >> 0 and repulsive gravity. The force sign
flip is the clearest signal: amplitude linearity determines both
whether interference is pairwise (Born rule) and whether gravity
attracts.

The mass exponent beta stays near 1.0 for all propagators because
beta comes from the linearity of the Poisson equation (field ~ M),
which is unchanged. The propagator nonlinearity instead shows up in
the force sign and distance exponent.

## Experimental Implication

The diamond NV Born-rule experiment (Sorkin test near a mass) is
framework-specific: measuring I_3 = 0 in a gravitational field
simultaneously confirms both the quantum and gravitational sectors.

## Script

`scripts/frontier_nonlinear_born_gravity.py`
