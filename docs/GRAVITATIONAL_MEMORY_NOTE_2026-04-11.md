# Gravitational Memory Note (Retained, Bounded)

Status: bounded-retained

Primary artifact:
- `/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_gravitational_memory.py`

## What was rerun

Rerun command:

```bash
source /tmp/physics_venv/bin/activate && python scripts/frontier_gravitational_memory.py
```

Operating point from the runner:
- 1D periodic ring, `N=61`
- marker positions `15` and `45`
- source position `30`
- `MASS=0.30`
- `MU2=0.22`
- `DT_MATTER=0.12`
- `DT_FIELD=0.03`
- `N_FIELD_SUBSTEPS=4`
- `c=1.0`
- `gamma=0.05`
- `beta=5.0`
- pulse active during matter steps `10-20`
- amplitudes tested: `0.1, 0.5, 1.0, 2.0, 5.0`

## Exact rerun numbers

Control run:
- initial separation: `30.000000`
- final separation: `30.000000`
- free drift: `+0.000000`
- final norms: `1.000000`, `1.000000`

Amplitude sweep:

| amplitude | final separation | net memory | peak `|Phi|` |
| --- | ---: | ---: | ---: |
| `0.10` | `30.001164` | `+0.001164` | `0.363927` |
| `0.50` | `30.006501` | `+0.006501` | `1.819634` |
| `1.00` | `30.012742` | `+0.012742` | `3.639269` |
| `2.00` | `30.021965` | `+0.021965` | `7.278537` |
| `5.00` | `30.039601` | `+0.039601` | `18.196343` |

Weak-pulse linearity (`0.1, 0.5, 1.0`):
- memory/amplitude mean: `+0.012460`
- memory/amplitude std: `0.000592`

Strong-pulse nonlinearity:
- strong/weak ratio deviation: `0.319`

Time-resolved detail at amplitude `1.0`:
- separation remains exactly `30.000000` through the pulse window in the printed precision
- post-pulse offset appears late and accumulates after the field pulse has passed
- final net memory at `t=60`: `+0.012742`

## Retained claim

The retained claim is narrow:

- On this 1D ring protocol, a transient retarded field pulse produces a small but repeatable permanent shift in marker separation after the pulse has passed.
- The weak-pulse response is approximately linear in amplitude over the tested range `0.1-1.0`.
- Stronger pulses show clear nonlinearity.

## What this does **not** establish

- This is not a claim of full general-relativistic memory equivalence.
- This is not yet a geometry-changing or gauge-invariant memory observable.
- This is not yet a retained multi-family graph result; it is currently a bounded 1D-ring result.
- The observed signal is small: at amplitude `1.0`, the permanent shift is `+0.012742` on a baseline separation of `30`.

## Why keep it

- The control drift is exactly zero in the rerun.
- The sign and magnitude of the permanent offset are stable across the tested amplitude sweep.
- The weak-regime proportionality is quantitatively clean enough to preserve as a bounded positive result.

