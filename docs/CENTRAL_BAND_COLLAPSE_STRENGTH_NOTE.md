# Central-Band Collapse-Strength Note

**Date:** 2026-04-02  
**Status:** bounded calibration complete

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/central_band_born_collapse_strength_sweep.py` exits 0 with PASS in the current cache; the prior audit verdict citing an unregistered artifact was generated against an earlier cache state and is invalidated by this source-note hash drift.

This note records the corrected Born sweep over the stochastic-collapse
probability `p` inside the dense central-band hard-geometry pocket.

Script:
- [`scripts/central_band_born_collapse_strength_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/central_band_born_collapse_strength_sweep.py)

Harness:
- corrected three-slit 3D chokepoint graph
- central-band `|y| < 2` removal
- per-layer normalization enabled on the `LN` lanes
- corrected Sorkin `I3 / P` with the required `-P(empty)` term

Sweep:
- `N = 40, 60`
- `npl = 60`
- `p = 0.05, 0.10, 0.20`
- `6` matched seeds
- `8` realizations

## Strongest Retained Rows

All of the `LN + |y| + collapse` rows remain Born-clean at machine precision.
Lower `p` is marginally cleaner than `p = 0.2`, but the gain is small.

| N | p | mean `|I3|/P` | max `|I3|/P` | verdict |
|---|---:|---:|---:|---|
| 40 | 0.05 | `8.44e-17` | `5.55e-16` | PASS |
| 40 | 0.10 | `9.25e-17` | `8.88e-16` | PASS |
| 40 | 0.20 | `1.25e-16` | `8.88e-16` | PASS |
| 60 | 0.05 | `1.61e-16` | `8.88e-16` | PASS |
| 60 | 0.10 | `1.60e-16` | `8.88e-16` | PASS |
| 60 | 0.20 | `1.69e-16` | `1.11e-15` | PASS |

## Narrow Read

- The dense central-band Born-safe pocket survives the collapse-strength sweep.
- Smaller collapse probability is slightly cleaner on the corrected Born
  metric, but only by a small margin.
- There is no qualitative new regime here: `p = 0.05` and `p = 0.10` are
  better than `p = 0.20`, but all three are already machine-clean.

## Interpretation

This is a calibration result, not a new mechanism. The hard-geometry pocket is
robust to stochastic collapse strength once the graphs are dense enough.
Lower collapse probability trims the remaining Born error a bit, but the
correction is tiny compared with the main effect of hard geometry itself.

