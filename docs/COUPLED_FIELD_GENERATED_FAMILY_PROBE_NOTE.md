# Coupled Field Generated Family Probe

**Date:** 2026-04-05  
**Status:** bounded no-go for the minimal source-driven coupled-field rescue on the compact generated DAG family

## Artifact chain

- [`scripts/coupled_field_generated_family_probe.py`](/Users/jonreilly/Projects/Physics/scripts/coupled_field_generated_family_probe.py)
- [`logs/2026-04-05-coupled-field-generated-family-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-coupled-field-generated-family-probe.txt)

## Question

Can a minimal source-driven coupled field on the retained compact generated DAG
family preserve the weak-field sign and linear mass scaling class?

This note is intentionally narrow:

- one family: compact generated 3D DAG family
- one candidate architecture: forward source-driven diffusion
- one reduction check: zero source should recover free propagation exactly
- one comparison: instantaneous `1/r` field versus source-driven field

## Frozen result

The retained compact family uses:

- `N_LAYERS = 16`
- `NODES_PER_LAYER = 24`
- `Y_RANGE = 10.0`
- `CONNECT_RADIUS = 3.2`
- `N_SEEDS = 4`
- source strengths `s = [1e-4, 2e-4, 4e-4, 8e-4]`

Reduction check:

- seed 0: `+0.000000e+00`
- seed 1: `+0.000000e+00`
- seed 2: `+0.000000e+00`
- seed 3: `+0.000000e+00`
- max `|zero-source shift| = 0.000e+00`

Frozen readout:

| `s` | instantaneous shift | coupled-field shift | coupled / inst | sign survival |
| --- | ---: | ---: | ---: | ---: |
| `0.0001` | `-6.968870e-02` | `-2.862755e-01` | `4.108` | `4/4` |
| `0.0002` | `-9.661772e-02` | `-3.103999e-01` | `3.213` | `4/4` |
| `0.0004` | `-1.314999e-01` | `-2.328980e-01` | `1.771` | `4/4` |
| `0.0008` | `-1.724723e-01` | `-1.838923e-01` | `1.066` | `4/4` |

Absolute-scaling fits:

- instantaneous `|F~M|` exponent: `0.44`
- coupled-field `|F~M|` exponent: `-0.23`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction holds
- the coupled field preserves the sign of the instantaneous comparator on all
  sampled rows
- but the strength dependence is not a clean linear mass-scaling law on this
  retained compact generated family

## Honest limitation

This is a no-go for the minimal source-driven rescue.

- the architecture does not recover `|F~M| ≈ 1`
- the source-driven coupled field is therefore not enough to upgrade the
  retained generated-family story into a self-consistent field sector

## Branch verdict

Treat this as a useful boundary:

- sign survives
- exact reduction survives
- clean linear mass scaling does not

That means the minimal coupled-field architecture is not the missing rescue.
