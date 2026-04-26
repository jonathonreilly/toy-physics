# Teleportation Adiabatic Convergence and Robustness Note

**Status:** planning / first artifact; not a preparation proof
**Runner:** `scripts/frontier_teleportation_adiabatic_convergence_robustness.py`

## Scope

This note tightens the finite-time adiabatic result for the default `2D 4x4`
Poisson smoothstep candidate at `T=40`. The audited object is only an ordinary
quantum state teleportation resource after tracing cells/spectator tastes and
keeping the last Kogut-Susskind taste bit per species.

It does not claim matter transfer, mass transfer, charge transfer, energy
transfer, object transport, or faster-than-light signaling.

## Commands Run

```bash
python3 -m py_compile scripts/frontier_teleportation_adiabatic_convergence_robustness.py
python3 scripts/frontier_teleportation_adiabatic_convergence_robustness.py
```

Both commands completed successfully.

## Default Candidate

Default finite-time row:

```text
case = 2d_poisson_chsh
dim = 2
side = 4
mass = 0
G = 1000
schedule = smoothstep
runtime T = 40
steps = 320
method = expm_multiply
```

Target ground reference:

| gap | `Phi+` | `Favg` | best Bell | CHSH | negativity |
| ---: | ---: | ---: | --- | ---: | ---: |
| `0.246378` | `0.970283` | `0.980189` | `0.970283 (Phi+)` | `2.745662` | `0.470283` |

The initial `G=0` ground state is unique on this surface:
`E0=-8.000000`, initial gap `2.000000`.

## Step-Count Convergence

Smoothstep `T=40`, fixed-step midpoint piecewise-unitary evolution:

| steps | dt | final ground overlap | diabatic loss | `Phi+` | `Favg` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `80` | `0.500000` | `0.995309` | `0.004691` | `0.960840` | `0.973893` |
| `160` | `0.250000` | `0.999917` | `8.327871e-05` | `0.970423` | `0.980282` |
| `320` | `0.125000` | `0.999985` | `1.546251e-05` | `0.970437` | `0.980291` |
| `640` | `0.062500` | `0.999985` | `1.487643e-05` | `0.970438` | `0.980292` |

The `320 -> 640` changes were small:

| metric | `320 - 640` |
| --- | ---: |
| final ground overlap | `-5.861e-07` |
| diabatic loss | `+5.861e-07` |
| `Phi+` | `-1.122e-06` |
| `Favg` | `-7.478e-07` |

This supports treating the `T=40`, `320`-step row as numerically stable for
this first artifact.

## Propagator Check

At `160` steps, `expm_multiply` and per-step dense `eigh` propagation agreed
to numerical precision:

| method | final ground overlap | diabatic loss | `Phi+` | `Favg` | `d_Favg` vs `expm_multiply` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `expm_multiply` | `0.999917` | `8.327871e-05` | `0.970423` | `0.980282` | `0` |
| `eigh` | `0.999917` | `8.327871e-05` | `0.970423` | `0.980282` | `+4.774e-15` |

## Schedule Comparison

Same runtime/step budget: `T=40`, `320` steps.

| schedule | final ground overlap | diabatic loss | `Phi+` | best Bell | `Favg` | negativity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `linear` | `0.992742` | `0.007258` | `0.951895` | `0.951895 (Phi+)` | `0.967930` | `0.452665` |
| `smoothstep` | `0.999985` | `1.546251e-05` | `0.970437` | `0.970437 (Phi+)` | `0.980291` | `0.470440` |
| `sine` | `0.999990` | `1.048574e-05` | `0.970666` | `0.970666 (Phi+)` | `0.980444` | `0.470668` |

Endpoint-smoothed schedules are materially better than the linear ramp at the
same budget. The sine schedule is slightly stronger in this row, but the
existing smoothstep candidate remains converged and strong.

## Perturbation Controls

Status threshold for this table: `Favg >= 0.95` and diabatic loss `<= 1e-3`.

Runtime/timing sensitivity, smoothstep with fixed `320` steps:

| runtime | final ground overlap | diabatic loss | `Phi+` | `Favg` | status |
| ---: | ---: | ---: | ---: | ---: | --- |
| `36` | `0.999976` | `2.351617e-05` | `0.969916` | `0.979944` | PASS |
| `40` | `0.999985` | `1.546251e-05` | `0.970437` | `0.980291` | PASS |
| `44` | `0.999989` | `1.118256e-05` | `0.970255` | `0.980170` | PASS |

Target `G` amplitude sensitivity:

| `G` scale | target `Phi+` | final ground overlap | diabatic loss | `Phi+` | `Favg` | status |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `0.98` | `0.969174` | `0.999985` | `1.476462e-05` | `0.969937` | `0.979958` | PASS |
| `1.00` | `0.970283` | `0.999985` | `1.546251e-05` | `0.970437` | `0.980291` | PASS |
| `1.02` | `0.971335` | `0.999984` | `1.611161e-05` | `0.970773` | `0.980515` | PASS |

Small mass perturbation:

| mass | target `Phi+` | final ground overlap | diabatic loss | `Phi+` | `Favg` | status |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `0` | `0.970283` | `0.999985` | `1.546251e-05` | `0.970437` | `0.980291` | PASS |
| `0.02` | `0.968824` | `0.999985` | `1.542586e-05` | `0.969009` | `0.979339` | PASS |

Deterministic schedule-control noise:

| noise sigma | final ground overlap | diabatic loss | `Phi+` | `Favg` | status |
| ---: | ---: | ---: | ---: | ---: | --- |
| `0` | `0.999985` | `1.546251e-05` | `0.970437` | `0.980291` | PASS |
| `0.01` | `0.954788` | `0.045212` | `0.996659` | `0.997773` | FIDELITY_ONLY |

The noise row is deliberately reported as not robust adiabatic preparation.
It retains a very strong reduced teleportation resource, but the full state is
no longer close to the target ground state. That is a useful warning: reduced
logical fidelity alone can be misleading under noisy controls.

## Null Control

The `G=0` path stays non-resource:

| final ground overlap | diabatic loss | `Phi+` | best Bell | `Favg` | negativity | verdict |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `1.000000` | `0` | `0.500000` | `0.500000 (Phi+)` | `0.666667` | `0.000000` | PASS non-resource |

## Bob Pre-Message Input-Independence

Candidate audited: `2d_poisson_chsh`, smoothstep, `T=40`, `320` steps,
`expm_multiply`.

| metric | value |
| --- | ---: |
| sampled inputs | `70` |
| sampled mean fidelity | `0.980813` |
| sampled min fidelity | `0.970437` |
| sampled max fidelity | `1.000000` |
| output trace error | `1.110e-15` |
| Bob no-record distance to resource marginal | `4.163e-16` |
| Bob no-record pairwise input distance | `2.220e-16` |
| Bob marginal bias from `I/2` | `1.210e-01` |
| input-independence verdict | PASS |

The marginal bias is a property of the imperfect shared resource, not input
information. The pairwise no-record distance across Alice inputs is at
numerical precision.

## Verdict

The default `2D 4x4` smoothstep `T=40` candidate remains a strong finite-time
resource diagnostic after step-count convergence, method comparison,
same-budget schedule comparison, small `G`/mass/timing controls, a schedule
noise stress row, the `G=0` null control, and Bob pre-message
input-independence.

This is still not a preparation proof.

## Limitations

- Small exact surface only: `2D 4x4`.
- Closed-system, ideal-control Hamiltonian evolution.
- The initial `G=0` ground state is assumed prepared.
- Perturbations are cheap first controls, not a full noise model.
- The schedule-noise row shows that reduced logical resource quality can stay
  high even with non-negligible full-state diabatic loss.
- Taste-qubit extraction, Bell measurement, correction, and readout remain
  ideal protocol-level operations.
- No scaling theorem, hardware-preparation theorem, object transport, or
  faster-than-light claim is made.
