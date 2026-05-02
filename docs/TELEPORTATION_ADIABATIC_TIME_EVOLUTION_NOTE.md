# Teleportation Adiabatic Time-Evolution Probe

**Date:** 2026-04-25
**Status:** planning / first artifact; not a manuscript claim surface
**Runner:** `scripts/frontier_teleportation_adiabatic_time_evolution.py`

## Scope

This note records a bounded finite-time Schrodinger-evolution diagnostic for
the native Poisson ramp used in the adiabatic preparation probe:

```text
H(s) = H(G=0) + s(t) * (H(G_target) - H(G=0)).
```

The audited object is an ordinary quantum state teleportation resource after
tracing cells and spectator taste bits and keeping the last Kogut-Susskind
taste bit per species. It is not matter teleportation, mass transfer, charge
transfer, energy transfer, object transport, or faster-than-light signaling.

## Method

The runner starts from the `G=0` ground state and evolves under a finite-time
schedule using midpoint piecewise-constant unitary steps. For `2D 4x4`, the
default propagator uses `scipy.sparse.linalg.expm_multiply`; for small `1D`
spot checks it uses per-step exact diagonalization.

For each final state it reports:

- overlap with the instantaneous/final target ground state;
- diabatic loss `1 - |<g(T)|psi(T)>|^2`;
- traced logical `Phi+` and best Bell overlap;
- standard mean teleportation fidelity `Favg`;
- logical CHSH, negativity, purity, and final energy excess;
- Bob pre-message input-independence for the selected final candidate.

Schedules in the default run:

```text
linear:     s(u)=u
smoothstep: s(u)=3u^2-2u^3
```

## Commands Run

```bash
python3 -m py_compile scripts/frontier_teleportation_adiabatic_time_evolution.py
python3 scripts/frontier_teleportation_adiabatic_time_evolution.py
python3 scripts/frontier_teleportation_adiabatic_time_evolution.py --case 1d_null --case 1d_poisson_chsh --runtimes 20,80,160 --schedules smoothstep --random-inputs 16
```

The default run uses the `2D 4x4` null and Poisson cases. The 1D command is a
cheap spot check only; the `2D 4x4` case remains the priority.

## 2D Null Control

The `G=0` path is constant, remains non-entangled under the traced logical
extraction, and does not beat the classical average-fidelity boundary.

| case | schedule | T | final ground overlap | `Phi+` | best Bell | `Favg` | negativity | verdict |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `2d_null` | linear | `20` | `1.000000` | `0.500000` | `0.500000` | `0.666667` | `0.000000` | PASS non-resource |

## 2D 4x4 Target Reference

The final target ground state from the earlier Poisson resource artifact is
recovered as the adiabatic endpoint reference:

| target | gap | `Phi+` | best Bell | `Favg` | logical CHSH | negativity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `2d_poisson_chsh`, `G=1000` | `0.246378` | `0.970283` | `0.970283` | `0.980189` | `2.745662` | `0.470283` |

## 2D 4x4 Finite-Time Table

Default numerics: `steps_per_unit=8`, `min_steps=160`.

| schedule | T | steps | final ground overlap | diabatic loss | `Phi+` | `Favg` | negativity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| linear | `1` | `160` | `0.529913` | `0.470087` | `0.836850` | `0.891233` | `0.345314` |
| linear | `2` | `160` | `0.707471` | `0.292529` | `0.759362` | `0.839575` | `0.269698` |
| linear | `5` | `160` | `0.880580` | `0.119420` | `0.877385` | `0.918257` | `0.393445` |
| linear | `10` | `160` | `0.946609` | `0.053391` | `0.916670` | `0.944447` | `0.425589` |
| linear | `20` | `160` | `0.979209` | `0.020791` | `0.940209` | `0.960140` | `0.443442` |
| linear | `40` | `320` | `0.992742` | `0.007258` | `0.951895` | `0.967930` | `0.452665` |
| linear | `80` | `640` | `0.997848` | `0.002152` | `0.958617` | `0.972411` | `0.458633` |
| smoothstep | `1` | `160` | `0.528450` | `0.471550` | `0.831341` | `0.887561` | `0.355526` |
| smoothstep | `2` | `160` | `0.798036` | `0.201964` | `0.795008` | `0.863339` | `0.295340` |
| smoothstep | `5` | `160` | `0.971091` | `0.028909` | `0.952638` | `0.968425` | `0.459760` |
| smoothstep | `10` | `160` | `0.995417` | `0.004583` | `0.963139` | `0.975426` | `0.464192` |
| smoothstep | `20` | `160` | `0.999667` | `3.333244e-04` | `0.966438` | `0.977626` | `0.466462` |
| smoothstep | `40` | `320` | `0.999985` | `1.546251e-05` | `0.970437` | `0.980291` | `0.470440` |
| smoothstep | `80` | `640` | `0.999999` | `1.206717e-06` | `0.970077` | `0.980051` | `0.470077` |

Runtime sensitivity is clear. The endpoint-smoothed schedule reaches low
diabatic loss far faster than the linear schedule. The `T=40` smoothstep row is
the best default resource by standard mean fidelity, while `T=80` has the
smallest ground-state loss.

The slight `T=40` resource-fidelity overshoot relative to the target ground
state is not a new endpoint claim. It means the traced logical Bell overlap is
not identical to full-state target-ground overlap, so a tiny diabatic component
can marginally improve this reduced metric on the small surface.

## Candidate Bob Pre-Message Audit

Selected candidate: `2d_poisson_chsh`, smoothstep, `T=40`, `320` steps,
`expm_multiply`.

| metric | value |
| --- | ---: |
| final ground overlap | `0.999985` |
| diabatic loss | `1.546251e-05` |
| `Phi+` / best Bell | `0.970437` |
| standard `Favg` | `0.980291` |
| sampled mean fidelity | `0.980813` |
| sampled min fidelity | `0.970437` |
| sampled max fidelity | `1.000000` |
| output trace error | `1.110e-15` |
| Bob no-record distance to resource marginal | `4.163e-16` |
| Bob no-record pairwise input distance | `2.220e-16` |
| Bob marginal bias from `I/2` | `1.210e-01` |

The marginal bias is not input information. The relevant pre-message
input-independence check is the pairwise no-record distance across inputs,
which is at numerical precision here.

## 1D Spot Check

The optional 1D spot check is cheap enough for a small smoothstep table, but it
is not the priority because the target gap is much smaller (`0.018683`).

| case | schedule | T | final ground overlap | diabatic loss | `Phi+` | `Favg` | verdict |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `1d_null` | smoothstep | `20` | `1.000000` | `0` | `0.500000` | `0.666667` | PASS non-resource |
| `1d_poisson_chsh` | smoothstep | `20` | `0.731598` | `0.268402` | `0.794437` | `0.862958` | too diabatic |
| `1d_poisson_chsh` | smoothstep | `80` | `0.947180` | `0.052820` | `0.927266` | `0.951511` | useful but diabatic |
| `1d_poisson_chsh` | smoothstep | `160` | `0.993552` | `0.006448` | `0.984362` | `0.989575` | useful resource diagnostic, still diabatic |

The `1D T=160` candidate also passed Bob pre-message input-independence in the
spot run: pairwise input distance `1.110e-16`, distance to marginal
`3.608e-16`.

## Verdict

This is a useful preparation-candidate diagnostic for the `2D 4x4` Poisson
ramp, not a preparation proof. The finite-time closed-system simulation shows
that a smooth endpoint schedule can reach the target logical Bell-resource
quality with small full-state diabatic loss on the default small surface. The
null controls remain non-resource, and Bob's pre-message state remains
input-independent for the selected candidate.

## Limitations

- Small exact-diagonalization surface only: `2D 4x4` is the default priority.
- The Hamiltonian and schedule are ideal controls with no amplitude noise,
  timing noise, leakage model, or bath.
- The initial `G=0` ground state is assumed prepared.
- The time-dependent evolution is a midpoint piecewise-constant approximation;
  step convergence is not separately swept in this artifact.
- Logical Bell measurement, correction, and taste-only readout are still ideal
  protocol-level operations.
- No scaling, robustness, or hardware-preparation theorem is claimed.
- Scope remains ordinary quantum state teleportation only.
