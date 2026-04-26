# Teleportation Taste Readout/Operator Model

**Date:** 2026-04-25
**Status:** planning / first artifact; not a promotion claim
**Runner:** `scripts/frontier_teleportation_taste_readout_operator_model.py`

## Scope

This note audits which native site/taste operators are operationally compatible
with the traced logical taste-qubit lane:

```text
single-particle site Hilbert space
  -> retained logical qubit = last KS taste bit
  -> environment = cell labels + spectator taste bits
  -> allowed operator form: O_logical tensor I_env
```

The goal is to move beyond "the trace is mathematically valid" and test the
operator condition that would make cells and spectator tastes ignorable during
readout, Bell measurement, and correction.

This remains ordinary quantum state teleportation planning only. It does not
claim matter teleportation, mass transfer, charge transfer, energy transfer,
object transport, or faster-than-light signaling.

## Command

```bash
python3 -m py_compile scripts/frontier_teleportation_taste_readout_operator_model.py
python3 scripts/frontier_teleportation_taste_readout_operator_model.py
```

Both commands completed successfully.

Default settings:

```text
dims = 1,2,3
sides = 2,4
retained taste axis = dim - 1
tolerance = 1e-12
Bob no-message probes = 22 (six Pauli-axis states plus 16 random states)
```

## Single-Register Classification

Residuals are measured after projecting each native operator onto the subspace
`O_logical tensor I_env`. A zero residual means the operator is taste-only for
the retained logical bit.

| dim | side | envs | native sublattice `Z` | axis logical `Z` | axis-adapted `X` | fixed pair-hop `X` | native `Z` then fixed `X` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | 1 | PASS, rel `0` | PASS | PASS | PASS | PASS |
| 1 | 4 | 2 | PASS, rel `0` | PASS | PASS | PASS | PASS |
| 2 | 2 | 2 | FAIL, rel `1.000000` | PASS | PASS | PASS | FAIL, rel `1.000000` |
| 2 | 4 | 8 | FAIL, rel `1.000000` | PASS | PASS | PASS | FAIL, rel `1.000000` |
| 3 | 2 | 4 | FAIL, rel `1.000000` | PASS | PASS | PASS | FAIL, rel `1.000000` |
| 3 | 4 | 32 | FAIL, rel `1.000000` | PASS | PASS | PASS | FAIL, rel `1.000000` |

Key result: native sublattice parity `Z` is `xi_5`, the product of all taste
`Z` signs. It equals retained-bit logical `Z` only in 1D. In 2D and 3D its
logical candidate averages to zero because it changes sign across spectator
taste sectors, so it leaks spectator information.

The fixed row-major pair-hop `X` matches the axis-adapted retained-bit `X` on
this lane for every audited case:

```text
max |fixed_pair_hop_X - axis_adapted_X| = 0
```

This is conditional on retaining the last taste axis. If a different taste bit
is retained, the fixed row-major pair-hop is no longer automatically the
logical `X`; an axis-adapted operator must be used.

## Representative Projectors and Measurements

| dim | side | native `Z+` projector | axis `Z+` projector | axis `X+` projector | fixed site projector | fixed env projector |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | PASS, rel `0` | PASS | PASS | PASS, rel `0` | PASS, rel `0` |
| 1 | 4 | PASS, rel `0` | PASS | PASS | FAIL, rel `0.707107` | FAIL, rel `0.707107` |
| 2 | 2 | FAIL, rel `0.707107` | PASS | PASS | FAIL, rel `0.707107` | FAIL, rel `0.707107` |
| 2 | 4 | FAIL, rel `0.707107` | PASS | PASS | FAIL, rel `0.935414` | FAIL, rel `0.935414` |
| 3 | 2 | FAIL, rel `0.707107` | PASS | PASS | FAIL, rel `0.866025` | FAIL, rel `0.866025` |
| 3 | 4 | FAIL, rel `0.707107` | PASS | PASS | FAIL, rel `0.984251` | FAIL, rel `0.984251` |

The 1D side-2 fixed-site/fixed-env passes are vacuous because there is only one
environment label. Once there is more than one cell/spectator sector, a
site-resolved or environment-resolved measurement is not taste-only.

## Two-Register Measurement Classification

The script also tests representative two-register measurements using algebraic
Frobenius projection onto `O_logical_pair tensor I_env_pair`.

| dim | side | axis Bell `Phi+` projector | native-`Z`/fixed-`X` Bell `Phi+` projector | native `ZZ` stabilizer | fixed `XX` stabilizer |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2 | PASS, rel `0` | PASS, rel `0` | PASS, rel `0` | PASS, rel `0` |
| 1 | 4 | PASS, rel `0` | PASS, rel `0` | PASS, rel `0` | PASS, rel `0` |
| 2 | 2 | PASS, rel `0` | FAIL, rel `0.707107` | FAIL, rel `1.000000` | PASS, rel `0` |
| 2 | 4 | PASS, rel `0` | FAIL, rel `0.707107` | FAIL, rel `1.000000` | PASS, rel `0` |
| 3 | 2 | PASS, rel `0` | FAIL, rel `0.707107` | FAIL, rel `1.000000` | PASS, rel `0` |
| 3 | 4 | PASS, rel `0` | FAIL, rel `0.707107` | FAIL, rel `1.000000` | PASS, rel `0` |

The native-`Z` Bell projector fails in 2D/3D for the same reason as the
single-register `Z`: it depends on spectator taste signs. A Bell measurement
for the traced logical resource must use retained-axis logical `Z` and `X`
stabilizers, or else explicitly include an environment measurement/heralding
model.

## Bob Pre-Message Separation

The runner includes a deliberately biased resource control:

```text
resource = |00><00|
Bob marginal bias from I/2 = 0.500000
max no-record state distance to Bob marginal = 2.220e-16
max pairwise no-record distance across inputs = 1.110e-16
max Bell-branch probability span = 0.500000
```

This confirms the separation:

- Bob's no-record state can be input-independent to numerical precision;
- Bob's marginal can still be biased relative to `I/2`;
- neither fact establishes that a native readout/correction operator is
  taste-only or operational.

## Conditions for Ignoring Cells and Spectators

Cells and spectator tastes can be ignored only when at least one of these is
provided:

1. every preparation, readout, Bell-measurement, and correction operator used by
   the protocol is proved to factor as `O_logical tensor I_env`;
2. the physical apparatus is proved readout-blind to environment labels within
   the protocol tolerance;
3. branch variation over environment labels is bounded below the protocol error
   budget for every logical observable used;
4. an explicit environment measurement, heralding rule, and branch-conditioned
   operation set is supplied, including the postselection cost.

For the current retained-last-taste-bit lane, the operator model supports:

- retained-axis logical `Z`;
- retained-axis logical `X`;
- fixed pair-hop `X` only because it equals retained-last-axis `X`;
- axis-built logical `Z+`, `X+`, `ZZ`, `XX`, and Bell projectors.

It does not support using native sublattice parity `Z` as a taste-only retained
logical readout/correction in 2D or 3D.

## Limitations

This is a static finite-dimensional operator audit. It does not build a
physical detector, pulse sequence, or fault-tolerant measurement primitive. It
does not audit noisy readout, dynamical preparation, Poisson ground-state
resource fidelity, or nonideal feed-forward. It also does not turn
environment-selected branches into protocol resources without an explicit
heralding and branch-conditioned correction workflow.
