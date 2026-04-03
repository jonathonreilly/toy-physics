# Asymmetry Persistence Born Calibration Note

This note records the corrected Born calibration for the generated
asymmetry-persistence lane on the dense `N=100` probe.

Script:
[`scripts/asymmetry_persistence_born_calibration.py`](/Users/jonreilly/Projects/Physics/scripts/asymmetry_persistence_born_calibration.py)

## Narrow probe

The lowest-cost dense check was run at:

- `N = 100`
- `npl = 60`
- thresholds `0.10` and `0.20`
- `2` seeds
- `4` realizations
- corrected Sorkin metric with `-P(empty)`

## Result

On this corrected harness, the relevant retained rows are Born-clean at
machine precision:

| Threshold | linear `|I3|/P` | persistence `|I3|/P` | persistence+LN `|I3|/P` | persistence+LN+collapse `|I3|/P` |
| --- | --- | --- | --- | --- |
| `0.10` | `8.49e-16±1.7e-16` | `8.49e-16±1.7e-16` | `2.78e-16±7.2e-17` | `2.78e-16±4.1e-17` |
| `0.20` | `1.12e-15±2.5e-16` | `1.12e-15±2.5e-16` | `2.59e-16±3.9e-17` | `2.59e-16±4.1e-17` |

## Narrow conclusion

- persistence does not spoil Born on this dense `N=100` probe
- persistence + layer normalization remains Born-clean
- persistence + layer normalization + collapse is also Born-clean in this narrow probe
- the result is strong enough to keep the lane alive, but it is still only a narrow probe and should be treated as a density-limited confirmation rather than a final asymptotic claim

