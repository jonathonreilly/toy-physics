# Operator-Consistent End-To-End Teleportation Audit

**Date:** 2026-04-26
**Status:** planning / first artifact; not a promotion claim
**Runner:** `scripts/frontier_teleportation_operator_consistent_end_to_end.py`

## Scope

This note records the operator-consistent end-to-end audit for the
Poisson-backed taste-qubit teleportation lane. It hardens the previous
end-to-end Poisson artifact after the taste-readout operator model result.

The audited convention is:

```text
single-particle site Hilbert space
  -> retained logical qubit = last KS taste bit
  -> environment = cells + spectator taste bits
  -> allowed traced logical operators factor as O_logical tensor I_env
```

The passing lane therefore uses retained-axis logical `Z` and `X` operators
for traced readout, Bell measurement, and Bob correction. Raw sublattice
parity `Z=xi_5` is included only as a control. It is valid as retained-bit `Z`
in 1D, but it is rejected in dimensions greater than one because spectator
taste signs remain.

This remains ordinary quantum state teleportation planning only. It does not
claim matter teleportation, mass transfer, charge transfer, energy transfer,
object transport, or faster-than-light signaling.

## Command

```bash
python3 -m py_compile scripts/frontier_teleportation_operator_consistent_end_to_end.py
python3 scripts/frontier_teleportation_operator_consistent_end_to_end.py
```

Both commands completed successfully.

Default settings:

```text
input probes = 134 states (six Pauli-axis probes + 128 random, seed=20260425)
fidelity threshold = 0.900
protocol tolerance = 1e-10
operator tolerance = 1e-12
```

## Operator-Consistency Guards

| surface | envs | retained-axis `Z` | retained-axis `X` | retained-axis Bell projectors | raw `xi_5` as `Z` | raw-`Z` Bell projectors | expected raw result |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| `1D side=8` | 4 | PASS | PASS | PASS | PASS | PASS | valid in 1D |
| `2D side=4` | 8 | PASS | PASS | PASS | FAIL | FAIL | rejected |
| `3D side=2` | 4 | PASS | PASS | PASS | FAIL | FAIL | rejected |

Raw-control residuals:

| surface | raw `Z` relative residual | raw `Z` expected error vs retained `Z` | raw Bell max relative residual | raw Bell max expected error |
| --- | ---: | ---: | ---: | ---: |
| `1D side=8` | `0` | `0` | `0` | `0` |
| `2D side=4` | `1.000000` | `1.000000` | `0.707107` | `0.250000` |
| `3D side=2` | `1.000000` | `1.000000` | `0.707107` | `0.250000` |

Interpretation: the retained-axis logical operators satisfy the traced
`O_logical tensor I_env` condition on all selected surfaces. Raw `xi_5` fails
the retained-bit guard in 2D and 3D, including when used inside Bell
projectors.

## End-To-End Results

The runner keeps the default Poisson cases from the previous end-to-end lane
and accepts a case only when both the retained-axis operator guard and the
protocol gates pass.

| case | full CHSH | best Bell overlap | exact `F_avg` | sampled min fidelity | min conditional branch fidelity | Bob pre-record pairwise distance | retained-axis operator guard | pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `1d_null` | `2.000000` | `0.500000` (`Psi+`) | `0.666667` | `0.500000` | `0.006062` | `2.776e-16` | PASS | no |
| `1d_poisson_chsh` | `2.822668` | `0.997963` (`Phi+`) | `0.998642` | `0.997963` | `0.997963` | `2.220e-16` | PASS | yes |
| `2d_poisson_chsh` | `2.668376` | `0.970283` (`Phi+`) | `0.980189` | `0.970283` | `0.969835` | `2.220e-16` | PASS | yes |

Both selected positive Poisson cases pass under the retained-axis logical
`Z/X` convention. The `G=0` null control remains below the high-fidelity gate
and does not pass.

## Branch, Record, And No-Signaling Checks

All four Bell outcomes are represented for the passing cases:

```text
1d_poisson_chsh outcomes: Phi+, Phi-, Psi+, Psi-
2d_poisson_chsh outcomes: Phi+, Phi-, Psi+, Psi-
```

Passing-case Bob pre-message input-independence remains clean:

```text
1d_poisson_chsh max no-record distance to resource marginal = 4.163e-16
1d_poisson_chsh max pairwise no-record input distance = 2.220e-16
2d_poisson_chsh max no-record distance to resource marginal = 4.441e-16
2d_poisson_chsh max pairwise no-record input distance = 2.220e-16
```

Bob's marginal can still be biased from `I/2`; that bias is not input
information:

```text
1d_poisson_chsh Bob marginal bias from I/2 = 3.189e-02
2d_poisson_chsh Bob marginal bias from I/2 = 1.213e-01
```

The causal two-bit record harness remains clean:

```text
1d_poisson_chsh delivered record = Psi+, delivered-branch fidelity = 0.998546
2d_poisson_chsh delivered record = Psi-, delivered-branch fidelity = 0.989495
early delivery blocked = True
delivered once = True
```

## Acceptance Gates

The default run reports `PASS` for:

- selected non-null Poisson cases pass retained-axis end-to-end;
- null controls do not pass the high-fidelity protocol;
- retained-axis operator guard passes for all selected cases;
- 2D and 3D raw `xi_5` controls are rejected;
- Bob pre-message input-independence is clean for passing cases;
- all four Bell outcomes are represented for passing cases;
- random input-state fidelity is represented for passing cases;
- causal two-bit record remains clean for passing cases.

## Limitations

- The Poisson resources are still obtained by offline diagonalization and
  tracing over cells and spectator tastes.
- The Bell measurement, readout, feed-forward, and Bob correction are ideal
  retained-logical operators, not a physical apparatus derivation.
- The raw `xi_5` rejection is an operator-factorization control. It does not
  itself build a detector, pulse sequence, or hardware readout model.
- The 3D item here is a raw-operator control on `3D side=2`, not a 3D
  Poisson resource teleportation result.
- The audited surfaces are small and finite: `1D side=8`, `2D side=4`, and a
  `3D side=2` operator control.
- No matter, charge, mass, energy, or object is teleported. Only an unknown
  quantum state on Bob's already-present encoded taste qubit is reconstructed
  after Bob receives Alice's classical Bell record.
