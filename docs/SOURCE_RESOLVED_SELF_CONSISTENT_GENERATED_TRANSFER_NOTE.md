# Source-Resolved Self-Consistent Generated Transfer

**Date:** 2026-04-05  
**Status:** bounded no-go for transfer of the self-consistent Green pocket to the compact generated DAG family

## Artifact chain

- [`scripts/source_resolved_self_consistent_generated_transfer.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_self_consistent_generated_transfer.py)

## Question

Does the self-consistent Green pocket that survives on the exact lattice transfer
to the compact generated DAG family while preserving:

- exact zero-source reduction
- weak-field `TOWARD` sign
- near-linear mass scaling

This note is intentionally narrow:

- one family: compact generated 3D DAG family
- one candidate architecture: self-consistent source-resolved Green kernel
- one reduction check: zero-source returns free propagation exactly
- one comparison: instantaneous `1/r` field vs self-consistent Green field

## Frozen result

The frozen probe uses:

- family seeds `0..3`
- `N_LAYERS = 16`
- `NODES_PER_LAYER = 24`
- `CONNECT_RADIUS = 3.2`
- source strengths `s = 0.0001, 0.0002, 0.0004, 0.0008`
- kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.50`
- calibration gain `1.335386e+02`
- one self-consistency update from the source-cluster amplitudes

Reduction check:

- seed 0: `+0.000000e+00`
- seed 1: `+0.000000e+00`
- seed 2: `+0.000000e+00`
- seed 3: `+0.000000e+00`
- max `|zero-source shift| = 0.000e+00`

Frozen readout:

| `s` | instantaneous shift | self-consistent shift | self / inst | sign survival |
| --- | ---: | ---: | ---: | ---: |
| `0.0001` | `-6.835015e-02` | `-8.435233e-02` | `1.234` | `1/4` |
| `0.0002` | `-9.454729e-02` | `-8.893522e-02` | `0.941` | `1/4` |
| `0.0004` | `-1.282711e-01` | `-7.117551e-02` | `0.555` | `1/4` |
| `0.0008` | `-1.673655e-01` | `-4.548761e-02` | `0.272` | `1/4` |

Fitted exponents:

- instantaneous `F~M`: `0.43` or lower-level noisy negative class
- self-consistent Green `F~M`: `0.00`-class collapse on the retained sweep

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives on the compact generated DAG family
- the self-consistent Green field remains nontrivial
- but the generated-family readout is `AWAY`, not `TOWARD`
- and the strength dependence does not preserve the Newtonian linear class

## Honest limitation

This is a clean no-go for the generated-family transfer of the self-consistent
Green architecture.

- the exact-lattice self-consistent pocket does **not** transfer to the compact
  generated DAG family in the retained weak-field class
- sign and linear scaling do not survive together on the generated family
- so the transfer is not a hidden positive waiting to be promoted

## Branch verdict

Treat this as the generated-geometry answer for the self-consistent Green
candidate:

- exact reduction survives
- amplitude survives
- weak-field gravity sign does not
- Newtonian mass scaling does not
