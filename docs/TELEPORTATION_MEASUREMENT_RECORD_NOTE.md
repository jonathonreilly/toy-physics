# Teleportation Bell-Measurement Record Note

**Date:** 2026-04-25
**Status:** planning / explicit ideal record model
**Runner:** `scripts/frontier_teleportation_measurement_record.py`

## Scope

This note pushes the first teleportation artifact's measurement limitation one
step past a bare ideal projective Bell measurement.

The runner adds an explicit von-Neumann-style record register for Alice's Bell
measurement:

```text
V |Psi>_ARB = sum_zx (P_zx^AR tensor I_B) |Psi>_ARB tensor |zx>_M
```

Here `A,R` are Alice's two teleportation registers, `B` is Bob's qubit, and
`M` is a four-state Bell-record register. The record states are assumed
orthogonal and classical in the Bell label basis:

```text
|Phi+>, |Phi->, |Psi+>, |Psi->
```

This is a measurement-record model. It is not a derivation of apparatus
dynamics, environment-induced decoherence, or durable endogenous records.

## Construction

The runner keeps the Bell-state and correction convention used by
`scripts/frontier_teleportation_protocol.py`:

```text
P_zx = 1/4 (I + (-1)^x Z_A Z_R) (I + (-1)^z X_A X_R)
U_zx = Z^z X^x
```

The model does three checks.

1. The Bell projectors still resolve identity, are mutually orthogonal, and
   match the corresponding Bell-state outer products.
2. After premeasurement into the inaccessible record register, Bob's reduced
   density matrix is obtained by tracing out `A,R,M`. It remains `I/2` to
   numerical precision and is pairwise input-independent across random input
   states.
3. When a record label is delivered and Bob conditions on that branch, applying
   `U_zx` reconstructs the original input state.

## First Run

Command:

```bash
python3 scripts/frontier_teleportation_measurement_record.py
```

Observed output:

```text
resolution error: 0.000e+00
orthogonality error: 0.000e+00
idempotence error: 0.000e+00
state-projector error: 1.110e-16
max premeasurement isometry norm error: 6.661e-16
max Bell-record probability error from 1/4: 1.665e-16
max pairwise record-probability distance across inputs: 1.665e-16
max Bob trace distance to I/2 before receiving record: 3.331e-16
max pairwise Bob pre-record distance across inputs: 3.331e-16
delivered records conditioned: Phi+, Phi-, Psi+, Psi-
minimum post-delivery corrected fidelity: 0.9999999999999997
maximum post-delivery infidelity: 3.331e-16
max corrected-state trace distance to input: 2.618e-16
```

The runner reports `PASS` for:

- Bell projector algebra;
- record isometry;
- record marginal input-independence;
- Bob pre-record input-independence;
- delivered-record correction.

## What This Adds

The first protocol already modeled an ideal Bell measurement plus a delayed
classical message. This runner separates the measurement-record step:

- Alice's Bell projectors write to an explicit orthogonal four-state record
  register.
- Before Bob has access to that record, tracing over the record leaves Bob's
  reduced state input-independent.
- After a record label is available, conditioning on that label recovers the
  same correction branch as the standard teleportation protocol.

This is the smallest explicit record-register model needed to remove ambiguity
about whether the "classical bits" are being treated as an actual orthogonal
record degree of freedom.

## Limitations

- Orthogonality of the record basis is assumed, not derived.
- The model is an ideal premeasurement/isometry plus branch conditioning, not a
  physical apparatus Hamiltonian.
- It does not derive Born weights, decoherence, collapse, or durable
  endogenous record persistence.
- It does not derive the Bell resource or the Bell measurement from the
  Poisson-coupled CHSH lane.
- It does not add noise, imperfect records, loss, or finite apparatus errors.
- It does not transport matter, mass, charge, or energy and does not enable
  faster-than-light signaling.

## Status

The limitation is now narrowed: the lane has an explicit ideal orthogonal
measurement-record model, while a durable native measurement-record derivation
remains open.
