# Teleportation Bell-Measurement Circuit Note

**Date:** 2026-04-25
**Status:** planning / ideal logical taste-measurement decomposition
**Runner:** `scripts/frontier_teleportation_bell_measurement_circuit.py`

## Scope

This note records the next bounded planning artifact for native taste-qubit
teleportation: an explicit decomposition of Alice's ideal Bell measurement.

The scope is ordinary quantum state teleportation on encoded taste qubits. It
is not matter teleportation, mass transfer, charge transfer, energy transfer,
object transport, or faster-than-light signaling.

## Native Logical Surface

The runner uses the same fixed encoded taste-qubit surface as the first
teleportation artifact:

```text
C^N = C^N_cells tensor C^(2^d)
Z_L = I_cells tensor xi_5
X_L = I_cells tensor xi_last
```

On the default 3D side-4 lattice, fixed cell `(0,0,0)`, and last taste axis,
the encoded basis is:

```text
|0_L> = site index 0
|1_L> = site index 1
```

The runner verifies that the restricted native operators are Pauli `Z` and
`X`, and that the taste `Z_L` eigenprojectors are the computational readout
projectors on this encoded subspace.

## Stabilizer Decomposition

The ideal Bell projectors used by the protocol are:

```text
P_zx = 1/4 (I + (-1)^x Z_A Z_R) (I + (-1)^z X_A X_R)
```

The bit `x` is the `Z_A Z_R` parity or Bell flip record, and the bit `z` is
the `X_A X_R` parity or Bell phase record:

| label | z | x | ZZ eigenvalue | XX eigenvalue |
| --- | ---: | ---: | ---: | ---: |
| `Phi+` | 0 | 0 | `+1` | `+1` |
| `Phi-` | 1 | 0 | `+1` | `-1` |
| `Psi+` | 0 | 1 | `-1` | `+1` |
| `Psi-` | 1 | 1 | `-1` | `-1` |

The direct native-logical measurement construction is therefore:

```text
measure Z_L^A Z_L^R -> x
measure X_L^A X_L^R -> z
emit classical Bell record (z, x)
```

Because the two stabilizers commute, the projector is the product of the two
single-stabilizer eigenspace projectors. This is an algebraic logical/taste
decomposition. It assumes the corresponding ideal logical parity measurements
are available.

## Circuit Decomposition

The equivalent logical circuit form is:

```text
CNOT(A -> R)
H(A)
measure A and R in the computational Z_L basis
```

The measured output bits are:

```text
A output bit = z
R output bit = x
```

In the Heisenberg picture, pulling the final computational measurements back
through the circuit gives:

```text
Z_A output -> X_A X_R
Z_R output -> Z_A Z_R
```

Therefore the pulled-back computational-basis measurement projectors equal the
same `P_zx` projectors above. The runner checks this matrix identity directly.

## First Run

Command:

```bash
python3 scripts/frontier_teleportation_bell_measurement_circuit.py --trials 64 --seed 20260425
```

Observed output:

```text
native ZZ/XX stabilizer projector error vs ideal P_zx: 0.000e+00
resolution error: 0.000e+00
orthogonality error: 0.000e+00
idempotence error: 0.000e+00
Bell-state outer-product error: 1.110e-16
Bell-state stabilizer eigenvalue error: 0.000e+00
circuit unitarity error: 2.220e-16
pulled-back first output Z observable error vs X_A X_R: 2.220e-16
pulled-back second output Z observable error vs Z_A Z_R: 2.220e-16
max circuit measurement projector error vs P_zx: 1.110e-16
Bell input -> computational record min right probability: 0.9999999999999996
Bell input -> computational record max wrong probability: 0.000e+00
Bell outcomes exercised: Phi+, Phi-, Psi+, Psi-
max Bell probability error from 1/4: 2.776e-16
minimum corrected fidelity: 0.9999999999999997
maximum corrected infidelity: 3.331e-16
max corrected-state trace distance to input: 2.618e-16
max Bob trace distance to I/2 before Alice measurement: 3.331e-16
max Bob trace distance to I/2 after Alice measurement but before message: 5.551e-16
max pairwise pre-message Bob-state distance across inputs: 3.331e-16
```

The runner reports `PASS` for:

- native taste logical Pauli surface;
- stabilizer Bell projectors;
- `CNOT-H` circuit decomposition;
- all Bell outcomes;
- random-state correction fidelity;
- Bob pre-message input-independence.

## What This Adds

The prior protocol and measurement-record artifacts used ideal Bell projectors.
This artifact shows two explicit logical decompositions of those projectors:

- direct ideal taste-stabilizer parity measurements of `Z_L Z_L` and
  `X_L X_L`;
- an ideal logical circuit made from `CNOT`, `H`, and computational `Z_L`
  readout.

Both decompositions reproduce exactly the same Bell records and correction
map used by the protocol:

```text
U_zx = Z^z X^x
```

The teleportation checks are rerun using the circuit-derived projectors rather
than a separately named Bell-measurement primitive.

## Limitations

- The encoded Bell resource is still assumed or supplied by another artifact.
- The logical `CNOT`, logical `H`, or equivalent logical `ZZ` and `XX`
  stabilizer measurements are ideal primitives here.
- Computational taste-basis readout is ideal.
- Classical record creation, durability, and delivery are idealized and remain
  delegated to the record/channel artifacts.
- No apparatus Hamiltonian, error model, decoherence process, or durable
  endogenous measurement-record derivation is supplied here.
- The construction is logical and algebraic; it does not derive a native
  physical gate schedule from the Poisson/CHSH dynamics.
- It does not transport matter, mass, charge, or energy and does not enable
  faster-than-light signaling.

## Status

The Bell-measurement limitation is narrowed from an undecomposed ideal Bell
projector to an ideal logical/taste stabilizer or circuit measurement. The
remaining gap is physical implementation: deriving or supplying a durable
native apparatus/gate/readout mechanism with quantified imperfections.
