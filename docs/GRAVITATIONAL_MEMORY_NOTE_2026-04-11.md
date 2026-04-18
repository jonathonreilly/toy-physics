# Gravitational Memory Note

Status: exploratory / protocol-specific

Primary artifact:
- [`scripts/frontier_gravitational_memory.py`](../scripts/frontier_gravitational_memory.py)

Robustness / diagnosis companions:
- [`scripts/frontier_memory_mu2_size_sweep.py`](../scripts/frontier_memory_mu2_size_sweep.py)
- [`MEMORY_DECAY_DIAGNOSIS_2026-04-11.md`](MEMORY_DECAY_DIAGNOSIS_2026-04-11.md)
- [`MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md`](MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md)

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

## Original narrow signal

The narrow `N=61` ring protocol still reproduces:

- On this 1D ring protocol, a transient retarded field pulse produces a small but repeatable permanent shift in marker separation after the pulse has passed.
- The weak-pulse response is approximately linear in amplitude over the tested range `0.1-1.0`.
- Stronger pulses show clear nonlinearity.

## What the later robustness pass changed

The later robustness/diagnosis surface does **not** support treating this as a
retained positive discovery:

- size sweep:
  - `N=41`: `+0.468668`
  - `N=61`: `+0.012742`
  - `N=81`: `+0.000005`
  - `N=101`: `+0.000000000135`
- position sweep at `N=61` changes sign:
  - `-0.296017` to `+0.347204`
- 13-config summary:
  - mean `+0.053218`
  - std `0.198658`
  - standard error `0.055098`

The current best diagnosis is that the original signal is a screened,
protocol-specific finite-size effect under `mu^2 = 0.22`, not a stable
graph-family memory observable.

## What this does **not** establish

- This is not a claim of full general-relativistic memory equivalence.
- This is not yet a geometry-changing or gauge-invariant memory observable.
- This is not a retained multi-family graph result.
- This should not currently be used as a publication-grade positive result.

## Why keep it

- It records the exact narrow-ring signal that triggered the robustness audit.
- The failure mode is scientifically useful: the signal collapses with size and
  points directly to Yukawa screening as the likely cause.
- It remains a good exploratory lead if the field law is changed, for example
  by removing screening.
