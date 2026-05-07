# Teleportation Taste Readout/Operator Model

**Date:** 2026-04-25
**Status:** open_gate / finite operator-factorization audit; not a physical promotion claim
**Claim type:** open_gate
**Status authority:** independent audit lane only; effective status is pipeline-derived after independent review.
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

## Algebraic Closure of the Native-Parity Obstruction

Write each site coordinate as

```text
x_i = 2 c_i + eta_i,      eta_i in {0,1}.
```

For this note the retained logical axis is `r = dim - 1`, so the logical bit is
`b = eta_r`.  The environment label is the cell vector together with the
spectator taste bits,

```text
e = (c, s),      s = (eta_i)_{i != r}.
```

The site basis is therefore identified as `|x> = |b>_logical tensor |e>_env`.
For an operator to be usable after tracing cells and spectator tastes, every
environment diagonal block must be the same `2 x 2` logical operator and all
environment off-diagonal blocks must vanish.

Native sublattice parity acts by

```text
Z_native |x> = (-1)^(sum_i x_i) |x>
             = (-1)^(sum_i eta_i) |x>
             = (-1)^b (-1)^(sum_{i != r} eta_i) |b,e>.
```

Thus on a fixed environment sector,

```text
Z_native|_e = sigma_s Z_logical,
sigma_s = (-1)^(sum_{i != r} eta_i).
```

For `dim = 1`, the spectator tuple is empty, `sigma_s = 1` for every cell, and
`Z_native = Z_logical tensor I_env`.  For `dim > 1`, at least one spectator bit
exists.  Holding the cell fixed and flipping one spectator bit changes
`sigma_s` while leaving the retained bit untouched, so two environment sectors
carry opposite logical blocks, `+Z_logical` and `-Z_logical`.  No single
`O_logical` can equal both blocks, hence `Z_native` cannot factor as
`O_logical tensor I_env`.

This also gives the runner's projection numbers.  The Frobenius projection used
by the runner is the environment average of the logical blocks:

```text
O_candidate = (1 / n_env) sum_e sigma_s Z_logical
            = (1 / 2^(dim-1)) sum_s (-1)^|s| Z_logical
            = 0                 for dim > 1.
```

The residual blocks are therefore `sigma_s Z_logical`; their Frobenius norm is
the full operator norm, giving relative residual `1.000000` and max residual
`1.000000` in every 2D and 3D audited case.  The native `Z+` projector has
blocks `(I + sigma_s Z_logical)/2`, so its projection is `I/2` and its residual
is `sigma_s Z_logical/2`, giving the table's relative residual `0.707107`.

The same sign is inherited by any native-parity correction or Bell stabilizer.
Because the fixed row-major pair-hop equals `X_logical tensor I_env` only for
the retained last taste axis, `Z_native` followed by fixed `X` has blocks
`sigma_s Z_logical X_logical` and fails by the same averaging argument.  On two
registers, native `ZZ` has environment-pair blocks
`sigma_s sigma_t (Z_logical tensor Z_logical)`, so its projected candidate is
again zero and the relative residual is `1.000000`.  A native-`Z`/fixed-`X`
Bell projector keeps the environment-blind `I tensor I` and `X tensor X` terms
but averages away the signed `Z tensor Z` and `ZX tensor ZX` terms, producing a
mixed logical candidate rather than the Bell `Phi+` projector.  This is the
`0.707107` two-register Bell-projector failure reported in the table.

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

## Coordinated Algebraic Closure (2026-05-07)

The case-by-case factorization audit documented above is now subsumed by a
single algebraic theorem (T1 + T2 + T4 in the companion closure note):
RALA(a) is the unique closed *-subalgebra of single-site operators that
factors as `O_logical (x) I_env`; native sublattice parity Z is in RALA
iff dim = 1.

See [`TELEPORTATION_RETAINED_AXIS_OPERATOR_ALGEBRA_CLOSURE_NOTE.md`](TELEPORTATION_RETAINED_AXIS_OPERATOR_ALGEBRA_CLOSURE_NOTE.md)
(runner `scripts/frontier_teleportation_retained_axis_operator_algebra_closure.py`)
for the proof. The closure note supplies bounded algebraic theorem support
for the operator-factorization content of this note; the physical-implementation
gate (native apparatus blind to environment labels, noisy readout,
dynamical preparation, heralded branch protocol) remains open.
