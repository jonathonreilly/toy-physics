# Wave Static Single-Source Compare

**Date:** 2026-04-08
**Status:** proposed_retained comparison probe
**Primary runner:** `scripts/wave_static_single_source_compare.py`

## Inputs

This note depends on:

- [WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md](./WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md)

The cited continuum-limit note supplies the physical construction and
readout primitives this comparator probe imports as `solve_wave`, `grow`,
`prop_beam`, `cz`, and the shared physical constants `K_PER_H`, `PW_PHYS`,
`S_PHYS`, `SRC_LAYER_FRAC`, `T_PHYS_LAYERS`. The single-source comparison
table is then a top-level arithmetic readout on those primitives at the
listed frozen-source positions and shared lattice spacing.

This focused probe removes the moving-source sweep and asks a narrower
question:

> If the source is frozen at one or two fixed source positions, do the
> comparator mismatches already show up?

It compares four quantities at a fixed source position:

- `dM`: retarded wave response
- `dI`: cached static slice
- `dIeq`: equilibrated cached static slice
- `dN`: imposed Newton-style comparator
- `dS`: direct discrete static solve

## Results

The retained evidence in this note is the coarse `H = 0.5` lattice and
two frozen source positions (`z_phys = 3.0` and `z_phys = 0.0`).
This is a smoke test, not a continuum claim.

### Frozen source at `z_phys = 3.0`

| quantity | value |
| --- | ---: |
| `dM` | `+0.009857` |
| `dI` | `+0.018250` |
| `dIeq` | `+0.003038` |
| `dN` | `+0.013402` |
| `dS` | `+0.009507` |
| `rel_MS` | `3.56%` |
| `rel_MI` | `45.99%` |
| `rel_MIeq` | `69.18%` |
| `rel_MN` | `26.45%` |
| static residual | `1.998e-10` |

The exact direct static solve tracks the retarded response closely,
but the cached static and equilibrated cached comparators do not.
The mismatch is already present with the source frozen in place.

### Frozen source at `z_phys = 0.0`

| quantity | value |
| --- | ---: |
| `dM` | `+0.001926` |
| `dI` | `+0.001696` |
| `dIeq` | `+0.001931` |
| `dN` | `+0.008041` |
| `dS` | `+0.001807` |
| `rel_MS` | `6.18%` |
| `rel_MI` | `11.93%` |
| `rel_MIeq` | `0.25%` |
| `rel_MN` | `76.04%` |
| static residual | `1.969e-10` |

This on-axis frozen source is much better behaved. `dIeq` is almost
identical to `dM`, while `dN` remains a poor comparator.

## Honest read

The frozen-source probe says the moving-source mismatch is **not**
caused purely by source motion. It is already visible for the frozen
off-center source at `z_phys = 3.0`.

At the same time, comparator quality is source-position dependent:

- off-center frozen source: cached comparators are poor, direct static
  solve is close to `dM`
- on-axis frozen source: `dIeq` becomes close to `dM`, while `dN`
  remains poor

So the remaining problem is not “motion vs no motion” alone. It is the
interaction between source position, comparator construction, and the
direct static solve.

## Artifact chain

- [`scripts/wave_static_single_source_compare.py`](../scripts/wave_static_single_source_compare.py)
