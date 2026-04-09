# Central Band Hard-Geometry + Collapse Note

This note records the joint gravity/decoherence card for the central-band lane with stochastic collapse.

Setup:
- same matched seeds on the same generated graphs
- `N = 25, 40, 60`
- central-band removal with `|y - center| < 2.0`
- `npl = 25`, `y_range = 12.0`, `connect_radius = 3.0`
- collapse probability `p = 0.2`

Metrics:
- deterministic rows report `pur_min`
- collapse rows report Monte Carlo density-matrix purity
- gravity is the same centroid delta used elsewhere in the central-band lane

## Strongest retained rows

| N | Config | Decoherence | Gravity delta | Note |
| --- | --- | --- | --- | --- |
| 25 | collapse | `0.637 +/- 0.047` | `+1.807 +/- 1.029` | Strong decoherence, positive gravity |
| 40 | collapse | `0.540 +/- 0.052` | `+3.262 +/- 1.301` | Strongest gravity on this card |
| 60 | `LN + \|y\| + collapse` | `0.575 +/- 0.037` | `+1.239 +/- 0.735` | Best joint retained row at N=60 |

## Full matched-seed card

| N | Config | Decoherence | Gravity delta | g/SE | Removed fraction |
| --- | --- | --- | --- | --- | --- |
| 25 | linear | `0.930 +/- 0.027` | `+1.854 +/- 1.669` | `+1.1` | `15.6%` |
| 25 | LN | `0.785 +/- 0.047` | `+1.369 +/- 1.321` | `+1.0` | `15.6%` |
| 25 | collapse | `0.637 +/- 0.047` | `+1.807 +/- 1.029` | `+1.8` | `15.6%` |
| 25 | `LN + \|y\|` | `0.727 +/- 0.077` | `+0.439 +/- 0.722` | `+0.6` | `15.6%` |
| 25 | `LN + \|y\| + collapse` | `0.633 +/- 0.074` | `+0.475 +/- 0.730` | `+0.7` | `15.6%` |
| 40 | linear | `0.929 +/- 0.031` | `+2.482 +/- 1.147` | `+2.2` | `15.9%` |
| 40 | LN | `0.750 +/- 0.062` | `+2.024 +/- 1.096` | `+1.8` | `15.9%` |
| 40 | collapse | `0.540 +/- 0.052` | `+3.262 +/- 1.301` | `+2.5` | `15.9%` |
| 40 | `LN + \|y\|` | `0.746 +/- 0.074` | `+2.569 +/- 1.442` | `+1.8` | `15.9%` |
| 40 | `LN + \|y\| + collapse` | `0.630 +/- 0.055` | `+2.685 +/- 1.491` | `+1.8` | `15.9%` |
| 60 | linear | `0.962 +/- 0.034` | `-0.400 +/- 0.235` | `-1.7` | `17.6%` |
| 60 | LN | `0.917 +/- 0.040` | `-0.235 +/- 0.318` | `-0.7` | `17.6%` |
| 60 | collapse | `0.670 +/- 0.064` | `-0.294 +/- 0.245` | `-1.2` | `17.6%` |
| 60 | `LN + \|y\|` | `0.810 +/- 0.061` | `+1.283 +/- 0.797` | `+1.6` | `17.6%` |
| 60 | `LN + \|y\| + collapse` | `0.575 +/- 0.037` | `+1.239 +/- 0.735` | `+1.7` | `17.6%` |

## Takeaways

- Central-band removal is the clean hard-geometry lever on this lane.
- Collapse is a real decoherence booster at `N = 25` and `N = 40`.
- At `N = 60`, collapse alone does not rescue gravity, but `LN + |y|` does.
- The best retained joint row on this card is `N = 60`, `LN + |y| + collapse`, which keeps positive gravity and the lowest retained purity on the `N = 60` rows.
- The removed fraction stays in a narrow band around `15%` to `18%`.

## Interpretation

The central-band lane is now a real bounded joint result, not a one-off. Hard geometry and collapse help in compatible ways at smaller `N`, but the gravity side becomes more fragile by `N = 60`. The safest statement is that the lane improves the joint window, not that it solves the asymptotic gravity law.
