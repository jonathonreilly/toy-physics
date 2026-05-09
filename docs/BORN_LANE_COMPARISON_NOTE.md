# Born Lane Comparison Note

**Date:** 2026-04-02  
**Status:** complete, bounded comparison

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/born_compare_modular_central_ln.py` exits 0 with PASS in the current cache; the prior audit verdict citing an unregistered artifact was generated against an earlier cache state and is invalidated by this source-note hash drift.

This note compares the two best bounded unitary lanes on the same corrected
Sorkin harness:

- modular gap + layer normalization
- central-band `|y|` removal + layer normalization

Script:
[scripts/born_compare_modular_central_ln.py](/Users/jonreilly/Projects/Physics/scripts/born_compare_modular_central_ln.py)

## Setup

- `N = 25, 40, 60`
- `npl = 25`
- same seed set across both lanes
- corrected Sorkin metric with `-P(empty)`
- `gap = 2.0`
- `y_cut = 2.0`

## Strongest retained rows

### Modular gap + LN

| N | pur_min | mean `|I3|/P` | max `|I3|/P` | seeds |
|---|---:|---:|---:|---:|
| 25 | `0.908` | `3.28e-16` | `9.99e-16` | 8 |
| 40 | `0.958` | `3.15e-16` | `7.77e-16` | 8 |
| 60 | `0.957` | `2.70e-16` | `7.77e-16` | 7 |

### Central-band `|y|<2` + LN

| N | pur_min | mean `|I3|/P` | max `|I3|/P` | seeds | removed |
|---|---:|---:|---:|---:|---:|
| 25 | `0.942` | `2.78e-16` | `9.99e-16` | 8 | `15.9%` |
| 40 | `0.948` | `2.96e-16` | `8.88e-16` | 8 | `16.1%` |
| 60 | `0.947` | `3.60e-16` | `1.22e-15` | 7 | `17.3%` |

## Readout

Both best LN lanes are Born-clean on the corrected harness at machine
precision. The modular lane is slightly more stable on the Born metric in
this sample because its `|I3|/P` maxima are a bit lower overall, while the
central-band lane keeps a small finite-`N` decoherence advantage at `N=40`
and `N=60`.

The safe summary is:

- Born cleanliness is retained for both lanes
- modular is marginally more stable on the corrected Sorkin metric here
- central-band remains the simpler hard-geometry lever and keeps the better
  bounded joint-decoherence story

## Interpretation

The result is an apples-to-apples tie in the main sense: both lanes survive
the corrected Born harness cleanly. The distinction is not Born compliance
but which bounded trade-off they prefer:

- modular gap + LN: slightly cleaner Born stability
- central-band `|y|` + LN: slightly stronger hard-geometry decoherence at
  the larger `N` rows

