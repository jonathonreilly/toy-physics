# Central-Band Large-N Corrected Born Note

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/central_band_born_largeN.py` exits 0 with PASS in the current cache; the prior audit verdict citing an unregistered artifact was generated against an earlier cache state and is invalidated by this source-note hash drift.

This note records the large-`N` extension of the dense central-band hard-geometry
lane under the corrected three-slit Sorkin metric.

Script:
- [`scripts/central_band_born_largeN.py`](/Users/jonreilly/Projects/Physics/scripts/central_band_born_largeN.py)

Harness:
- corrected three-slit 3D chokepoint graph
- central-band `|y|` removal after the barrier
- exact propagation
- corrected `I3 / P` with `-P(empty)`

Sweep:
- `N = 80, 100`
- `npl = 60`
- `4` matched seeds
- `8` realizations
- `y_cut = 2.0`
- `p_collapse = 0.2`

## Retained Large-N Rows

The dense pocket survives at `N = 80` and `N = 100` for both `LN + |y|`
and `LN + |y| + collapse`.

| N | mode | mean `|I3|/P` | max `|I3|/P` | verdict |
|---|---|---:|---:|---|
| 80 | `LN + |y|` | `3.70e-17` | `3.33e-16` | PASS |
| 80 | `LN + |y| + collapse` | `4.32e-17` | `6.66e-16` | PASS |
| 100 | `LN + |y|` | `0.00e+00` | `0.00e+00` | PASS |
| 100 | `LN + |y| + collapse` | `0.00e+00` | `0.00e+00` | PASS |

## Narrow Read

- The dense central-band Born pocket does survive beyond `N = 60`.
- At `npl = 60`, the corrected Born metric stays at machine precision for the
  retained large-`N` rows above.
- The pocket is still density-sensitive and should not be read as universal;
  it is the dense version of the bounded hard-geometry lane.

## Interpretation

The clean large-`N` takeaway is now:

- central-band hard geometry survives the corrected Born gate at `N = 80, 100`
- `LN + |y|` remains the stable backbone of the pocket
- adding collapse does not break Born inside this dense pocket

