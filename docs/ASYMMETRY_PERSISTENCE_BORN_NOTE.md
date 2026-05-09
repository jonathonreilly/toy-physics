# Asymmetry Persistence Born Calibration Note

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/asymmetry_persistence_born_calibration.py` previously timed out under the audit-lane 120s default budget; AUDIT_TIMEOUT_SEC=1800 has been declared and the cache refreshed under the new budget. The runner output and pass/fail semantics are unchanged.

This note records the corrected Born calibration for the generated
asymmetry-persistence lane. The lane is now confirmed as a narrow dense
Born-safe pocket, but the pocket is density-sensitive and does not yet have a
fully hardened large-`N` confirmation.

Script:
[`scripts/asymmetry_persistence_born_calibration.py`](/Users/jonreilly/Projects/Physics/scripts/asymmetry_persistence_born_calibration.py)

## Confirmed probe

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

## Hardening Attempt

I also tried to widen this to denser `N=80/100` sweeps with more seeds and
realizations. That broader run was computationally heavy in this harness and
did not finish within the session window, so it did not produce a stronger
confirmation than the dense `N=100` probe above.

## Narrow conclusion

- persistence does not spoil Born on this dense `N=100` probe
- persistence + layer normalization remains Born-clean
- persistence + layer normalization + collapse is also Born-clean in this narrow probe
- the lane is alive, but it remains a density-limited confirmation rather than
  a final asymptotic claim
