# Claude Complex-Action Carryover Note

**Date:** 2026-04-05  
**Status:** proposed_retained narrow carryover of the branch exact-lattice complex-action
harness

## Artifact chain

- [`scripts/exact_lattice_complex_action_carryover.py`](/Users/jonreilly/Projects/Physics/scripts/exact_lattice_complex_action_carryover.py)
- [`logs/2026-04-05-exact-lattice-complex-action-carryover.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-exact-lattice-complex-action-carryover.txt)

## Question

Can the strongest narrow part of Claude's branch-side complex-action story be
carried onto `main` without importing the broader, weaker claims?

This carryover stays deliberately narrow:

- exact ordered 3D lattice family only
- one fixed instantaneous field family
- exact `gamma = 0` reduction check
- Born test on the frozen field
- one crossover sweep in `gamma`

It does **not** claim geometry independence, continuum closure, or a retained
effective-theory derivation from self-gravity.

## Frozen result

Exact-lattice replay at `h = 0.5`, `W = 6`, `L = 30`, `s = 0.1`, `z_src = 3`:

- exact `gamma = 0` reduction:
  - baseline deflection: `+9.339748e-02`
  - complex-action at `gamma = 0`: `+9.339748e-02`
- Born on the frozen field:
  - `gamma = 0.0`: `|I3|/P = 2.409e-15`
  - `gamma = 0.5`: `|I3|/P = 3.941e-16`
  - `gamma = 1.0`: `|I3|/P = 1.236e-16`
- crossover sweep:

| `gamma` | deflection | direction | escape |
| --- | ---: | --- | ---: |
| `0.00` | `+9.339748e-02` | `TOWARD` | `2.7311` |
| `0.05` | `+3.863016e-02` | `TOWARD` | `2.0970` |
| `0.10` | `-1.791678e-02` | `AWAY` | `1.6119` |
| `0.20` | `-1.353356e-01` | `AWAY` | `0.9558` |
| `0.50` | `-5.075192e-01` | `AWAY` | `0.2056` |
| `1.00` | `-1.133647e+00` | `AWAY` | `0.0177` |

The transition lies between `gamma = 0.05` and `0.10` on this family.

## Safe read

The strongest honest statement is:

- the branch exact-lattice complex-action harness survives a narrow replay on
  `main`
- exact `gamma = 0` reduction is preserved
- Born stays machine-clean on the frozen field
- increasing `gamma` drives a clean `TOWARD -> AWAY` crossover while detector
  escape falls sharply

## What this is not

- It is not a geometry-generic complex-action result.
- It is not a continuum theorem.
- It is not evidence that complex action is the retained effective theory of
  Poisson self-gravity.

The grown-geometry and broader effective-theory language stay branch-side until
they earn their own hardened artifact chains.

## Final verdict

**retained narrow carryover**
