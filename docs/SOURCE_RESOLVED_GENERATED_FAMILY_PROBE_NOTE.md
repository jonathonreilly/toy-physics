# Source-Resolved Generated Family Probe

**Date:** 2026-04-05  
**Status:** bounded no-go for transfer of the source-resolved Green pocket to the compact generated DAG family

## Artifact chain

- [`scripts/source_resolved_generated_family_probe.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_generated_family_probe.py)
- [`logs/2026-04-05-source-resolved-generated-family-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-generated-family-probe.txt)

## Question

Does the source-resolved Green-pocket architecture that survives on the exact
lattice transfer to the compact generated DAG family while preserving:

- exact zero-source reduction
- weak-field `TOWARD` sign
- near-linear mass scaling

This note is intentionally narrow:

- one family: compact generated 3D DAG family
- one candidate architecture: source-resolved Green-like kernel
- one reduction check: zero-source returns free propagation exactly
- one comparison: instantaneous `1/r` field vs Green-kernel field

## Frozen result

The frozen probe uses:

- family seeds `0..3`
- `N_LAYERS = 16`
- `NODES_PER_LAYER = 24`
- `CONNECT_RADIUS = 3.2`
- source strengths `s = 0.0001, 0.0002, 0.0004, 0.0008`
- kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.50`
- calibration gain `3.338465e+01`

Reduction check:

- seed 0: `+0.000000e+00`
- seed 1: `+0.000000e+00`
- seed 2: `+0.000000e+00`
- seed 3: `+0.000000e+00`
- max `|zero-source shift| = 0.000e+00`

Frozen readout:

| `s` | instantaneous shift | Green-kernel shift | Green / inst | sign survival |
| --- | ---: | ---: | ---: | ---: |
| `0.0001` | `-6.835015e-02` | `-9.011916e-02` | `1.318` | `3/4` |
| `0.0002` | `-9.454729e-02` | `-1.246389e-01` | `1.318` | `3/4` |
| `0.0004` | `-1.282711e-01` | `-1.662177e-01` | `1.296` | `3/4` |
| `0.0008` | `-1.673655e-01` | `-2.059969e-01` | `1.231` | `3/4` |

Fitted exponents:

- instantaneous `F~M`: `0.43`
- Green-kernel `F~M`: `0.40`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives on the compact generated DAG family
- the Green-kernel field remains nontrivial and stronger than the instantaneous
  comparator in amplitude
- but the generated-family readout is `AWAY`, not `TOWARD`
- and the strength dependence is not close to the Newtonian linear class

## Honest limitation

This is a clean no-go for the generated-family transfer of this architecture.

- the exact-lattice Green pocket does **not** transfer to the compact
  generated DAG family in the retained weak-field class
- sign and exponent both fail together on the generated family
- so the transfer is not a hidden positive waiting to be promoted

## Branch verdict

Treat this as the generated-geometry answer for the strongest current
coupled-field candidate:

- exact reduction survives
- amplitude survives
- weak-field gravity sign does not
- Newtonian mass scaling does not

