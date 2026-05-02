# Teleportation No-Signaling Audit

**Date:** 2026-04-25
**Status:** planning / first artifact audit
**Runner:** `scripts/frontier_teleportation_protocol.py`

## Question

Does the first native taste-qubit teleportation artifact allow Bob to learn
anything about Alice's unknown input state before the two-bit classical record
arrives?

The tested answer is no. Bob's reduced density matrix is input-independent
before the classical message, both before Alice's Bell measurement and after
Alice's Bell measurement when Bob has not received the outcome.

## Setup

The protocol uses three encoded taste-qubit registers:

```text
A = Alice unknown state
R = Alice half of Bell pair
B = Bob half of Bell pair
```

The initial state is:

```text
|psi>_A tensor |Phi+>_RB
```

where `|psi>` is sampled randomly and `|Phi+>` is the encoded Bell resource.

Alice's Bell measurement has four outcomes labeled by two classical bits
`(z,x)`. Before Bob receives those bits, Bob's local state is computed by
tracing or averaging over Alice's inaccessible degrees of freedom and record.

## Audit Conditions

The runner checks three no-signaling quantities:

1. Before Alice's measurement:

```text
rho_B = Tr_AR(|psi><psi|_A tensor |Phi+><Phi+|_RB) = I/2
```

2. After Alice's Bell measurement but before Bob receives the outcome:

```text
rho_B = sum_zx p_zx rho_B|zx = I/2
```

3. Across random input states, the pre-message Bob state is pairwise equal up
to numerical precision.

The runner also verifies that every Bell outcome has probability `1/4`, so
the inaccessible classical record is not biased by the unknown input state.

## Causal Record Channel

The classical record is represented as a concrete two-bit message:

```text
sender = Alice
receiver = Bob
bits = (z, x)
created_at_tick = t
deliver_at_tick = t + latency
```

The channel has positive latency. Bob's receive call before `deliver_at_tick`
returns no record. Bob's correction is applied only after delivery.

In the first run, the demonstration record was:

```text
record: Psi- bits(z,x)=(1, 1) created t=10 deliver t=13
receive at t=12 blocked: True
receive at delivery tick exactly once: True
post-delivery correction fidelity: 1.0000000000000000
```

## Numerical Results

Command:

```bash
python3 scripts/frontier_teleportation_protocol.py --trials 64 --seed 20260425
```

Observed no-signaling quantities:

```text
max Bob trace distance to I/2 before Alice measurement: 3.331e-16
max Bob trace distance to I/2 after Alice measurement but before message: 4.163e-16
max pairwise pre-message Bob-state distance across inputs: 3.886e-16
max Bell probability error from 1/4: 2.220e-16
```

These are machine-precision deviations from the analytic no-signaling value.

## Claim Boundary

This review supports only the standard teleportation no-signaling statement:
without Alice's two classical bits, Bob's reduced state is input-independent.

It does not support:

- faster-than-light communication;
- controllable signaling before the classical record arrives;
- transport of matter, mass, charge, or energy;
- a final theory of measurement or durable records;
- a derivation of the Bell resource from the Poisson-coupled CHSH system.

## Status

The first no-signaling audit passes for the ideal encoded taste-qubit protocol.
The lane remains planning / first artifact.
