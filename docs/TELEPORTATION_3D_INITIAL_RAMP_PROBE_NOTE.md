# Teleportation 3D Initial-State And Ramp Probe

**Date:** 2026-04-25
**Status:** planning / first artifact; not a manuscript claim surface
**Runner:** `scripts/frontier_teleportation_3d_initial_ramp_probe.py`

## Scope

This note records a smallest-surface 3D pressure test for the teleportation
preparation lane. The audited geometry is three spatial lattice directions
plus one finite ramp-time diagnostic direction.

Strict boundary: ordinary quantum state teleportation only. This artifact does
not claim matter transfer, mass transfer, charge transfer, energy transfer,
object transport, or faster-than-light signaling.

## Commands Run

```bash
python3 -m py_compile scripts/frontier_teleportation_3d_initial_ramp_probe.py
python3 scripts/frontier_teleportation_3d_initial_ramp_probe.py
```

Both commands completed successfully.

Default run:

- `dim=3`, `side=2`, `N=8`, two-species Hilbert dimension `64`;
- `mass=0`, `G_target=1000`;
- sampled ramp grid: `21` points in `s in [0, 1]`;
- finite-time ramp: `smoothstep`, `T=40`, `steps=320`, `dt=0.125`;
- resource threshold: best Bell overlap `>= 0.900`;
- target tracking threshold: `|<g_target|psi(T)>|^2 >= 0.990`;
- sampled ramp gap threshold: `>= 1e-3`.

## G=0 Initial State

The 3D side-2 `G=0` state is spectrally clean and product/separable, but it is
maximally delocalized in the native site basis.

| diagnostic | value |
| --- | ---: |
| single-species `H1` ground energy | `-3.000000` |
| single-species `H1` gap | `2.000000` |
| two-species `H(G=0)` ground energy | `-6.000000` |
| two-species `H(G=0)` degeneracy | `1` |
| two-species `H(G=0)` gap | `2.000000` |
| `|<g_G0 | g_H1 x g_H1>|^2` | `1.000000` |
| `|<g_G0 | uniform x uniform>|^2` | `1.000000` |

Separability diagnostics were numerical rank `1` with entropy near zero:

| partition | entropy bits | purity |
| --- | ---: | ---: |
| species A / species B | `6.513504e-28` | `1.000000` |
| logical pair / environment pair | `5.867702e-28` | `1.000000` |
| single `H1` logical / single `H1` environment | `8.940889e-29` | `1.000000` |

The traced logical resource at `G=0` is not an entangled resource:

| quantity | value |
| --- | ---: |
| `Phi+` overlap | `0.500000` |
| best Bell overlap | `0.500000` (`Psi+`) |
| best-frame average fidelity | `0.666667` |
| CHSH | `2.000000` |
| negativity | `0.000000` |

Native site support:

| state | basis dim | support | PR | `PR/dim` | max probability | site entropy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| single `H1` ground | `8` | `8` | `8.000000` | `1.000000` | `0.125000` | `3.000000` bits |
| two-species `G=0` ground | `64` | `64` | `64.000000` | `1.000000` | `0.015625` | `6.000000` bits |

Initial-state verdict: **unresolved gap**. The state is unique, gapped,
exactly product, and separable, but it is not native-basis localized under the
default `PR/dim <= 0.25` localization threshold.

## Ramp Diagnostics

Null control (`G_target=0`) stayed non-resource throughout the sampled path:

| quantity | value |
| --- | ---: |
| `||dH/ds||_2` | `0` |
| minimum sampled gap | `2.000000` |
| endpoint best Bell overlap | `0.500000` (`Psi+`) |
| endpoint best-frame average fidelity | `0.666667` |
| endpoint CHSH | `2.000000` |
| endpoint negativity | `0.000000` |

The 3D Poisson target (`G_target=1000`) produced a high Bell-frame logical
resource on the side-2 lattice:

| `s` | gap | target overlap | best Bell | best frame fidelity | CHSH | negativity |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.000` | `2.000000` | `0.163630` | `0.500000` (`Psi+`) | `0.666667` | `2.000000` | `0.000000` |
| `0.250` | `0.355996` | `0.950303` | `0.969091` (`Psi+`) | `0.979394` | `2.742398` | `0.469091` |
| `0.500` | `0.188053` | `0.993598` | `0.991220` (`Psi+`) | `0.994146` | `2.803703` | `0.491220` |
| `0.750` | `0.126801` | `0.999265` | `0.995993` (`Psi+`) | `0.997329` | `2.817116` | `0.495993` |
| `1.000` | `0.095490` | `1.000000` | `0.997724` (`Psi+`) | `0.998483` | `2.821998` | `0.497724` |

Path summary:

- minimum sampled gap: `0.095490` at `s=1.000`;
- target gap: `0.095490`;
- maximum exact eigenbasis adiabatic diagnostic: `3.115584` at `s=0.000`;
- maximum conservative `||dH||/gap^2`: `3.312934e+04` at `s=1.000`.

The high-overlap Bell state is `Psi+`, not `Phi+`, so the direct `Phi+`-frame
average fidelity at the endpoint is low (`0.334850`). With the Bell-frame
choice made explicit, the best-frame average fidelity is `0.998483`.

## Finite-Time Diagnostic

The finite-time `smoothstep` ramp with `T=40`, `steps=320` remained close to
the 3D target ground state.

| case | target overlap | diabatic loss | energy excess | best Bell | best-frame fidelity | negativity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| null | `1.000000` | `0` | `8.881784e-16` | `0.500000` (`Psi+`) | `0.666667` | `0.000000` |
| Poisson `G=1000` | `0.999954` | `4.578600e-05` | `0.002244` | `0.997444` (`Psi+`) | `0.998296` | `0.497451` |

The Poisson finite-time final state had native site-pair support:

| dim | support | PR | `PR/dim` | max probability | site entropy |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `64` | `64` | `8.123775` | `0.126934` | `0.124043` | `3.077086` bits |

## Verdict

Null control: **clean**.

3D side-2 ramp resource check: **candidate**. The sampled 3D Poisson endpoint
and the finite-time `T=40` ramp both yield a high best-Bell-overlap logical
resource in the `Psi+` frame.

Combined preparation verdict: **unresolved gap**. The side-2 ramp is a useful
3D resource candidate, but the required `G=0` initial state is maximally
delocalized in the native basis and this artifact does not supply a scalable
preparation, control, noise, or readout proof.

## Limitations

- Exact smallest 3D surface only: `side=2`, `N=8`, two-species dimension `64`.
- No `side=4` 3D dense diagonalization or scaling study was attempted.
- The finite-time result is one schedule and one runtime, not a runtime/error
  theorem.
- The conservative norm-bound diagnostic is large (`3.312934e+04`) despite the
  favorable exact finite-time result.
- No bath, cooling, calibration, control-noise, disorder, or readout model is
  included.
- The Bell resource is reported in the best Pauli frame; using the wrong fixed
  `Phi+` frame would not yield the stated fidelity.
- Scope remains ordinary quantum state teleportation only.
