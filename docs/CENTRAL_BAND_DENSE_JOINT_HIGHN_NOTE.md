# Central-Band Dense High-N Joint Card Note

**Date:** 2026-04-03  
**Status:** complete, bounded high-N extension of the dense central-band lane

This note records the higher-N extension of the dense central-band same-graph
hard-geometry lane. It keeps the corrected Born harness fixed and sweeps only
the dense central-band family.

Script:
[`scripts/central_band_dense_joint_highN.py`](/Users/jonreilly/Projects/Physics/scripts/central_band_dense_joint_highN.py)

## Setup

- corrected dense central-band graph family
- `N = 80, 100`
- candidate densities `npl = 60, 70, 80`
- `y_cut = 2.0`
- `yz_range = 12.0`
- `connect_radius = 3.0`
- `4` matched seeds
- `8` Monte Carlo realizations for the collapse rows

## Strongest Retained Rows

The high-N lane remains Born-clean on the retained rows, but it is
noticeably narrower than the `N=60` pocket.

| N | npl | mode | Born `|I3|/P` | `pur_min` / purity | gravity delta | note |
|---|---:|---|---:|---:|---:|---|
| 80 | 80 | `LN + |y|` | `0.000±0.000` | `0.500±0.000` | `+2.799±1.612` | strongest retained `N=80` row |
| 80 | 80 | `LN + |y| + collapse` | `0.000±0.000` | `0.374±0.057` | `+2.929±1.467` | best retained `N=80` decoherence floor |
| 100 | 70 | `LN + |y|` | `0.000±0.000` | `1.000±0.000` | `+0.748±1.396` | strongest retained `N=100` gravity row in the dense scan |
| 100 | 70 | `LN + |y| + collapse` | `0.000±0.000` | `0.678±0.094` | `+0.696±1.344` | strongest retained `N=100` decoherence row in the dense scan |

## Narrow Read

- The dense central-band lane still survives at high `N`, but only as a
  bounded pocket.
- `N=80` retains a genuinely strong gravity-positive row at `npl=80`, and
  collapse further lowers the purity floor while staying Born-clean.
- `N=100` is much thinner:
  - `npl=60` remains Born-clean but gravity is weak or negative.
  - `npl=70` gives the strongest retained positive-gravity rows in the scan,
    but with large uncertainty.
  - `npl=80` starts violating Born and is not retained.

## Interpretation

The review-safe high-N conclusion is narrower than the lower-N dense pocket:

- Born-safe dense central-band coexistence survives at `N=80` and `N=100`
  only inside a narrow density window.
- The strongest retained `N=80` row is at `npl=80`.
- The strongest retained `N=100` rows are at `npl=70`, but the gravity signal
  is noisy and should be treated as bounded rather than definitive.
- This is still the same dense hard-geometry family, but the joint window is
  clearly thinning as `N` rises.
